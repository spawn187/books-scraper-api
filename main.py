from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Létrehozzuk az adatbázist, bár a scraper már valószínűleg megtette
models.Base.metadata.create_all(bind=engine)

# Az API inicializálása
app = FastAPI(
    title="Books Scraper API",
    description="RESTful API a Books to Scrape oldalról gyűjtött adatokhoz.",
    version="1.0.0"
)

# Adatbázis session kezelése minden kéréshez
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Végpont: Könyvek listázása lapozással
@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Visszaadja a könyvek listáját. Támogatja a lapozást (skip és limit)."""
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

# 2. Végpont: A legdrágább könyv lekérése
@app.get("/books/statistics/most-expensive", response_model=schemas.Book)
def get_most_expensive_book(db: Session = Depends(get_db)):
    """Visszaadja a legdrágább könyvet."""
    book = db.query(models.Book).order_by(models.Book.price.desc()).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Nem található könyv az adatbázisban.")
    return book

# 3. Végpont: A legolcsóbb könyv lekérése
@app.get("/books/statistics/least-expensive", response_model=schemas.Book)
def get_least_expensive_book(db: Session = Depends(get_db)):
    """Visszaadja a legolcsóbb könyvet."""
    book = db.query(models.Book).order_by(models.Book.price.asc()).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Nem található könyv az adatbázisban.")
    return book