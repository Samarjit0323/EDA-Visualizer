from services.visuals import Visualization
from helper.file import file_to_df
import json

df1, filename, extension =file_to_df("static/datasets/weight-height.csv")
df2, _, _ = file_to_df("static/datasets/customer.csv")
visuals1=Visualization(df1)
visuals2=Visualization(df2)
# print(df1.dtypes)
# print(visuals1)
# print(df2.dtypes)
# print(visuals2)

# print(df2["review"].nunique(), df2["education"].nunique())

print(json.dumps(visuals1.get_all(), indent=1))
#python -m test.visuals_check 