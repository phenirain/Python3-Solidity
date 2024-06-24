from flask import Flask
from flask_login import LoginManager
from web3 import Web3
from web3.middleware import geth_poa_middleware
from .database import init_db

from contract_info import address_contract, abi


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

app = Flask(__name__)
app.secret_key = "phenirain"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

