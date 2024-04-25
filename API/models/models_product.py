from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base
from pydantic import BaseModel

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), default="Default Name")
    description = Column(String(250), default="Default Description")
    price = Column(Float, default=0)

class ProductBase(BaseModel) :
    id: int
    name: str
    description: str
    price: float

class ProductResponse(BaseModel) :
    name: str
    description: str
    price: float





