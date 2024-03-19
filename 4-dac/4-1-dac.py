import RPi.GPIO as IO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

IO.setmode(IO.BCM)

IO.setup(dac, IO.OUT)


def dec_to_bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


try:
    while True:
        inp = input()

        if inp == "q":
            break

        if not inp.isdigit():
            print("Negative or not a number")
            continue

        if float(int(inp)) - float(inp) > 0.00001:
            print("Must be integer")
            continue

        num = int(inp)

        if num < 0 or num >= 256:
            print("Must be between 0 and 255")
            continue

        IO.output(dac, dec_to_bin(num))

        print(3.3 / 2**8 * num)

finally:
    IO.output(dac, 0)
    IO.cleanup()
