import math
import numpy as np

def f(oznaceniopodminky, X, Y, t):
    pi=math.pi
    f=15
    f1=300
    f2=200
    f3=100
    a = 0
    c=50
    R=0.1


    if oznaceniopodminky==100: # 
        #a =np.sin(2*pi*f1*t) # +np.sin(2*pi*f2*t)  #100* R**2 * (X**2-Y**2)*np.cos(2*pi*f*t) # dipol            #    #monopol
        period=1/f1
        amplituda=1

        if (t % period) < period/2:
            xx = t % period-amplituda
        else:
            xx = -t % period-amplituda

        a = 2 * amplituda / period * xx
        #a= np.sin(2*pi*f2*t)         
        #100*1/R**2 * (X**2-Y**2)*np.cos(2*pi*f2*t)
        a=0


    if oznaceniopodminky==200: # 
        a = 0 
    if oznaceniopodminky==300: # 
        a = 0
    if oznaceniopodminky==400: # 
        a = 0 #np.sin(2*pi*f*t)
    if oznaceniopodminky==500: # 
        a = 0

    return a


