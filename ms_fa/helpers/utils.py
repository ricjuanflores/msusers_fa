import random
import string
import secrets
from typing import Any, List, Optional


def random_string(length: int) -> str:
    return ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits +
            string.ascii_lowercase,
            k=length
        )
    )


def random_integer(length: int) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def array_search(array: List[dict], key: str, value: Any) -> Optional[dict]:
    for item in array:
        if item.get(key) == value:
            return item
    return None

