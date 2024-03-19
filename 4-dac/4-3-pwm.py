import RPi.GPIO as IO

pin = 24

IO.setmode(IO.BCM)

IO.setup(pin, IO.OUT)

pwm = IO.PWM(pin, 1000)
pwm.start(0)


try:
    while True:
        dc = int(input())
        pwm.ChangeDutyCycle(dc)

        print(3.3 * dc / 100)

finally:
    pwm.stop()
    IO.output(pin, 0)
    IO.cleanup()
