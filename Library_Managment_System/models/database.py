from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

DATABASE_NAME = "library.sqlite"

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
session = sessionmaker(bind=engine)

Base = declarative_base()


class LibraryBase(Base):
    __abstract__ = True

    def add(self, db_session: Session, params=None):
        new_ex = self.__class__()
        for key, value in params.items():
            setattr(new_ex, key, value)
        db_session.add(new_ex)
        db_session.commit()

    def select(self, db_session: Session, identifier=None, params=None):
        query = db_session.query(self.__class__)
        if identifier:
            query = query.filter_by(id=identifier)
            return query.first()
        elif params:
            for key, value in params.items():
                query = query.filter(getattr(self.__class__, key) == value)
            result = query.all()
        else:
            result = query.all()
        return result

    def update(self, db_session: Session, identifier: int, params=None):
        result = db_session.query(self.__class__).filter_by(id=identifier).first()
        for key, value in params.items():
            setattr(result, key, value)
        db_session.commit()

    def delete(self, db_session: Session, identifier: int):
        result = db_session.query(self.__class__).filter_by(id=identifier).first()
        db_session.delete(result)
        db_session.commit()


def create_db():
    Base.metadata.create_all(engine)
