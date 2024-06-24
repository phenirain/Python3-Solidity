
from flask_login import UserMixin
from app import w3, contract


class User(UserMixin):
    def __init__(self, user_id, password, public_key):
        self.id = user_id
        self.password = password
        self.public_key = public_key
        w3.geth.personal.unlock_account(public_key, password)

    def deposit(self, wei: int, ) -> None:
        contract.functions.deposit().transact({
            "value": wei,
            "from": self.public_key
        })

    def withdraw(self, wei: int) -> None:
        contract.functions.withdraw(wei).transact({
            "from": self.public_key
        })

    def balance(self) -> None:
        return w3.eth.get_balance(self.public_key)

    def get_my_balance_on_contract(self) -> None:
        return contract.functions.getBalance().call({
            "from": self.public_key
        })
        
    def create_estate(self, size: int, address: str, estate_type_id: int) -> None:
        print(size, address, estate_type_id)
        print('################################')
        contract.functions.createEstate(size, address, estate_type_id).transact({
            'from': self.public_key
        })

    def create_advert(self, price: int, estate_id: int) -> None:
        contract.functions.createAdv(estate_id, price).transact({
            'from': self.public_key
        })

    def change_estate_status(self, estate_id: int) -> None:
        contract.functions.changeStatusOfEstate(estate_id).transact({
            'from': self.public_key
        })

    def change_advert_status(self, advert_id: int) -> None:
        contract.functions.changeStatusOfAdv(advert_id).transact({
            'from': self.public_key
        })

    def buy_estate(self,  advert_id: int)-> None:
        contract.functions.buyEstate(advert_id).transact({
            'from': self.public_key
        })

    def get_all_estates(self) -> None:
        return contract.functions.getEstates().call({
            'from': self.public_key
        })

    def get_all_advertisments(self) -> None:
        return contract.functions.getAdvs().call({
            'from': self.public_key
        })

    def get_public_key(self) -> str:
        return self.public_key



