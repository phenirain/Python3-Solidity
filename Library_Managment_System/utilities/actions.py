from datetime import datetime

from Library_Managment_System.utilities import inputs, check_to_continue
from Library_Managment_System.models import Books, Users, Library, Admins
from .help_actions import get_book_id, get_user_id, get_book, modify_book, modify_user, delete_user, return_book
from sqlalchemy.orm import Session


def simple_actions(db_session: Session, user_id):
    response = 0
    while response != 3:
        prompt = ["Let choice your action:\n"
                  "[1] - take book\n"
                  "[2] - return book\n"
                  "[3] - get back\n"
                  "Your choice: "]
        response = int("".join(inputs(prompt, [int], [1, 2, 3])))
        if response == 1:
            book_id = get_book_id(db_session)
            if book_id:
                get_book(db_session, user_id, book_id)
        elif response == 2:
            return_book(db_session, user_id)


def admin_actions(db_session: Session, action: int, admin: Users):
    message = ("Let choice your action:\n"
               "[1] - add new ?\n"
               "[2] - modify ?\n"
               "[3] - delete ?\n"
               "[4] - get back\n"
               "Your choice: ")
    response = 0
    if action == 1:
        while response != 4:
            prompt = [message.replace("?", "book")]
            response = int("".join(inputs(prompt, [int], [1, 2, 3, 4])))
            if response == 1:
                prompt = ["Input the book title: ", "Input the author of the book: "]
                title, author = inputs(prompt, [str, str])
                while True:
                    try:
                        year = datetime.strptime(input("Input book`s year: "), '%d.%m.%Y').date()
                        break
                    except Exception:
                        print("Date`s format is dd.mm.yyyy(13.01.2006)\n")
                books = Books().select(db_session)
                for book in books:
                    if title == book.title:
                        print("title`s book is not unique(")
                        return admin_actions(db_session, action)
                book_params = {
                    "title": title,
                    "author": author,
                    "year": year
                }
                Books().add(db_session, book_params)
                books = Books().select(db_session)
                library_params = {
                    "book_id": books[-1].id
                }
                Library().add(db_session, library_params)
                print("Adding successfully!\n")
            elif response == 2:
                cont = True
                while cont:
                    book_id = get_book_id(db_session)
                    modify_item = modify_book()
                    Books().update(db_session, identifier=book_id, params=modify_item)
                    print("Updating successfully!\n")
                    cont = check_to_continue()
            elif response == 3:
                all_books = Books().get_all_books(db_session)
                library_books = Library().select(db_session)
                library_books = [record.book_id for record in library_books]
                book_id = int("".join(inputs(["Let choice book`s id: "], [int], all_books)))
                if book_id in library_books:
                    library = Library().select(db_session, params={"book_id": book_id})[-1]
                    Library().delete(db_session, identifier=library.id)
                Books().delete(db_session, identifier=book_id)
                print("Removal successfully\n")
    elif action == 2:
        while response != 4:
            prompt = [message.replace("?", "user")]
            response = int("".join(inputs(prompt, [int], [1, 2, 3, 4])))
            if response == 1:
                Users().sign_up(db_session, adding=True)
            elif response == 2:
                cont = True
                while cont:
                    user_id = get_user_id(db_session)
                    modify_item = modify_user(db_session, admin=True)
                    if user_id == admin.id and "login" in list(modify_item.keys()):
                        admin_class = Admins().select(db_session, params={"login": admin.login})[-1]
                        Admins().update(db_session, identifier=admin_class.id, params=modify_item)
                    Users().update(db_session, identifier=user_id, params=modify_item)
                    print("Updating successfully\n")
                    cont = check_to_continue()
            elif response == 3:
                self_delete = delete_user(db_session, admin=admin)
                if self_delete:
                    return True
    elif action == 3:
        cont = True
        while cont:
            simple_actions(db_session, admin.id)
            cont = check_to_continue()
    else:
        print("Program is closed\nSee you later!")


def user_actions(db_session: Session, action: int, user: Users):
    if action == 1:
        response = 0
        while response != 3:
            prompt = ["Let choose your action:\n"
                      "[1] - modify yourself\n"
                      "[2] - delete yourself\n"
                      "[3] - get back\n"
                      "Your choice: "]
            response = int("".join(inputs(prompt, [int], [1, 2, 3])))
            if response == 1:
                modify_item = modify_user(db_session, user_password=user.password)
                if modify_item:
                    if "password" in modify_item.keys():
                        user.password = modify_item["password"]
                    if "login" in modify_item.keys():
                        user.login = modify_item["login"]
                    Users().update(db_session, identifier=user.id, params=modify_item)
                    print("Updating succesfully")
            elif response == 2:
                self_delete = delete_user(db_session, user_id=user.id)
                if self_delete:
                    return True
    elif action == 2:
        cont = True
        while cont:
            simple_actions(db_session, user.id)
            cont = check_to_continue()
