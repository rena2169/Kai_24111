from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///tasks.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)