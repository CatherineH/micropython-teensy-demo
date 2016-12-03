import pyb

print("Executing main.py")

led = pyb.LED(1)
num_blink = 0

while True:
    print(num_blink)
    num_blink += 1
    led.on()
    pyb.delay(100)
    led.off()
    pyb.delay(100)
