#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

import neumanovaop_13_02_2 as nop 
import dirichletovaop_2 as dop
import matice_tuhosti_13_02_3 as mattuh
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import ticker, cm
import matplotlib.tri as tri



def assembleSystemMECH(mesh, material, function_PS,triplet):

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]
    
    
    # Neumanova okrajova podminka
    oznaceniopodminkyN=100
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN1=NeumanovaOP[0]


    oznaceniopodminkyN=300
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN3=NeumanovaOP[0]

    oznaceniopodminkyN=400
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN4=NeumanovaOP[0]
    
    b=b+bN1+bN3+bN4

    #K=K.toarray()

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=100
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,K,b)
    #b=DirichletOP[0]
    #K=DirichletOP[1]
    

    oznaceniopodminkyD=200
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,K,b)
    b=DirichletOP[0]
    K=DirichletOP[1]

 

    



    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=100
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD1=DirichletOP[0]
    #D1=DirichletOP[1]

    

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=300
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD3=DirichletOP[0]
    #D3=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=400
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD4=DirichletOP[0]
    #D4=DirichletOP[1]
    
     #bD1+bD2+bD3+bD4
    #D1+D2+D3+D4
    


    
    #bN[20]=0
    #bN[21]=0
    #bN[2]=0
    B=K
    
    

    #a=B[2,2]
    #B[2,:]=0
    #B[2,2]=a
    #c=int(mesh.nBsides/2+1)
    #a=B[c,c]
    #B[c,:]=0
    #B[c,c]=a


    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(Xi*pi)+np.sin(Yi*pi)

    x = spsolve(B, b)
    x[2]=0
    
    c2=int(mesh.nBsides/2+1)
    #x[c2]=0
    print("x",x)
    plt.plot(x)
    plt.plot(UU)
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    plt.show()

    z=UU-x
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU-x, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    
    plt.show()

    plt.plot(UU-x)
    plt.show()

    return 1    #I, J, VAL, nz #RHS
    
    


    

