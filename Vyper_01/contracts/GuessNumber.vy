# @version ^0.2.0

# Contract Guess Number
# Contract should take a secret number upon deployment. 
# The secret number should be between 0-100
# It should cost 10 Eth to deploy the contract
# Each guess that a player makes will cost 1 Eth
# Whoever makes the right guess will have the balance of the contract transfer to his address
# Once the right guess is made the contract should not allow people to play

secret_number: uint256
current_balance: public(uint256)
active: public(bool)

@external
@payable
def __init__(_secret_number: uint256):
    assert (_secret_number >= 0) and (_secret_number <= 100), "Number should be between 0-100"
    assert msg.value == 10*(10**18), "Contract creating needs 10 Ether"
    self.secret_number = _secret_number
    self.current_balance = self.current_balance + msg.value
    self.active = True

@external
@payable
def play(_guessed_number:uint256):
    assert self.active == True, "Contract is inactive!"
    assert msg.value == 10**18, "You need to pay 1 Eth to play!"
    
    if _guessed_number == self.secret_number:
        send(msg.sender, self.balance)
        self.current_balance = 0
        self.active = False


