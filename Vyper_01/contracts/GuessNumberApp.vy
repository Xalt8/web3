# @version ^0.2.0

# Contract Guess Number
# Contract should take a secret number upon deployment. 
# The secret number should be between 0-10
# It should cost 10 Eth to deploy the contract
# Each guess that a player makes will cost 1 Eth
# Whoever makes the right guess will have the balance of the contract transfer to his address
# Once the right guess is made the contract should not allow people to play


event Player_registered:
    player_address: indexed(address)
    time: uint256


event Game_solved:
    player_address: indexed(address)
    time: uint256
    game_balance: uint256
    creator_balance: uint256


event Guess_count_exceeded:
    player_address: indexed(address)
    time: uint256
    game_balance: uint256
    creator_balance: uint256



secret_number: uint256
game_creator: public(address)
game_player: public(address)
game_balance: public(uint256)
creator_balance: public(uint256)
active: public(bool)
guess_count: public(uint256)


@external
@payable
def __init__(_secret_number: uint256):
    assert (_secret_number >= 0) and (_secret_number <= 10), "Number should be between 0-10"
    assert msg.value == 10*(10**18), "Contract creating needs 10 Ether"
    assert self.creator_balance == 0, "Creator balance should be 0"
    self.secret_number = _secret_number
    self.game_balance = self.game_balance + msg.value
    self.active = True
    self.game_creator = msg.sender


@external
@payable
def player_registration():
    assert self.active == True, "Contract is inactive!"
    assert msg.value == 1*(10**18), "You need to pay 1 Eth to play!"
    self.game_player = msg.sender  
    self.creator_balance = self.creator_balance + msg.value # Add the player's fee to creator_balance
    log Player_registered(msg.sender, block.timestamp)        
    

@external
def play(_guessed_number:uint256) -> bool:
    assert self.active == True, "Contract is inactive!"
    assert msg.sender == self.game_player, "You are not authorised to play"

    self.guess_count = self.guess_count + 1
    self.game_balance = self.game_balance - 1*(10**18)
    self.creator_balance = self.creator_balance + 1*(10**18)
    
    # Correct guess -> 
    if _guessed_number == self.secret_number:
        send(self.game_player, self.game_balance)
        send(self.game_creator, self.creator_balance)
        log Game_solved(msg.sender, block.timestamp, self.game_balance, self.creator_balance)
        self.active = False
        self.game_balance = 0
        self.creator_balance = 0
    elif self.guess_count == 5:
        send(self.game_creator, self.game_balance)
        send(self.game_creator, self.creator_balance)
        log Guess_count_exceeded(msg.sender, block.timestamp, self.game_balance, self.creator_balance)
        self.active = False
        self.game_balance = 0
        self.creator_balance = 0
        

    return True


