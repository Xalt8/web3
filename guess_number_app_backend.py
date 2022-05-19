from web3 import Web3
import json
from os.path import exists

# Source: 
# https://www.dappuniversity.com/articles/web3-py-intro
# https://www.youtube.com/watch?v=8-GeDWpUeVI&list=PLFPZ8ai7J-iQMTChqif-XVP8DYABA4rx1&index=12&ab_channel=MoralisWeb3

# Set the node provider to Ganache
NODE_PROVIDER = 'http://127.0.0.1:7545'
web3_connection = Web3(Web3.HTTPProvider(NODE_PROVIDER))

web3_connection.eth.defaultAccount = web3_connection.eth.accounts[0]


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


def deploy_contract_get_tx_hash(contract_inst, secret_number:int, value:int):
    assert value == 10, "You need 10 Eth to deploy this contract"
    assert 1 <= secret_number <= 10, "Secret number has to be between 1 & 10"
    transaction= {'from': web3_connection.eth.defaultAccount, 'value': web3_connection.toWei(value, 'ether')}
    return contract_inst.constructor(secret_number).transact(transaction)


def get_tx_receipt(tx_hash):
    return web3_connection.eth.waitForTransactionReceipt(tx_hash)


def write_contract_address_to_file(contract_address:str):
    """ Deletes any existing address in the file and writes a 
        new address to file. """
    try:
        f = open("contract_address.txt", "r+") 
        f.seek(0)
        f.truncate()
    except FileNotFoundError:
        print('contract_address.txt does not exists!')
    # Write the address to file
    with open('contract_address.txt', 'w') as f1:
        f1.write(contract_address)


def get_contract_address(tx_receipt):
    contract_address = tx_receipt.contractAddress
    write_contract_address_to_file(contract_address)
    return contract_address 


def get_contract_instance(contract_address, abi):
    return web3_connection.eth.contract(address=contract_address, abi=abi)


def get_address_from_private_key(private_key):
    ''' Gets the account address/public key from private key'''
    global web3_connection
    return web3_connection.eth.account.from_key(private_key).address


def main():
    ''' Setup a game instance'''
    
    abi, byte_code = get_abi_byteCode('Vyper_01/build/contracts/GuessNumberApp.json')
    contract_app = instantiate_contract(abi=abi, byte_code=byte_code)
    tx_hash = deploy_contract_get_tx_hash(contract_inst=contract_app, secret_number=8, value=10)
    tx_receipt = get_tx_receipt(tx_hash)
    contract_address = get_contract_address(tx_receipt)
    contract = get_contract_instance(contract_address=contract_address, abi=abi)
    
    print(f"\ncontract address: {contract_address}\n")    
    

if __name__ == '__main__':
    
    print("\nConnected to Ganache" if web3_connection.isConnected() else "Not connected to Ganache\n")
    
    main()

