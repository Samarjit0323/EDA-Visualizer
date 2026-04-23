import numpy as np
import pandas as pd
from helper.file import file_to_df
class EDA:

    def __init__(self, dataframe, filename, ext):
        self.df : pd.DataFrame =dataframe  
        self.filename: str=filename 
        self.ext=ext   
        self.row_count=0
        self.features=None
        self.col_count=0

    def dimensions(self):
        self.rowcount=self.df.shape[0]
        self.colcount=self.df.shape[1]
    
    def get_dtypes(self):
        self.features=dict(zip(self.df.columns, self.df.dtypes))

    def get_final_dict(self):
        pass

