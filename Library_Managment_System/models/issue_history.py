from sqlalchemy import Integer, String, Column, ForeignKey
from .database import LibraryBase


class Issue_history(LibraryBase):
    __tablename__ = "issue_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    action = Column(String)
