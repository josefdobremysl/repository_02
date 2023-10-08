import math
import numpy as np
import matplotlib.pyplot as plt


xmax=0.025
dx=0.00005
period=0.0025
amplituda=1

x = np.arange(0.,xmax,dx)
xx = np.zeros((len(x),1))

for i in range(len(x)):
    xi=x[i]
    if (xi % period) <= period/2:
        xxi = xi % period
    else:
        xxi = -xi % period
    xx[i] = xxi

y = 2 * amplituda / period * xx
plt.plot(x,y)
plt.show()