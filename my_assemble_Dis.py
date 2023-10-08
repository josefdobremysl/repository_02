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

import neumanovaop_Dis as nop 
import dirichletovaop_Dis as dop
import matice_tuhosti_13_02_1 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import math
import casova_diskretizace as casdis
import somerfieldop_13_02_1 as som

from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import ticker, cm
import matplotlib.tri as tri
import matplotlib.pyplot as plt


def assembleSystemMECH(mesh, material, function_PS,triplet):

    



    #Matice hmotnosti
    M=mathmot.matice_hmotnosti(mesh)
    

    #matice tuhosti + vektor prave strany
    mat_tuh=mattuh.matice_tuhosti(mesh)
    K=mat_tuh[0]
    b=mat_tuh[1]
    t=0
    
    # Neumanova okrajova podminka
    oznaceniopodminkyN=100
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh,t)
    bN2=NeumanovaOP

    oznaceniopodminkyN=300
    NeumanovaOP=nop.NOP(oznaceniopodminkyN,mesh,t)
    bN5=NeumanovaOP

    
    B=K#+S3+S4
    b=bN2+bN5
    M=M

    CASDIS=casdis.CD(M,K,b,mesh)

    




    return 1    
    
    


    

