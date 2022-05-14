from web3 import Web3
import json

# Set the node provider to Ganache
NODE_PROVIDER = 'http://127.0.0.1:7545'
web3_connection = Web3(Web3.HTTPProvider(NODE_PROVIDER))

# Get the ABI path from ny_fungible_token folder
ABI_PATH = '../ny_fungible_token/build/contracts/hello_world_coin.json'
with open(ABI_PATH) as j:
    abiJson = json.load(j)

# Get the contracts address -> deploy contract from another cmd prompt and copy addess here
ADDRESS = '0xEA8C1056885FbCF4d07b063ab0f884cBB93872c4'


def build_contract(address, abi_json):
    contract = web3_connection.eth.contract(address=address, abi=abi_json['abi'])
    return contract


def get_address(private_key):
    ''' Gets the public key/address from a signature/private key'''
    return web3_connection.eth.account.from_key(private_key).address


def transfer(_contract, _to, _amount, _signature):
    ''' nonce:  need the public key of whoever is signing 
                this transaction to calculate the nonce -> get_address()
        function_call:  use the transfer() from the _contract and 
                        buildTransaction using the nonce
        signed_transaction: signing the trasaction using the function_call & _signature
        result: expecting a transaction hash from sending raw transaction
    '''
    nonce = web3_connection.eth.get_transaction_count(get_address(_signature))
    function_call = _contract.functions.transfer(_to, _amount).buildTransaction({'nonce':nonce})
    signed_transaction = web3_connection.eth.account.sign_transaction(function_call, _signature)
    result = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return result


def allowanceUp(_contract, _to, _amount, _signature):
    ''' Increase the allowance '''
    nonce = web3_connection.eth.get_transaction_count(get_address(_signature))
    function_call = _contract.functions.increaseAllowance(_to, _amount).buildTransaction({'nonce':nonce})
    signed_transaction = web3_connection.eth.account.sign_transaction(function_call, _signature)
    result = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return result


if __name__ == '__main__':
    
    print(f'Are we connected: {"Yes" if web3_connection.isConnected() else "No"}\n')
    
    token = build_contract(address=ADDRESS, abi_json=abiJson)

    print('Balance of account[0]')
    print(token.functions.balanceOf('0xE2d7B95B82927aBb9a5444F8d42500365d1B452a').call()/10**18)

    print('\ntransfer()')
    transfer(token, '0x3284Fd4Df704B4CBf7D2C6cc5D3b6Ef17F930961', 1000*10**18, '87fd1d1d167821135ce1730d6aae12bf5a2742f015d2bbb496ed686142313b49')

    print('Balance of account[0]')
    print(token.functions.balanceOf('0xE2d7B95B82927aBb9a5444F8d42500365d1B452a').call()/10**18)

    print('Balance of account[1]')
    print(token.functions.balanceOf('0x3284Fd4Df704B4CBf7D2C6cc5D3b6Ef17F930961').call()/10**18)


    
