from _pytest.recwarn import T
import pytest
from app.calculations import add, BankAccount


@pytest.fixture
def zero_bank_account():
    print('creating empty bank account')
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize('num1, num2, expected', [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16),
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    print('testing my bank account')
    assert zero_bank_account.balance == 0

@pytest.mark.parametrize("init, withdraw, expect",[
    (50, 5, 45),
    (80, 40, 40),
    (99, 77, 22)
])
def test_wihdraw(init, withdraw, expect):
    bank_account = BankAccount(starting_balance=init)
    bank_account.withdraw(withdraw)
    assert bank_account.balance == expect

def test_deposit(bank_account):
    bank_account.deposit(60)
    assert bank_account.balance == 110

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited, withdraw, expected",[
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected