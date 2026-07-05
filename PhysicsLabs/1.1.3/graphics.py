import numpy as np
import math
import matplotlib.pyplot as plt

# m = 20
#X = [497, 497.415, 497.83, 498.245, 498.66, 499.075, 499.49, 499.905, 500.32, 500.735, 501.15, 501.565, 501.98, 502.395, 502.81, 503.225, 503.64, 504.055, 504.47, 504.885, 505.3]
#Y = [8.924587238, 53.54752343, 98.17045962, 142.7933958, 151.717983, 267.7376171, 303.4359661, 276.6622044, 339.134315, 232.0392682, 178.4917448, 116.0196341, 71.3966979, 89.24587238, 35.69834895, 17.84917448, 8.924587238, 0, 8.924587238, 8.924587238]

# m = 10
X = [497, 497.83, 498.66, 499.49, 500.32, 501.15, 501.98, 502.81, 503.64, 504.47, 505.3]
Y = [31.23605533, 120.4819277, 209.7278001, 290.0490852, 285.5867916, 147.2556894, 80.32128514, 26.77376171, 4.462293619, 8.924587238]

for i in range(len(Y)):
    Y[i] = Y[i] / 1000

avgR = 500.2237037
sigma = 1.358060022

R = np.arange(min(X) - 1, max(X) + 1.01, 0.01)
plt.plot(R, 1 / math.sqrt(2*math.pi) / sigma * np.exp(-(R - avgR)**2 / (2*sigma**2)))

x = []
y = []

x.append(X[0])
x.append(X[0])
for i in range(1, len(X) - 1):
    x.append(X[i])
    x.append(X[i])
x.append(X[-1])
x.append(X[-1])

y.append(0)
for i in Y:
    y.append(i)
    y.append(i)
y.append(0)

plt.plot(x, y)

plt.ylim(ymin = 0)


plt.title('Гистограмма для m = 10')
plt.xlabel(r"$R, Ом$")
plt.ylabel(r"$\omega, Ом^{-1}$")
plt.grid(True)

plt.text(500.2, 0, r"$R_{ср}$"+"\n"+r"$\downarrow$", horizontalalignment="center")

plt.text(500.2 - sigma, 0, r"$R_{ср} - \sigma$"+"\n"+r"$\downarrow$", horizontalalignment="center")
plt.text(500.2 + sigma, 0, r"$R_{ср} + \sigma$"+"\n"+r"$\downarrow$", horizontalalignment="center")

plt.text(500.2 - 2*sigma, 0, r"$\downarrow$", horizontalalignment="center")
plt.text(500.2 + 2*sigma, 0, r"$\downarrow$", horizontalalignment="center")

plt.text(500.2 - 3*sigma, 0, r"$\downarrow$", horizontalalignment="center")
plt.text(500.2 + 3*sigma, 0, r"$\downarrow$", horizontalalignment="center")


plt.text(504, 0.25, r"$\langle R \rangle = " + "{:.1f}".format(avgR) + r" \ Ом$"+"\n" + r"$\sigma = " + "{:.1f}".format(sigma) + r" \ Ом$", bbox={'boxstyle':'square', 'facecolor': '#FFFFFF'})

plt.show()
