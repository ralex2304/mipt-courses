import RPi.GPIO as IO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

comp = 14

troyka = 13

IO.setmode(IO.BCM)

IO.setup(dac, IO.OUT)

IO.setup(troyka, IO.OUT, initial = 1)

IO.setup(comp, IO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for i in range(0, 256):
        IO.output(dac, decimal2binary(i))

        time.sleep(0.001)

        if IO.input(comp) == 1:
            return i

    return 256

try:
    while True:
        val = adc()
        print("adc: {}; V: {}".format(val, val / 256 * 3.3))

finally:
    IO.output(dac, 0)
    IO.cleanup()


