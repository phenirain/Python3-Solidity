from models import create_db, Users
from Library_Managment_System.models import session
from Library_Managment_System.utilities import inputs, admin_actions
from Library_Managment_System.utilities.actions import user_actions


def main():
    user = Users()
    create_db()
    prompt = ["[1] - log in\n[2] - sign up\nYour choice: "]
    response = int("".join(inputs(prompt, [int], [1, 2])))
    admin = False
    if response == 1:
        admin = user.log_in(session())
    else:
        user.sign_up(session())
    if admin:
        response = 0
        while response != 4:
            prompt = ["Let choose your action:\n"
                      "[1] - add/modify/delete book\n"
                      "[2] - add/modify/delete user\n"
                      "[3] - take/return book\n"
                      "[4] - exit program\n"
                      "Your choice: "]
            response = int("".join(inputs(prompt, [int], [1, 2, 3, 4])))
            self_delete = admin_actions(session(), response, admin=user)
            if self_delete:
                return main()
    else:
        response = 0
        while response != 3:
            prompt = ["Let choose your action:\n"
                      "[1] - modify/delete yourself\n"
                      "[2] - take/return book\n"
                      "[3] - exit program\n"
                      "Your choice: "]
            response = int("".join(inputs(prompt, [int], [1, 2, 3])))
            self_delete = user_actions(session(), response, user)
            if self_delete:
                return main()


if __name__ == "__main__":
    main()
