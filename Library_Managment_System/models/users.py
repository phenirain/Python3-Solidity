from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Library_Managment_System.utilities import inputs
from .database import LibraryBase
from .admins import Admins


class Users(LibraryBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String, unique=True)
    login = Column(String, unique=True)
    password = Column(String)

    def log_in(self, db_session: Session):
        prompts = ["Input login: ", "Input password: "]
        types = [str, str]
        login, password = inputs(prompts, types)
        admins = [admin.login for admin in Admins().select(db_session)]
        users = self.select(db_session)
        for user in users:
            if login == user.login:
                if password == user.password:
                    self.login = login
                    self.password = password
                    self.id = user.id
                    print(f"Hello, {self.login}")
                    if login in admins:
                        return True
                    return False
        print("Login or password is incorrect(")
        return self.log_in(db_session)

    def sign_up(self, db_session: Session, adding=False):
        try:
            prompts = ["Input name: ", "Input surname: ", "Input patronymic(if it exists, else '-'): "]
            types = [str, str, str]
            name, surname, patronymic = inputs(prompts, types)
            user_info = {
                "fullname": "",
                "login": "",
                "password": ""
            }
            fullname = f"{surname} {name}{f' {patronymic}' if patronymic != '-' else ''}"
            user_info['fullname'] = fullname
            users = self.select(db_session)
            logins = []
            for user in users:
                logins.append(user.login)
                if user.fullname == self.fullname:
                    raise ValueError
            user_info['login'] = "".join(inputs(["Input login: "], [str]))
            self.login = user_info['login']
            if self.login in logins:
                raise IntegrityError(statement="", params="", orig=BaseException)
            user_info['password'] = "".join(inputs(["Input password: "], [str]))
            self.add(db_session, params=user_info)
            if not adding:
                new_user = self.select(db_session, params={"login": self.login})[-1]
                self.id = new_user.id
                print(f"Hello, {self.login}")
            else:
                print("Adding successfully")
        except IntegrityError:
            print("This login is already exists(\n")
            if adding:
                return self.sign_up(db_session, adding)
            return self.sign_up(db_session)
        except ValueError:
            print("User with this fullname already exists(\n")
            if adding:
                return self.sign_up(db_session, adding)
            return self.sign_up(db_session)
