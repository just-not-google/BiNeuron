import pytest
from AlexRadar.additional_functions.defining_programming_language import DefiningProgrammingLanguage
from AlexRadar.data import TYPE_DEFAULT


@pytest.mark.parametrize("translated_text, answer, proprietary_algorithms", [
    (
"""
def calc(a, b):
    return a + b
result = calc(5, 3)
print(result)
""",
"python", False
    ),
    (
"""
<!DOCTYPE html>
<html>
<head><title>Page</title></head>
<body><h1>Hello</h1></body>
</html>
""",
TYPE_DEFAULT, True
    ),
    (
"""
SELECT id, name FROM users WHERE age > 18 ORDER BY name;
""",
TYPE_DEFAULT, False
    ),
    (
"This is just a simple text without any programming constructs.",
TYPE_DEFAULT, False
    ),
    (
"""
def greet(name):
    console.log("Hello " + name);
greet("World");
""",
TYPE_DEFAULT, True
    )
])
def test_defining_programming_language_for_str(translated_text: str,
                                          answer: str,
                                          proprietary_algorithms: bool):
    assert DefiningProgrammingLanguage(translated_text=translated_text,
        proprietary_algorithms=proprietary_algorithms).defining_programming_language_for_str() == answer