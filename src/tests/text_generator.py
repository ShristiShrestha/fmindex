import random
import string
def random_string(n: int, alpha: str = string.ascii_letters) -> str:
    return ''.join(random.choices(alpha, k=n))