#() Ao editar ou excluir um hotel, em relação aos quartos, em especial na quantidade de quartos, a aplicação deverá apresentar 
#   antes os quartos que estavam reservados e serão cancelados por conta da edição da quantidade (ou seja, as reservas serão perdidas por conta do ajuste).
#() Deverão apresentar um gráfico demonstrando a quantidade de quartos reservados e disponíveis de cada hotel cadastrado.

class Reservation:
    def __init__(self, reservation_id, hotel_id, room_id, 
                 guest_id, check_in_date, check_out_date, canceled: bool):
        self.__reservation_id = reservation_id
        self.__hotel_id = hotel_id
        self.__room_id = room_id
        self.__guest_id = guest_id
        self.__check_in_date = check_in_date
        self.__check_out_date = check_out_date
        self.__canceled = canceled

    @property
    def reservation_id(self):
        return self.__reservation_id

    @property
    def hotel_id(self):
        return self.__hotel_id

    @property
    def room_id(self):
        return self.__room_id

    @property
    def guest_id(self):
        return self.__guest_id

    @property
    def check_in_date(self):
        return self.__check_in_date

    @property
    def check_out_date(self):
        return self.__check_out_date

    @property
    def canceled(self):
        return self.__canceled
