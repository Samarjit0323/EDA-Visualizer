import numpy as np
import pandas as pd
from helper.categories import detect_categories
import json

class StatsAnalyser:

    def __init__(self, dataframe):
        self.df = dataframe
        self.feature_wise_measures={col:{} for col in self.df.columns}
        self.features, self.df = detect_categories(self.df)

    def get_dtypes(self):
        return dict(zip(self.df.columns, self.df.dtypes))    

    def measures_of_central_tendency(self):
        for col in self.df.columns:
            self.feature_wise_measures[col] = {}
            if self.features.get(col)=="numerical":
                self.feature_wise_measures[col]["Mean"] = np.round(self.df[col].mean(),2)
                self.feature_wise_measures[col]["Median"] = np.round(self.df[col].median(),2)
            elif self.features.get(col)=="categorical":
                mode = self.df[col].mode()
                self.feature_wise_measures[col]["Mode"] = mode.tolist() if not mode.empty else None
    
    def measures_of_dispersion(self):
        for col in self.df.columns:
            if self.features.get(col)=="numerical":
                self.feature_wise_measures[col]["Range"]=max(self.df[col])-min(self.df[col])
                self.feature_wise_measures[col]["Variance"]=np.var(self.df[col], ddof=0)
                self.feature_wise_measures[col]["Standard Deviation"]=np.std(self.df[col], ddof=0)
                self.feature_wise_measures[col]["Q1"]=np.percentile(self.df[col].dropna(), 0.25)
                self.feature_wise_measures[col]["Q2"]=np.percentile(self.df[col].dropna(), 0.5)
                self.feature_wise_measures[col]["Q3"]=np.percentile(self.df[col].dropna(), 0.75)
                self.feature_wise_measures[col]["IQR"]=self.feature_wise_measures[col]["Q3"]-self.feature_wise_measures[col]["Q1"]

    def max_min(self):
        for col in self.df.columns:
            if self.features.get(col)=="numerical":
                self.feature_wise_measures[col]["Maximum"]=max(self.df[col])
                self.feature_wise_measures[col]["Minimum"]=min(self.df[col])
            elif self.features.get(col)=="categorical":
                self.feature_wise_measures[col]["Frequency Count"]=self.df[col].value_counts().reset_index()
                cats=self.feature_wise_measures[col]["Frequency Count"].iloc[:,0].to_list()
                vals=self.feature_wise_measures[col]["Frequency Count"].iloc[:,1].to_list()
                self.feature_wise_measures[col]["Frequency Count"]=list(zip(cats,vals))
                # print(self.feature_wise_measures[col]["Categories by count"])
            elif self.features.get(col)=="datetime":
                months=self.df[col].dt.month
                years=self.df[col].dt.year
                self.feature_wise_measures[col]["Most Occuring Year(s)"]=years.mode().tolist()
                self.feature_wise_measures[col]["Most Occuring Month(s)"]=months.mode().tolist()

    def normality(self):
        for col in self.df.columns:
            if self.features.get(col)=="numerical":
                self.feature_wise_measures[col]["Skewness"]=self.df[col].skew()
                self.feature_wise_measures[col]["Kurtosis"]=self.df[col].kurt()

    @property
    def get_stats(self):
        self.measures_of_central_tendency()
        self.measures_of_dispersion()
        self.max_min()
        self.normality()
        return self.feature_wise_measures

