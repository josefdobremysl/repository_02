import funkce_fN_Dir_plus_09_02 as fun
import numpy as np


oznaceniopodminky=100
delkahrany=1
w=0.5
X1=0.5-1/(2*np.sqrt(3))
Y1=0.5
X2=0.5+1/(2*np.sqrt(3))
Y2=0


b = delkahrany * w * ( fun.f(oznaceniopodminky, X1, Y1) +fun.f(oznaceniopodminky, X2, Y2)  )

print(b)