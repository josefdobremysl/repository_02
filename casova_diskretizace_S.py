import numpy as np
import numpy.linalg
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

import dirichletovaop_Dis_S as dop
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
    c=343
    M0=M0

    dt=0.01
    tn=0.3
    n=int(tn/dt)
    y0=np.zeros((mesh.nNodes,1))
    dy0=np.zeros((mesh.nNodes,1))
    beta=0.25
    gamma=0.5
    L=60
    c=343
    pi=np.pi
    f=0.1
    


    y_n=y0
    dy_n=dy0
    ddy_n=spsolve(M0,b0-K*y_n)
    t=0
  
    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], ddy)
    #plt.title("pocatecni reseni")
    #plt.show()
    oznaceniopodminky=300
    S3=som.SOM(oznaceniopodminky,mesh)

    oznaceniopodminky=200
    S4=som.SOM(oznaceniopodminky,mesh)

    my_cmap=mpl.colormaps['winter']
    ax = plt.figure().add_subplot(projection='3d')
    ims=[]

    for k in range(n):
        t=t+dt
        # Dirichletova okrajova podminka
        oznaceniopodminkyD=500
        DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,t)
        bD1=DirichletOP[0]
        D1=DirichletOP[1]
        oznaceniopodminkyD=600
        DirichletOP=dop.DOP(oznaceniopodminkyD,mesh,t)
        bD2=DirichletOP[0]
        D2=DirichletOP[1]
        bD=bD1+bD2
        D=D1+D2
        

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
        

       
    #print("mesh.nNodes",mesh.nNodes)  
    #print(len(y_n)) 
    #print("y_n",y_n)

    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], y_n[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("konecne reseni")
    plt.show()

    




















    return