import random


def to_leet(phrase):
    replacements = {
        'o': 0,
        'O': 0,
        'i': 1,
        'I': 1,
        'z': 2,
        'Z': 2,
        'e': 3,
        'E': 3,
        'a': 4,
        'A': 4,
        's': 5,
        'S': 5,
        't': 7,
        'T': 7,
        'B': 8,
    }

    rep = ''

    for char in phrase:
        if char in replacements:
            if random.choice([True, False]):
                rep += str(replacements[char])
            else:
                rep += char
        else:
            rep += char

    if phrase[-1] == phrase[-1].upper():
        rep = rep[:-1] + phrase[-1]

    return rep
