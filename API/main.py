from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Annotated
import models.models_product as models_product
import models.models_users as models_users
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models.models_product import ProductBase, ProductResponse
from models.models_users import UserBase, UserResponse


app = FastAPI()
models_product.Base.metadata.create_all(bind=engine)
models_users.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(user: ProductBase, db: db_dependency):
    print("Received user data:", user.dict())
    try:
        db_product = models_product.Product(**user.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        print("Error creating user:", e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.get("/products", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_products(db: Session = Depends(get_db)):
    products = db.query(models_product.Product).all()
    return products

@app.get("/product/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_byid(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models_product.Product).filter(models_product.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.delete("/product/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int , db: Session = Depends(get_db)):
    # Check if the user exists in the database
    product = db.query(models_product.Product).filter(models_product.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # Delete the user from the database
    db.delete(product)
    db.commit()
    return {"message": "Successfully deleted product"}

@app.put("/product/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, updated_product: ProductResponse, db: Session = Depends(get_db)):
    existing_product = db.query(models_product.Product).filter(models_product.Product.id == product_id).first()
    if existing_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for field, value in updated_product.dict().items():
        setattr(existing_product, field, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product

#----------------------------------------------------------C R U D    U S E R S-------------------------------

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    print("Received user data:", user.dict())
    try:
        db_user = models_users.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print("Error creating user:", e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
@app.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    products = db.query(models_users.User).all()
    return products

@app.get("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_byid(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models_users.User).filter(models_users.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user

@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int , db: Session = Depends(get_db)):
    user = db.query(models_users.User).filter(models_users.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    db.delete(user)
    db.commit()
    return {"message": "Successfully deleted user"}

@app.put("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, updated_user: UserResponse, db: Session = Depends(get_db)):
    existing_user = db.query(models_users.User).filter(models_users.User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    for field, value in updated_user.dict().items():
        setattr(existing_user, field, value)
    db.commit()
    db.refresh(existing_user)
    return existing_user
























