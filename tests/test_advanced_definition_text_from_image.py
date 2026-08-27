import pytest
from AlexRadar.additional_functions.advanced_definition_text_from_image import LaunchDeepSeekOCR


@pytest.mark.parametrize("photo_path, answer_text", [
    (r"data_for_tests\data_3.jpg", "Test_Image_1234"),
    (r"data_for_tests\data_4.jpg", "Hello, World!")
])
def test_advanced_definition_text_from_image(photo_path: str,
                                             answer_text: str):
    assert (LaunchDeepSeekOCR(photo_path=photo_path).
            advanced_definition_text_from_image() == answer_text)