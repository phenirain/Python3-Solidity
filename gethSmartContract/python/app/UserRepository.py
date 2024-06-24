from sqlalchemy import select
from .database import UserModel
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user_by_id(self, id: int) -> UserModel:
        with self.db() as session:
            return session.execute(select(UserModel).where(UserModel.id == id)).scalar_one()

    def create_user(self, password: str, public_key: str) -> UserModel:
        with self.db() as session:
            user = UserModel(password=password, public_key=public_key)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
    def get_user_by_info(self, password: str, public_key: str) -> UserModel:
        with self.db() as session:
            query = select(UserModel).where((UserModel.password == password) & (UserModel.public_key == public_key))
            return session.execute(query).scalar_one()         

