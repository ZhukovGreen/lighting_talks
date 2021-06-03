import os


def test_one():
    os.environ["TEST_ONE"] = "15"
    pass


def test_two():
    assert os.environ["TEST_ONE"] == "15"
    pass


def test_three():
    pass
