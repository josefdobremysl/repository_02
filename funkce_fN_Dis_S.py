import math
import numpy as np

def f(oznaceniopodminky, X, Y, t):
    pi=math.pi
    f=5
    a = 0
    c=343
    R=0.1
    if oznaceniopodminky==100: # spodni hrana Y=0
        a = 0#1/c/R**2 * (X**2-Y**2)*np.cos(2*pi*f*t) # dipol            # np.sin(2*pi*f*t)   #monopol
    if oznaceniopodminky==200: # prava hrana X=1
        a = 0 
    if oznaceniopodminky==300: # horni hrana Y=1
        a = 0
    if oznaceniopodminky==400: # leva hrana X=0
        a = 0
    if oznaceniopodminky==500: # leva hrana X=0
        a = np.sin(2*pi*f*t)   #monopol
    if oznaceniopodminky==600: # leva hrana X=0
        a = np.sin(2*pi*f*t)   #monopol


    return a


