import functools
import io
import sys


def check_print(assert_in: str = "", length: int = -1):
    """Captures output of print function and checks if the function contains a given string"""

    def checker(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            capturedOutput = io.StringIO()
            sys.stdout = capturedOutput
            func(*args, **kwargs)
            sys.stdout = sys.__stdout__
            capt = capturedOutput.getvalue()
            if assert_in:
                assert assert_in in capt
                return None
            if length >= 0:
                assert len(capt) > length
            return capt

        return wrapper

    return checker


def return_vals(*args, **_):
    for arg in args:
        print(arg)


def get_post(message):
    return {
        "attachments": [],
        "avatar_url": "https://i.groupme.com/1024x1024.jpeg.c64d4fc5aeca45cb9fd2c1ca054fc22d",
        "created_at": "1632929238",
        "group_id": "69502628",
        "id": "163292923878111513",
        "name": "Colin Delahunty",
        "sender_id": "29762584",
        "sender_type": "user",
        "source_guid": "baac853e03cdf5d1d1ff77f105711ef3",
        "system": False,
        "text": f"@SportsBot {message}",
        "user_id": "29762584",
    }
