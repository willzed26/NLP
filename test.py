from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
# from main import list

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
background = "static/background.webp"

@app.get("/", response_class=HTMLResponse)
async def read(request: Request):
    context = {'request': request, 'background': background}
    return templates.TemplateResponse("index.html", context)

class Item(BaseModel):
    name: str

@app.post("/item")
async def create_item(item: Item):
    
    return item
