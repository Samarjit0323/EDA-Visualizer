from services.eda import EDA
from services.stats import StatsAnalyser
from helper.file import file_to_df

df, filename, extension =file_to_df("static/datasets/weight-height.csv")
eda=EDA(df, filename, extension)
stats=StatsAnalyser(df)
print("StatsAnalyser object initialised")
print(stats.get_stats)
print(stats.feature_wise_measures.keys())

#python -m test.stats_check 