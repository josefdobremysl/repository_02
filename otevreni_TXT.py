import ast
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


with open('furier.txt', encoding='utf-8') as soubor:
    obsah = soubor.read()
print(obsah)

js = json.loads(obsah)


x = js[1]
bod1 = js[2]
plt.plot(x,bod1)
plt.show()
dt = js[3]
n = js[4]

yf=fft(bod1)
xf=fftfreq(n, d=dt)[:n//2]
plt.plot(xf,  np.abs(yf[0:n//2]))
plt.grid()
plt.show()