from sqlalchemy import Integer, String, Column, Date
from sqlalchemy.orm import Session

from .database import LibraryBase


class Books(LibraryBase):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    author = Column(String)
    year = Column(Date)

    def get_all_books(self, db_session: Session):
        books = self.select(db_session)
        print("All available books: ")
        all_books = list()
        if books:
            for book in books:
                all_books.append(book.id)
                print(f"{book.id}: {book.title}, {book.author}")
            return all_books
        else:
            print("There are no books available\n")
            return None
