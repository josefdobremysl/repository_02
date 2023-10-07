import numpy as np
import funkce_f_333 as fun

def matice_tuhosti(mesh,t):

    nTri = mesh.nTri
    # vektor prave strany
    b = np.zeros((mesh.nNodes,1))

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
        
        CoQ = np.array([[(coA[0]+coB[0])/2 , (coB[0]+coC[0])/2 , (coC[0]+coA[0])/2 ],
                     [ (coA[1]+coB[1])/2 , (coB[1]+coC[1])/2 , (coC[1]+coA[1])/2]])
      
        matA = [ [coB[0]-coA[0], coC[0]-coA[0]],      
                 [coB[1]-coA[1], coC[1]-coA[1]]]   
        
        detA = np.linalg.det(matA)
  
        for i in range(3):
                                
            for l in range(nQuadrature):
                
                X = CoQ[0,l]
                Y = CoQ[1,l]
   
                b[verTri[i]] = b[verTri[i]] + 0.5 * detA * w * ( fun.f(X, Y, t) * basisFE_ref[i,l] ) 
    
    return  b