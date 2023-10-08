import math
import numpy as np

def f(oznaceniopodminky, X, Y):
    pi=math.pi
    a = 0
    verze=1
    if verze == 3:
        if oznaceniopodminky==100: # spodni hrana
            a = -pi#*np.sin(pi*X)*np.cos(pi*Y)           # -pi
        if oznaceniopodminky==200: # prava hrana 
            a = np.sin(pi*X)+np.sin(pi*Y) #np.sin(pi*X)*np.sin(pi*Y)#(np.sin(pi*X)+np.sin(pi*Y))*4
        if oznaceniopodminky==300: # horni hrana
            a = -pi#*np.sin(pi*X)*np.cos(pi*Y)           # -pi
        if oznaceniopodminky==400: # leva hrana
            a = -pi#*np.sin(pi*Y)*np.cos(pi*X)          #-pi
    if verze == 1:
        if oznaceniopodminky==100: # spodni hrana
            a = -pi*np.sin(pi*X)*np.cos(pi*Y)
        if oznaceniopodminky==200: # prava hrana 
            a = 0
        if oznaceniopodminky==300: # horni hrana
            a = pi*np.sin(pi*X)*np.cos(pi*Y)
        if oznaceniopodminky==400: # leva hrana
            a = -pi*np.sin(pi*Y)*np.cos(pi*X)
    if verze == 2:
        if oznaceniopodminky==100: # spodni hrana
            a =  -(X-X**2)
        if oznaceniopodminky==200: # prava hrana 
            a = 0
        if oznaceniopodminky==300: # horni hrana
            a = -(X-X**2)
        if oznaceniopodminky==400: # leva hrana
            a = -(Y-Y**2)
      
    
    return a


