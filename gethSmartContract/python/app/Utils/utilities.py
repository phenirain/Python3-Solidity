import re


def check_password(password: str) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
    return re.search(pattern, password) and len(
        password) > 12 and "qwerty" not in password and "password" not in password


