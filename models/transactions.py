from sqlalchemy import Column,String,Integer,ForeignKey,Numeric,Date
from sqlalchemy.orm import relationship
from database import Base

class Transactions(Base):
    __tablename__ = "transactions"
    category = relationship("Categories",back_populates="transaction")
    user = relationship("Users",back_populates="transaction")
    transaction_id = Column(Integer,primary_key=True)
    amount = Column(Numeric(12,2))
    type = Column(String(100))
    description = Column(String(100))
    date = Column(Date)
    user_id = Column(Integer,ForeignKey("users.id"))
    category_id = Column(Integer,ForeignKey("categories.category_id"))