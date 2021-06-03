import pytest

TEST_MAP = [
    dict(a=1, b=2, exp=3),
    dict(a=2, b=3, exp=5),
    dict(a=1, b=2, exp=3),
]


@pytest.mark.parametrize(
    tuple(TEST_MAP[0]), ((test.values()) for test in TEST_MAP)
)
def test_parametrization(a, b, exp):
    assert a + b == exp


@pytest.mark.parametrize(
    tuple(TEST_MAP[0]), ((test.values()) for test in TEST_MAP)
)
def test_parametrization(a, b, exp):
    assert a + b == exp
