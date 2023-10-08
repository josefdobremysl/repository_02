import numpy as np
import numpy.linalg
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import dirichletovaop_Dis as dop
import somerfieldop_13_02_1 as som
import matplotlib as mpl
import matplotlib.animation as animation
from matplotlib import cm
from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import numpy as np
from random import random, seed
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation

def CD(M0,K,b0,mesh):
    c=10

    
    M0=M0

    dt=0.1 #1e-7
    tn=45 #1e-5
    n=int(tn/dt)
    y0=np.zeros((mesh.nNodes,1))
    dy0=np.zeros((mesh.nNodes,1))
    beta=0.25
    gamma=0.5
    
    
    pi=np.pi
   


    y_n=y0
    dy_n=dy0
    ddy_n=spsolve(M0,b0-K*y_n)
    t=0
  
    oznaceniopodminky=200
    S3=som.SOM(oznaceniopodminky,mesh)

    oznaceniopodminky=500
    S4=som.SOM(oznaceniopodminky,mesh)

    my_cmap=mpl.colormaps['winter']
    ax = plt.figure().add_subplot(projection='3d')
    ims=[]

    for k in range(n):
        t=t+dt
        # Dirichletova okrajova podminka
        oznaceniopodminkyD=400
        DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,t)
        bD=DirichletOP[0]
        D=DirichletOP[1]

        

        M=M0+D+S3+S4
        b=b0+bD


        #f_n=np.sin(2*pi*f*t)
        #t=t+dt
        #f_n1=np.sin(2*pi*f*t)

        A=M+beta*dt**2*K
        g_n1=b-K*y_n-dt*K*dy_n-(1-2*beta)/2*dt**2*K*ddy_n
        ddy_n1=spsolve(A,g_n1)
        y_n1=y_n + dt*dy_n + dt**2*(beta*ddy_n1+(0.5-beta)*ddy_n)
        dy_n1=dy_n+dt*(gamma*ddy_n1+(1-gamma)*ddy_n)
        y_n=y_n1
        dy_n=dy_n1
        ddy_n=ddy_n1
        

    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], y_n[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("konecne reseni")
    plt.show()

    





    return