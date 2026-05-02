from services.eda import EDA
from helper.file import file_to_df
from pandas import DataFrame
import json

df1, f1, e1 =file_to_df(r"datasets\59576eac-c0ab-4496-ae7f-055231fc44b8.csv")
eda1=EDA(df1, f1, e1)

print(eda1.features)
print(eda1.get_dimensions)
# eda1.missing_values()
# eda1.get_groups()
# eda1.get_outliers()
print(eda1.collinearity())
# print(eda1.results)


# python -m test.eda_check