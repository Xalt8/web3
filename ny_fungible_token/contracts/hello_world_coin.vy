# @version ^0.2.0

# We need to keep track of _balances of address
# Retrieve the balance of any address
# Transfer from one address to another
# Give our token a name
# Need to be able to deal with decimals
# Need to be able to allow other smart contracts to interact with our token
# Produce relevant events
# Allow a dynamic supply of tokens


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


_totalSupply: uint256
_balances: HashMap[address, uint256]
_allowances: HashMap[address, HashMap[address, uint256]]
_minted: bool
_minter: address


@external
def __init__():
    self._minter = msg.sender
    self._minted = False


@external
@view
def name() -> String[10]:
    return NAME


@external
@view
def totalSupply() -> uint256:
    return self._totalSupply


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


@external
def mint(_to:address, _tSupply:uint256) -> bool:
    assert msg.sender == self._minter, "Only owner can mint and only once"
    assert self._minted == False, "This token has already been minted"
    self._totalSupply = _tSupply * 10 ** DECIMALS
    self._balances[_to] = self._totalSupply
    self._minted = True
    log Transfer(ZERO_ADDRESS, _to, self._totalSupply)
    return True


@internal
def _approve(_owner: address, _spender:address, _amount: uint256):
    assert _owner != ZERO_ADDRESS
    assert _spender != ZERO_ADDRESS
    self._allowances[_owner][_spender] = _amount
    log Approve(_owner, _spender, _amount)


@external
def increaseAllowance(_spender:address, _amount_increased:uint256) -> bool:
    self._approve(msg.sender, _spender, self._allowances[msg.sender][_spender] + _amount_increased)
    return True


@external
def decreaseAllowance( _spender:address, _amount_decreased: uint256) -> bool:
    assert self._allowances[msg.sender][_spender] >= _amount_decreased, "Negative allowances not allowed"
    self._approve(msg.sender, _spender, self._allowances[msg.sender][_spender] - _amount_decreased)
    return True


@internal
def _transfer(_from: address, _to: address, _amount:uint256):
    assert self._balances[_from] >= _amount, "The balance in not enough"
    assert _from != ZERO_ADDRESS
    assert _to != ZERO_ADDRESS
    self._balances[_from] -= _amount
    self._balances[_to] += _amount
    log Transfer(_from, _to, _amount)



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


