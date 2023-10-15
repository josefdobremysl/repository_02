import numpy as np
import math
import funkce_fN_PP as fun
import matplotlib.pyplot as plt

def NOP(oznaceniopodminky,mesh,t):

    hrany=mesh.Elmts[1]
    #print("Nvrcholu",hrany)
    VekOznaOP=hrany[0]
    #print("VekOznaOP",VekOznaOP)
    
    Vrcholyhran=hrany[1]
    #print('VekSouradnic',Vrcholyhran)

    size=len(VekOznaOP)
    HranyOznacene=np.zeros((size,2))
    n=np.zeros((2,1))
    nM=np.zeros((size,2))
    bNvbodech=np.zeros((mesh.nNodes,1))
    bz=np.zeros((mesh.nNodes,1))

    w=0.25

    for i in range(size):
        if VekOznaOP[i]==oznaceniopodminky:
            HranyOznacene[i]=Vrcholyhran[i]

            D, E = list(HranyOznacene[i,:])
            D=int(D)
            E=int(E)
            #seznam krajnich bodu hranic oznacenych podminkou
            coD = mesh.nodeXY[D, :]   
            coE = mesh.nodeXY[E, :]

            coB1=coD+(coE-coD)*(0.5-1/2/np.sqrt(3))
            coB2=coD+(coE-coD)*(0.5+1/2/np.sqrt(3))
            delkahrany=math.sqrt((coD[0]-coE[0])**2+(coD[1]-coE[1])**2)

            #normalove vektory
            n=[(coE[1]-coD[1])/delkahrany,(coD[0]-coE[0])/delkahrany]
            nM[i]=n

            X1=coB1[0]
            Y1=coB1[1]
            X2=coB2[0]
            Y2=coB2[1]

            bN = delkahrany * w *( fun.f(oznaceniopodminky, X1, Y1,t) +fun.f(oznaceniopodminky, X2, Y2,t)  )

            bNvbodech[E]+=bN
            bNvbodech[D]+=bN
            bz[E] = 1
            bz[D] = 1

       
    #print("bNvbodech",bNvbodech)
    #plt.show()
    #plt.plot(bNvbodech)

    return bNvbodech, bz


            

