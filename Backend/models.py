from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email    = Column(String, unique=True, nullable=False, index=True)  # ← added
    password = Column(String, nullable=False)

class History(Base):
    __tablename__ = "history"
    id           = Column(Integer, primary_key=True, index=True)
    input_text   = Column(String, nullable=False)
    mbart_output = Column(String, nullable=True)
    mt5_output   = Column(String, nullable=True)
    username     = Column(String, nullable=True)