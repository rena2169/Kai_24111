import random
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from database import Base, SessionLocal, engine
from models import Link
from schemas import URLCreate

BASE_URL = "http://lab5.chayka-cafe.ru"

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/shorten")
def shorten(payload: URLCreate):
    if not payload.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Невалидный URL")

    db = SessionLocal()
    existing = db.query(Link).filter(Link.url == payload.url).first()

    if existing:
        db.close()
        return {"short": f"{BASE_URL}/{existing.code}"}

    code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    link = Link(code=code, url=payload.url)
    db.add(link)
    db.commit()
    db.close()
    return {"short": f"{BASE_URL}/{code}"}


@app.get("/{code}")
def redirect(code: str):
    db = SessionLocal()
    link = db.query(Link).filter(Link.code == code).first()
    db.close()

    if link is None:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    return RedirectResponse(link.url)