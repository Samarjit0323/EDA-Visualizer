from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.eda import EDA
from services.stats import StatsAnalyser
from services.visuals import Visualization
from helper.file import file_to_df, generate_stats_report, generate_visual_report, generate_eda_report
from helper.info import get_stats_info, get_stats_detailed_info, get_static_media, get_formula
import pandas as pd
from io import BytesIO
from uuid import uuid4, UUID
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
import shutil

app=FastAPI()
templates=Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_DIR=Path(__file__).resolve().parent

@app.get("/home")
@app.get("/", name="home")
def home(request: Request):
    if os.path.exists(os.path.join(BASE_DIR, "reports")):
        shutil.rmtree(os.path.join(BASE_DIR, "reports"))
    os.mkdir(os.path.join(BASE_DIR, "reports"))
    return templates.TemplateResponse(request,"home.html", context={})

features = {"Visualizations": ["Histograms", "Box Plots", "Scatter Plots", "Correlation Heatmaps"],
            "Statistical Analysis": ["Summary Statistics",  "Measures of Central Tendency", "Measures of Dispersion"],
            "Exploratory Data Analysis": ["Missing Value Analysis", "Outlier Analysis"],}

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(request,"about.html", context={"features":features})

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(request,"contact.html", context={})

@app.post("/upload", name="upload")
async def upload(file: UploadFile ):
    content = await file.read()
    file_id=uuid4()
    if os.path.exists(os.path.join(BASE_DIR, "datasets")):
        shutil.rmtree(os.path.join(BASE_DIR, "datasets"))
    os.mkdir(os.path.join(BASE_DIR, "datasets"))
    filepath=os.path.join(BASE_DIR, "datasets",f"{file_id}.csv")
    with open(filepath,"wb") as f:
        f.write(content)
    return {"message":"success","fileid":str(file_id)}

@app.get("/download/{file_id}", response_class=FileResponse)
def download_file(file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(filepath, media_type="text/csv", filename=f"{file_id}.csv")

@app.get("/download/{file_id}/stats_report", response_class=FileResponse, name="download_stats_report")
def download_stats_report(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, _, _ =file_to_df(filepath)
    stats=StatsAnalyser(df)
    info=stats.get_stats
    features=stats.features
    file=generate_stats_report(file_id, info, features)
    if os.path.exists(file):
        return FileResponse(file, media_type="application/pdf", filename=f"{file_id}_stats_report.pdf")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error generating the report.")

@app.get("/download/{file_id}/visual_report", response_class=FileResponse, name="download_visual_report")
def download_visual_report(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, _, _ =file_to_df(filepath)
    viz=Visualization(df)
    visuals=viz.get_all()
    file,path=generate_visual_report(file_id, visuals)
    if path and os.path.exists(path):
        shutil.rmtree(path)
    if os.path.exists(file):
        return FileResponse(file, media_type="application/zip", filename=f"{file_id}_visual_report.zip")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error generating the report.")

@app.get("/download/{file_id}/eda_report", response_class=FileResponse, name="download_eda_report")
def download_eda_report(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, _, _ =file_to_df(filepath)
    eda=EDA(df, "", "")
    dim=eda.get_dimensions
    features=eda.features
    results, inferences=eda.get_results()
    file=generate_eda_report(file_id, results, inferences, dim, features)
    if os.path.exists(file):
        return FileResponse(file, media_type="application/pdf", filename=f"{file_id}_eda_report.pdf")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error generating the report.")

@app.get("/{file_id}/action", name="action")
def action(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, filename, extension =file_to_df(filepath)
    eda=EDA(df, filename, extension)
    context={
        "file_id": file_id,
        "filename": filename,
        "eda": eda
    }
    return templates.TemplateResponse(request, "ready_landing.html", context=context)

@app.get("/{file_id}/action/stats", name="stats")
def stats_analysis(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, _, _ =file_to_df(filepath)
    stats=StatsAnalyser(df)
    stats_info=get_stats_info()
    return templates.TemplateResponse(request, "stats.html",context={"stats":stats, "info":stats_info,"file_id":file_id})

@app.get("/{file_id}/action/visuals", name="visuals")
def get_visuals(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, _, _ =file_to_df(filepath)
    visuals=Visualization(df)
    plots=visuals.get_all()
    return templates.TemplateResponse(request, "visuals.html", context={"plots":plots,"file_id":file_id})

@app.get("/{file_id}/action/eda", name="eda")
def get_eda(request: Request, file_id: UUID):
    filepath=os.path.join(BASE_DIR, f"datasets/{file_id}.csv")
    df, filename, extension =file_to_df(filepath)
    eda=EDA(df, filename, extension)
    dim=eda.get_dimensions
    results, inferences=eda.get_results()
    print(inferences)
    return templates.TemplateResponse(request, "eda.html", context={"eda":eda,"file_id":file_id,"dim":dim, "results":results, "inferences":inferences})

@app.get("/learn/stats", name="learn_stats")
def learn_stats(request: Request):
    stats_info=get_stats_detailed_info()
    images=get_static_media()
    formula=get_formula()
    return templates.TemplateResponse(request, "learn_stats.html",context={"info":stats_info,'images':images, "formula":formula})

@app.get("/learn/visuals", name="learn_visuals")
def learn_visuals(request: Request):
    return templates.TemplateResponse(request, "coming_soon.html",context={})

@app.get("/learn/eda", name="learn_eda")
def learn_eda(request: Request):
    return templates.TemplateResponse(request, "coming_soon.html",context={})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse(request, "coming_soon.html", context={})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse(request, "coming_soon.html", context={})

#Exception handlers

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message=(
        exception.detail 
        if exception.status_code 
        else "An unexpected error occurred. Please try again later."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": f"Error {exception.status_code}",
            "message": message
        },
        status_code=exception.status_code
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Validation Error",
            "message": "Invalid input. Please check your data and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

@app.exception_handler(Exception)
def general_exception_handler(request: Request, exception: Exception):
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "title": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )