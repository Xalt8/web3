import pytest
from brownie import Wei, accounts, GuessNumber201

@pytest.fixture
def guess_number():
    guess_number = GuessNumber201.deploy({'from': accounts[0]})
    guess_number.create_game(9, {'from': accounts[1], 'value': '10 ether'})
    return guess_number


def test_wrong_guess(guess_number) -> None:
    pre_game_balance = guess_number.get_game_balance(0)
    pre_player_balance = accounts[2].balance()
    pre_guess_count = guess_number.get_game_guesses(0)
    guess_number.play_game(0, 8, {'from': accounts[2], 'value': '1 ether'})
    assert guess_number.get_game_balance(0) == pre_game_balance + Wei('1 ether'), "Game bal error"
    assert accounts[2].balance() == pre_player_balance - Wei('1 ether'), "Player bal error"
    assert guess_number.get_game_guesses(0) == pre_guess_count + 1, "Guess count error"
    assert guess_number.is_game_active(0) == True, "Game inactive error" 


def test_right_guess(guess_number):
    pre_game_balance = guess_number.get_game_balance(0)
    pre_player_balance = accounts[2].balance()
    pre_contract_owner_balance = accounts[0].balance()
    guess_number.play_game(0, 9, {'from': accounts[2], 'value': '1 ether'})
    assert guess_number.get_game_balance(0) == 0, "Game balance not reset"
    assert accounts[0].balance() == pre_contract_owner_balance + (pre_game_balance + Wei('1 ether'))/100, "Commission error"
    assert accounts[2].balance() == (pre_player_balance - Wei('1 ether')) + (pre_game_balance + Wei('1 ether'))*99/100, "Player bal error"
    assert guess_number.is_game_active(0) == False, "Game status error"



# def test_10_wrong_guesses(guess_number):
    
#     pre_guess_count = guess_number.get_game_guesses(0)
#     pre_game_balance = guess_number.get_game_balance(0)
#     pre_contract_owner_balance = accounts[0].balance()
    
#     # pre_creator_balance = accounts[1].balance()
    
#     for i in range(11):
#         if i != 9:
#             guess_number.play_game(0, i, {'from': accounts[2], 'value': '1 ether'})

#     assert guess_number.get_game_guesses(0) == pre_guess_count + 10      
#     assert accounts[0].balance() == (pre_contract_owner_balance - (pre_game_balance + Wei('10 ether')))/100, "Commission error"

#     # send(self.game_index[_game_id].game_owner, (self.game_index[_game_id].game_balance * 99) / 100)
#     # assert accounts[1].balance() == (pre_owner_balance + pre_game_balance + Wei('10 ether')) * 0.99, "Game owner bal error" 
#     # assert accounts[0].balance() == pre_contract_owner_balance + (pre_game_balance + Wei('10 ether')) * 0.01, "Commission error"
#     # assert guess_number.get_game_balance(0) == 0, "Game balance not reset"
#     # assert guess_number.is_game_active(0) == False, "Game status error"
#     # assert guess_number.game_index[0].guess_count == 10
