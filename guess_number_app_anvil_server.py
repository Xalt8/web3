import anvil.server
from hexbytes import HexBytes
from guess_number_app_backend import web3_connection, contract_address, contract
from web3 import Web3

# Connect to Anvil server using uplink key
anvil.server.connect('server_QU6WQ53GJBCZ7MY7GOGX7YRZ-TU5EUJ7KKAH53HP3')

@anvil.server.callable
def get_contract_address():
    global contract_address
    return contract_address

@anvil.server.callable
def get_game_balance() -> int:
    global contract
    return contract.functions.game_balance().call()

@anvil.server.callable
def get_nonce(ETH_address):
    ''' Get the nonce of an Eth address -> used in transfer_eth()'''
    return web3_connection.eth.get_transaction_count(ETH_address)

@anvil.server.callable
def transfer_eth(sender, signature):
    ''' Use this function to transfer 1 Eth from player's account to default account (game creator)'''
    global web3_connection
    trasaction_body = {
        'nonce':get_nonce(sender),
        'to':web3_connection.eth.defaultAccount,
        'value':web3_connection.toWei(1, 'ether'),
        'gas':4500000,
        'gasPrice': web3_connection.toWei(8, 'gwei')
        }
    signed_transaction = web3_connection.eth.account.sign_transaction(trasaction_body, signature)
    result = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
    string_result = result.hex()
    return string_result


# Set the node provider to Ganache
NODE_PROVIDER = 'http://127.0.0.1:7545'
web3_connection = Web3(Web3.HTTPProvider(NODE_PROVIDER))

set_default_account(0)
abi, byte_code = get_abi_byteCode('Vyper_01/build/contracts/GuessNumberApp.json')
contract_app = instantiate_contract(abi=abi, byte_code=byte_code)
tx_hash = deploy_contract_get_tx_hash(secret_number=8, value=10)
tx_receipt = get_tx_receipt(tx_hash)
contract_address = get_contract_address(tx_receipt)
contract = get_contract_instance(contract_address=contract_address, abi=abi)
player_registration_event = contract.events.Player_registered()



if __name__ == '__main__':
    print("\nConnected to Ganache" if web3_connection.isConnected() else "Not connected to Ganache")
    print(f'\nContract address:{contract_address}')

    anvil.server.wait_forever()

    
    
