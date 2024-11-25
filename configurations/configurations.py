class Configurations():
    def __init__(self):
        self.__storage_path = './infrastructure/database'
        self.__room_types = ['Double Room', 'Single Room', 'Queen Room', 'King Room', 'Twin Room']

    @property
    def storage_path(self):
        return self.__storage_path
    
    @property
    def room_types(self):
        return self.__room_types
        