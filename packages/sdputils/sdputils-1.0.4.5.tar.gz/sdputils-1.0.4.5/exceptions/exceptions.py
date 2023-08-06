class EmptyDataFrame(Exception):

    def __init__(self, df_name, message="The dataframe is empty."):
        self.df_name = df_name
        self.message = message
        super().__init__(self.message)
        
class FileTypeNotSpecified(Exception):

    def __init__(self, message="The file_type variable must be specified"):
        self.message = message
        super().__init__(self.message)
        
class FileTypeNotRecognized(Exception):

    def __init__(self, message="The file_type variable specified isn't recognized as valid. Please check that or implement the new type."):
        self.message = message
        super().__init__(self.message)
        
class WrongFileType(Exception):

    def __init__(self, message="This method is used for upload a CSV file."):
        self.message = message
        super().__init__(self.message)
        
class InvalidIdCol(Exception):

    def __init__(self, message="When check_duplicates is true the id_col must be passed."):
        self.message = message
        super().__init__(self.message)

class MissingParamenters(Exception):

    def __init__(self, message="The query and the table_name cannot be both None, at leats one must be passed."):
        self.message = message
        super().__init__(self.message)