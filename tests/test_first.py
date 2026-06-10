import pytest

def add(a, b):
    return a + b

@pytest.fixture
def numbers():
    return {"a": 10, "b": 5}

def test_더하기(numbers):
    """두 양수를 더하면 올바른 합이 나와야 한다"""
    assert add(numbers["a"], numbers["b"]) == 15

def test_빼기(numbers):
    """큰 수에서 작은 수를 빼면 올바른 값이 나와야 한다"""
    assert add(numbers["a"], -numbers["b"]) == 5

def test_zero(numbers):
    """같은 수를 더하고 빼면 0이 나와야 한다"""
    assert add(numbers["a"], -numbers["a"]) == 0

@pytest.mark.parametrize("a, b, 기대값", [
    (1, 2, 3),
    (10, 20, 30),
    (-1, -1, -2),
    (0, 0, 0),
])
def test_다양한_더하기(a, b, 기대값):
    """다양한 숫자 조합으로 더하기가 동작해야 한다"""
    assert add(a, b) == 기대값