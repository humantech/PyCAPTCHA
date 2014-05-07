# -*- coding: utf-8 -*-

import random
import string

chars = string.digits + string.ascii_letters


def get_random(size=8, min_=6):
    if min_ > size:
        raise TypeError("size can't be lower then min_")
    n = random.choice(range(min_, size))
    s = ''
    for i in range(0, n):
        s += no_repeat_random(s, chars)
    return s


def no_repeat_random(string, chars):
    r = random.choice(chars)
    if(r in string):
        return no_repeat_random(string, chars)
    else:
        return r

if __name__ == '__main__':
    print get_random()
    print get_random(10)
    print get_random(20)
    print get_random(20,10)
    print get_random(20,10)
    print get_random(20,10)
