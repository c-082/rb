import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from db.connection import get_database

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    db = await get_database()
    async with db.execute("SELECT exp FROM user") as cursor:
        rows = await cursor.fetchall()
    exp_values = [row[0] for row in rows]
    return templates.TemplateResponse("index.html", {"request": request, "exp": exp_values})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
