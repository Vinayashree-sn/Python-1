import pytest
from banking import Account

# ---------- Fixtures ----------
@pytest.fixture
def account_a():
    return Account("Alice", 1000)

@pytest.fixture
def account_b():
    return Account("Bob", 500)

# ---------- Basic Tests ----------
def test_initial_balance(account_a):
    assert account_a.balance == 1000

def test_deposit(account_a):
    account_a.deposit(200)
    assert account_a.balance == 1200

def test_withdraw(account_a):
    account_a.withdraw(300)
    assert account_a.balance == 700

# ---------- Exception Tests ----------
def test_deposit_negative(account_a):
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account_a.deposit(-100)

def test_withdraw_insufficient(account_a):
    with pytest.raises(ValueError, match="Insufficient funds"):
        account_a.withdraw(2000)

# ---------- Parametrized Tests ----------
@pytest.mark.parametrize("initial, deposit, expected", [
    (0, 100, 100),
    (50, 50, 100),
    (100, 0, 100),
])
def test_deposit_various(initial, deposit, expected):
    acc = Account("Test", initial)
    if deposit > 0:
        acc.deposit(deposit)
        assert acc.balance == expected
    else:
        with pytest.raises(ValueError):
            acc.deposit(deposit)

# ---------- Transfer Tests ----------
def test_transfer(account_a, account_b):
    account_a.transfer(account_b, 200)
    assert account_a.balance == 800
    assert account_b.balance == 700

def test_transfer_insufficient(account_a, account_b):
    with pytest.raises(ValueError):
        account_a.transfer(account_b, 2000)

# ---------- Grouped Tests ----------
class TestAccountOperations:
    def test_multiple_deposits(self):
        acc = Account("GroupTest", 100)
        acc.deposit(50)
        acc.deposit(150)
        assert acc.balance == 300

    def test_multiple_withdrawals(self):
        acc = Account("GroupTest", 500)
        acc.withdraw(100)
        acc.withdraw(200)
        assert acc.balance == 200

    def test_transfer_chain(self):
        acc1 = Account("A", 1000)
        acc2 = Account("B", 500)
        acc3 = Account("C", 300)

        acc1.transfer(acc2, 200)
        acc2.transfer(acc3, 100)

        assert acc1.balance == 800
        assert acc2.balance == 600
        assert acc3.balance == 400

