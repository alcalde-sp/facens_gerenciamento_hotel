from configurations.configurations import Configurations
from datetime import datetime
import pandas as pd
import os

class Utils():
    def __init__(self):
        self.config = Configurations()

    def is_int(self, values):
        try:
            dummy = list(map(int, values))
            return True
        except ValueError:
            return False

    def is_float(self, values):
        try:
            dummy = list(map(float, values))
            return True
        except ValueError:
            return False

    def empty_file(self, file_path):
        return os.path.exists(file_path) and os.path.getsize(file_path) <= 0

    def dict_to_dataframe(self, dictionary):
        return pd.DataFrame(dictionary, index=[0])

    def format_dataframe(self, df, new_col_names):
        df = df.rename(columns=new_col_names)
        # return df.reset_index(drop=True).applymap(str).to_string(index=False, justify='left')
        return df.reset_index(drop=True).map(str).to_string(index=False, justify='left')

    def format_date(self, data_str):        
        try:
            date = datetime.strptime(data_str, '%d/%m/%Y')
            return date.strftime('%d/%m/%Y')
        except ValueError:
            return None

    # def str_to_date_format(self, df, key):
    #     df[key] = pd.to_datetime(df[key], format='%d-%m-%Y', errors='coerce')
    #     return df

    def read_file(self, type, date_columns=[], dtype_col_and_type={}):
        file_path = f'{self.config.storage_path}/{type}.csv'
        
        if self.empty_file(file_path):
            return pd.DataFrame()
        else:        
            return pd.read_csv(file_path, parse_dates=date_columns, dtype=dtype_col_and_type)

    def write_file(self, type, df, mode='w'):
        file_path = f'{self.config.storage_path}/{type}.csv'
        if self.empty_file(file_path):
            df.to_csv(file_path, mode='w', index=False, header=True)
        else:
            df.to_csv(file_path, mode=mode, index=False, header=(mode == 'w'))
