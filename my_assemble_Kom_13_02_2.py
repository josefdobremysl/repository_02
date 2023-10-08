#
import numpy as np
import numpy.linalg
from scipy import sparse
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

import neumanovaop_13_02_2 as nop 
import dirichletovaop_2 as dop
import matice_tuhosti_13_02_2 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.tri as tri
import matplotlib as mpl

def assembleSystemMECH(mesh, material, function_PS,triplet):

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]

    M=mathmot.matice_hmotnosti(mesh)
    
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
    #b=b+bd
    #K=K+D
    # oznaceniopodminkyD=300
    # DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,K,b)
    # b=DirichletOP[0]
    # K=DirichletOP[1]

    #oznaceniopodminkyD=400
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,K,b)
    #b=DirichletOP[0]
    #K=DirichletOP[1]

    
    
    my_cmap=mpl.colormaps['winter']


    pi=math.pi
    UU=np.zeros(mesh.nNodes)
    for i in range(mesh.nNodes):
        Xi = mesh.nodeXY[i,0]   
        Yi = mesh.nodeXY[i,1]   
        UU[i] = np.sin(pi*Xi)*np.sin(pi*Yi)#Xi*(1-Xi)*Yi*(1-Yi)#np.sin(pi*Xi)*np.sin(pi*Yi)

    x = spsolve(K, b)
    print("x",x)

    E_max=0
    for i in range(mesh.nNodes):
        em=np.abs(UU[i]-x[i])
        if em>E_max:
            E_max=em
    print("E_max",E_max)

    E_L2=0
    nTri = mesh.nTri
    for i in range(nTri):
        

                # vrcholy
        verTri = mesh.triangles[i, :]  
        A, B, C = list(verTri)
       
        coA = mesh.nodeXY[A, :]   
        coB = mesh.nodeXY[B, :]
        coC = mesh.nodeXY[C, :]
        
        
        
        matA = [ [coB[0]-coA[0], coC[0]-coA[0]],      
                 [coB[1]-coA[1], coC[1]-coA[1]]]   
        
        detA = np.linalg.det(matA)
        for k in range(3):
            E_L2+=(UU[verTri[k]]-x[verTri[k]])**2*detA/3/2
        
        
        
        
    E_L2=np.sqrt(E_L2)
    du=(UU-x)
    E_L22=np.transpose(du) @ M @ du

    E_L22=np.sqrt(E_L22)

    
    print("E_L2",E_L2)
    print("E_L22",E_L22)

    plt.plot(x)
    plt.plot(UU)
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x,cmap=my_cmap)
    plt.grid(b=None)
    plt.show()

    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], UU)
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
    
    plt.show()

    plt.plot(UU-x)
    plt.show()

    return 1    #I, J, VAL, nz #RHS
    
    


    

