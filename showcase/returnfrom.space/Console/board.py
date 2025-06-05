from machine import Pin, UART
try:
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
except ImportError:
    usb_hid = None
    Keyboard = None
    Keycode = None

# Mapping of 16 tactile switches to keyboard keys
KEY_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
KEYS = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in KEY_PINS]

uart = UART(0, baudrate=115200)

# Key codes for each tactile switch
KEY_CODES = [
    Keycode.A, Keycode.B, Keycode.C, Keycode.D,
    Keycode.E, Keycode.F, Keycode.G, Keycode.H,
    Keycode.I, Keycode.J, Keycode.K, Keycode.L,
    Keycode.M, Keycode.N, Keycode.O, Keycode.P,
] if Keycode else [0] * 16

keyboard = Keyboard(usb_hid.devices) if usb_hid else None


def read_keys():
    """Read key states, send bytes over UART and optional HID presses."""
    states = [not key.value() for key in KEYS]
    uart.write(bytes(states))
    if keyboard:
        for pressed, code in zip(states, KEY_CODES):
            if pressed:
                keyboard.send(code)

