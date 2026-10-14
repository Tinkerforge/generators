This ZIP contains the MicroPython bindings for all Tinkerforge Bricks and
Bricklets. The bindings are designed for MicroPython on ESP32 and other
MicroPython-capable boards.

The ZIP file for the bindings is structured as follows:

 source/ -- source code of the bindings
 examples/ -- examples for every supported Brick and Bricklet
 stubs/ -- .pyi type stubs for IDE code completion

The source/ folder contains the ip_connection.py and all device bindings as
flat Python modules. To use the bindings, copy ip_connection.py and the device
bindings you need to your MicroPython board.

You can copy files to your board using tools such as:
 - mpremote (recommended): mpremote cp source/ip_connection.py :
 - Thonny IDE: Use the file browser to upload files
 - ampy: ampy --port /dev/ttyUSB0 put source/ip_connection.py

For WiFi-capable boards (e.g. ESP32), connect to your network first:

  import network
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect("YOUR_SSID", "YOUR_PASSWORD")

If you want to use authentication (ipcon.authenticate()), the hmac module is
required. Most MicroPython builds do not include it by default. Install it
using MicroPython's package manager (requires network connection):

  import mip
  mip.install("hmac")

Because MicroPython does not support threads, you need to call
ipcon.dispatch_callbacks(seconds) periodically if you want to receive
callbacks. The recommended dispatch time is 0. This will just dispatch all
pending callbacks without waiting for further callbacks.

To reduce file size on your board, you can compile .py files to .mpy bytecode
using mpy-cross. Make sure the mpy-cross version matches your MicroPython
firmware version.

See the documentation for details:

 pip install mpy-cross==1.23.0  # adjust version to match your firmware
 mpy-cross source/bricklet_temperature_v2.py

The stubs/ folder contains .pyi type stub files for IDE code completion and
type checking (e.g. VS Code with Pylance). Add the stubs/ folder to your IDE's
analysis paths. These files are not needed on the board.

Documentation for the API can be found at:

 https://www.tinkerforge.com/en/doc/Software/API_Bindings_MicroPython.html
