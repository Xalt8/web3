import anvil.server
from hexbytes import HexBytes
from guess_number_app_backend import web3_connection, get_abi_byteCode
from web3 import Web3

anvil.server.connect('server_QU6WQ53GJBCZ7MY7GOGX7YRZ-TU5EUJ7KKAH53HP3')

abi, _ = get_abi_byteCode('Vyper_01/build/contracts/GuessNumberApp.json')
contract = web3_connection.eth.contract(address='0x2Ca1Ccdb67FFfe598d012818bB6f68fE6AE708C0', abi=abi)


@anvil.server.callable
def get_game_balance() -> int:
    global contract
    return contract.functions.game_balance().call()


@anvil.server.callable
def get_guess_count() -> int:
    global contract 
    return contract.functions.guess_count().call()


@anvil.server.callable
def get_players_address():
    global contract
    return contract.functions.game_player().call()


@anvil.server.callable
def get_nonce(ETH_address):
    global web3_connection
    ''' Get the nonce of an Eth address -> used in transfer_eth()'''
    return web3_connection.eth.get_transaction_count(ETH_address)


# Not used in the app
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


@anvil.server.callable
def player_registration(player_address, signature):
    global web3_connection, contract
    transaction_body = {
        'nonce': get_nonce(player_address),
        'value': web3_connection.toWei(1, 'ether'),
        'gas': 4500000,
        'gasPrice': web3_connection.toWei(8, 'gwei')
        }
    
    function_call = contract.functions.player_registration().buildTransaction(transaction_body)
    signed_transaction = web3_connection.eth.account.sign_transaction(function_call, signature)
    tx_hash = web3_connection.eth.send_raw_transaction(signed_transaction.rawTransaction)
    tx_receipt = web3_connection.eth.wait_for_transaction_receipt(tx_hash) 
    return tx_receipt.status


@anvil.server.callable
def play(guessed_number, player_address):
    global contract
    return contract.functions.play(guessed_number).call({'from':player_address})
    


if __name__ == '__main__':
    print("\nConnected to Ganache" if web3_connection.isConnected() else "Not connected to Ganache")

    
    anvil.server.wait_forever()

    
    
