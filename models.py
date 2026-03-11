from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Book(Base):
    __tablename__ = "books" # Így fogják hívni a táblát az adatbázisban

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    category = Column(String, index=True)