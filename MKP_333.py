import my_importGmsh as impG
import neumanovaop_333 as nop 
import matice_tuhosti_333 as mattuh
import matice_hmotnosti_25_02_1 as mathmot
import casova_diskretizace_333 as casdis

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

meshfile = 'obdelnik.msh' #KRUH_15.msh'
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



CASDIS = casdis.CD(M,K,b,mesh)
x = CASDIS[0]
E = CASDIS[4]
P_1 = CASDIS[5]
P_2 = CASDIS[6]
P_1S = CASDIS[7]
P_2S = CASDIS[8]
print("shape E",np.shape(E))

fig, ax = plt.subplots()

ax.plot(x, E, label="E")
ax.plot(x, P_1S, label="P_1S")
ax.plot(x, P_2S, label="P_2S")
ax.plot(x, P_1S+P_2S, label="P_1S+P_2S")
ax.plot(x, E-P_1S-P_2S, label="E-P_1S-P_2S")
ax.legend(loc=2); # upper left corner
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('title');
plt.show()


fig.savefig("filename.png")



# ax2.plot(E)
# #plt.plot(x,P_1)
# #plt.plot(x,P_2)
# ax2.plot(P_1S)
# ax2.plot(P_2S)
# ax2.plot(P_1S+P_2S)
# ax2.plot(E-P_1S-P_2S)
# #ax2.imshow()


