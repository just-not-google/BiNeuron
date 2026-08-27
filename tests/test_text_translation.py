import pytest
from AlexRadar.additional_functions import TranslatorText


LST_FOR_TESTS = [
    "1010",
    "Hello, man. How are you?",
    "",
    "嗨,你好吗?",
    "¿Por qué no tomamos algo alcohólico?",
    "!@#$%^&*"
]

@pytest.mark.parametrize("original_text, bool_answer", [
    (LST_FOR_TESTS[0], True),
    (LST_FOR_TESTS[1], False),
    (LST_FOR_TESTS[2], True),
    (LST_FOR_TESTS[3], True),
    (LST_FOR_TESTS[4], True),
    (LST_FOR_TESTS[5], True),
])
def test_needs_translation_to_main_language(original_text: str, bool_answer: bool):
    translator = TranslatorText(original_text=original_text)
    assert translator._needs_translation_to_main_language() == bool_answer

@pytest.mark.parametrize("text, expected_translation", [
    (LST_FOR_TESTS[0], LST_FOR_TESTS[0]),
    (LST_FOR_TESTS[1], LST_FOR_TESTS[1]),
    (LST_FOR_TESTS[2], LST_FOR_TESTS[2]),
    (LST_FOR_TESTS[3], "Hi, how are you?"),
    (LST_FOR_TESTS[4], "Why don't we drink something alcoholic?"),
    (LST_FOR_TESTS[5], LST_FOR_TESTS[5]),
])
def test_main_translater(text: str, expected_translation: str):
    translator = TranslatorText(original_text=text)
    assert translator.main_translater() == expected_translation