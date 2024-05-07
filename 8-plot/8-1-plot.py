import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

settings = open("7-measures/settings.txt", "r")
freq, step = map(float, settings.readlines())
settings.close()

data = open("7-measures/data.txt")
measures = list(map(float, data.readlines()))
data.close()

mpl.rcParams['font.size'] = 16
plt.figure(figsize = (10,8), facecolor = "white")

plt.title("Процесс заряда и разряда конденсатора в RC-цепочка", ha="center", wrap=True)
plt.ylabel("Напряжение, В")
plt.xlabel("Время, с")

x = [1 / freq * i for i in range(len(measures))]
y = [i * step for i in measures]

plt.plot(x, y, "b-", marker=".", mfc="r", mec="orange", markersize=10, label="V(t)", markevery=5)
plt.xlim(min(x), max(x) * 1.1)
plt.ylim(min(y), max(y) * 1.1)

plt.grid(visible = True, color = "gray", which = 'major', axis = 'both', alpha = 1, linewidth = 0.9)
plt.grid(visible = True, color = "gray", which = 'minor', axis = 'both', alpha = 0.5, linestyle = ':')

mmax = 0
peak_i = 0
for i in range(len(y)):
    if mmax < y[i]:
        peak_i = i
        mmax = y[i]

t_charge = x[peak_i] - x[0]
t_discharge = x[-1] - t_charge

plt.text(x[-1] - (x[-1] - x[0]) * 0.3, max(y) - abs(max(y) - min(y)) * 0.45, "Время заряда = %.1f с" % (t_charge), size=15)
plt.text(x[-1] - (x[-1] - x[0]) * 0.3, max(y) - abs(max(y) - min(y)) * 0.55, "Время разряда = %.1f с" % (t_discharge), size=15)

plt.minorticks_on()
plt.tight_layout()
plt.legend(loc = "best", fontsize = 12)

plt.savefig("8-plot/plot.svg")
plt.show()
