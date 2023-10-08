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

import neumanovaop_Dis_S as nop 
import dirichletovaop_Dis as dop
import matice_tuhosti_13_02_1 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import math
import casova_diskretizace_S as casdis
import somerfieldop_13_02_1 as som

from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt


def assembleSystemMECH(mesh, material, function_PS,triplet):

    

    #oznaceniopodminky=300
    #S3=som.SOM(oznaceniopodminky,mesh)

    #oznaceniopodminky=400
    #S4=som.SOM(oznaceniopodminky,mesh)



    #Matice hmotnosti
    M=mathmot.matice_hmotnosti(mesh)
    #plt.spy(M,markersize = 4)
    #plt.show()

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]
    t=0
    
    # Neumanova okrajova podminka
    oznaceniopodminkyN=100
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh,t)
    bN2=NeumanovaOP

    oznaceniopodminkyN=400
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh,t)
    bN5=NeumanovaOP

    #oznaceniopodminkyN=400
    #NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh)
    #bN4=NeumanovaOP
    
    #bN=bN1+bN3+bN4

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
    #oznaceniopodminkyD=300
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD3=DirichletOP[0]
    #D3=DirichletOP[1]

    # Dirichletova okrajova podminka
    #oznaceniopodminkyD=400
    #DirichletOP=dop.DOP(oznaceniopodminkyD,mesh)
    #bD4=DirichletOP[0]
    #D4=DirichletOP[1]
    
    
    #bD=bD4
    #D=D4

    B=K#+S3+S4
    b=bN2+bN5
    M=M

    CASDIS=casdis.CD(M,K,b,mesh)

    

    #x = spsolve(B, b)
    #print("x",x)
    #plt.plot(x)
    
    #plt.title("Numericke/ analyticke reseni")
    #plt.show()

    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], x)
    #plt.title("Reseni ulohy 1")
    #plt.show()

    

    #plt.plot(UU-x)
    #plt.show()
   

    #k=mesh.nNodes-2
    #k=15
    #vals, vecs = eigs(M, k=k, M=B)

    #print("vals",vals)
    #print("vecs",vecs)
    #rvecs=vecs.real
    #print("rvecs",rvecs)
    



    return 1    #I, J, VAL, nz #RHS
    
    


    

