from models.room import Room

class Hotel():
    def __init__(self, hotel_id, name, address, total_floors, 
                 rooms_per_floor, default_room_type, default_price):
        self.__hotel_id = hotel_id
        self.__name = name
        self.__address = address
        self.__total_floors = total_floors
        self.__rooms_per_floor = rooms_per_floor
        self.__total_rooms = total_floors * rooms_per_floor
        self.__default_rooms = self.__generate_rooms(default_room_type,
                                                     default_price)

    @property
    def hotel_id(self):
        return self.__hotel_id

    @property
    def name(self):
        return self.__name
    
    @property
    def address(self):
        return self.__address

    @property
    def total_floors(self):
        return self.__total_floors

    @property
    def rooms_per_floor(self):
        return self.__rooms_per_floor

    @property
    def total_rooms(self):
        return self.__total_rooms

    @property
    def default_rooms(self):
        return self.__default_rooms
    
    def __generate_rooms(self, default_room_type, default_price):
        list_of_rooms = []
        for floor_idx in range(1, self.__total_floors + 1):
            for room_idx in range(1, self.__rooms_per_floor + 1):
                room_id = f'{floor_idx}0{room_idx}'
                room = Room(self.hotel_id, room_id, floor_idx, default_room_type, default_price)
                list_of_rooms.append(room)
        return list_of_rooms