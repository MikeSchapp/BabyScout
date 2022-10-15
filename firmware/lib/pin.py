from machine import Pin


def onboard_led(value=None):
    """
    Toggle the onboard led, a call without a value causes it to switch to the opposite state.
    Calls int (0 or 1) cause the led to be set to on or off

    params:

        value(int): 1 - on or 0 - off state of onboard led
    """
    led = Pin("LED", Pin.OUT)
    if type(value) is int:
        led.value(value)
    else:
        led.toggle()


def create_button(pin):
    """
    Reuseable function for creating buttons

    params:
        pin(int): GPIO Number to detect pulldown action on.
    """
    button = Pin(pin, Pin.IN, Pin.PULL_DOWN)
    return button
