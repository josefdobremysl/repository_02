# importing the module
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.fft import dct, idct

from matplotlib import pyplot as plt
import numpy as np
from scipy.sparse.linalg import eigs
from scipy.sparse import coo_matrix, bmat
import math
import pickle
#import matlab.engine
#import polyeig as polyeig
from scipy import signal
from scipy.fft import fftshift
  

  
# reading the data from the file
with open('ppp_PP.txt', 'rb') as handle:
    data = handle.read()
  
print("Data type before reconstruction : ", type(data))
  
# reconstructing the data as dictionary
d = pickle.loads(data)
  
print("Data type after reconstruction : ", type(d))
print(d)
x = d[1]
y = d[2]
y=y.flatten()
x = x[0:len(y)]
print(y)

q=0
fon=20

c=len(y)
y=y[q:c]
x=x[q:c]
n=len(y)


# a=1.0002
# for i in range(len(y)):
#     y[i]=(y[i]-0.0092769-0.06016)*a**i

#y=y[:1800]
#x=x[:1800]
n=len(y)

dt = d[3]
print("n",n)
print(y)


#y=y[10:c]
#x=x[10:c]
plt.plot(x,y)
#plt.title("2")
plt.xlabel("Čas [s]",fontsize=fon)
plt.ylabel("Akustický tlak [Pa]",fontsize=fon)
plt.rcParams['font.size'] = 15
plt.grid()

yf = fft(y)
xf = fftfreq(n, dt)[:n//2]
zoboblast=7000
yf=yf[:zoboblast]
xf=xf[:zoboblast]

yf[0]=0


plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))
plt.grid()
#plt.title("1")
plt.xlabel("Frekvence [Hz]",fontsize=fon)
plt.ylabel("Spektrální hustota",fontsize=fon)

plt.rcParams['font.size'] = 15
plt.show()

#########################################################

x = d[1]
y = d[6]
x = x[0:len(y)]
y=y[q:c]
x=x[q:c]

y=y.flatten()
#y=y[10:c]
#x=x[10:c]
plt.plot(x,y)
#plt.title("2")
plt.xlabel("Čas [s]",fontsize=fon)
plt.ylabel("Akustický tlak [Pa]",fontsize=fon)
plt.rcParams['font.size'] = 15
plt.grid()

plt.show()

yf = fft(y)
xf = fftfreq(n, dt)[:n//2]

yf=yf[:zoboblast]
xf=xf[:zoboblast]
yf[0]=0
plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))
plt.grid()
#plt.title("2")
plt.xlabel("Frekvence [Hz]",fontsize=fon)
plt.ylabel("Spektrální hustota",fontsize=fon)
plt.rcParams['font.size'] = 15
plt.show()

f, t, Sxx = signal.spectrogram(y, 1/dt)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# ############################################################

x = d[1]
y = d[7]
x = x[0:len(y)]
y=y[q:c]
x=x[q:c]

y=y.flatten()
#y=y[10:c]
#x=x[10:c]
plt.plot(x,y)
#plt.title("2")
plt.xlabel("Čas [s]",fontsize=fon)
plt.ylabel("Akustický tlak [Pa]",fontsize=fon)
plt.rcParams['font.size'] = 15
plt.grid()

plt.show()

yf = fft(y)
xf = fftfreq(n, dt)[:n//2]

yf=yf[:zoboblast]
xf=xf[:zoboblast]
yf[0]=0
plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))
plt.grid()
#plt.title("2")
plt.xlabel("Frekvence [Hz]",fontsize=fon)
plt.ylabel("Spektrální hustota",fontsize=fon)
plt.rcParams['font.size'] = 15
plt.show()

file = open("model_cp.txt", "w")
my_dict = {1 : x, 2 : dt, 3 : n, 4 : d[6], 5 : d[7]}
# serializing dictionary 
# closing the file
yy=d[6]

for i in range(len(yy)):
    file.write(str(yy[i])+"\n")
file.close()

# ############################################################

# x = d[1]
# y = d[6]
# x = x[0:len(y)]
# y=y[:c]
# x=x[:c]

# y=y.flatten()
# y=y[380:c]
# x=x[380:c]

# a=1.01
# for i in range(len(y)):
#     y[i]=y[i]*np.exp(a*i)

# plt.plot(x,y)
# plt.title("3")
# plt.show()

# yf = fft(y)
# xf = fftfreq(n, dt)[:n//2]

# yf=yf[:zoboblast]
# xf=xf[:zoboblast]
# yf[0]=0
# plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))
# plt.grid()
# plt.title("3")
# plt.show()

# #############################################################

# x = d[1]
# y = d[7]
# x = x[0:len(y)]

# y=y.flatten()
# y=y[380:c]
# x=x[380:c]
# plt.plot(x,y)
# plt.title("4")
# plt.show()

# yf = fft(y)
# xf = fftfreq(n, dt)[:n//2]

# yf=yf[:zoboblast]
# xf=xf[:zoboblast]
# yf[0]=0
# plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))

# plt.grid()
# plt.title("4")
# plt.show()

# ##############################################################

# x = d[1]
# y = d[8]
# x = x[0:len(y)]

# y=y.flatten()
# y=y[10:c]
# x=x[10:c]
# plt.plot(x,y)
# plt.title("5")
# plt.show()

# yf = fft(y)
# xf = fftfreq(n, dt)[:n//2]

# yf=yf[:zoboblast]
# xf=xf[:zoboblast]
# yf[0]=0
# plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))

# plt.grid()
# plt.title("5")
# plt.show()

# #################################################################

# x = d[1]
# y = d[9]
# x = x[0:len(y)]

# y=y.flatten()
# yf = fft(y)
# y=y[10:c]
# x=x[10:c]
# plt.plot(x,y)
# plt.title("6")
# plt.show()

# yf = fft(y)
# xf = fftfreq(n, dt)[:n//2]

# yf=yf[:zoboblast]
# xf=xf[:zoboblast]
# yf[0]=0
# plt.plot(xf, 2.0/n * np.abs(yf[0:n//2]))

# plt.grid()
# plt.title("6")
# plt.show()