import pandas as pd
from sqlalchemy import create_engine, engine


class SdpUtils:

    def __init__(self, engine: engine) -> None:
        self.engine = engine

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
