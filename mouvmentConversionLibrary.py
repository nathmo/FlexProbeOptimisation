"""
this file contains function to represent conversion of distance
like from an input mouvment of 1 mm, you get 0.1 rad in output.
or from an input mouvement of 1 rad, you get 2 rad in output.
"""

import math
from mpmath import mp
def f_x(x):
        return x

def f_XYRotation(x):
    hypotenuse = 0.02 #20 mm radius of wheel to hole anchor (sorry for the dirty Hardcoded value...)
    return hypotenuse*(1-mp.cos(mp.asin(x/hypotenuse)))

def f_XtoRotation(x):
    hypotenuse = 0.02 #20 mm radius of wheel to hole anchor (sorry for the dirty Hardcoded value...)
    return mp.asin(x/hypotenuse)

def f_Xby8(x):
    ratioReductionWheel = 8
    return x/ratioReductionWheel