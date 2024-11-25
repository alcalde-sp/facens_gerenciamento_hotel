import pandas as pd
from utils.utils import Utils
from models.reservation import Reservation

class ReservationRepository():
    def __init__(self):
        self.__utils = Utils()

    def save(self, reservation: Reservation):
        reservation_dict = self.__reservation_to_dict(reservation)
        df = self.__utils.dict_to_dataframe(reservation_dict)
        self.__utils.write_file('reservations', df, 'a')
        print('\nParabéns! Sua reserva foi concluída com sucesso.')      

    def read_reservation(self):
        reserv_df = self.__utils.read_file('reservations', 
                                           ['check_in_date', 'check_out_date']) 
        if not reserv_df.empty:
            return reserv_df
        else:
            return pd.DataFrame()

    def update_reservation(self, reservation_df):
        self.__utils.write_file('reservations', reservation_df, 'w')

    def delete_reservation(self, reservation_id):
        df = self.read_reservation()
        new_df = df[df['reservation_id'] != reservation_id]
        self.update_reservation(new_df)

    def __reservation_to_dict(self, reservation):
        reservation_data = {'reservation_id': reservation.reservation_id,
                            'hotel_id': reservation.hotel_id,
                            'room_id': reservation.room_id,
                            'guest_id': reservation.guest_id,
                            'check_in_date': reservation.check_in_date,
                            'check_out_date': reservation.check_out_date,
                            'canceled': reservation.canceled}
        
        return reservation_data
