from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app=FastAPI()
templates=Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
