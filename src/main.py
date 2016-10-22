import pyb


def pattern():
    # this could be a static global variable, but in anticipation of it
    # changing in future, I'm currently returning the pattern as a method
    # output.
    return [[0, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0]]


def init_row(row_num):
    # initialize an empty array of tri-state logic
    pins = [2, 2, 2, 2, 2, 2, 2, 2, 2]
    # initialize the ground pin
    pins[row_num] = 0
    for i in range(0, 8):
        if pattern()[row_num][i]:
            # the matrix is charlieplexed. This means that if the column pin
            # is larger or equal to the row pin, it must be offset.
            pins[i if i < row_num else i + 1] = 1
    return pins


def pin_state(i, state):
    # set pin i to either low (0), high (1) or floating (2). Setting the pin
    # to floating requires setting it as an input pin (and thus has high
    # resistance)
    pin_name = 'D' + str(i)
    if state == 2:
        pin = pyb.Pin(pin_name, pyb.Pin.IN)
    else:
        pin = pyb.Pin(pin_name, pyb.Pin.OUT)
        if state == 0:
            pin.low()
        else:
            pin.high()


def output_row(pin_row):
    # set all pins in pin_row to their output state
    for k in range(0, 9):
        pin_state(k, pin_row[k])


def scroll():
    # turn each pin on, one at a time
    for j in range(0, 9):
        for i in range(0, 8):
            pins = [2, 2, 2, 2, 2, 2, 2, 2, 2]
            pins[j] = 0
            pins[i if i < j else i + 1] = 1
            output_row(pins)
            pyb.delay(100)


def show_pattern():
    # show the pattern
    for current_row in range(0, 9):
        pins = init_row(current_row)
        output_row(pins)


while True:
    # scroll()
    show_pattern()

# if something went wrong, the LED will turn on
pin = pyb.Pin()

led = pyb.LED(1)
led.on()
