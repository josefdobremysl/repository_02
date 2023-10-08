import math
import numpy as np

def f(oznaceniopodminky, X, Y, t):
    pi=math.pi
    f=0.05
    a = 0
    c=343
    R=0.1
    if oznaceniopodminky==100: # 
        a =  0# np.sin(2*pi*f*t)  # 1/c/R**2 * (X**2-Y**2)*np.cos(2*pi*f*t) # dipol            # np.sin(2*pi*f*t)   #monopol
    if oznaceniopodminky==200: # 
        a = 0 
    if oznaceniopodminky==300: # 
        a = 0
    if oznaceniopodminky==400: # 
        a = np.sin(2*pi*f*t)
    if oznaceniopodminky==500: # 
        a = 0

    return a


