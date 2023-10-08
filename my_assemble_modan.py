#
import numpy as np
#import numpy.linalg
#from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
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
import polyeig as polyeig

import math
#from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
#from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix, bmat
import scipy.io


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
    oznaceniopodminkyS=200
    DirichletOP=som.SOM(oznaceniopodminkyS,mesh)
    C=DirichletOP


    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=200
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD2=DirichletOP[0]
    #D2=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=300
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD3=DirichletOP[0]
    #D3=DirichletOP[1]

    # Dirichletova okrajova podminka
    # oznaceniopodminkyD=400
    # DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    # bD4=DirichletOP[0]
    # D4=DirichletOP[1]
    # # Dirichletova okrajova podminka
    #oznaceniopodminkyD=500
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD5=DirichletOP[0]
    #D5=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=600
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD6=DirichletOP[0]
    #D6=DirichletOP[1]
    
    #bD=bD2 #+bD3+bD4+bD5+bD6
    #D=D2    #+D3+D4+D5+D6
    c=50
    K=csr_matrix.toarray(K)#+D4
    b=b#+bD
    M=csr_matrix.toarray(M)
    C=csr_matrix.toarray(C)

    X,e = polyeig.polyeig(K,C,M)
    print(X)
    print(e)
    X=X.real

    my_cmap=mpl.colormaps['winter']
    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(X[:,0])
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], X[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    #ax.set_box_aspect((asx,asy,asz))
    plt.title("Vlastni kmity 1.")
    plt.grid(b=None)
    plt.show()



    scipy.io.savemat('test.mat', dict(K=K, C=C, M=M))



    # pi=math.pi
    # UU=np.zeros(mesh.nNodes)
    # for i in range(mesh.nNodes):
    #     Xi = mesh.nodeXY[i,0]   
    #     Yi = mesh.nodeXY[i,1]   
    #     UU[i] = np.sin(Xi*pi)*np.sin(Yi*pi)

    # x = spsolve(K, b)
    # print("x",x)
    #plt.plot(x)
    #plt.plot(UU)
    #plt.title("Numericke/ analyticke reseni")
    #plt.show()

    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    #plt.title("Reseni ulohy 1")
    #plt.show()

    #z=UU-x
    #levels = np.linspace(z.min(), z.max(), 7)
    #fig, ax = plt.subplots()
    #ax.plot(mesh.nodeXY[:,0],mesh.nodeXY[:,1], 'o', markersize=0, color='blue')
    #ax.tricontourf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU-x, levels=levels)
    #triang = tri.Triangulation(mesh.nodeXY[:,0],mesh.nodeXY[:,1])
    #tcf = ax.tricontourf(triang, z)
    #fig.colorbar(tcf)
    #ax.set(xlim=(0, 1), ylim=(0, 1))
    #plt.title("odchylka od presneho reseni")
    #plt.show()

    #plt.plot(UU-x)
    #plt.show()
   
    
    # N = coo_matrix(np.identity(mesh.nNodes))
    
    # O = coo_matrix(np.zeros([mesh.nNodes,mesh.nNodes]))
    

    # A = bmat([[O,N],[-K,-C]])
    
    # B = bmat([[N,O],[O,M]])
    

  

    # k=mesh.nNodes-2
    # k=1
    # vals, vecs = eigs(B, k=k, M=A)

    # print("vals",vals)
    # print("vecs",vecs)
    # rvecs=np.sqrt(vecs.real**2+vecs.imag**2)
    # #rvecs=vecs.real
    # print("rvecs",rvecs)

    #for i in range(len(rvecs)):
    #    for j in range(k):
    #        if rvecs[i,j]>2:
    #            rvecs[i,j]=0
    #        if rvecs[i,j]<-2:
    #            rvecs[i,j]=0

    # print(rvecs.shape)
    # rvecs=rvecs[0:mesh.nNodes]
    # my_cmap=mpl.colormaps['winter']


    # asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,0])
    # ax = plt.figure().add_subplot(projection='3d')
    # ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    # #ax.set_box_aspect((asx,asy,asz))
    # plt.title("Vlastni kmity 1.")
    # plt.grid(b=None)
    # plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,1])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,1], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 2.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,2])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,2], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 3.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,3])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,3], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 4.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,4])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,4], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 5.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,5])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,5], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 6.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,6])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,6], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 7.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,7])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,7], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 8.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,8])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,8], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 9.")
    #plt.show()

#    asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(rvecs[:,9])
#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,9], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 10.")
#    plt.show()

    # A = bmat([[-K,O],[O,N]])
    
    # B = bmat([[C,M],[N,O]])    

    # k=mesh.nNodes-2
    # k=1
    # vals, vecs = eigs(B, k=k, M=A)
    # print("vals",vals)
    # print("vecs",vecs)
    # rvecs=np.sqrt(vecs.real**2+vecs.imag**2)
    # #rvecs=vecs.real
    # print("rvecs",rvecs)
    # rvecs=rvecs[0:mesh.nNodes]

    # ax = plt.figure().add_subplot(projection='3d')
    # ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    # #ax.set_box_aspect((asx,asy,asz))
    # plt.title("Vlastni kmity 1.")
    # plt.grid(b=None)
    # plt.show()



    # A = bmat([[K,O],[C,K]])
    
    # B = bmat([[O,K],[-M,O]])    

    # k=mesh.nNodes-2
    # k=1
    # vals, vecs = eigs(B, k=k, M=A)
    # print("vals",vals)
    # print("vecs",vecs)
    # rvecs=np.sqrt(vecs.real**2+vecs.imag**2)
    # #rvecs=vecs.real
    # print("rvecs",rvecs)
    # rvecs=rvecs[0:mesh.nNodes]

    # ax = plt.figure().add_subplot(projection='3d')
    # ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    # #ax.set_box_aspect((asx,asy,asz))
    # plt.title("Vlastni kmity 1.")
    # plt.grid(b=None)
    # plt.show()

    
#    A = bmat([[O,-K],[M,O]])
    
#    B = bmat([[M,C],[O,M]])    

#    k=mesh.nNodes-2
#    k=1
#    vals, vecs = eigs(B, k=k, M=A)
#    print("vals",vals)
#    print("vecs",vecs)
#    #rvecs=np.sqrt(vecs.real**2+vecs.imag**2)
#    rvecs=vecs.real
#    print("rvecs",rvecs)
#    rvecs=rvecs[0:mesh.nNodes]

#    ax = plt.figure().add_subplot(projection='3d')
#    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], rvecs[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
#    #ax.set_box_aspect((asx,asy,asz))
#    plt.title("Vlastni kmity 1.")
#    plt.grid(b=None)
#    plt.show()














    return 1    #I, J, VAL, nz #RHS
    
    


    

