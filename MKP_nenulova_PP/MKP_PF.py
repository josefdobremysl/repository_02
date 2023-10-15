import my_importGmsh as impG
import neumanovaop_PP as nop 
import matice_tuhosti_PP as mattuh
import matice_hmotnosti_PP as mathmot
import casova_diskretizace_PP as casdis
import prenosova_funkce as pref
import somerfieldop_PP as som

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

meshfile = 'model_3.msh' #KRUH_15.msh'
mesh = impG.GMSH_READER()        # create a object 'mesh'
mesh.readMesh(meshfile)  



#Matice hmotnosti
M = mathmot.matice_hmotnosti(mesh)
t=0 
#matice tuhosti + vektor prave strany
mat_tuh = mattuh.matice_tuhosti(mesh,t)
K = mat_tuh[0]
b = mat_tuh[1]
t = 0
    
# Neumanova okrajova podminka
oznaceniopodminkyN = 100
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN1 = NeumanovaOP[0]

oznaceniopodminkyN = 300
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN3 = NeumanovaOP[0]

oznaceniopodminkyN = 400
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN4 = NeumanovaOP[0]
    
oznaceniopodminkyN = 500
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN5 = NeumanovaOP[0]

oznaceniopodminkyN = 600
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN6 = NeumanovaOP[0]

oznaceniopodminkyN = 800
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN8 = NeumanovaOP[0]

oznaceniopodminkyN = 1000
NeumanovaOP = nop.NOP(oznaceniopodminkyN,mesh,t)
bN10 = NeumanovaOP[0]
#B = K
b = b+bN1+bN3+bN4+bN5+bN6+bN8+bN10
M = M

oznaceniopodminky = 200
S2 = som.SOM(oznaceniopodminky,mesh)

oznaceniopodminky = 700
S3 = som.SOM(oznaceniopodminky,mesh)

oznaceniopodminky = 900
S4 = som.SOM(oznaceniopodminky,mesh)
  
C = (S2+S3+S4)




PRENOS_F = pref.PF(M,C,K,b)
print(PRENOS_F[0],PRENOS_F[1])




# ax2.plot(E)
# #plt.plot(x,P_1)
# #plt.plot(x,P_2)
# ax2.plot(P_1S)
# ax2.plot(P_2S)
# ax2.plot(P_1S+P_2S)
# ax2.plot(E-P_1S-P_2S)
# #ax2.imshow()


