import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from configurations.configurations import Configurations

class ChartService():

    def __init__(self):
        self.__config = Configurations()

    def show_chart(self):
        file_path = f'{self.__config.storage_path}/hotels.csv'
        hotels_df = pd.read_csv(file_path, sep=',', engine='python')
        file_path = f'{self.__config.storage_path}/reservations.csv'
        reservations_df = pd.read_csv(file_path, sep=',', engine='python')

        reservations_df['check_out_date'] = pd.to_datetime(reservations_df['check_out_date'], format='%d/%m/%Y', errors='coerce')

        reservas_ativas = reservations_df[
            (reservations_df['canceled'] != 'False') &
            (reservations_df['check_out_date'] > pd.Timestamp.now())
        ]

        reservas_por_hotel = reservas_ativas.groupby('hotel_id').size().reset_index(name='reservas_ativas')

        dados_hotel = hotels_df[['hotel_id', 'name', 'total_rooms']].merge(
            reservas_por_hotel, on='hotel_id', how='left'
        )
        dados_hotel['reservas_ativas'] = dados_hotel['reservas_ativas'].fillna(0).astype(int)
        dados_hotel['quartos_vagos'] = dados_hotel['total_rooms'] - dados_hotel['reservas_ativas']

        x = range(len(dados_hotel))
        plt.figure(figsize=(12, 6))

        plt.bar(x, dados_hotel['reservas_ativas'], width=0.4, label='Reservas Ativas', color='blue')

        plt.bar(
            [pos + 0.4 for pos in x],
            dados_hotel['quartos_vagos'],
            width=0.4,
            label='Quartos Vagos',
            color='orange'
        )

        plt.title('Reservas vs Quartos Vagos por Hotel', fontsize=16)
        plt.xlabel('Hotel', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        plt.xticks([pos + 0.2 for pos in x], dados_hotel['name'], rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()

        plt.show()

        reservations_df['check_in_date'] = pd.to_datetime(reservations_df['check_in_date'], format='%d/%m/%Y', errors='coerce')
        reservations_df['check_out_date'] = pd.to_datetime(reservations_df['check_out_date'], format='%d/%m/%Y', errors='coerce')

        reservations_df = reservations_df.merge(hotels_df[['hotel_id', 'name', 'total_rooms']], on='hotel_id', how='left')

        check_in_date = reservations_df['check_in_date'].min()
        check_out_date = reservations_df['check_out_date'].max()
        date_range = pd.date_range(start=check_in_date, end=check_out_date)

        availability_data = []

        for hotel_name in hotels_df['name']:
            hotel_rooms = hotels_df.loc[hotels_df['name'] == hotel_name, 'total_rooms'].values[0]
            
            for current_date in date_range:
                active_reservations = reservations_df[
                    (reservations_df['name'] == hotel_name) &
                    (reservations_df['check_in_date'] <= current_date) &
                    (reservations_df['check_out_date'] >= current_date)
                ]
                
                rooms_reserved = active_reservations.shape[0]
                rooms_available = hotel_rooms - rooms_reserved
                
                availability_data.append({'Date': current_date, 'name': hotel_name, 'Rooms_Available': rooms_available})

        availability_df = pd.DataFrame(availability_data)

        plt.figure(figsize=(12, 8))

        for hotel_name in hotels_df['name']:
            hotel_data = availability_df[availability_df['name'] == hotel_name]
            plt.plot(hotel_data['Date'], hotel_data['Rooms_Available'], label=hotel_name)

        plt.title('Quartos Disponíveis por Hotel ao Longo do Tempo', fontsize=16)
        plt.xlabel('Data', fontsize=12)
        plt.ylabel('Quartos Disponíveis', fontsize=12)
        plt.legend(title='Hotel', fontsize=10)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
