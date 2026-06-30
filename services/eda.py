import numpy as np
import pandas as pd
from helper.file import file_to_df
from helper.categories import detect_categories
import json

class EDA:

    def __init__(self, dataframe, filename, ext):
        self.df : pd.DataFrame =dataframe  
        self.filename: str=filename 
        self.ext=ext   
        self.rowcount=self.df.shape[0]
        self.colcount=self.df.shape[1]
        self.features, self.df = detect_categories(self.df)
        self.results={col:[] for col in self.features.keys()}
        self.inferences={}
            
    @property
    def get_dimensions(self):
        return {"Rows":self.rowcount,"Columns":self.colcount}
    
    def get_dtype(self):
        for col in self.df.columns:
            self.results[col].append(("Data Type", self.df[col].dtype))

    def missing_values(self):
        for col in self.df.columns:
            self.results[col].append(("Total Number of Missing Values",self.df[col].isna().sum()))

    def get_groups(self):
        for col in self.df.columns:
            if self.features.get(col)=="categorical":
                grouped=self.df[col].value_counts().to_dict()
                self.results[col].append(("Grouped Categories by frequency",grouped))

    def get_outliers(self):
        for col in self.df.columns:
            if self.features.get(col)=="numerical":
                q1=np.percentile(self.df[col], 0.25)
                q3=np.percentile(self.df[col],0.75)
                iqr=q3-q1
                lboundary=q1 - 1.5*iqr;
                rtboundary=q3 + 1.5*iqr;
                ans=""
                if lboundary==rtboundary:
                    ans="There are likely no outliers"
                else:
                    ans=f"Values less than {lboundary} and greater than {rtboundary} are likely outliers."
                self.results[col].append(("Outlier Analysis",ans))

    def collinearity(self):
        corr_matrix = self.df[[col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])]].corr()
        threshold=0.8
        self.inferences["Collinearity"]=[]
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    self.inferences["Collinearity"].append(f"{col1} and {col2} are likely collinear")
                else:
                    self.inferences["Collinearity"].append(f"{col1} and {col2} are likely not collinear and hence independent")

    
    def get_results(self):
        self.missing_values()
        self.get_groups()
        self.collinearity()
        self.get_outliers()
        self.get_dtype()
        return self.results, self.inferences

