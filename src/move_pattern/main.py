import pyb

# declare which pins go where in the PCB
b_bank = ['D8',  'D7',  'D6',  'D5',  'D4',  'D3',  'D2',  'D1',  'D0']
a_bank = ['D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17']

buttons = [['D18', 'D19', 'D20'],
           ['D21', 'D22', 'D23'],
           ['A18', 'A19', 'A20']]



def pin_state(pin_name, state):
    # set pin i to either low (0), high (1) or floating (2). Setting the pin
    # to floating requires setting it as an input pin (and thus has high
    # resistance)
    if state == 2:
        pyb.Pin(pin_name, pyb.Pin.IN)
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


class DemoBoard(object):

    def __init__(self):
        self.pattern = [[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                   [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                   [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                   [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                   [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
                   [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
                   [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                   [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                   [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]
        self.directions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.button_pins = [[pyb.Pin(buttons[i][j], pyb.Pin.IN) for j in range(3) ]
                            for i in range(3)]

    def move_pattern(self):
        # this could be a static global variable, but in anticipation of it
        # changing in future, I'm currently returning the pattern as a method
        # output.
        up_active = (self.directions[0][0] or self.directions[0][1] or self.directions[0][2])
        down_active = (self.directions[2][0] or self.directions[2][1] or self.directions[2][2])
        left_active = (self.directions[0][0] or self.directions[1][0] or self.directions[2][0])
        right_active = (self.directions[0][2] or self.directions[1][2] or self.directions[2][2])
        center = self.directions[1][1]
        up_down = up_active - down_active
        left_right = left_active - right_active
        if up_down == -1:
            # move the pattern down
            self.pattern.insert(0, self.pattern.pop())
        elif up_down == 1:
            # move the pattern up
            self.pattern.insert(-1, self.pattern.pop(0))
        if left_right == -1:
            for row in range(len(self.pattern)):
                self.pattern[row].insert(0, self.pattern[row].pop())
        elif left_right == 1:
            for row in range(len(self.pattern)):
                self.pattern[row].insert(-1, self.pattern[row].pop(0))
        elif center == 1:
            for i in range(len(self.pattern)):
                for j in range(len(self.pattern[0])):
                    self.pattern[i][j] = not self.pattern[i][j]

    def read_buttons(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.directions[i][j] = self.button_pins[i][j].value()

    def on_off(self):

        if self.directions[1][1]:
            self.pattern = [[1 for i in range(16)] for j in range(9)]
        elif self.directions[1][2]:
            self.pattern = [[0 for i in range(16)] for j in range(9)]

    def run(self):
        while True:
            self.read_buttons()
            self.move_pattern()
            self.show_pattern()

    def scroll(self):
        # turn each pin on, one at a time
        for j in range(0, len(self.pattern)):
            for i in range(0, len(self.pattern[0])):
                pins = [2 for k in range(len(self.pattern[0]) + 2)]
                _j = j if i < 8 else j + 9
                _i = i if i < 8 else i + 1
                pins[_j] = 0
                pins[_i if _i < _j else _i + 1] = 1
                output_row(pins)

    def init_row(self, row_num):
        # initialize an empty array of tri-state logic
        pins_a = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        pins_b = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        # initialize the ground pin
        pins_a[row_num] = 0
        pins_b[row_num] = 0
        for i in range(0, len(pins_a) - 1):
            if self.pattern[row_num][i]:
                # the matrix is charlieplexed. This means that if the column pin
                # is larger or equal to the row pin, it must be offset.
                pins_a[i if i < row_num else i + 1] = 1
            if self.pattern[row_num][i + 8]:
                pins_b[i if i < row_num else i + 1] = 1
        return pins_a + pins_b

    def show_pattern(self):
        # show the pattern
        for current_row in range(0, 9):
            pins = self.init_row(current_row)
            output_row(pins)

_db = DemoBoard()
_db.run()

# if something went wrong, the LED will turn on
led = pyb.LED(1)
led.on()
