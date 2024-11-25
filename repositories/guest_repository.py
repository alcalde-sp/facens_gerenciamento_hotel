from utils.utils import Utils
from models.guest import Guest

class GuestRepository():
    def __init__(self):
        self.__utils = Utils()
        
    def create_guest(self, guest: Guest):
        if self.guest_exists(guest):
            print(f'\nO CPF \'{guest.cpf}\' já foi cadastrado.')
            return False
        else:
            guest_data = self.__guest_to_dict(guest)
            guest_data = self.__utils.dict_to_dataframe(guest_data)
            self.__utils.write_file('guests', guest_data, mode='a') 
            return True
        
    def read_guest(self):
        df = self.__utils.read_file('guests')
        df['cpf'] = df['cpf'].apply(lambda cpf: str(cpf))
        df['phone'] = df['phone'].apply(lambda phone: str(phone))
        return df
        # return self.__utils.read_file('guests')
    
    def update_guest(self, guest_df):
        return self.__utils.write_file('guests', guest_df, 'w')        
    
    def delete_guest(self, id=None):
        df = self.read_guest()

        if df.empty or not (id in df['id'].values):
            print("\nHóspede não encontrado para exclusão.")
            return False
        
        new_df = df[df['id'] != id]

        self.update_guest(new_df)
        print("\nHóspede excluído com sucesso!")
        return True

        
    def guest_exists(self, guest):
        df = self.read_guest()
        if not df.empty:
            return not df[df['cpf'] == guest.cpf].empty
        else:
            return False
        
    def __guest_to_dict(self, guest):
        guest_data = {
            'id': guest.id,
            'cpf': guest.cpf,
            'name': guest.name,
            'date_birth': guest.date_birth,
            'phone': guest.phone
        }
        return guest_data