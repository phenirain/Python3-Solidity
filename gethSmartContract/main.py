from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)
print(w3.eth.get_balance("0xC24f6f51bA4bA81377Dd199Aebe13d164d2c53A5"))
print(w3.eth.get_balance("0x26663a21D2B29eB563A6fdEF17a41E3fC1BEfE1A"))
print(w3.eth.get_balance("0x3643F1Ab8211defa4D3eEe483Fef48AB007f76a6"))
print(w3.eth.get_balance("0x9b2AF2e7190AbAE09210181cAff8F320Cd121dE4"))
print(w3.eth.get_balance("0x5239473F51f746f5F3EE70763C134F02c05bD5c9"))

