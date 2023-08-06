from random import choice
from turtle import color

from coloratura import cprint, Pantone, Bit4


def test_string():
    cprint('Single string', color=Pantone.EMERALD, sep=' | ')


def test_strings():
    cprint('string one', 'string two', 'string three', color=Pantone.EMERALD, sep=' | ')


def test_dictionary():
    is_dictionary = {0: {1: {2: {3: 'Dictionary'}}}}
    cprint(is_dictionary[0][1][2][3], color=Bit4.WHITE)


def test_tuple():
    is_tuple = 'one', 'two', 'three'
    cprint(is_tuple, color=Pantone.ILLUMINATING)


def test_list():
    is_tuple = ['one', 'two', 'three']
    cprint(is_tuple, color=Pantone.ILLUMINATING)


def test_set():
    is_tuple = {'one', 'two', 'three'}
    cprint(is_tuple, color=Pantone.ILLUMINATING)


def test_boolean():
    cprint(True, color=Bit4.GREEN, end=', ')
    cprint(False, color=Bit4.RED, end=', ')
    cprint(None, color=Bit4.BLUE)


def colors_list(colour):
    c = list()
    for i in colour.__dict__:
        c.append(i)
    return c[2:-2:]


def colors(palette):
    for i in colors_list(palette):
        cprint('\033[7m', i, '\033[0m', color=getattr(palette, i))


# test_string()
# test_strings()
# test_dictionary()
# test_tuple()
# test_list()
# test_set()
# test_boolean()

colors(Pantone)
colors(Bit4)

# cprint('\n', bg=getattr(Bit4, choice(colors_list(Bit4))), end='')
cprint('\n', bg=Pantone.CLASSIC_BLUE, end='')
cprint('\xA0', bg=Pantone.CLASSIC_BLUE)


