import os
from os import mkdir
import pandas as pd
from services.stats import StatsAnalyser
from fpdf import FPDF
from pathlib import Path
from base64 import b64decode
import shutil

BASE_DIR=Path(__file__).resolve().parent.parent

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

def generate_stats_report(file_id: str, info : dict, features: dict) -> Path | None :
    filepath=os.path.join(BASE_DIR, "reports")
    os.makedirs(filepath, exist_ok=True)
    txt_filepath=os.path.join(filepath, f"{file_id}_stats_report.txt")
    pdf_filepath=os.path.join(filepath, f"{file_id}_stats_report.pdf")

    with open(txt_filepath, "w") as f:
        f.write("Statistical Analysis Report\n".upper())
        f.write("\n\n")
        for key, value in info.items():
            f.write(f"{key.upper()}:\n")
            f.write(f"This feature is likely to be {features.get(key)} type\n")
            if not value:
                f.write("No data available\n\n")
                continue
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    f.write(f"  {sub_key}: {sub_value}\n")
            else:
                f.write(f"{value}\n")
            f.write("\n")
    print(f"Text report generated at: {txt_filepath}")
      
    pdf_report = FPDF()
    pdf_report.add_page()
    pdf_report.set_font("Times", size=14)
    with open(txt_filepath, "r") as f:
        for line in f:
            if line=="Statistical Analysis Report\n".upper():
                pdf_report.set_font("Times", style="B", size=16)
                pdf_report.multi_cell(200, 10, align="C", txt=line, border=1)
                pdf_report.set_font("Times", size=16)
            elif "This feature" in line:
                pdf_report.multi_cell(200, 10, align="L", txt=line, border=1)
            else:
                pdf_report.multi_cell(200, 10, align="L", txt=line) 
    pdf_report.output(pdf_filepath)
    return Path(pdf_filepath) if os.path.exists(pdf_filepath) else None

def generate_visual_report(file_id: str, visuals : dict) :
    if os.path.exists(f"{BASE_DIR}/temp_visuals"):
        shutil.rmtree(f"{BASE_DIR}/temp_visuals")
    else:
        mkdir(f"{BASE_DIR}/temp_visuals")
    for key, value in visuals.items():
        if not value:
            continue
        if isinstance(value, list):
            mkdir(f"{BASE_DIR}/temp_visuals") if not os.path.exists(f"{BASE_DIR}/temp_visuals") else None
            
            for i,sub_value in enumerate(value):
                img_data = b64decode(sub_value)
                with open(f"{BASE_DIR}/temp_visuals/{key}_{i}_{file_id}.png", "wb") as img_file:
                    img_file.write(img_data)             
        else:
            mkdir(f"{BASE_DIR}/temp_visuals") if not os.path.exists(f"{BASE_DIR}/temp_visuals") else None
            img_data = b64decode(sub_value.split(",")[1])
            with open(f"{BASE_DIR}/temp_visuals/{key}_{file_id}.png", "wb") as img_file:
                img_file.write(img_data)
    reports_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    zip_path = shutil.make_archive(base_name=os.path.join(reports_dir, "visuals_zipped"), format="zip", root_dir=f"{BASE_DIR}/temp_visuals")
    return zip_path, Path(f"{BASE_DIR}/temp_visuals") if os.path.exists(f"{BASE_DIR}/temp_visuals") else None

def generate_eda_report(file_id: str, results: dict, inferences: dict, dim: tuple, features: dict) -> Path | None:
    filepath=os.path.join(BASE_DIR, "reports")
    os.makedirs(filepath, exist_ok=True)
    txt_filepath=os.path.join(filepath, f"{file_id}_eda_report.txt")
    pdf_filepath=os.path.join(filepath, f"{file_id}_eda_report.pdf")

    with open(txt_filepath, "w") as f:
        f.write("Exploratory Data Analysis Report\n".upper())
        f.write("\n\n")
        f.write(f"Dataset Dimensions \n{dim['Rows']} rows, {dim['Columns']} columns\n\n")
        f.write("Feature Summary:\n")
        for key, value in results.items():
            f.write(f"{key.upper()}:\n")
            f.write(f"This feature is likely to be {features.get(key)} type\n")
            #value is a list of tuples
            if not value:
                f.write("No data available\n\n")
                continue
            if isinstance(value, list):
                for items in value:
                    f.write(f"  {items[0]}: {items[1]}\n")
            else:
                f.write(f"{value}\n")
            f.write("\n")

        f.write("Inferences:\n")
        for key, value in inferences.items():
            f.write(f"{key.upper()}:\n")
            if not value:
                f.write("No data available\n\n")
                continue
            if isinstance(value, list):
                for items in value:
                    f.write(f"  {items}\n")
            else:
                f.write(f"{value}\n")
            f.write("\n")
    print(f"Text report generated at: {txt_filepath}")
      
    pdf_report = FPDF()
    pdf_report.add_page()
    pdf_report.set_font("Times", size=14)
    with open(txt_filepath, "r") as f:
        for line in f:
            if line=="Exploratory Data Analysis Report\n".upper():
                pdf_report.set_font("Times", style="B", size=16)
                pdf_report.multi_cell(200, 10, align="C", txt=line, border=1)
                pdf_report.set_font("Times", size=16)
            elif "This feature" in line:
                pdf_report.multi_cell(200, 10, align="L", txt=line, border=1)
            else:
                pdf_report.multi_cell(200, 10, align="L", txt=line) 
    pdf_report.output(pdf_filepath)
    return Path(pdf_filepath) if os.path.exists(pdf_filepath) else None