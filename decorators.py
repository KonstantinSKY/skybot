import sys
from say import Say


def try_decor(func):            # Decorator for handling exceptions
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            msg = f'ERROR!!! - Cant execute function: , {func} \n{repr(e)} {sys.exc_info()[0]}'
            Say(msg).prn_err()

    return inner

@to_json
def get_data():
    return {
        'data': 42
    }


print(get_data())
print(get_data.__name__)
