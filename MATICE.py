import numpy as np
import math


A=np.array([[1,2,3],
   [4,5,6],
   [7,8,9]])

print(A)
v=A[1,:]
print(v)
v1=A[:,1]

x=v@v1

print(x)