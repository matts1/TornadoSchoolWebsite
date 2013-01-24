from string import ascii_uppercase as upper, ascii_lowercase as lower, digits
import random
def random_key(length, chars=upper+lower+digits):
    return "".join(random.choice(chars) for i in range(length))
