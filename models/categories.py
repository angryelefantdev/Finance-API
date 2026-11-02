from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Categories(Base):
    __tablename__ = "categories"
    user = relationship("Users",back_populates="category")
    transaction = relationship("Transactions",back_populates="category")
    category_id = Column(Integer,primary_key=True)
    category_name = Column(String(100))
    user_id = Column(Integer,ForeignKey("users.id"))