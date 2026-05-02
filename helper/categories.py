import pandas as pd
from collections import defaultdict

def detect_categories(df: pd.DataFrame) -> dict :
    features={}

    for col in df.columns:
        series=df[col].dropna()
        unique_vals=series.nunique()
        total_vals=len(series)

        #datetime detection
        if pd.api.types.is_datetime64_any_dtype(series):
            features[col]="datetime"
            continue

        if pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
            converted=pd.to_datetime(series, errors='coerce')
            if converted.notna().sum() / total_vals > 0.9 and pd.api.types.is_datetime64_any_dtype(converted):  
                df[col]=pd.to_datetime(df[col], errors='coerce')
                features[col]="datetime"
                continue

        #Fallback to other detection if datetime conversion fails
        #identifier detection (id means likely to be unique)
        if "id" in col.lower() and unique_vals/total_vals>0.98 and pd.api.types.is_integer_dtype(series):
            features[col]="id"
            continue

        #numeric detection
        if pd.api.types.is_numeric_dtype(series): 
            if pd.api.types.is_integer_dtype(series): 
                if unique_vals/total_vals < 0.1 : 
                    features[col]="categorical"
                else:
                    features[col]="numerical"
            else:
                features[col]="numerical"

        #non-numeric:  object/str
        else: 
            if unique_vals/total_vals < 0.1: 
                features[col] = "categorical"
            else:
                features[col] = "others"

    return features, df

def categorize(features: dict) ->  dict:
    types: dict[str,list[str]] =defaultdict(list)
    for feature, dt in features.items():
        if "id" in feature.lower() and dt == "numerical":
            continue
        types[dt].append(feature)
    return dict(types)