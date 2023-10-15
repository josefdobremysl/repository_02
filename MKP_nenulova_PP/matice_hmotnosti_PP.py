import numpy as np
from scipy import sparse


def matice_hmotnosti(mesh):

    nTri = mesh.nTri
    I = [0] 
    J = [0] 
    VAL = [0] 

    nz = 0

    # bazove funkce v kvadraturnich uzlech
    basisFE_ref = np.array([[0.5 ,   0.,  0.5],
                            [0.5 ,  0.5,   0.],  
                            [0.  ,  0.5,  0.5]])
    
    nQuadrature = 3
    w = 1./3

    for k in range(nTri):
        
        # vrcholy
        verTri = mesh.triangles[k, :]  
        A, B, C = list(verTri)
       
        coA = mesh.nodeXY[A, :]   
        coB = mesh.nodeXY[B, :]
        coC = mesh.nodeXY[C, :]
    
        
        matA = [ [coB[0]-coA[0], coC[0]-coA[0]],      
                 [coB[1]-coA[1], coC[1]-coA[1]]]   
        
        detA = np.linalg.det(matA)

        
        for i in range(3):
            for j in range(3):
                  k_val = 0.
                  for l in range(nQuadrature):
                      basisFE_ref_I = basisFE_ref[i,l]
                      basisFE_ref_J = basisFE_ref[j,l]  
                      k_val = k_val + 0.5 * detA * w * (basisFE_ref_I*basisFE_ref_J) 
                  
                  I.insert(nz,verTri[i])
                  J.insert(nz,verTri[j])
                  VAL.insert(nz,k_val)
                  nz = nz+1
                  
    
    M = sparse.coo_matrix((VAL,(I,J)),shape=(mesh.nNodes,mesh.nNodes)).tocsr()  
    return M