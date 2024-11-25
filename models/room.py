class Room():
    def __init__(self, hotel_id, room_id, floor, room_type, daily_rate):
        self.__hotel_id = hotel_id
        self.__room_id = room_id
        self.__floor = floor
        self.__room_type = room_type
        self.__daily_rate = round(daily_rate, 2)

    @property
    def hotel_id(self):
        return self.__hotel_id

    @property
    def room_id(self):
        return self.__room_id

    @property
    def floor(self):
        return self.__floor

    @property
    def room_type(self):
        return self.__room_type

    @property
    def daily_rate(self):
        return self.__daily_rate