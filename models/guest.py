import pandas as pd

class Guest:
    def __init__(self, id=None, name=None, cpf=None, date_birth=None, phone=None):
        self.__id = id
        self.__name = name
        self.__cpf = self.__validate_cpf(cpf)
        self.__date_birth = self.__validate_date(date_birth)
        self.__phone = phone

    # Propriedades
    @property
    def id(self):
        return self.__id

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = self.__validate_cpf(value)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def date_birth(self):
        return self.__date_birth

    @date_birth.setter
    def date_birth(self, value):
        self.__date_birth = self.__validate_date(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    # Métodos Internos
    def __validate_cpf(self, cpf):
        cpf = str(cpf).strip()

        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
        
        return cpf

    def __validate_date(self, date_birth):
        try:
            if date_birth:
                pd.to_datetime(date_birth, format="%d/%m/%Y") 
            return date_birth
        except ValueError:
            raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
        