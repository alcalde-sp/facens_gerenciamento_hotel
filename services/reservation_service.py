import pandas as pd
from datetime import datetime
from utils.utils import Utils
from models.reservation import Reservation
from services.room_service import RoomService
from repositories.reservation_repository import ReservationRepository

class ReservationService():

    def __init__(self):
        self.__reserv_menu_columns = {'room_id': 'Código', 
                                      'floor': 'Andar', 
                                      'room_type': 'Tipo', 
                                      'daily_rate': 'Valor(dia)'}
        self.__utils = Utils()
        self.__room_service = RoomService()
        self.__reservation_repository = ReservationRepository()

    def get_reservations_by_date_range(self, check_in_date, check_out_date):
        reserv_df = self.__reservation_repository.read_reservation()

        # if not reserv_df.empty:
            # reserv_df = reserv_df[(reserv_df['check_in_date'] >= check_in_date) & (reserv_df['check_out_date'] <= check_out_date)]
        return reserv_df

    def show_available_rooms(self, hotel_id, check_in_date=None, check_out_date=None):
        rooms_df = self.__room_service.get_rooms_by_hotel_id(hotel_id)
        reserv_df = self.get_reservations_by_date_range(check_in_date, check_out_date)

        if not reserv_df.empty:
            reserv_df = reserv_df[(reserv_df['hotel_id'] == hotel_id) & (reserv_df['canceled'] != True)]            
        
        available_rooms_df = rooms_df

        if not reserv_df.empty:
            unavailable_rooms = list(reserv_df.loc[:,'room_id'])
            unavailable_rooms = list(map(str, unavailable_rooms))
            available_rooms_df = rooms_df[~(rooms_df['room_id'].isin(unavailable_rooms))]

        available_rooms_df['daily_rate'] = available_rooms_df['daily_rate'].map(lambda num: f'{float(num):.2f}')
        available_rooms_df = available_rooms_df.loc[:, list(self.__reserv_menu_columns.keys())]
        df_to_print = self.__utils.format_dataframe(available_rooms_df, self.__reserv_menu_columns)
        print(f'\n{df_to_print}')

        return available_rooms_df

    def choose_room(self, hotel_id, check_in_date, check_out_date):
        rooms_df = self.show_available_rooms(hotel_id, check_in_date, check_out_date)
        room_ids = list(rooms_df.loc[:, 'room_id'])

        # choose room
        room_id = None
        while True:
            room_id = input('\nEscolha um dos quartos acima através de seu código: ')
            if room_id in room_ids: 
                break
            else: 
                print('\nCódigo inválido! Informe um dos códigos presentes.')
        return room_id

    def get_last_column_val(self, column_key):
        df = self.__reservation_repository.read_reservation()            
        return df[column_key].iloc[-1] if not df.empty else 0

    def generate_id(self):
        return self.get_last_column_val('reservation_id') + 1

    def create_and_save_reservation(self, hotel_id, room_id, guest_id, 
                                    check_in_date, check_out_date):
        reservation_id = self.generate_id()
        check_in_date = self.__utils.format_date(check_in_date)
        check_out_date = self.__utils.format_date(check_out_date)
        
        reservation = Reservation(reservation_id, hotel_id, room_id, 
                                  guest_id, check_in_date, check_out_date, False) 
        return self.__reservation_repository.save(reservation) 
    
    def get_reservations_by_hotel_id(self, hotel_id):
        df = self.__reservation_repository.read_reservation()            
        if not df.empty:
            df = df[df['hotel_id']==hotel_id]
            return df
    
    def get_reservations_by_hotel_and_guest_ids(self, hotel_id, guest_id):
        df = self.__reservation_repository.read_reservation()            
        if not df.empty:
            df = df[(df['hotel_id']==hotel_id) & (df['guest_id']==guest_id)]
            return df

    def delete_reservations_by_hotel_id(self, hotel_id):
        df = self.get_reservations_by_hotel_id(hotel_id)
        if not df.empty:
            reserv_ids = list(df.loc[:, 'reservation_id'])
            reserv_ids = list(map(int, reserv_ids))
            for reserv_id in reserv_ids:
                self.__reservation_repository.delete_reservation(reserv_id)

    def cancel_reserv_by_id(self, reserv_id):
        df = self.__reservation_repository.read_reservation()            
        df.loc[df['reservation_id']==reserv_id, 'canceled'] = True
        self.__reservation_repository.update_reservation(df)            
