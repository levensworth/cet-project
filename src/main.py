from pathlib import Path
import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init
from fastapi.middleware.cors import CORSMiddleware
from src.knn_engine_impl import KNNEngineImpl, PreferenceRecord, RecommendationRequestDTO
# decompress data
import zipfile
with open('data/1m_music_dataset.zip', 'rb') as f:
    zipfile.ZipFile(f).extractall('data')

with open(pathlib.Path('data/spotify_data.csv'), "r+") as f: s = f.read(); f.seek(0); f.write("idx" + s)


app = FastAPI(
    title='cet-music',
    debug=False,
    version='0.1.0',
)

htmx_init(templates=Jinja2Templates(directory=Path(".") / "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


engine = KNNEngineImpl(path=pathlib.Path('data/spotify_data.csv'))
# routers


@app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def root_page(request: Request):
    return {"greeting": "Hello World"}


@app.post("/search", response_class=HTMLResponse)
@htmx("search-results")
async def search(request: Request):
    form = await request.form()
    records = engine.search_for_song(query=str(form.get('search')))
    return {'records': [{"name": r.name, 'band': r.band, 'id': r.id} for r in records[:5]]}


@app.put("/liked/{record_id}", response_class=HTMLResponse)
@htmx("search-item")
async def add_search_item(
    record_id: int, 
    request: Request):
    record =  engine.get_song_by_id(record_id)
    if record is None:
        raise ValueError

    return {'record': {"name": record.name, 'band': record.band, "id": record.id, 'color': 'green'}}

@app.put("/disliked/{record_id}", response_class=HTMLResponse)
@htmx("search-item")
async def add_disliked(
    record_id: int, 
    request: Request):
    record =  engine.get_song_by_id(record_id)
    if record is None:
        raise ValueError

    return {'record': {"name": record.name, 'band': record.band, "id": record.id, 'color': 'red'}}


@app.post("/recommendation", response_class=HTMLResponse)
@htmx("recommendation")
async def get_recommendation(
    request: Request):
    form = await request.form()
            
    # format a query
    prediction = engine.predict(RecommendationRequestDTO(
        preference_records=[PreferenceRecord(id=int(k), is_positive= v == 'green') for k, v in form.items()]
    ))
    
    return {'records': [ {"name": record.name, 'band': record.band, "id": record.id} for record in prediction.records[:5]] } #{'record': {"name": record.name, 'band': record.band, "id": record.id, 'color': 'red'}}

