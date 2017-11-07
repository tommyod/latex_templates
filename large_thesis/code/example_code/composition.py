#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:30:35 2017

@author: tommy
"""

def square(x):
    return x*x

def add(x):
    return x + 2

def compose(f, g):
    """Composition of functions. A higher order function.
    """
    def composed_function(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composed_function

f, g = square, add

composed_f_g = compose(f, g)
composed_g_f = compose(g, f)

print(composed_f_g(2)) # 16
print(composed_g_f(2)) # 6
