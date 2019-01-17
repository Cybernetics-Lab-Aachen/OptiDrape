import pytest


def test_dict():
    input = []  # Todo: Input richtig setzen
    assert isinstance(input, dict)


def test_number_of_keys():
    input = dict() # Todo: Input richtig setzen
    assert 500 == input.keys()


def test_keys():
    input = dict() # Todo: Input richtig setzen

    right_keys = [i for i in range(1,500+1)]
    assert input.keys() == right_keys

def test_sanity_values():
    # Todo: Hier checken, ob die Werte alle Sinn ergeben. Schranken, Typ, etc.
    assert 1==0