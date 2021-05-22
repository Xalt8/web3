from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.isConnected()

# Set the default account to the first account from Ganache
web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
# Copied from Remix deployed contract
address = Web3.toChecksumAddress("0xcf8c0C663C051787c62E6f7236746c4f92a63c46")

contract = web3.eth.contract(address=address, abi=abi)

print(contract.functions.greet().call())
# Hello

# Not hex when printed
tx_hash = contract.functions.setGreeting("Ciao").transact()

# Convert tx_hash to hex
hex_tx_hash = web3.toHex(tx_hash)
print(hex_tx_hash)
# From Ganache: 
# "0x04e02feddb75c88cba04eb9be654b19ece026913280d404bb3af133b5f95e72f"

''' When you send a transaction - you receive an transaction hash almost immediately 
    Then you have to wait for the transaction to be mined and confirmed. 
    You need a receipt before you can say that the transaction was successful 
'''
# This stops executing any code till we receive the transaction receipt
web3.eth.waitForTransactionReceipt(tx_hash)
web3.eth.waitForTransactionReceipt(hex_tx_hash)


print(f'Updated greeting: {contract.functions.greet().call()}')
# Updated greeting: Ciao