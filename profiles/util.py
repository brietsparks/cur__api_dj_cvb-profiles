import random


def shuffle_string(string):
    l = list(string)
    random.shuffle(l)
    result = ''.join(l)

    return result
