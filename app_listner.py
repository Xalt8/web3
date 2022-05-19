from web3 import Web3
import time
import json
from hexbytes import HexBytes
from guess_number_app_backend import web3_connection


def get_contract(contract_address, build_path):
    try:
        with open(build_path) as j:
            buildJson = json.load(j)
    except FileNotFoundError:
        print('Could not find file - check path!')
    abi = buildJson['abi']
    contract = web3_connection.eth.contract(address=contract_address, abi=abi)
    return contract


def handle_event(event, event_of_interest):
    receipt = web3_connection.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = event_of_interest.processReceipt(receipt)
    # result is a tuple -> get the first value
    if result[0].event == 'Player_registered': 
        print('Player_registered successfully')
    elif result[0].event == 'Game_solved':
        print('Game solved!!')
    elif result[0].event == 'Guess_count_exceeded':
        print('Guess count exceeded - Game Over!')


def handle_player_registered_event(event, contract):
    event_of_interest = contract.events.Player_registered()
    receipt = web3_connection.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = event_of_interest.processReceipt(receipt)
    print(result)


def handle_game_solved_event(event, contract):
    event_of_interest = contract.events.Game_solved()
    receipt = web3_connection.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = event_of_interest.processReceipt(receipt)
    print(result)


# def log_loop(event_filter, poll_interval, event_of_interest):
#     while True:
#         for event in event_filter.get_new_entries():
#             handle_event(event, event_of_interest)
#             time.sleep(poll_interval)


def log_loop2(event_filter, poll_interval, contract):
    while True:
        for Player_registered in event_filter.get_new_entries():
            handle_player_registered_event(Player_registered, contract)
        for Game_solved in event_filter.get_new_entries():
            handle_game_solved_event(Game_solved, contract)

            time.sleep(poll_interval)



def listen(contract_address, build_path):
    block_filter = web3_connection.eth.filter({'fromBlock':'latest', 'address': contract_address})
    contract = get_contract(contract_address, build_path)
    # log_loop(event_filter=block_filter, poll_interval=2, event_of_interest=get_player_registered_event(contract))
    log_loop2(event_filter=block_filter, poll_interval=2, contract=contract)
    

with open('contract_address.txt', 'r') as f:
    CONTRACT_ADDRESS = f.readline()


if __name__ == '__main__':

    print('Listening...')
    listen(contract_address=CONTRACT_ADDRESS, build_path="Vyper_01/build/contracts/GuessNumberApp.json")
    