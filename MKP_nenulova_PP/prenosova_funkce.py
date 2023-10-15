import numpy as np
from scipy.linalg import lu_factor, lu_solve, solve
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import pyplot as plt
import cmath


def PF(M,C,K,b):
    
    n=1400  #vzorkování
    u=np.zeros(n)
    fr=np.zeros(n)

    c=343
    b[150]=0.00001
    




    for f in range(n):
        
        frekvence=(f+5)*0.5
        fr[f]=frekvence
        omega=2*np.pi*frekvence    

        u[f]=np.linalg.norm(spsolve(-omega**2/c**2*M+1j*omega*C+K,b))
        
    plt.plot(fr,u)
    plt.show()
    
    return fr,u


