import math
import numpy as np
import matplotlib.pyplot as plt
# importing the module
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.fft import dct, idct
  

xmax=0.025
dx=0.00001
period=0.00003
amplituda=1

x = np.arange(0.,period,dx)
xx = np.zeros((len(x),1))


for i in range(len(x)):
    xi=x[i]
    if xi <= period:
        
        if xi <= period/3:
            xxi = xi * 3 * amplituda / period
        if xi <= period * 2 / 3 and xi >= period / 3:
            xxi=amplituda
        if xi >= period * 2 / 3:
            xxi = 3*amplituda - xi * 3 * amplituda / period
        xx[i] = xxi

y = xx
fon=20
n=len(y)
plt.plot(x,y)
plt.show()
zoboblast=7000
yf = fft(y)
xf = fftfreq(n, dx)[:n//2]

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