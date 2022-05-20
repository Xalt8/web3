import anvil.server
from hexbytes import HexBytes
from guess_number_app_backend import web3_connection, get_abi_byteCode
from web3 import Web3

anvil.server.connect('server_QU6WQ53GJBCZ7MY7GOGX7YRZ-TU5EUJ7KKAH53HP3')

abi, _ = get_abi_byteCode('Vyper_01/build/contracts/GuessNumberApp.json')

with open('contract_address.txt', 'r') as f:
    CONTRACT_ADDRESS = f.readline()

contract = web3_connection.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    

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
def is_game_active() -> bool:
    global contract
    return contract.functions.active().call()


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
    
    process_logs = contract.events.Player_registered().processReceipt(tx_receipt)
    print('In player_registration() process_logs:')
    print(process_logs)
    return tx_receipt.status


def deconstruct_log(game_solved_logs):
    ''' Takes a log object and returns the event, player address
        time, game balance, and creator balance '''
    event_name = game_solved_logs[0]['event']
    player_add, _time, game_bal, creat_bal = [v for _, v in game_solved_logs[0]['args'].items()]
    return event_name, player_add, _time, game_bal, creat_bal


@anvil.server.callable
def play(guessed_number, player_address):
    global contract
    tx_hash = contract.functions.play(guessed_number).transact({'from':player_address})
    tx_receipt = web3_connection.eth.wait_for_transaction_receipt(tx_hash)
    
    game_solved_process_logs = contract.events.Game_solved().processReceipt(tx_receipt)
    guess_count_exceed_process_logs = contract.events.Guess_count_exceeded().processReceipt(tx_receipt) 

    if len(game_solved_process_logs) !=0:
        return deconstruct_log(game_solved_process_logs)
    elif len(guess_count_exceed_process_logs) !=0:
        return deconstruct_log(guess_count_exceed_process_logs)
    


if __name__ == '__main__':
    print("\nConnected to Ganache" if web3_connection.isConnected() else "Not connected to Ganache\n")
    print(f'Contract address: {CONTRACT_ADDRESS}' if CONTRACT_ADDRESS else 'No contract')


    anvil.server.wait_forever()

    
    
