from repositories.room_repository import RoomRepository
from models.room import Room
import pandas as pd

class RoomService():
    
    def __init__(self):
        self.__room_repository = RoomRepository()

    def create_and_save_room(self, hotel_id, room_id, floor, room_type, daily_rate):
        room = Room(hotel_id, room_id, floor, room_type, daily_rate)
        return self.__room_repository.save(room)
    
    def delete_hotel_rooms(self, hotel_id):
        rooms_df = self.__room_repository.read_room()
        for room_id in rooms_df.loc[rooms_df['hotel_id']==hotel_id, 'room_id']:
            self.__room_repository.delete_room(hotel_id, room_id)

    def remove_room(self, hotel_id, room_id):
        self.__room_repository.delete_room(hotel_id, room_id)

    def get_rooms_by_hotel_id(self, hotel_id):
        rooms_df = self.__room_repository.read_room()
        return rooms_df[rooms_df['hotel_id']==hotel_id] if not rooms_df.empty else pd.DataFrame()
    