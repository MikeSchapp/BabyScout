from machine import Pin

def onboard_led(value=None):
    led = Pin("LED", Pin.OUT)
    if type(value) is int:
        led.value(value)
    else:
        led.toggle()
        

def button_one():
    button = Pin(9, Pin.IN, Pin.PULL_DOWN)
    return button

def button_two():
    button = Pin(8, Pin.IN, Pin.PULL_DOWN)
    return button

def button_three():
    button = Pin(7, Pin.IN, Pin.PULL_DOWN)
    return button

def button_four():
    button = Pin(6, Pin.IN, Pin.PULL_DOWN)
    return button

def button_five():
    button = Pin(5, Pin.IN, Pin.PULL_DOWN)
    return button

def button_six():
    button = Pin(4, Pin.IN, Pin.PULL_DOWN)
    return button

def button_seven():
    button = Pin(3, Pin.IN, Pin.PULL_DOWN)
    return button

def button_eight():
    button = Pin(2, Pin.IN, Pin.PULL_DOWN)
    return button
