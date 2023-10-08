#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigs
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib as mpl

import neumanovaop_Dir_kruh as nop 
import dirichletovaop_Dir_kruh as dop
import matice_tuhosti_kruh as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt


def assembleSystemMECH(mesh, material, function_PS,triplet):

    #Matice hmotnosti
    M=mathmot.matice_hmotnosti(mesh)
    #plt.spy(M,markersize = 4)
    #plt.show()

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]

    
    # Neumanova okrajova podminka
    #oznaceniopodminkyN=100
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN1=NeumanovaOP

    #oznaceniopodminkyN=300
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN3=NeumanovaOP

    #oznaceniopodminkyN=400
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN4=NeumanovaOP
    
    #bN=bN1+bN3+bN4

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
    # Dirichletova okrajova podminka
    oznaceniopodminkyD=500
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD5=DirichletOP[0]
    D5=DirichletOP[1]

    # Dirichletova okrajova podminka
    oznaceniopodminkyD=600
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD6=DirichletOP[0]
    D6=DirichletOP[1]
    
    bD=bD1+bD2+bD3+bD4+bD5+bD6
    D=D1+D2+D3+D4+D5+D6

    B=K+D
    b=b+bD


    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(np.sqrt(Xi**2+Yi**2)*pi)

    x = spsolve(B, b)
    print("x",x)
    plt.plot(x)
    plt.plot(UU)
    plt.title("Numericke/ analyticke reseni")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    plt.title("Reseni ulohy 1")
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
    plt.title("odchylka od presneho reseni")
    plt.show()

    #plt.plot(UU-x)
    #plt.show()
   

    k=mesh.nNodes-2
    k=15
    vals, vecs = eigs(M, k=k, M=B)

    print("vals",vals)
    print("vecs",vecs)
    rvecs=vecs.real
    print("rvecs",rvecs)

    #for i in range(len(rvecs)):
    #    for j in range(k):
    #        if rvecs[i,j]>2:
    #            rvecs[i,j]=0
    #        if rvecs[i,j]<-2:
    #            rvecs[i,j]=0


     
    my_cmap=mpl.colormaps['winter']

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 1.")
    plt.grid(b=None)
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,1], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 2.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,2], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 3.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,3], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 4.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,4], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 5.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,5], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 6.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,6], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 7.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,7], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 8.")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,8], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 9.")
    plt.show()


    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,9], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("Vlastni kmity 10.")
    plt.show()

    



    return 1    #I, J, VAL, nz #RHS
    
    


    

