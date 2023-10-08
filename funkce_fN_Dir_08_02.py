import math
import numpy as np

def f(oznaceniopodminky, X, Y):
    pi=math.pi
    a = 0
    if oznaceniopodminky==100: # spodni hrana
        a = -pi*np.sin(pi*X)*np.cos(pi*Y)
    if oznaceniopodminky==200: # prava hrana 
        a = np.sin(pi*X)*np.sin(pi*Y) #    pi*np.cos(pi*X)*np.sin(pi*Y)
    if oznaceniopodminky==300: # horni hrana
        a =  pi*np.sin(pi*X)*np.cos(pi*Y)
    if oznaceniopodminky==400: # leva hrana
        a = -pi*np.cos(pi*X)*np.sin(pi*Y)

    return a


