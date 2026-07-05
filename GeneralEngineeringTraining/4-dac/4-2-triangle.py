import RPi.GPIO as IO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

IO.setmode(IO.BCM)

IO.setup(dac, IO.OUT)


def dec_to_bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


try:
    period = int(input())
    delay = period / (256 * 2)

    while True:
        for i in range(0, 256):
            IO.output(dac, dec_to_bin(i))
            time.sleep(delay)

        for i in range(254, 0, -1):
            IO.output(dac, dec_to_bin(i))
            time.sleep(delay)

finally:
    IO.output(dac, 0)
    IO.cleanup()
