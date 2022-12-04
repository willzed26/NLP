import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
import fileinput

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

# Membaca dataset(excel)
df = pd.read_csv('file.csv')

# df.head()

# Membuat DataFrame kolom 'Lyric' menjadi n-dimensional array
lyricss = df['Lyric'].str.lower()
lyrics = lyricss.values.astype(str)

"""# **TF IDF**"""

# Menggunakan TfidfVectorizer() yang didalamnya dapat menghitung CountVectorizer dan TfidfTransformer
vectorizer = TfidfVectorizer()

# %%time
X = vectorizer.fit_transform(lyrics) # TF

"""# **INPUT USER**"""

@app.post("/")
async def create_item(request: Request, input:str = Form(...)):
    query = input.lower() # Input user
    query_vec = vectorizer.transform([query]) # TF-IDF
    results = cosine_similarity(X,query_vec).reshape((-1)) # Mencari kesamaan pada dataset dengan yang di input oleh user
    list=[]
    dummy3=""
    for i in np.argsort(results)[-5:]:
        dummy1 = str(df.iloc[i,1])
        dummy2 = str(df.iloc[i,2])
        dummy3=dummy1+"-"+dummy2
        list.append(dummy3)
    context = {'request': request, 'list': list}
    return templates.TemplateResponse("index.html", context)
