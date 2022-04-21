from web3 import Web3
import time
import json

ganache_node_provider = 'http://127.0.0.1:7545'

web3_connection = Web3(Web3.HTTPProvider(ganache_node_provider))
print(f'Are we connected: {"Yes" if web3_connection.isConnected() else "No"}\n')


def set_event(contract_address, abi_path):
    with open(abi_path) as f:
        abiJson = json.load(f)
    contract = web3_connection.eth.contract(address=contract_address, abi=abiJson['abi'])
    event_of_interest = contract.events.Game_created()
    return event_of_interest


def handle_event(event, event_of_interest):
    receipt = web3_connection.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = event_of_interest.processReceipt(receipt)
    print(result)


def log_loop(event_filter, poll_interval, event_of_interest):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event, event_of_interest)
            time.sleep(poll_interval)


def listen(contract_address, abi_path):
    block_filter = web3_connection.eth.filter({'fromBlock':'latest', 'address': contract_address})
    log_loop(event_filter=block_filter, poll_interval=2, event_of_interest=set_event(contract_address, abi_path))