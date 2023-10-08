#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix

from scipy.sparse.linalg import eigs

import neumanovaop_13_02_1 as nop 
import dirichletovaop_26_02_1 as dop
import matice_tuhosti_13_02_1 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import somerfieldop_13_02_1 as som
import casova_diskretizace as cas_dis
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt


def assembleSystemMECH(mesh, material, function_PS,triplet):

    #   Somerfieldova O.P.
    oznaceniopodminkyS=400
    S=som.SOM(oznaceniopodminkyS,mesh)
    plt.spy(S,markersize = 4)
    plt.show()

    #Matice hmotnosti

    M=mathmot.matice_hmotnosti(mesh)
    plt.spy(M,markersize = 4)
    plt.show()

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
    bN3=NeumanovaOP

    #oznaceniopodminkyN=400
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN4=NeumanovaOP
    
    bN=bN1+bN3#34+bN3

    

  

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
    bD2=DirichletOP[0]
    D2=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=400
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD4=DirichletOP[0]
    #D4=DirichletOP[1]
    
    bD=bD2     #bD1+bD2+bD3+bD4
    D=D2    #D1+D2+D3+D4

    B=K+D#+S
    b=b+bD+bN

    casova_diskret=cas_dis.CD(M,B,b,mesh)

  

    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(Xi*pi)*np.sin(Yi*pi)

    x =spsolve(B, b)
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


    return 1    #I, J, VAL, nz #RHS
    
    


    

