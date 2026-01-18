from fastapi import FastAPI, Depends
import database_models
from models import product
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
database_models.Base.metadata.create_all(bind=engine)


products=[
    product(id=1, name="phone", description="budget phone", price=299.99, quantity=50),
    product(id=2, name="laptop", description="gaming laptop", price=999.99, quantity=20),
]
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
def init_db():
    db=SessionLocal()
    count=db.query(database_models.product).count()
    if count==0:
        for product in products:
            db.add(database_models.product(**product.model_dump()))
            db.commit()

init_db()
@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_product(product: product,db:Session=Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.add(database_models.product(**product.model_dump()))
        db.commit()
        return "product updated successfully"
    return "product not found"

@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    return "invalid id" 
