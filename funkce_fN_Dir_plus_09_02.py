import math
import numpy as np

def f(oznaceniopodminky, X, Y):
    pi=math.pi
    a = 0
    if oznaceniopodminky==100: # spodni hrana
        a =np.sin(pi*X)+np.sin(pi*Y)
    if oznaceniopodminky==200: # prava hrana        Dirichlet
        a = np.sin(pi*X)+np.sin(pi*Y)
    if oznaceniopodminky==300: # horni hrana
        a =  np.sin(pi*X)+np.sin(pi*Y)
    if oznaceniopodminky==400: # leva hrana
        a = np.sin(pi*X)+np.sin(pi*Y)
    
    return a


