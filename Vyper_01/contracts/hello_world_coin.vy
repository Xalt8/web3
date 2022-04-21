# @version ^0.2.0

# We need to keep track of _balances of address
# Retrieve the balance of any address
# Transfer from one address to another
# Give our token a name
# Need to be able to deal with decimals
# Need to be able to allow other smart contracts to interact with our token
# Produce relevant events

TOTAL_SUPPLY: constant(uint256) = 10**27 # -> Amount of tokens (10**9) + decimals (18)
NAME: constant(String[10]) = "HelloWorld"
DECIMALS: constant(uint256) = 18


event Transfer:
    _from: address
    _to: address
    _value: uint256


event Approve:
    _owner: address
    _spender: address
    _value: uint256


_balances: HashMap[address, uint256]
_allowances: HashMap[address, HashMap[address, uint256]]


@external
def __init__():
    self._balances[msg.sender] = TOTAL_SUPPLY


@external
@view
def name() -> String[10]:
    return NAME


@external
@view
def totalSupply() -> uint256:
    return TOTAL_SUPPLY


@external
@view
def allowance(_owner:address, _spender:address) -> uint256:
    return self._allowances[_owner][_spender] 


@external
@view
def decimals() -> uint256:
    return DECIMALS


@external
@view
def balanceOf(_address: address) -> uint256:
    return self._balances[_address]


@internal
def _transfer(_from: address, _to: address, _amount:uint256):
    assert self._balances[_from] >= _amount, "The balance in not enough"
    self._balances[_from] -= _amount
    self._balances[_to] += _amount
    log Transfer(_from, _to, _amount)


@internal
def _approve(_owner: address, _spender:address, _amount: uint256):
    self._allowances[_owner][_spender] = _amount
    log Approve(_owner, _spender, _amount)

@external
def transfer(_to: address, _amount:uint256) -> bool:
    self._transfer(msg.sender, _to, _amount)
    return True


@external
def approve(_spender:address, _amount:uint256) -> bool:
    self._approve(msg.sender, _spender, _amount)
    return True


@external
def transferFrom(_owner:address, _to:address, _amount:uint256) -> bool:
    assert self._allowances[_owner][msg.sender] >= _amount, "The allowance is not enough for this operation"
    assert self._balances[_owner] >= _amount, "The balance is not enough for this operation"
    self._balances[_owner] -= _amount
    self._balances[_to] += _amount
    self._allowances[_owner][msg.sender] -= _amount
    return True


