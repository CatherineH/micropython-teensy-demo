import pyb

# declare which pins go where in the PCB
b_bank = ['D0',  'D1',  'D2',  'D3',  'D4',  'D5',  'D6',  'D7',  'D8']
a_bank = ['D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17']

buttons = [['D18', 'D19', 'D20'],
           ['D21', 'D22', 'D23'],
           ['A10', 'A11', 'A14']]

pattern = [[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
           [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
           [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
           [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
           [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]

directions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def move_pattern():
    # this could be a static global variable, but in anticipation of it
    # changing in future, I'm currently returning the pattern as a method
    # output.
    global directions
    global pattern
    #print(directions)
    up_active = (directions[0][0] or directions[0][1] or directions[0][2])
    down_active = (directions[2][0] or directions[2][1] or directions[2][2])
    left_active = (directions[0][0] or directions[1][0] or directions[2][0])
    right_active = (directions[0][2] or directions[1][2] or directions[2][2])
    up_down = up_active - down_active
    left_right = left_active - right_active
    if up_down == -1:
        # move the pattern down
        pattern.insert(0, pattern.pop())
    elif up_down == 1:
        # move the pattern up
        pattern.insert(-1, pattern.pop(0))
    if left_right == -1:
        for row in range(len(pattern)):
            pattern[row].insert(0, pattern[row].pop())
    elif left_right == 1:
        for row in range(len(pattern)):
            pattern[row].insert(-1, pattern[row].pop(0))
    #print(pattern)


def init_row(row_num):
    global pattern
    # initialize an empty array of tri-state logic
    pins_a = [2, 2, 2, 2, 2, 2, 2, 2, 2]
    pins_b = [2, 2, 2, 2, 2, 2, 2, 2, 2]
    # initialize the ground pin
    pins_a[row_num] = 0
    for i in range(0, len(pins_a)-1):
        if pattern[row_num][i]:
            # the matrix is charlieplexed. This means that if the column pin
            # is larger or equal to the row pin, it must be offset.
            pins_a[i if i < row_num else i + 1] = 1

        if pattern[row_num][i+8]:
            pins_b[i if i < row_num else i + 1] = 1
    return pins_a+pins_b


def pin_state(pin_name, state):
    # set pin i to either low (0), high (1) or floating (2). Setting the pin
    # to floating requires setting it as an input pin (and thus has high
    # resistance)
    if state == 2:
        pin = pyb.Pin(pin_name, pyb.Pin.IN)
    else:
        pin = pyb.Pin(pin_name, pyb.Pin.OUT)
        if state == 0:
            pin.low()
        else:
            pin.high()


def output_row(pin_row):
    pins = a_bank + b_bank
    # set all pins in pin_row to their output state
    for i in range(0, len(pins)):
        pin_state(pins[i], pin_row[i])


def scroll():
    global pattern
    # turn each pin on, one at a time
    for j in range(0, len(pattern)):
        for i in range(0, len(pattern[0])):
            pins = [2 for i in range(len(pattern))]
            pins[j] = 0
            pins[i if i < j else i + 1] = 1
            output_row(pins)
            pyb.delay(100)


def show_pattern():
    # show the pattern
    for current_row in range(0, 9):
        pins = init_row(current_row)
        output_row(pins)


def read_buttons():
    global directions
    global button_pins
    for i in range(0, 3):
        for j in range(0, 3):
            directions[i][j] = button_pins[i][j].value()
    print(directions)

button_pins = [[pyb.Pin(buttons[i][j], pyb.Pin.IN) for j in range(3) ]
               for i in range(3)]


while True:
    read_buttons()
    move_pattern()

    # scroll()
    show_pattern()

# if something went wrong, the LED will turn on
pin = pyb.Pin()

led = pyb.LED(1)
led.on()
