import dirichletovaop_PP as dop
import somerfieldop_PP as som
import pravastrana_PP as prst
import numpy as np
import matice_tuhosti_PP as mattuh

from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import *
import pickle
from scipy.linalg import lu_factor, lu_solve, solve
from mpl_toolkits.mplot3d import Axes3D
print('numpy: '+np.version.full_version)
import matplotlib.animation as animation
import matplotlib
print('matplotlib: '+matplotlib.__version__)
import scipy.io



def CD(M0,K0,b0,mesh):
    
    c = 343
    beta = 0.25
    gamma = 0.5
    
    t = 0
    dt = 0.0001
    tn = 0.5
    n = int(tn/dt)
    bod1 = np.zeros(n)
    bod2 = np.zeros(n)
    bod3 = np.zeros(n)
    bod4 = np.zeros(n)
    bod5 = np.zeros(n)
    bod6 = np.zeros(n)
    
    E   = np.zeros(n)
    P_1 = np.zeros(n)
    P_2 = np.zeros(n)
    P_1S = np.zeros(n)
    P_2S = np.zeros(n)
    
    N = mesh.nNodes  # Meshsize
    fps = 1/dt # frame per sec
    frn = n # frame number of the animation
    
    zarray = np.zeros((N, frn))

    print(mesh.nNodes)

    y_n = np.zeros(mesh.nNodes)
    dy_n = np.zeros(mesh.nNodes)
      

    ddy_n = spsolve(M0/c**2,b0-K0*y_n)
      
    oznaceniopodminky = 200
    S2 = som.SOM(oznaceniopodminky,mesh)

    oznaceniopodminky = 700
    S3 = som.SOM(oznaceniopodminky,mesh)

    oznaceniopodminky = 900
    S4 = som.SOM(oznaceniopodminky,mesh)


    
    C = (S2+S3+S4)/c  #+S4
    K = K0
    M = M0
    M = M/c**2
    A =  M + np.dot(dt/2,C) + np.dot(beta*dt**2,K)   #   M + dt/2*C + beta*dt**2*K
    A=A.toarray()
    lu, piv = lu_factor(A)

    for k in range(n):

        
        t = t+dt
        # Dirichletova okrajova podminka
        #oznaceniopodminkyD = 100
        #DirichletOP = dop.DOP(oznaceniopodminkyD,mesh,t,K0,b0)
        #bD = DirichletOP[0]
        #K = K0     #DirichletOP[1]

        #matice tuhosti + vektor prave strany
        pravast = prst.matice_tuhosti(mesh, t)
        b = pravast
        if t<0.0005:
            b[250]=1
  

        # Newmarkova metoda
        #A = M + np.dot(dt/2,C) + np.dot(beta*dt**2,K)   #   M + dt/2*C + beta*dt**2*K
        g_n1 =  b - C@dy_n - dt/2*C@ddy_n - K@y_n - dt*K@dy_n - (1-2*beta)/2*dt**2*K@ddy_n
        

        ddy_n1 = lu_solve((lu,piv),g_n1)
        #ddy_n1 = solve(A,g_n1)
        y_n1 =  y_n + dt*dy_n + dt**2*(beta*ddy_n1+(0.5-beta)*ddy_n)
        dy_n1 = dy_n + dt*(gamma*ddy_n1+(1-gamma)*ddy_n)
        y_n = y_n1
        dy_n = dy_n1
        ddy_n = ddy_n1
        bod1[k] = y_n[136,0]
        bod2[k] = y_n[170,0]
        bod3[k] = y_n[242,0]
        bod4[k] = y_n[823,0]
        bod5[k] = y_n[166,0]
        bod6[k] = y_n[80,0]
       
        zarray[:,k] = y_n[:,0]*1000
        E[k] = 1/2 * (np.transpose(dy_n1[:,0]) @ M @ dy_n1[:,0] + np.transpose(y_n1[:,0]) @ K @ y_n1[:,0])
        P_1[k] = np.transpose(dy_n[:,0]) @ b
        P_2[k] = -np.transpose(dy_n[:,0]) @ C @ dy_n[:,0]
    
        P_1S[0] = 0
        P_2S[0] = 0
        P_1S[1] = (P_1[1])/2
        P_2S[1] = (P_2[1])/2
        if k > 1:
            P_1S[k] = P_1S[k-1] + (P_1[k-1]+P_1[k])/2
            P_2S[k] = P_2S[k-1] + (P_2[k-1]+P_2[k])/2

    P_1S=P_1S*dt
    P_2S=P_2S*dt


    file = open("zarray", "wb")
    my_dict = {1 : zarray,2: mesh.nodeXY[:,0],3: mesh.nodeXY[:,1] }
    # serializing dictionary 
    pickle.dump(my_dict, file)
    # closing the file
    file.close() 

      

    
    #bod1=np.transpose(bod1)
    x = np.arange(0.,tn,dt)
    #plt.plot(x,bod1)
    #plt.show()

    xlim=0.7
    ylim=0.7

    for i in range(7):
        my_cmap = mpl.colormaps['winter']
        ax = plt.figure().add_subplot(projection='3d') 
        pc=n//7*i-1
        asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(zarray[:,pc])
        #ax.set_xlim3d(0,xlim)
        #ax.set_ylim3d(0, ylim)
        #ax.set_zlim3d(-np.ptp(zarray[:,pc]),np.ptp(zarray[:,pc])/4)#np.ptp(zarray[:,pc]))#np.ptp(zarray[:,pc])/1000 )
        ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], zarray[:,pc], cmap=my_cmap, linewidth=0, edgecolor='none', antialiased=False)
        #ax.set_box_aspect((asx,asy,asz))
        ax.view_init(elev=20, azim=-120, roll=0)
        #ax.yaxis.set_ticks([0.,0.5,1.])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('akustický tlak  $ [10^{-3}Pa]$', rotation=0)
        plt.title(i)
        #plt.axis('equal')
        plt.show()

    



    

    # ANIMACE

# def update_plot(frame_number, zarray, plot):
#     plot[0].remove()
#     plot[0] = ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], zarray[:,frame_number], cmap="magma", linewidth=0, edgecolor='none', antialiased=False)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# plot = [ax.plot_trisurf(mesh.nodeXY[:,0],mesh.nodeXY[:,1], zarray[:,0], color='0.75')]#, rstride=1)]#, cstride=1)]
# ax.set_zlim(-3,3)#(-0.003,0.003)

# #asx,asy,asz=asx, asy, asz = np.ptp(mesh.nodeXY[:,0]), np.ptp(mesh.nodeXY[:,1]), np.ptp(zarray[:,10])
# #ax.set_box_aspect((asx,asy,asz))
# ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=10000/fps)


# fn = 'animation_M3_1'
# #ani.save(fn+'.mp4',writer='ffmpeg',fps=fps)
# ani.save(fn+'.gif',writer='imagemagick',fps=fps))





    # opening file in write mode (binary)
    file = open("ppp_PP.txt", "wb")
    my_dict = {1 : x, 2 : bod1, 3 : dt, 4 : n, 5 : bod2, 6 : bod3, 7 : bod4, 8 : bod5, 9 : bod6 }
    # serializing dictionary 
    pickle.dump(my_dict, file)
    # closing the file
    file.close()   



    return x, bod1, dt, n, E, P_1, P_2, P_1S, P_2S