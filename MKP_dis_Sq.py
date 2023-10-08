import my_importGmsh as impG
import neumanovaop_Dis_Sq as nop 
import matice_tuhosti_13_02_1 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import casova_diskretizace_Sq as casdis

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


meshfile = 'sit_DNNSS_0.03_zjemneni.msh'

mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  

#Matice hmotnosti
M = mathmot.matice_hmotnosti(mesh)
 
#matice tuhosti + vektor prave strany
mat_tuh = mattuh.matice_tuhosti(mesh)
K = mat_tuh[0]
b = mat_tuh[1]
t = 0
    
# Neumanova okrajova podminka
oznaceniopodminkyN = 200
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN2 = NeumanovaOP

oznaceniopodminkyN = 500
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN5 = NeumanovaOP

#oznaceniopodminkyN = 400
#NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
#bN4 = NeumanovaOP
    
B = K
b = bN2+bN5#+bN4
M = M



CASDIS = casdis.CD(M,K,b,mesh)


