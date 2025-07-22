from app.core.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(70))
    email = Column(String(70), unique=True)
    password = Column(String(250))
