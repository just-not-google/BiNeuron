import pytest
from BiNeuron.additional_functions.definition_swearing import definition_swearing


@pytest.mark.parametrize("original_text, bool_answer", [
    ("How are you doing?", False),
    ("123243535", False),
    ("Fuck you", True),
    ("", False),
    ("Damn you to death!", False),
    ("Shit happens", True),
    ("You son of a bitch", True),
    ("Asshole!", True),
    ("What the hell is this?", False),
    ("FUCK YOU", True),
])
def test_definition_swearing(original_text: str,
                             bool_answer: bool):
    assert definition_swearing(text=original_text) == bool_answer