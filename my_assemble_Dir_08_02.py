#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import funkce_f_08_02 as fun
import neumanovaop_08_02 as nop 
import dirichletovaop_08_02 as dop
import matice_tuhosti_08_02 as mattuh
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve



def assembleSystemMECH(mesh, material, function_PS,triplet):

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]
    
    # Neumanova okrajova podminka
    #oznaceniopodminkyN=300
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN1=NeumanovaOP

    #oznaceniopodminkyN=200
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN2=NeumanovaOP
    #print("bNvbodechN:",bN)



    #bN=bN1+bN2
    # Dirichletova okrajova podminka
    oznaceniopodminkyD=100
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD1=DirichletOP[0]
    D1=DirichletOP[1]

    # Dirichletova okrajova podminka
    oznaceniopodminkyD=200
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD2=DirichletOP[0]
    D2=DirichletOP[1]

    # Dirichletova okrajova podminka
    oznaceniopodminkyD=300
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD3=DirichletOP[0]
    D3=DirichletOP[1]

    # Dirichletova okrajova podminka
    oznaceniopodminkyD=400
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD4=DirichletOP[0]
    D4=DirichletOP[1]
    
    bD=bD1+bD2+bD3+bD4
    D=D1+D2+D3+D4

    B=K+D
    b=b+bD

    #plt.plot(b)
    #plt.show()
           
    #print('b',b)
    #print(B.todense())
    #marksiz=200/mesh.nNodes
    #plt.spy(B, markersize = marksiz)
    #plt.show()
    #print("delka_b:",len(b))
    #print("delka_bN:",len(bN))
    #print("bN:",bN)
    #print("Okrajoznaceny",Okrajoznaceny)

    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(Xi*pi)*np.sin(Yi*pi)

    x = spsolve(B, b)
    print("x",x)
    plt.plot(x)
    plt.plot(UU)
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU)
    plt.show()

    return 1    #I, J, VAL, nz #RHS
    
    


    

