from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "t_user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
    dept_id = Column(Integer, unique=True)