import pytest
from BiNeuron.additional_functions.request_anonymization import request_anonymization


@pytest.mark.parametrize("original_text, answer", [
    ("", ""),
    ("Hello, world!", "Hello, world!"),
    ("My email is john.doe@example.com", "My email is <EMAIL_ADDRESS>"),
    ("Call me at 212-555-1234", "Call me at <PHONE_NUMBER>"),
    ("My credit card is 4111 1111 1111 1111", "My credit card is <CREDIT_CARD>"),
    ("John Smith is here", "<PERSON> is here"),
    ("I live in New York", "I live in <LOCATION>"),
    ("Meeting on 2023-01-01", "Meeting on <DATE_TIME>"),
    ("IP address: 192.168.1.1", "IP address: <IP_ADDRESS>"),
    ("Visit https://example.com", "Visit <URL>"),
])
def test_request_anonymization(original_text: str,
                               answer: str):
    assert request_anonymization(original_text=original_text) == answer