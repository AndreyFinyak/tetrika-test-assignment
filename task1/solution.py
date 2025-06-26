from functools import wraps
import inspect


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)  # получаем сигнатуру функции
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        for name, value in bound_args.arguments.items():
            expected_type = func.__annotations__.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f'Argument {name} must be of type {expected_type}'
                    )
        return func(*args, **kwargs)
    return wrapper
