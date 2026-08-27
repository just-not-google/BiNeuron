import pytest
from typing import List
from AlexRadar.additional_functions import detect_programming_language


@pytest.mark.parametrize("text, answer_lst", [
    (
"""
def greet(name):
    print(f"Hello, {name}!")
greet("World")
""",
['python']),
    (
"""
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
""",
['java']),
    (
"""
#include <iostream>
#include <vector>
int main() {
    std::vector<int> v = {1, 2, 3};
    for (auto x : v) std::cout << x << ' ';
    return 0;
}
""",
['haskell', 'cpp']),
    (
"""
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <script>
        function sayHello() {
            alert('Hi!');
        }
    </script>
</head>
<body>
    <button onclick="sayHello()">Click</button>
</body>
</html>
""",
['html'])
])
def test_detect_programming_language(text: str,
                                     answer_lst: List[str]):
    assert detect_programming_language(text) == answer_lst