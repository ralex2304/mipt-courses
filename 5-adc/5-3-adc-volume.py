import RPi.GPIO as IO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

leds = [2, 3, 4, 17, 27, 22, 10, 9]

comp = 14

troyka = 13

IO.setmode(IO.BCM)

IO.setup(dac, IO.OUT)

IO.setup(leds, IO.OUT)

IO.setup(troyka, IO.OUT, initial = 1)

IO.setup(comp, IO.IN)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

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

try:
    while True:
        val = adc()
        
        led_vals = [0] * 8
        for i in range(8):
            if val > i * 32:
                led_vals[i] = 1
        
        IO.output(leds, led_vals)


finally:
    IO.output(dac, 0)
    IO.output(leds, 0)
    IO.cleanup()


