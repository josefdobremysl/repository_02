#
import numpy as np
#import numpy.linalg
#from scipy import sparse
from scipy.sparse import coo_matrix
#from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from scipy.sparse.linalg import eigs
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits import mplot3d
import matplotlib as mpl

import neumanovaop_Dir_13_02_1 as nop 
import dirichletovaop_Dir_13_02_1 as dop
import somerfieldop_13_02_1 as som   
import matice_tuhosti_13_02_1 as mattuh
import matice_hmotnosti_25_02_1 as mathmot

import math
#from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
#from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix, bmat


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
    #oznaceniopodminkyS=100
    #DirichletOP=som.SOM(oznaceniopodminkyS,mesh)
    #C=DirichletOP


    # Dirichletova okrajova podminka
    oznaceniopodminkyD=200
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD2=DirichletOP[0]
    D2=DirichletOP[1]

    oznaceniopodminkyD=700
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD7=DirichletOP[0]
    D7=DirichletOP[1]

    oznaceniopodminkyD=800
    DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    bD8=DirichletOP[0]
    D8=DirichletOP[1]

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
    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=500
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD5=DirichletOP[0]
    #D5=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=600
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD6=DirichletOP[0]
    #D6=DirichletOP[1]
    
    bD=bD2+bD7+bD8 #+bD3+bD4+bD5+bD6
    D=D2+D7+D8    #+D3+D4+D5+D6

    K=K+D
    bD = b+bD
    M=M


    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(Xi*pi)*np.sin(Yi*pi)

    x = spsolve(K, b)
    print("x",x)
    #plt.plot(x)
    #plt.plot(UU)
    #plt.title("Numericke/ analyticke reseni")
    #plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    #plt.title("Reseni ulohy 1")
    #plt.show()

    z=UU-x
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU-x, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    #plt.title("odchylka od presneho reseni")
    #plt.show()

    #plt.plot(UU-x)
    #plt.show()
   
    
    N = coo_matrix(np.identity(mesh.nNodes))
    
    O = coo_matrix(np.zeros([mesh.nNodes,mesh.nNodes]))
    

    #A = bmat([[K,O],[C,K]])
    #print(A.shape)
    #B = bmat([[O,K],[-M,O]])
    #print(B.shape)


    c=343
    A=K
    B=M/c**2

    k=mesh.nNodes-2
    k=25
    vals, vecs = eigs(B, k=k, M=A)

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

    print(rvecs.shape)
    rvecs=rvecs[0:mesh.nNodes]
    my_cmap=mpl.colormaps['winter']

    w=1.5
    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 1.")
    plt.grid(False)
    #plt.show()

    z=rvecs[:,0]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,1], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 2.")
    #plt.show()

    z=rvecs[:,1]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,2], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 3.")
    #plt.show()

    z=rvecs[:,2]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,3], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 4.")
    #plt.show()

    z=rvecs[:,3]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,4], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 5.")
    #plt.show()

    z=rvecs[:,4]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,5], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 6.")
    #plt.show()

    z=rvecs[:,5]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,6], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 7.")
    #plt.show()

    z=rvecs[:,6]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,7], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 8.")
    #plt.show()

    z=rvecs[:,7]
    levels = np.linspace(z.min(), z.max(), 7)
    fig, ax = plt.subplots()
    ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], z, levels=levels)
    triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    tcf = ax.tricontourf(triang, z)
    fig.colorbar(tcf)
    ax.set(xlim=(0, np.max(mesh.nodeXY[:,0])), ylim=(0, np.max(mesh.nodeXY[:,1])))

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,8], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 9.")
    #plt.show()

    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]),  np.ptp(rvecs[:,0]/w)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,9], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    ax.set_box_aspect((asx,asy,asz))
    ax.yaxis.set_ticks([0.,0.5,1.])
    plt.title("Vlastni kmity 10.")
    plt.show()

    



    return 1    #I, J, VAL, nz #RHS
    
    


    

