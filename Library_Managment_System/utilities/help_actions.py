from datetime import datetime
from Library_Managment_System.utilities import inputs
from Library_Managment_System.models import Books, Users, Library, Issue_history, Admins
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get_book_id(db_session: Session):
    all_books = Library().get_all_books(db_session)
    if all_books:
        record_id = int("".join(inputs(["Let choose book`s id: "], [int],
                                       all_books)))
        record = Library().select(db_session, identifier=record_id)
        return record.book_id
    return None


def get_user_id(db_session: Session):
    all_users = Users().select(db_session)
    users_ids = list()
    for user in all_users:
        users_ids.append(user.id)
        print(f"{user.id}: {user.fullname}, login: {user.login}")
    return int("".join(inputs(["Let choose user`s id: "], [int], users_ids)))


def get_book(db_session: Session, user_id, book_id):
    params = {
        "user_id": user_id,
        "book_id": book_id,
        "action": "get"
    }
    record = Library().select(db_session, params={"book_id": book_id})[-1]
    Library().delete(db_session, identifier=record.id)
    Issue_history().add(db_session, params=params)
    print("Getting succesfully!\n")


def return_book(db_session: Session, user_id):
    get_params = {
        "user_id": user_id,
        "action": "get"
    }
    return_params = {
        "user_id": user_id,
        "action": "return"
    }
    all_get_books = Issue_history().select(db_session, params=get_params)
    return_books = Issue_history().select(db_session, params=return_params)
    all_get_books = [book.book_id for book in all_get_books]
    return_books = [book.book_id for book in return_books]
    get_books = set([book for book in all_get_books if all_get_books.count(book) > return_books.count(book)])
    if get_books:
        all_books = dict()
        for id, book_id in enumerate(get_books):
            book = Books().select(db_session, identifier=book_id)
            all_books[id + 1] = book.id
            print(f"{id + 1}: {book.title}, {book.author}")
        book_id = int("".join(inputs(['Let choose book`s id: '], [int], list(all_books.keys()))))
        Library().add(db_session, params={"book_id": all_books[book_id]})
        history_params = {
            "user_id": user_id,
            "book_id": all_books[book_id],
            "action": "return"
        }
        Issue_history().add(db_session, params=history_params)
        print("Return successfully")
    else:
        print("You haven`t taken any books yet\n")


def modify_book():
    prompt = ["What you want to modify:\n"
              "[1] - title\n"
              "[2] - author\n"
              "[3] - year\n"]
    modify_to = int("".join(inputs(prompt, [int], [1, 2, 3])))
    if modify_to == 1:
        title = "".join(inputs(['Input new book`s title: '], [str]))
        return {"title": title}
    elif modify_to == 2:
        author = "".join(inputs(['Input new book`s author: '], [str]))
        return {"author": author}
    else:
        while True:
            try:
                year = "".join(inputs(['Input new book`s year: '], [str]))
                year = datetime.strptime(year, '%d.%m.%Y').date()
                return {"year": year}
            except Exception:
                print("Date`s format is dd.mm.yyyy(13.01.2006)\n")


def modify_user(db_session: Session, user_password=None, admin=False):
    prompt = ["What do you want to modify:\n"
              "[1] - fullname\n"
              "[2] - login\n"
              "[3] - password\n"
              "Your choice: "]
    modify_to = int("".join(inputs(prompt, [int], [1, 2, 3])))
    if modify_to == 1:
        prompts = ["Input name: ", "Input surname: ", "Input patronymic(if it exists, else '-'): "]
        types = [str, str, str]
        name, surname, patronymic = inputs(prompts, types)
        fullname = f"{surname} {name}{f' {patronymic}' if patronymic != '-' else ''}"
        return {"fullname": fullname}
    elif modify_to == 2:
        while True:
            try:
                login = "".join(inputs(['Input new login: '], [str]))
                users = Users().select(db_session)
                for user in users:
                    if user.login == login:
                        raise IntegrityError
                return {"login": login}
            except IntegrityError:
                print("User with this login already exists(\n")
    else:
        if not admin:
            i = 0
            while i < 3:
                old_password = "".join(inputs(["Input old password: "], [str]))
                if user_password == old_password:
                    new_password = "".join(inputs(['Input new password: '], [str]))
                    return {"password": new_password}
                else:
                    i += 1
                    print("Incorrect password\n"
                          f"You have got {3 - i} attempts left\n")
            print("Let remember your password and try again\n")
            return None
        else:
            new_password = "".join(inputs(['Input new password'], [str]))
            return {"password": new_password}


def delete_user(db_session: Session, user_id=None, admin=None):
    if user_id:
        delete = ""
        while delete != "n":
            delete = input("Are you sure you want to delete yourself(y/n): ").strip().lower()
            if delete == "y" or delete == "yes":
                Users().delete(db_session, identifier=user_id)
                print("Removal successfully!\n")
                return True
        print("It`s right decision\n")
        return False
    else:
        user = get_user_id(db_session)
        if admin.id == user:
            delete = ""
            while delete != "n":
                delete = input("Are you sure you want to delete yourself(y/n): ").strip().lower()
                if delete == "y" or delete == "yes":
                    admin_id = Admins().select(db_session, params={"login": admin.login})
                    Users().delete(db_session, identifier=admin.id)
                    Admins().delete(db_session, identifier=admin_id)
                    print("Removal successfully!\n")
                    return True
            print("It`s right decision\n")
            return False
        Users().delete(db_session, identifier=user)
        print("Removal successfully!")
