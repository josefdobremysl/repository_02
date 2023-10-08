import math
import numpy as np

def f(oznaceniopodminky, X, Y):
    pi=math.pi
    a = 0
    if oznaceniopodminky==100: # spodni hrana
        a = -pi
    if oznaceniopodminky==200: # prava hrana N.O.P.
        a = 1+np.sin(pi*Y)        
    if oznaceniopodminky==300: # Dir.
        a =  -pi
    if oznaceniopodminky==400: # leva hrana
        a = -pi
    #if X>0.92 and Y>0.92:
    #    a=0
    #if X>0.92 and Y<0.08:
    #    a=0
    
    return a


