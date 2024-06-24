from typing import Optional

from .UserRepository import UserRepository, UserModel
from .Models import User
from .Utils import check_password
from app import w3, contract


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, id: int) -> User:
        user: UserModel = self.user_repository.get_user_by_id(id)
        current: User = User(user_id=user.id, password=user.password, public_key=user.public_key)
        return current

    def create_user(self, password: str) -> Optional[User]:
        if check_password(password):
            public_key: str = w3.geth.personal.new_account(password)
            user: UserModel = self.user_repository.create_user(password, public_key)
            current: User = User(user_id=user.id, password=user.password, public_key=user.public_key)
            w3.geth.personal.unlock_account(public_key, password)
            w3.eth.send_transaction({
                'from': w3.eth.coinbase,
                'to': public_key,
                'value': 5000000000000000
            })
            return current
        else:
            return None
        
    def get_user_by_info(self, password: str, public_key: str) -> User:
        user: UserModel = self.user_repository.get_user_by_info(password, public_key)
        if user:
            current: User = User(user_id=user.id, password=password, public_key=public_key)
            return current
        else:
            return None


