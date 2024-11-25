from repositories.hotel_repository import HotelRepository 
from repositories.room_repository import RoomRepository
from services.room_service import RoomService
from services.reservation_service import ReservationService
from utils.utils import Utils
from models.hotel import Hotel
from models.room import Room
import pandas as pd

class HotelService():
    def __init__(self):
        self.__hotel_menu_columns = {'hotel_id': 'Código',
                                     'name': 'Hotel',
                                     'address': 'Endereço'}
        self.__reserv_full_menu_columns = {'reservation_id': 'Reserva',
                                           'room_id': 'Quarto', 
                                           'guest_id': 'ID Hóspede', 
                                           'check_in_date': 'Data de Check-In', 
                                           'check_out_date': 'Data de Check-Out'}
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.colheader_justify', 'left')
        self.__utils = Utils()
        self.__room_service = RoomService()
        self.__hotel_repository = HotelRepository()
        self.__reservation_service = ReservationService()

    
    def get_last_column_val(self, column_key):
        df = self.__hotel_repository.read_hotel()            
        return df[column_key].iloc[-1] if not df.empty else 0

    def generate_id(self):
        return self.get_last_column_val('hotel_id') + 1

    def create_and_save_hotel(self, name, address, total_floors,
                              rooms_per_floor, default_room_type, default_price):
        hotel_id = self.generate_id()  
        hotel = Hotel(hotel_id, name, address, total_floors, rooms_per_floor, default_room_type, default_price) 
        return self.__hotel_repository.save(hotel) 

    def get_hotels_and_addresses(self):
        df = self.__hotel_repository.read_hotel()
        if df.empty:
            print('\n\t< Não há hotéis registrados >')
            return pd.DataFrame()
        else:
            return df[['hotel_id', 'name', 'address']]

    def choose_hotel(self):
        hotels_df = self.get_hotels_and_addresses()
        if hotels_df.empty:
            return pd.DataFrame()
        else:
            hotel_codes = list(map(str, hotels_df['hotel_id']))
            df_to_print = self.__utils.format_dataframe(hotels_df, self.__hotel_menu_columns)
            print(f'\n{df_to_print}')

            while True:
                hotel_code = input('\nEscolha um dos hotéis acima através de seu código: ')
                if hotel_code in hotel_codes:
                    break
                else:
                    print('\n\t< Opção inválida! Informe um código existente. >')

            return int(hotel_code)
    
    def update_hotel_total_rooms(self, hotel_id, op='increment'):
        df = self.__hotel_repository.read_hotel()
        df.loc[df['hotel_id']==hotel_id, 'total_rooms'] += 1 if op == 'increment' else -1
        self.__hotel_repository.update_hotel(df)

    def add_new_room_to_hotel(self, hotel_id, room_id, floor, room_type, daily_rate):
        self.__room_service.create_and_save_room(hotel_id, room_id, floor, room_type, daily_rate)
        self.update_hotel_total_rooms(hotel_id, op='increment')
        return True

    def __show_reservations(self, df):
        if not df.empty:
            df = df.loc[:, self.__reserv_full_menu_columns.keys()]
            df_to_print = self.__utils.format_dataframe(df, self.__reserv_full_menu_columns)
            print(f'\nReservas realizadas nesse hotel:\n{df_to_print}')

    def show_reservations_by_hotel_id(self, hotel_id, only_active=False):
        df = self.__reservation_service.get_reservations_by_hotel_id(hotel_id)
        if only_active:
            df = df[df['canceled'] != True]
        self.__show_reservations(df)
        return df

    def show_reservations_by_hotel_and_guest_ids(self, hotel_id, guest_id, only_active=False):
        df = self.__reservation_service.get_reservations_by_hotel_and_guest_ids(hotel_id, guest_id)
        if only_active:
            df = df[df['canceled'] != True]
        self.__show_reservations(df)
        return df

    def choose_reservation(self, hotel_id, guest_id, only_active=False):
        reservs = self.show_reservations_by_hotel_and_guest_ids(hotel_id, guest_id, only_active)
        if reservs.empty:
            print('\nNão há reservas ativas para este usuário, neste hotel.')
            return -1
        reserv_ids = list(reservs.loc[:, 'reservation_id'])
        reserv_ids = list(map(int, reserv_ids))
        while True:
            reserv_id = input('\nInforme o código da reserva que deseja cancelar: ')
            if not self.__utils.is_int([reserv_id]) or int(reserv_id) not in reserv_ids:
                print(f'\t< Opção inválida! Informe um código existente. >')
            else:
                return int(reserv_id)

    def delete_hotel_data(self, hotel_id):
        self.show_reservations_by_hotel_id(hotel_id)
        self.__room_service.delete_hotel_rooms(hotel_id)
        self.__reservation_service.delete_reservations_by_hotel_id(hotel_id)       
        self.__hotel_repository.delete_hotel(hotel_id=hotel_id)

    def rename_hotel(self, hotel_id, new_name):
        df = self.__hotel_repository.read_hotel()
        df.loc[df['hotel_id']==hotel_id, 'name'] = new_name
        self.__hotel_repository.update_hotel(df)

    def remove_room(self, hotel_id, room_id):
        self.__room_service.remove_room(hotel_id, room_id)
        self.update_hotel_total_rooms(hotel_id, op='decrement')