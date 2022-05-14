import pytest
from brownie import Wei, accounts, GuessNumberApp

@pytest.fixture
def guess_number():
    guess_number = GuessNumberApp.deploy(8, {'from': accounts[0], 'value': '10 ether'})
    return guess_number

@pytest.fixture
def guess_number_w_player():
    guess_number = GuessNumberApp.deploy(8, {'from': accounts[0], 'value': '10 ether'})
    guess_number.player_registration({'from':accounts[1], 'value':'1 ether'})
    return guess_number


def test_player_registration(guess_number):
    player_pre_registration_game_balance = accounts[1].balance()
    pre_registration_game_balance = guess_number.game_balance()
    pre_registration_creator_balance = guess_number.creator_balance()
    assert guess_number.active() == True, "game active() error"
    assert pre_registration_game_balance == Wei('10 ether'), "pre_registration_game_balance error"
    assert pre_registration_creator_balance == 0, "Creator balance != 0"
    guess_number.player_registration({'from':accounts[1], 'value':'1 ether'})
    assert guess_number.game_player() == accounts[1].address, "Game player address error"
    assert accounts[1].balance() == player_pre_registration_game_balance - Wei('1 ether'), "Post registration player balance error"
    assert guess_number.creator_balance() == pre_registration_creator_balance + Wei('1 ether'), "Creator balance was not credited"
    

def test_one_wrong_guess(guess_number_w_player):
    pre_play_guess_count = guess_number_w_player.guess_count()
    pre_play_game_balance = guess_number_w_player.game_balance()
    pre_play_creator_balance = guess_number_w_player.creator_balance()
    pre_play_player_balance = accounts[1].balance()
    assert guess_number_w_player.active() == True, "game active() error"

    guess_number_w_player.play(1, {'from':accounts[1]})
    
    assert accounts[1].balance() == pre_play_player_balance, "Player balance should not change" 
    assert guess_number_w_player.guess_count() == pre_play_guess_count + 1, "Guess count error"
    assert guess_number_w_player.game_balance() == pre_play_game_balance - Wei('1 ether'), "Game balance error"
    assert guess_number_w_player.creator_balance() == pre_play_creator_balance + Wei('1 ether'), "Creator balance error" 
    assert guess_number_w_player.active() == True, "game active() error"


def test_5_wrong_guesses(guess_number_w_player):
    pre_play_guess_count = guess_number_w_player.guess_count()
    pre_play_game_balance = guess_number_w_player.game_balance()
    pre_play_creator_balance = guess_number_w_player.creator_balance()
    pre_play_player_balance = accounts[1].balance()
    pre_play_creator_account = accounts[0].balance()
    assert guess_number_w_player.active() == True, "game active() error"

    for i in range(1, 6):
        if i < 5:
            guess_number_w_player.play(i, {'from':accounts[1]})
            assert accounts[1].balance() == pre_play_player_balance, "Player balance should not change" 
            assert guess_number_w_player.guess_count() == pre_play_guess_count + i, "Guess count error"
            assert guess_number_w_player.game_balance() == pre_play_game_balance - Wei(f'{i} ether'), "Game balance error"
            assert guess_number_w_player.creator_balance() == pre_play_creator_balance + Wei(f'{i} ether'), "Creator balance error" 
            assert guess_number_w_player.active() == True, "game active() error"
        elif i == 5:
            guess_number_w_player.play(i, {'from':accounts[1]})
            assert guess_number_w_player.active() == False, "Game should be inactive"
            assert accounts[1].balance() == pre_play_player_balance, "Player balance should not change" 
            assert guess_number_w_player.guess_count() == i, "Guess count error"
            assert guess_number_w_player.game_balance() == 0, "Game balance should be 0 -> all funds should be transfered"
            assert guess_number_w_player.creator_balance() == 0, "Creator balance error" 
            assert accounts[0].balance() == pre_play_creator_account + pre_play_creator_balance + Wei(f'{i} ether') + Wei(f'{i} ether'), "Creator account error "  
        else:
            print("Oops -> we shouldn't be here")


def test_right_guess(guess_number_w_player):
    pre_play_player_account = accounts[1].balance()
    pre_play_creator_account = accounts[0].balance()
    pre_play_game_balance = guess_number_w_player.game_balance()
    pre_play_creator_balance = guess_number_w_player.creator_balance()
    
    guess_number_w_player.play(8, {'from':accounts[1]})

    assert guess_number_w_player.active() == False, "Game should be inactive"
    assert accounts[1].balance() == pre_play_player_account + pre_play_game_balance - Wei('1 ether'), "Player should get winnings"
    assert accounts[0].balance() == pre_play_creator_account + pre_play_creator_balance + Wei('1 ether'), "Creator account error"  
    assert guess_number_w_player.game_balance() == 0, "Game balance should be 0 -> all funds should be transfered"
    assert guess_number_w_player.creator_balance() == 0, "Creator balance error"