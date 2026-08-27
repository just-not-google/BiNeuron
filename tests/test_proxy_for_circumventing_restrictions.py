import pytest
import httpx
from typing import Dict
from AlexRadar.additional_functions import working_with_proxy


@pytest.mark.parametrize("version_1, proxy_answer", [
    (True, httpx.Client),
    (False, dict)
])
def test_working_with_proxy(version_1: bool,
                            proxy_answer: httpx.Client or Dict):
    assert type(working_with_proxy(version_1=version_1)) == proxy_answer