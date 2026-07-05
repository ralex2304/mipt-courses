import RPi.GPIO as IO
import time
import matplotlib.pyplot as plt

dac = [8, 11, 7, 1, 0, 5, 12, 6]

leds = [2, 3, 4, 17, 27, 22, 10, 9]

comp = 14

troyka = 13

IO.setmode(IO.BCM)

IO.setup(dac, IO.OUT)

IO.setup(leds, IO.OUT)

IO.setup(troyka, IO.OUT)

IO.setup(comp, IO.IN)

def dec_to_bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def show_binary(value):
    global leds
    IO.output(leds, dec_to_bin(value))


def adc():
    val = [0] * 8
    ans = 0

    for i in range(8):
        val[i] = 1
        IO.output(dac, val)

        time.sleep(0.005)
    
        if IO.input(comp) == 1:
            val[i] = 0
        else:
            ans += 2**(7 - i)
    
    return ans

def make_files(measures, t):
    data = open("7-measures/data.txt", "w")
    for i in measures:
        data.write(str(i) + "\n")
    data.close()

    settings = open("7-measures/settings.txt", "w")
    settings.write(str(len(measures) / t * 10**9) + "\n")
    settings.write(str(3.3 / 255) + "\n")

def make_plot(measures):
    plt.plot(measures)
    plt.savefig("7-measures/plot.png")
    plt.show()

try:
    input("Press button to discharge the capacitor")

    measures = []
    t1 = time.time_ns()

    IO.output(troyka, 1)
    res = adc()
    while res < 206:
        measures.append(res)
        res = adc()
        print(res)
    
    IO.output(troyka, 0)
    res = adc()
    while res > 166:
        measures.append(res)
        res = adc()
        print(res)

    t2 = time.time_ns()

    t = t2 - t1

    print("Time (ns):", t)
    print("Period (ns):", t / len(measures))
    print("Freq (Hz):", len(measures) / t * 10**9)
    print("Step (V):", str(3.3 / 255))

    make_plot(measures)

    make_files(measures, t)

finally:
    IO.output(dac, 0)
    IO.output(leds, 0)
    IO.output(troyka, 0)
    IO.cleanup()
