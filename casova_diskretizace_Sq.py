import dirichletovaop_Dis_Sq as dop
import somerfieldop_13_02_1 as som
import numpy as np
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import *
import numpy as np
import pickle


def CD(M0,K,b0,mesh):
    
    c = 50
    beta = 0.25
    gamma = 0.5
    
    t = 0
    dt = 0.00001
    tn = 0.1
    n = int(tn/dt)
    bod1= np.zeros((n,1))

    print(mesh.nNodes)

    y_n = np.zeros((mesh.nNodes,1))
    dy_n = np.zeros((mesh.nNodes,1))
    ddy_n = spsolve(M0/c**2,b0-K*y_n)
      
    oznaceniopodminky = 300
    S3 = som.SOM(oznaceniopodminky,mesh)

    oznaceniopodminky = 400
    S4 = som.SOM(oznaceniopodminky,mesh)

    my_cmap = mpl.colormaps['winter']
    ax = plt.figure().add_subplot(projection='3d')

    C = (S3+S4)/c  #+S4

    for k in range(n):

        t = t+dt
        # Dirichletova okrajova podminka
        oznaceniopodminkyD = 100
        DirichletOP = dop.DOP(oznaceniopodminkyD,mesh,t)
        bD = DirichletOP[0]
        D = DirichletOP[1]

        M = M0+D
        M = M/c**2
        b = b0+bD

        # Newmarkova metoda
        A=M + dt/2*C + beta*dt**2*K
        g_n1 = b - C@dy_n - dt/2*C@ddy_n - K@y_n - dt*K@dy_n - (1-2*beta)/2*dt**2*K@ddy_n
        ddy_n1 = spsolve(A,g_n1)
        y_n1 = y_n + dt*dy_n + dt**2*(beta*ddy_n1+(0.5-beta)*ddy_n)
        dy_n1 = dy_n + dt*(gamma*ddy_n1+(1-gamma)*ddy_n)
        y_n = y_n1
        dy_n = dy_n1
        ddy_n = ddy_n1
        bod1[k]=y_n[1061,0]
  
    #bod1=np.transpose(bod1)
    x = np.arange(0.,tn,dt)
    #plt.plot(x,bod1)
    #plt.show()

    ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], y_n[:,0], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
    plt.title("konecne reseni")
    plt.show()

   

    # opening file in write mode (binary)
    file = open("dictionary1.txt", "wb")
  
    my_dict = {1 : x, 2 : bod1, 3 : dt, 4 : n}
  
    # serializing dictionary 
    pickle.dump(my_dict, file)
  
    # closing the file
    file.close()    

    return x, bod1, dt, n 