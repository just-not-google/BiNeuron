import pytest
from typing import List
from AlexRadar.additional_functions.logic_virtual_storage import extraction_all_files


@pytest.mark.parametrize("path, path_lst", [
    ("data_for_tests",
     [
         'tests\\data_for_tests\\data_1.txt',
         'tests\\data_for_tests\\data_2.txt',
         'tests\\data_for_tests\\data_3.jpg',
         'tests\\data_for_tests\\data_4.jpg'
     ])
])
def test_extraction_all_files(path: str,
                              path_lst: List[str]):
    assert extraction_all_files(path) == path_lst