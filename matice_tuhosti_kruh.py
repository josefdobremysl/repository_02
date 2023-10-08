import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import funkce_f_kruh as fun
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve


def matice_tuhosti(mesh):

    nTri = mesh.nTri
    I=[0] 
    J=[0] 
    VAL=[0] 

    nz = 0

    # vektor prave strany
    b = np.zeros((mesh.nNodes,1))

    # bazove funkce v kvadraturnich uzlech
   
    
    basisFE_ref = np.array([[0.5 ,   0.,  0.5],
                            [0.5 ,  0.5,   0.],  
                            [0.  ,  0.5,  0.5]])
    # PD podle X baz. fci v kvadr. uzlech
    gradFEx_ref =  np.array([[-1,  -1,  -1],
                            [  1,   1,   1],  
                            [  0.,  0,   0]])
    # PD podle Y baz. fci v kvadr. uzlech
    gradFEy_ref =  np.array([[-1,  -1,  -1],
                            [  0.,  0,   0],  
                            [  1,   1,   1]])
    
    nQuadrature = 3
    w = 1./3

    for k in range(nTri):
        
        # vrcholy
        verTri = mesh.triangles[k, :]  
        A, B, C = list(verTri)
       
        coA = mesh.nodeXY[A, :]   
        coB = mesh.nodeXY[B, :]
        coC = mesh.nodeXY[C, :]
        
        CoQ=np.array([[(coA[0]+coB[0])/2 , (coB[0]+coC[0])/2 , (coC[0]+coA[0])/2 ],
                     [ (coA[1]+coB[1])/2 , (coB[1]+coC[1])/2 , (coC[1]+coA[1])/2]])
      
                # referencni zobrazeni
        b_ref = [coA]
        
        matA = [ [coB[0]-coA[0], coC[0]-coA[0]],      
                 [coB[1]-coA[1], coC[1]-coA[1]]]   
        
        detA = np.linalg.det(matA)
        invA = np.linalg.inv(matA)

        # prepocet gradientu baz. funkci
        gradFEx = invA[0,0]*gradFEx_ref + invA[1,0]*gradFEy_ref
        gradFEy = invA[0,1]*gradFEx_ref + invA[1,1]*gradFEy_ref
        
        for i in range(3):
            for j in range(3):
                  k_val = 0.
                  for l in range(nQuadrature):
                      k_val = k_val + 0.5 * detA * w * ( gradFEx[i,l] * gradFEx[j,l] + gradFEy[i,l] * gradFEy[j,l] ) 
                  #print("verTri:",verTri)
                  I.insert(nz,verTri[i])
                  J.insert(nz,verTri[j])
                  VAL.insert(nz,k_val)
                  nz = nz+1
                  
            for l in range(nQuadrature):
                
                X=CoQ[0,l]
                Y=CoQ[1,l]
   
                b[verTri[i]] = b[verTri[i]] + 0.5 * detA * w * ( fun.f(X, Y) * basisFE_ref[i,l] ) 
    
    B=sparse.coo_matrix((VAL,(I,J)),shape=(mesh.nNodes,mesh.nNodes)).tocsr()  
    return B, b