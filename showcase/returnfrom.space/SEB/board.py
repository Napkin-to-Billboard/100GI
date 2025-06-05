from machine import Pin, I2C, ADC, DAC, UART
import ssd1306

# Initialize I2C for SSD1306 display
i2c = I2C(0, scl=Pin(1), sda=Pin(2))
DISPLAY = ssd1306.SSD1306_I2C(128, 64, i2c)

# DAC output
try:
    dac = DAC(Pin(17))
except Exception:
    dac = None

# ADC input sampled at 8 kHz
adc = ADC(Pin(34))
SAMPLE_RATE = 8000

# UART input
uart = UART(1, baudrate=115200)

