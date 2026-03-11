from pydantic import BaseModel, ConfigDict

# Alapséma a könyv adataihoz
class BookBase(BaseModel):
    title: str
    price: float
    in_stock: bool
    rating: int
    category: str

# Ez a séma az adatbázisból visszaadott könyveket írja le (tartalmazza az ID-t is)
class Book(BookBase):
    id: int

    # Ez teszi lehetővé, hogy a Pydantic automatikusan olvasson az SQLAlchemy adatbázis modellekből
    model_config = ConfigDict(from_attributes=True)