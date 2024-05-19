from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi
import re
from typing import List

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)


class User:

    public_key: str
    password: str

    def __check_password(password: str) -> bool:
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
        return re.search(pattern, password) and len(password) > 12 and "qwerty" not in password and "password" not in password


    def sign_up(self) -> None:
        password = input("Придумайте пароль: ")
        if self.__check_password(password):
            self.password = password
            self.public_key = w3.geth.personal.new_account(password)
            print(f"Ваш публичный ключ: {self.public_key}")
        else:
            print("Пароль не соответсвует требованиям\nБольше 12 символов\nСодержит прописные буквы\nСодержит строчные буквы\nНе содержит спец символов или пробелов")

    def log_in(self) -> None:
        public_key = input("Введите Ваш публичный ключ: ")
        password = input("Введите Ваш пароль: ")
        if self.public_key == public_key and self.password == password:
            w3.geth.personal.unlock_account(self.public_key, self.password)
            print("Авторизация успешна!")
        else:
            print("Не корректные данные!")

    def deposit(self) -> None:
        try:
            wei = int(input("Введите сумму в WEI для пополнения: "))
            contract.functions.deposit().transact({
                "value": wei,
                "from": self.public_key
            })
            print(f"Успешное пополнение баланса на {wei} WEI")
        except ValueError:
            print("Не корректный ввод суммы")

    def withdraw(self) -> None:
        try:
            wei = int(input("Введите сумму в WEI для снятия: "))
            contract.functions.withdraw(wei).transact({
                "from": self.public_key
            })
            print(f"Успешный вывод средств себе на счет в размере: {wei} WEI")
        except ValueError:
            print("Не корректный ввод суммы")

    def balance(self) -> None:
        wei = w3.eth.get_balance(self.public_key)
        print(f"Ваш личный счет: {wei} WEI")

    def get_my_balance_on_contract(self) -> None:
        wei = contract.functions.getBalance().call({
            "from": self.public_key
        })
        print(f"Ваш баланс на контракте: {wei} WEI")
        
    def create_estate(self) -> None:
        try:
            size = int(input(f"Введите размер недвижки: "))
            address = input(f"Введите адрес недвижки: ")
            print("Все типы недвижимости:\n1.Дом\n2.Квартира\n3.Чердак\n")
            estate_type = int(input(f"Введите тип недвижимости: "))
            contract.functions.createEstate(size, address, estate_type).transact({
                'from': self.public_key
            })
            print(f"Недвижка успешно создана!")
        except ValueError:
            print("Не корректный ввод данных")
        except Exception as e:
            print(f"Ошибка: {e}")

    def create_advert(self) -> None:
        try:
            price = int(input(f"Введите цену недвижки: "))
            estate_id = int(input(f"Введите айди недвижки: "))
            contract.functions.createAdv(estate_id, price).transact({
                'from': self.public_key
            })
            print(f"Объявление успешно создано")
        except ValueError:
            print("Не корректный ввод данных")
        except Exception as e:
            print(f"Ошибка: {e}")

    def change_estate_status(self) -> None:
        try:
            estate_id = int(input('Введите айди недвижимости, статус которой хотите поменять: '))
            contract.functions.changeStatusOfEstate(estate_id).transact({
                'from': self.public_key
            })
            print(f"Статус успешно изменён!")
        except ValueError:
            print("Не корректный ввод данных")
        except Exception as e:
            print(f"Ошибка: {e}")

    def change_advert_status(self) -> None:
        try:
            advert_id = int(input('Введите айди объявления, статус которого хотите поменять: '))
            contract.functions.changeStatusOfAdv(advert_id).transact({
                'from': self.public_key
            })
            print(f"Статус успешно изменён")
        except ValueError:
            print("Не корректный ввод данных")
        except Exception as e:
            print(f"Ошибка: {e}")

    def buy_estate(self)-> None:
        try:
            advert_id = int(input('Введите айди объявления, по которому хотите купить недвижимость: '))
            contract.functions.buyEstate(advert_id).transact({
                'from': self.public_key
            })
            print(f"\nСтатус успешно изменён!")
        except ValueError:
            print("Не корректный ввод данных")
        except Exception as e:
            print(f"\nЧто-то пошло не так, ошибка {e}")

    def get_all_estates(self) -> None:
        try:
            estates = contract.functions.getEstates().call({
                'from': self.public_key
            })
            print(f'Доступная недвижимость:')
            for i, estate in enumerate(estates):
                print(f"{i + 1}. {estate}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def get_all_advertisments(self) -> None:
        try:
            ads = contract.functions.getAds().call({
                'from': self.public_key
            })
            print(f'Доступные объявления: ')
            for i, adv in enumerate(ads):
                print(f"{i + 1}. {adv}")
        except Exception as e:
            print(f"Ошибка {e}")

    def get_info(self):
        while True:
            actions = [self.get_all_estates, self.get_all_advertisments, self.get_my_balance_on_contract, self.balance]
            actions_info = ['Доступная недвижимость', 'Текущие объявления о продаже', 'Баланс на смартконтракте',
                    'Баланс аккаунта', 'Выход']
            print("Доступные действия: ")
            for i, action in enumerate(actions_info):
                print(f"{i + 1}. {action}")
            try:
                action = int(input("Что Вы хотите сделать: "))
                if action > 0 and action <= len(actions):
                    actions[action - 1]()
                elif action == len(actions_info):
                    break
                else:
                    print("Я не знаю такую команду")
            except ValueError:
                print("Я не знаю такую команду")
            except Exception as e:
                print(f"Ошибка: {e}")

    def get_public_key(self) -> str:
        return self.public_key


def main():
    while True:
        current_user: User = User()
        if current_user.get_public_key is None:
            print("Приветствую, чего Вы хотите:\n"
              "1 - Зарегистрироваться\n"
              "2 - Авторизоваться\n"
              "3 - Выход\n")
            action = input("Ваше действие: ")
            match action:
                case "1":
                    current_user.sign_up()
                case "2":
                    current_user.log_in()
                case "3":
                    print("Пока")
                    break
                case _:
                    print("Введите 1 или 2 или 3")
                    continue
        else:
            actions = [current_user.create_estate, current_user.create_advert, current_user.change_estate_status, current_user.change_advert_status, current_user.buy_estate, current_user.withdraw, current_user.get_info, current_user.deposit]
            actions_info = ['Создать недвижимость', 'Создать объявление', 'Изменить статус недвижимости',
                                          'Изменить статус объявления', 'Покупка недвижимости', 'Вывод средств',
                                          'Получение информации', 'Пополнить аккаунт', 'Выход']
            print("Все доступные действия")
            for i, action in enumerate(actions_info):
                print(f"{i + 1}. {action}")
            try:
                action = int(input("Ваше действие: "))
                if action > 0 and action <= len(actions):
                    actions[action - 1]()
                elif action ==  len(actions_info):
                    current_user = User()
                    continue
                else:
                    print("Не знаю такую команду")
            except ValueError:
                print("Не знаю такую команду")
            except Exception as e:
                print(f"Ошибка: {e}")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Программа завершена")



