from services.eda import EDA
from services.stats import StatsAnalyser
from helper.file import file_to_df, generate_stats_report
from helper.categories import detect_categories
from pathlib import Path
import os
import json

df, filename, extension =file_to_df(r"datasets\9061b2d4-ec56-483c-96a3-c9d35a5006cd.csv")
features, _ = detect_categories(df)
print(json.dumps(features, indent=2))
# eda=EDA(df, filename, extension)
# stats=StatsAnalyser(df)
# print("StatsAnalyser object initialised")
# print(stats.df.dtypes)
# # print(stats.get_stats)
# print(stats.feature_wise_measures.keys())
# info=stats.get_stats
# # print(generate_stats_report(info))

# filepath=Path(generate_stats_report(info))
# print(filepath)
# if filepath.is_file():
#     print(True)
#     os.startfile(filepath)

#python -m test.stats_check 