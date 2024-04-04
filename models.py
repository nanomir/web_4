from sqlalchemy import Column, Integer, String
from database import base

class Tuples(base):
    __tablename__ = "userList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    todo = Column(String)