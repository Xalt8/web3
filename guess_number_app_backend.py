from web3 import Web3
import json


# Source: 
# https://www.dappuniversity.com/articles/web3-py-intro
# https://www.youtube.com/watch?v=8-GeDWpUeVI&list=PLFPZ8ai7J-iQMTChqif-XVP8DYABA4rx1&index=12&ab_channel=MoralisWeb3

# Set the node provider to Ganache
NODE_PROVIDER = 'http://127.0.0.1:7545'
web3_connection = Web3(Web3.HTTPProvider(NODE_PROVIDER))


def set_default_account(account_num:int = 0):
    ''' Sets the default account to 0 by default'''
    web3_connection.eth.defaultAccount = web3_connection.eth.accounts[account_num]


def get_abi_byteCode(build_path: str) -> tuple:
    ''' Takes the path to json build file and 
        returns the ABI & byte code of a contract'''
    try:
        with open(build_path) as j:
            buildJson = json.load(j)
    except FileNotFoundError as e:
        print('Could not find file - check path!')
    
    return buildJson['abi'], buildJson['bytecode']


def instantiate_contract(abi, byte_code):
    return web3_connection.eth.contract(abi=abi, bytecode=byte_code)


def deploy_contract_get_tx_hash(secret_number:int, value:int):
    assert value == 10, "You need 10 Eth to deploy this contract"
    assert 1 <= secret_number <= 10, "Secret number has to be between 1 & 10"
    transaction= {'from': web3_connection.eth.defaultAccount, 'value': web3_connection.toWei(value, 'ether')}
    return contract_app.constructor(secret_number).transact(transaction)


def get_tx_receipt(tx_hash):
    return web3_connection.eth.waitForTransactionReceipt(tx_hash)


def get_contract_address(tx_receipt):
    return tx_receipt.contractAddress


def get_contract_instance(contract_address, abi):
    return web3_connection.eth.contract(address=contract_address, abi=abi)


# Set the first account in Ganache to be the default account
set_default_account(0)

# Get the ABI & Byte Code of the contract
abi, byte_code = get_abi_byteCode('Vyper_01/build/contracts/GuessNumberApp.json')

# Instantiate the contract 
contract_app = instantiate_contract(abi=abi, byte_code=byte_code)
# contract_app = web3_connection.eth.contract(abi=abi, bytecode=byte_code)

# Submit the transaction that deploys the contract from default account with 10 Ether
# Call the constructor of the contract with the secret number
tx_hash = deploy_contract_get_tx_hash(secret_number=8, value=10)

# transaction= {'from':web3_connection.eth.defaultAccount, 'value':web3_connection.toWei(10, 'ether')}
# tx_hash = contract_app.constructor(8).transact(transaction)

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = get_tx_receipt(tx_hash)
# tx_receipt = web3_connection.eth.waitForTransactionReceipt(tx_hash) 

# Get the contract's address
contract_address = get_contract_address(tx_receipt)

# Create the contract instance with the address & ABI
# contract = web3_connection.eth.contract(address=tx_receipt.contractAddress, abi=abi)
contract = get_contract_instance(contract_address=contract_address, abi=abi)

# Get the events of interest
player_registration_event = contract.events.Player_registered()


if __name__ == '__main__':
    pass
