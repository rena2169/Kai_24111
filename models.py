from sqlalchemy import Column, Integer, String
from database import Base


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    url = Column(String, unique=True)