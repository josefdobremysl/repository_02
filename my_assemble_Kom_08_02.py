#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

import neumanovaop_13_02_1 as nop 
import dirichletovaop_08_02_1 as dop
import matice_tuhosti_08_02 as mattuh
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.tri as tri



def assembleSystemMECH(mesh, material, function_PS,triplet):

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]
    
    # Neumanova okrajova podminka
    oznaceniopodminkyN=100
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN1=NeumanovaOP

    oznaceniopodminkyN=300
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN2=NeumanovaOP

    oznaceniopodminkyN=400
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    bN4=NeumanovaOP
    
    bN=bN1+bN2+bN4

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=100
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD1=DirichletOP[0]
    #D1=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=200
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD2=DirichletOP[0]
    #D2=DirichletOP[1]

    # Dirichletova okrajova podminka
    oznaceniopodminkyD=200
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD3=DirichletOP[0]
    D3=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=400
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD4=DirichletOP[0]
    #D4=DirichletOP[1]
    
    bD=bD3     #bD1+bD2+bD3+bD4
    D=D3    #D1+D2+D3+D4

    B=K+D
    b=b+bD+bN

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

    z=UU-x
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=2, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU-x, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    
    plt.show()    

    return 1    #I, J, VAL, nz #RHS
    
    


    

