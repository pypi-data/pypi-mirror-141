from sqlalchemy import create_engine
from pyhive import presto 
from unidecode import unidecode

import pandas as pd
from exceptions import WrongFileType, InvalidIdCol

class SdpUtils:

    def __init__(self, host:str, port:int, username:str) -> None:
        _engine_str = f'presto://{host}:{port}/hive'
        self.engine = create_engine(_engine_str)
        self.cursor = presto.connect(host, port, username)

    def get_csv_name(self, path):
        file = path.split('/')[-1]
        
        if not file.endswith('csv'):
            raise WrongFileType

        table_name = file.split('.')[0].lower()
        table_name = table_name.replace(" ", "_")
        return table_name

    def csv_to_raw(self, path, chunksize=700, separator=';', verbose=False, check_duplicates=False, id_col=None):
        '''
        Upload a CSV to a raw table.
        Args:
            path: Path to csv file;
        '''
        
        table_name = self.get_csv_name(path=path)
        if check_duplicates and id_col == None:
            raise InvalidIdCol

        df_generator = pd.read_csv(path, sep=separator, header=0, skipinitialspace=True, keep_default_na=True, infer_datetime_format=True, keep_date_col=True, encoding='utf-8', chunksize=chunksize, verbose=False)
        
        if verbose:
            print(f'Uploading {table_name} to raw zone..')
            upload_sign = ['.', '..', '...']
            up_idx = 0
            print(f'Uploading: {upload_sign[up_idx]}', end='\r')
        
        for df in df_generator:

            cols = df.columns.str.lower().str.replace(' ', "_", regex=False)\
                                        .str.replace(',','', regex=False)\
                                        .str.replace('.','', regex=False)
            
            df.columns = [unidecode(col) for col in cols]
                
            df = df.astype(str)
            
            if check_duplicates:
                df = self.get_new_entities(self.engine, df, id_col, f"hive.raw.{table_name}")
            
            df.to_sql(table_name, con=self.engine, schema='raw', if_exists='append', index=False, method='multi')
            
            if verbose:
                if up_idx == len(upload_sign)-1:
                    up_idx = 0
                else:
                    up_idx += 1
                print(f'Uploading: {upload_sign[up_idx]}', end='\r')
        if verbose:
            print('Finished upload!')

    def get_new_entities(self, df:pd.DataFrame, id_col:str, table:str, chunksize:int=700):
        '''
        Get only new entities from a dataframe (df) according to the table and id_col specified.
        Args:
            df: dataframe to be analyzed;
            id_col: column that matches the dataframe and table;
            table: database table name.
        Returns:
            A pd.DataFrame containing only unique rows.
        '''

        # Get all values in the column defined as id in the df
        ids = tuple(df[id_col].array)
        
        try:
            # Get all values that matches id between the dataframa and the table. 
            for chunk in pd.read_sql_query(f'''select {id_col} from {table} where {id_col} in {ids}''', con=self.engine, chunksize=chunksize):
                # Remove the matched values from the df
                mask = df[id_col].isin(chunk[id_col])
                df = df.loc[~mask]
        except:
            pass
        return df
