from repositories.guest_repository import GuestRepository
from utils.utils import Utils
from models.guest import Guest
import pandas as pd

class GuestService():
    def __init__(self):

        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.colheader_justify', 'left')
        self.__guest_repository = GuestRepository()
        self.__utils = Utils()
        # self.__guest_repository = guest_repository
        
    def get_last_column_val(self, column_key):
        df = self.__guest_repository.read_guest()
        return df[column_key].iloc[-1] if not df.empty else 0
    
    def generate_id(self):
        return self.get_last_column_val('id') + 1
    
    def create_and_save_guest(self, cpf, name, date_birth, phone):
        guest_id = self.generate_id()
        guest = Guest(id=guest_id, cpf=cpf, name=name, date_birth=date_birth, phone=phone)
        
        if self.__guest_repository.guest_exists(guest):
            print(f"Hóspede com CPF {cpf} já está cadastrado.")
            return False
        
        self.__guest_repository.create_guest(guest)
        print("\nHóspede cadastrado com sucesso!")
        return True
    
    def update_guest(self, guest_id, new_name, new_cpf, new_date_birth, new_phone):
        df = self.__guest_repository.read_guest()
        if guest_id in df['id'].values:
            df.loc[df['id'] == guest_id, ['name', 'cpf', 'date_birth', 'phone']] = [new_name, new_cpf, new_date_birth, new_phone]
            self.__guest_repository.update_guest(df)
            return True
        return False
        
    def get_guest_and_cpf(self):
        df = self.__guest_repository.read_guest()
        if df.empty:
            print('\n\t< Não há clientes registrados >')
            return pd.DataFrame()
        else:
            return df[['id', 'cpf', 'name', 'date_birth', 'phone']]
        
    def get_guest_by_cpf(self, cpf):
        df = self.__guest_repository.read_guest()
        guest_data = df[df['cpf'] == cpf]
        
        if not guest_data.empty:
            return guest_data.iloc[0].to_dict()  # Retorna a primeira linha como dicionário
        else:
            return None  # Retorna None caso o hóspede não seja encontrado

        
    def delete_guest_data(self, guest_id):
        df = self.__guest_repository.read_guest()
        if not df.empty and guest_id in df['id'].values:
            self.__guest_repository.delete_guest(id=guest_id)
            return True
        return False

    def get_guest_name_and_cpf(self):
        df = self.__guest_repository.read_guest()
        if df.empty:
            print('\n\t< Não há clientes registrados >')
            return pd.DataFrame()
        else:
            return df[['id', 'cpf', 'name']]
    
    def guest_exists(self, cpf):
        guest_df = self.get_guest_name_and_cpf()
        if guest_df.empty or guest_df[guest_df['cpf'] == cpf].empty:
            return False
        else:
            return True

    def choose_guest(self):
        guest_df = self.get_guest_and_cpf()
        if guest_df.empty:
            return pd.DataFrame()
        else:
            guest_codes = list(map(str, guest_df['id']))
            df_to_print = self.__utils.format_dataframe(guest_df, self.__guest_menu_columns)
            print(f'\n{df_to_print}')
            
            while True:
                guest_code = input('\nEscolha um dos clientes acima através de seu código: ')
                if guest_code in guest_codes:
                    break
                else:
                    print('\n\t< Opção inválida! Informe um código existente. >')

            return int(guest_code)