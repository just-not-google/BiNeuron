import pytest
from AlexRadar.additional_functions.getting_text_from_files import main_get_text_from_files


@pytest.mark.parametrize("file_name, answer_from_data", [
    (r"data_for_tests\data_1.txt", "hello"),
    (r"data_for_tests\data_2.txt", "")
])
def test_main_get_text_from_files(file_name: str,
                                  answer_from_data: str):
    assert main_get_text_from_files(file_name=file_name) == f"<< {answer_from_data} >> - {file_name}\n"