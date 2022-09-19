from machine import Pin

def onboard_led(value=None):
    led = Pin("LED", Pin.OUT)
    if type(value) is int:
        led.value(value)
    else:
        led.toggle()
        
def create_button(pin):
    button = Pin(pin, Pin.IN, Pin.PULL_DOWN)
    return button

