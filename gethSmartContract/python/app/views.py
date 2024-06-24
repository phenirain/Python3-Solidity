from typing import Optional
import time

from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_login import login_user, current_user, login_required, logout_user
from app import app, login_manager
from .Models import User
from .UserRepository import UserRepository
from .UserService import UserService
from .database import session

user_repository = UserRepository(session=session)
user_service = UserService(user_repository=user_repository)


@app.template_filter('enumerate')
def do_enumerate(iterable):
    return enumerate(iterable)

@login_manager.user_loader
def load_user(id):
    return user_service.get_user_by_id(id)


# getters

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html")

# require login

# getters and setters
@app.route('/advertisements', methods=['GET', 'POST', 'PUT'])
@login_required
def advertisements():
    user: User = current_user
    advs = user.get_all_advertisments()
    length = len(advs)
    estates = [est for est in user.get_all_estates() if est[4] == True]
    statuses = ["Открыт", "Закрыт"]
    print()
    if request.method == 'POST':
        price = int(request.form.get('adv_price'))
        estate_id = int(request.form.get('estate_id'))
        user.create_advert(price=price, estate_id=estate_id)
        while (length == len(advs)):
            time.sleep(0.05)
            advs = user.get_all_advertisments()
    elif request.method == 'PUT':
        data = request.get_json()
        advert_id = int(data['advert_id'])
        method = data['method']
        advert = next((adv for adv in advs if adv[-1] == advert_id))
        if advert[-2] == 0 and method == 'change':
            user.change_advert_status(advert_id=advert_id)
            return jsonify("Успешное изменение"), 200
        elif method == 'buy':
            if user.balance() >= advert[2]:
                try:
                    user.deposit(advert[2] + 100)
                    time.sleep(0.1)
                    user.buy_estate(advert_id=advert_id)
                    return jsonify("Успешная покупка"), 200
                except Exception as e:
                    print(e)
                    return jsonify("Вы уже владеете этой недвижимостью"), 400
            else:
                return jsonify("Недостаточно средств"), 400
    return render_template('advertisements.html', user=user, advs=tuple(advs), estates=estates, statuses=statuses)

@app.route('/estates', methods=['GET', 'POST', 'PUT'])
@login_required
def estates():
    user: User = current_user
    types = ["Дом", "Квартира", "Лофт"]
    statuses = ["Нет", "Да"]
    all_estates = user.get_all_estates()
    length = len(all_estates)
    if request.method == 'POST':
        size = int(request.form.get('estate_size'))
        address = request.form.get('estate_address')
        type_id = int(request.form.get('estate_type_id'))
        user.create_estate(size=size, address=address, estate_type_id=type_id)
        while (len(all_estates) == length):
            time.sleep(0.05)
            all_estates = user.get_all_estates()
    elif request.method == 'PUT':
        data = request.get_json()
        estate_id = int(data['estate_id'])
        estate = next((est for est in all_estates if est[-1] == estate_id))
        if estate[4] == True:
            user.change_estate_status(estate_id=estate_id)
            return jsonify("Успешное изменение"), 200
    return render_template('estates.html', user=user, estates=all_estates, types=types, statuses=statuses)

# logout

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# setters

@app.route('/login', methods=['POST'])
def authorize():
    public_key: str = request.form.get("public_key")
    password: str = request.form.get("password")
    user: Optional[User] = user_service.get_user_by_info(password=password, public_key=public_key)
    if user:
        if current_user.is_authenticated:
            return jsonify("Вы уже зарегистрированы!"), 400
        login_user(user)
        return redirect('advertisements')
    else:
        return jsonify("Ключ или пароль не верны\n"), 400


@app.route('/signup', methods=['POST'])
def register():
    password: str = request.form.get("password")
    user: Optional[User] = user_service.create_user(password=password)
    if user:
        if current_user.is_authenticated:
            return jsonify("Вы уже авторизованы!"), 400
        login_user(user)
        return jsonify(user.public_key), 201
    else:
        return jsonify("Пароль не соответсвует требованиям\nБольше 12 символов Содержит прописные буквы Содержит строчные буквы Cодержит спец символов или пробелов"), 400

@app.route('/asd')
def asd():
    abort(500)

# errors
@app.errorhandler(404)
def not_found(error):
    user = current_user if isinstance(current_user, User) else None
    return render_template("404.html", user=user)


@app.errorhandler(500)
def error_server(error):
    user = current_user if isinstance(current_user, User) else None
    return render_template("500.html", user=user)






