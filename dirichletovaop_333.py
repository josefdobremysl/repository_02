import numpy as np
import neumanovaop_333 as nop 
import scipy

def DOP(oznaceniopodminky,mesh,t,M,b):
    M=scipy.sparse.lil_matrix(M)
    
    #prispevek k prave strane
    NO = nop.NOP(oznaceniopodminky,mesh,t)
    bD = NO[0]
    bz = NO[1]
          
    o=np.zeros(mesh.nNodes)
   
    for k in range(mesh.nNodes):
        if bz[k] != 0:
            b[k]=bD[k]
            v = M[k,:]
            M[k,:] = o
            #M[:,k] = np.transpose(o)
            M[k,k] = 1
            x = v@b
            b[k] = b[k] - x

 
    return b, M