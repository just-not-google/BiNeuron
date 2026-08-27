import pytest
from AlexRadar.additional_functions.definition_swearing import definition_swearing


@pytest.mark.parametrize("original_text, bool_answer", [
    ("How are you doing?", False),
    ("123243535", False),
    ("Fuck you", True),
    ("", False),
    ("Damn you to death!", False)
])
def test_definition_swearing(original_text: str,
                             bool_answer: str):
    assert definition_swearing(text=original_text) == bool_answer