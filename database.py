from sqlalchemy.orm import sessionmaker,Session,declarative_base
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

DBPW = os.getenv("DBPW")




Base = declarative_base()

engine = create_engine(f"postgresql+psycopg2://postgres:{DBPW}@localhost:5432/financedatabase")

localsesh = sessionmaker(bind=engine)
