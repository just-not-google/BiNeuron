import pytest
from AlexRadar.additional_functions.checking_integer_for_condition import checking_int_and_float


@pytest.mark.parametrize("value, option_1, answer", [
    (100, True, True),
    ("Hello", True, False),
    (-10, True, False),
    ("012", True, False),
    (0.1, True, False),
    (0.1, False, True),
    ("000", False, False),
    (-0.9, False, False)
])
def test_checking_int_and_float(value: int or float,
                                option_1: bool,
                                answer: bool):
    assert checking_int_and_float(value=value,
                                  option_1=option_1) == answer
