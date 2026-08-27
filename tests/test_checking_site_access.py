import pytest
from AlexRadar.additional_functions.checking_site_access import checking_site_access


@pytest.mark.parametrize("url, url_answer", [
    ("https://httpbin.org/#/", True),
    ("https://isitdown.page/", True),
    ("https://cp.cloudflare.com", False),
    ("https://www.gstatic.com/generate_204", False),
    ("https://detectportal.firefox.com/success.txt", True)
])
def test_checking_site_access(url: str,
                              url_answer: bool):
    assert checking_site_access(url=url) == url_answer