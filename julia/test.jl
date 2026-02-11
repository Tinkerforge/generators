using Tinkerforge
ipcon = IPConnection("localhost", 4223)
connect(ipcon)
lcd = BrickletLCD20x4("BL1", ipcon)
backlight_off(lcd)