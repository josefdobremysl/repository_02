import numpy as np
import math
from scipy import sparse

def SOM(oznaceniopodminky,mesh):

    Hrany = mesh.Elmts[1]
    VekOznaOP = Hrany[0]
    VrcholyHran = Hrany[1]
    
    nTri = len(VekOznaOP)
    I = [0] 
    J = [0] 
    VAL = [0] 
    nz = 0

    ## bazove funkce v kvadraturnich uzlech
    basisFE_ref = np.array([[(1+1/math.sqrt(3))/2 ,   (1-1/math.sqrt(3))/2],
                            [(1-1/math.sqrt(3))/2 ,   (1+1/math.sqrt(3))/2]]) 
                            
    
    nQuadrature = 2
    w = 1/2

    for k in range(nTri):
        if VekOznaOP[k] == oznaceniopodminky:
            # vrcholy
            
            verTri = VrcholyHran[k,:]
            D, E = list(VrcholyHran[k,:])
            D = int(D)
            E = int(E)
            coD = mesh.nodeXY[D, :]   
            coE = mesh.nodeXY[E, :]
        
            
            delkahrany = math.sqrt((coD[0]-coE[0])**2+(coD[1]-coE[1])**2)
            
            for i in range(2):
                for j in range(2):
                    k_val = 0.
                    for l in range(nQuadrature):
                        k_val = k_val + delkahrany * w * ( basisFE_ref[j, l]*basisFE_ref[i, l] )

                    I.insert(nz,verTri[i])
                    J.insert(nz,verTri[j])
                    VAL.insert(nz,k_val)
                    
                    nz = nz+1
               
    B=sparse.coo_matrix((VAL,(I,J)),shape=(mesh.nNodes,mesh.nNodes)).tocsr()        
    print("CCCCCCCCCCCCCCCC",B)
            
    return B