import string
import random

def generate_short_url(domain, length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(length))
    return domain+short_url
