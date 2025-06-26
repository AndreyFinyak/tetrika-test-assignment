import pytest
from task1.solution import strict


@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def greet(name: str, age: int = 18):
    return f"{name}, {age}"


@strict
def scale(flag: bool, multiplier: float) -> float:
    return multiplier * 2 if flag else multiplier


class TestAdd:
    def test_valid(self):
        assert add(1, 2) == 3

    def test_invalid_type(self):
        with pytest.raises(TypeError) as exc:
            add(1, "two")
        assert "Argument b must be of type" in str(exc.value)


class TestGreet:
    def test_default_age(self):
        assert greet("Alice") == "Alice, 18"

    def test_all_args_valid(self):
        assert greet("Вася", 25) == "Вася, 25"

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            greet("Alexey", "twenty")

    def test_named_args(self):
        assert greet(name="Dina", age=21) == "Dina, 21"

    def test_named_args_type_error(self):
        with pytest.raises(TypeError):
            greet(name="Dina", age="wrong")


class TestScale:
    def test_valid_true(self):
        assert scale(True, 1.5) == 3.0

    def test_valid_false(self):
        assert scale(False, 1.5) == 1.5

    def test_invalid_bool(self):
        with pytest.raises(TypeError):
            scale("yes", 2.0)

    def test_invalid_float(self):
        with pytest.raises(TypeError):
            scale(True, "high")
