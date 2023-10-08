import numpy as np
import math
import funkce_fN_Dir_13_02_2 as fun
import matplotlib.pyplot as plt

def NOP(oznaceniopodminky,mesh):

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

    w=0.5

    for i in range(size):
        if VekOznaOP[i]==oznaceniopodminky:
            HranyOznacene[i]=Vrcholyhran[i]

            D, E = list(HranyOznacene[i,:])
            D=int(D)
            E=int(E)
            #seznam krajnich bodu hranic oznacenych podminkou
            coD = mesh.nodeXY[D, :]   
            coE = mesh.nodeXY[E, :]

            coS=(coD+coE)/2
            
            delkahrany=math.sqrt((coD[0]-coE[0])**2+(coD[1]-coE[1])**2)

            #normalove vektory
            n=[(coE[1]-coD[1])/delkahrany,(coD[0]-coE[0])/delkahrany]
            nM[i]=n

            DX=coD[0]
            DY=coD[1]
            EX=coE[0]
            EY=coE[1]

            bNvbodech[E]+=delkahrany * w * fun.f(oznaceniopodminky, EX, EY)
            bNvbodech[D]+=delkahrany * w * fun.f(oznaceniopodminky, DX, DY)

       
    #print("bNvbodech",bNvbodech)
    #plt.show()
    #plt.plot(bNvbodech)

    return bNvbodech


            

