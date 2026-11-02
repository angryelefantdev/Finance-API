from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "users"
    transaction = relationship("Transactions",back_populates="user")
    category = relationship("Categories",back_populates="user")
    id = Column(Integer,primary_key=True)
    username = Column(String(100),unique=True)
    hashed_password = Column(String)