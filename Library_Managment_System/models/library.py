from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import Session
from . import Books
from .database import LibraryBase


class Library(LibraryBase):
    __tablename__ = "library"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'))

    def get_all_books(self, db_session: Session):
        books = self.select(db_session)
        print("All available books: ")
        all_books = list()
        if books:
            for record in books:
                all_books.append(record.id)
                book = Books().select(db_session, identifier=record.book_id)
                print(f"{record.id}: {book.title}, {book.author}")
            return all_books
        else:
            print("There are no books available\n")
            return None
