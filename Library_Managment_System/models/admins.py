from sqlalchemy import Integer, String, Column
from .database import LibraryBase


class Admins(LibraryBase):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
