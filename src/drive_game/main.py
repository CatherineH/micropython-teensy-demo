import pyb

# declare which pins go where in the PCB
b_bank = ['D8',  'D7',  'D6',  'D5',  'D4',  'D3',  'D2',  'D1',  'D0']
a_bank = ['D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17']

buttons = [['D18', 'D19', 'D20'],
           ['D21', 'D22', 'D23'],
           ['A18', 'A19', 'A20']]

trail_to_follow = [9, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1,
                   2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,
                   11, 12, 12, 12, 13, 13, 13, 14, 14, 15, 15, 15, 14, 14, 14, 13, 13,
                   12, 12, 11, 11, 10, 10, 9, 9]


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
        self.sprite_pos = [8, 4]
        self.pattern = [[0 for i in range(16)] for j in range(9)]
        self.directions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.button_pins = [[pyb.Pin(buttons[i][j], pyb.Pin.IN) for j in range(3) ]
                            for i in range(3)]
        self.trail = [8 for i in range(9)]
        self.current_index = 0
        self.fill_index = 0

    def move_pattern(self):
        # this could be a static global variable, but in anticipation of it
        # changing in future, I'm currently returning the pattern as a method
        # output.
        left_active = self.directions[1][2]
        right_active = self.directions[1][0]
        up_active = self.directions[0][1]
        down_active = self.directions[1][1]
        if left_active:
            self.sprite_pos[0] -= 1
        if right_active:
            self.sprite_pos[0] += 1
        if up_active:
            self.sprite_pos[1] -= 1
        if down_active:
            self.sprite_pos[1] += 1

    def read_buttons(self):
        for i in range(0, 3):
            for j in range(0, 3):
                self.directions[i][j] = self.button_pins[i][j].value()

    def update_pattern(self):
        self.pattern = [[0 for i in range(16)] for j in range(9)]

        for i in range(8):
            for j in range(15):
                if j == self.trail[i] or j-1 == self.trail[i] or j+1 == self.trail[i]:
                    self.pattern[i][j] = 1
        self.pattern[8][self.sprite_pos[0] % 15] = 1
        self.pattern[8][(self.sprite_pos[0] + 1) % 15] = 1
        self.pattern[8][(self.sprite_pos[0] - 1) % 15] = 1
        self.trail.insert(0, trail_to_follow[self.current_index])
        if self.trail[-1] == self.sprite_pos[0]:
            self.fill_index += 1
        for i in range(8):
            if self.fill_index/20 > i:
                self.pattern[i][15] = 1
        self.current_index += 1
        self.current_index %= len(trail_to_follow)
        self.trail.pop()

    def run(self):
        while True:
            self.read_buttons()
            self.move_pattern()
            self.update_pattern()
            self.show_pattern()

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
