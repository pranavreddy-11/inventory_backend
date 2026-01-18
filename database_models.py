from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base=declarative_base()
class product(Base):
    __tablename__='product'
    id=Column(Integer, primary_key=True, index=True,autoincrement=True)
    name=Column(String)
    description=Column(String)
    price=Column(Float)
    quantity=Column(Integer)