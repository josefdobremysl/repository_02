import math
import numpy as np

def f(X, Y, t): # f-ce P strany
    pi=math.pi
    f=100
    a=0
    verze=3
    period=1/f
    amplituda=3

    if X > 0.45 and X < 0.55 and Y > 0.45 and Y < 0.55 and t < 0.03:
        if verze==1:
         
            if (t % period) < period/2:
                xx = 2 * amplituda / period * t % (period/2)-amplituda/2
            else:
                xx = 1/2*amplituda - 2 * amplituda / (period/2) * t % period

            a =xx         
        if verze==2:
            a = np.sin(2*pi*f*t)
        if verze==3:
            period=0.0003 
            
            if t <= period:
                
                if t <= period/3:
                    xxi = t * 3 * amplituda / period
                if t <= period * 2 / 3 and t >= period / 3:
                    xxi=amplituda
                if t >= period * 2 / 3:
                    xxi = amplituda - (t % (period/3) ) * 3 * amplituda / period
                a = xxi



    return 0

