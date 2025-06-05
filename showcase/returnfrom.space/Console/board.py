from machine import Pin, UART
import time
try:
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
except ImportError:
    usb_hid = None
    Keyboard = None
    Keycode = None

# Pin mapping derived from the numpad schematic (SW1..SW16)
ROW_PINS = [Pin(i, Pin.OUT) for i in (0, 1, 2, 3)]
COL_PINS = [Pin(i, Pin.IN, Pin.PULL_UP) for i in (4, 5, 6, 7)]

uart = UART(0, baudrate=115200)

KEY_CODES = [
    Keycode.A, Keycode.B, Keycode.C, Keycode.D,
    Keycode.E, Keycode.F, Keycode.G, Keycode.H,
    Keycode.I, Keycode.J, Keycode.K, Keycode.L,
    Keycode.M, Keycode.N, Keycode.O, Keycode.P,
] if Keycode else [0] * 16

keyboard = Keyboard(usb_hid.devices) if usb_hid else None

DEBOUNCE_MS = 20
_last_raw = [0] * 16
_last_change = [0] * 16
_state = [0] * 16


def _scan_matrix():
    states = [0] * 16
    for r, rpin in enumerate(ROW_PINS):
        rpin.low()
        time.sleep_us(20)
        for c, cpin in enumerate(COL_PINS):
            idx = r * 4 + c
            states[idx] = not cpin.value()
        rpin.high()
    return states


def read_keys():
    """Scan matrix with software debouncing and send states."""
    raw = _scan_matrix()
    now = time.ticks_ms()
    changed = False
    for i, val in enumerate(raw):
        if val != _last_raw[i]:
            _last_raw[i] = val
            _last_change[i] = now
        elif time.ticks_diff(now, _last_change[i]) >= DEBOUNCE_MS:
            if _state[i] != _last_raw[i]:
                _state[i] = _last_raw[i]
                changed = True
    if changed:
        uart.write(bytes(_state))
        if keyboard:
            for pressed, code in zip(_state, KEY_CODES):
                if pressed:
                    keyboard.send(code)
