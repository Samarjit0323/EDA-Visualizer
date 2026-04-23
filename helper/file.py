import os
import pandas as pd

def file_to_df(path):
    file = os.path.basename(path)
    _, ext= os.path.splitext(file)
    
    with open(path,'r') as f:
        if ext not in ['.csv','.xlsx','.xlx']:
                raise Exception("File format not suitable for analysis")
        elif ext==".csv":
            df= pd.read_csv(f)
        elif ext in ['.xlsx','.xlx']:
            df=pd.read_excel(f)
        else:
            try:
                df=pd.DataFrame(path)
            except Exception as e:
                print(repr(e))

    return df, file, ext