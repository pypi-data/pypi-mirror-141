from bs import *

def test_bs():
    assert len(phrase(5))>5
    assert slogan() is not None
    assert sentence() is not None
    assert paragraph() is not None
    assert article() is not None