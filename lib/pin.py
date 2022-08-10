from machine import Pin

def onboard_led(value=None):
    led = Pin("LED", Pin.OUT)
    if type(value) is int:
        led.value(value)
    else:
        led.toggle()
        
    