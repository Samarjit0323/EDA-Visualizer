from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.eda import EDA
from services.stats import StatsAnalyser
from helper.file import file_to_df
from helper.info import get_stats_info, get_stats_detailed_info, get_static_media, get_formula

app=FastAPI()
templates=Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

df, filename, extension =file_to_df("static/datasets/weight-height.csv")
eda=EDA(df, filename, extension)
stats=StatsAnalyser(df)

@app.get("/home")
@app.get("/", name="home")
def home(request: Request):
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

@app.get("/action")
def action(request: Request):
    eda.dimensions()
    eda.get_dtypes()
    context={
        "eda":eda,
    }
    return templates.TemplateResponse(request,"ready_landing.html",context=context)

@app.get("/stats", name='stats')
def stats_analysis(request: Request):
    stats_info=get_stats_info()
    return templates.TemplateResponse(request, "stats.html",context={"stats":stats, "info":stats_info})

@app.get("/learn_stats", name="learn_stats")
def learn_stats(request: Request):
    stats_info=get_stats_detailed_info()
    images=get_static_media()
    formula=get_formula()
    return templates.TemplateResponse(request, "learn_stats.html",context={"info":stats_info,'images':images, "formula":formula})