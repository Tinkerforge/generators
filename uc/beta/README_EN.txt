Tinkerforge C/C++ Bindings for Microcontrollers
===============================================

The C/C++ bindings for Microcontrollers allow you to control
Tinkerforge Co-Processor Bricklets from a C/C++ program
running on a Microcontroller.

Zip Contents
------------

 source/bindings/ - Implementation of the bindings
 source/demo/ - A demo program for a PTC 2.0 Bricklet and a LCD 128x64 Bricklet
 source/hal_arduino/ - HAL for Arduino boards (e.g. an Arduino Uno or a Teensy)
 source/hal_arduino_esp32/ - HAL for Arduino boards with an ESP32 (e.g. a NodeMCU)
 source/hal_linux/ - HAL for Linux systems with spidev support (e.g. a Raspberry Pi)

 source/Makefile - Makefile for the Linux variant of the demo program
 source/main.c - Linux variant of the demo program
 
 source/arduino.ino - Arduino variant of the demo program
 source/arduino_esp32.ino - Arduino ESP32 variant of the demo program

The bindings are nearly the same as the normal C/C++ bindings documented here:
https://www.tinkerforge.com/en/doc/Software/API_Bindings_C.html

However there are the following changes:
    - Only Co-Processor Bricklets (i.e. those with a 7 pole connector) are supported

    - All function, constant and type names are prefixed with tf_ or TF_. So the 
      function documented as ptc_v2_get_temperature is called tf_ptc_v2_get_temperature,
      the type PTCV2 is called TF_PTCV2, the constant PTC_V2_WIRE_MODE_2 is called
      TF_PTC_V2_WIRE_MODE_2

    - High level callbacks are not supported.
      "Normal" callbacks will only be delivered if you commmunicate periodically with the device.
      To receive callbacks for all devices with at least one registered handler, you can use
      int tf_hal_callback_tick(TF_HalContext *hal, uint32_t timeout_us);
      This function  blocks for the given time in microseconds and receives and delivers callbacks.
      This function can be called with a timeout of 0 to poll for one immediatly available callback.

      If the default round-robin scheduling is not useful, you can use the device specific functions
      with the folloing pattern:
      int tf_[device]_callback_tick(TF_[device] *[device], uint32_t timeout_us);
      These functions work the same way, but only on the passed device.

    - Callbacks always receive a pointer to the sending device as first parameter:
      The documented input value callback of the IO4 2.0 has the signature
      void callback(TF_IO4V2 *device, uint8_t channel, bool changed, bool value, void *user_data)
      instead of the documented
      void callback(uint8_t channel, bool changed, bool value, void *user_data)

    - Callbacks are registered with a specific function per callback. There is no
      [device]_register_callback function that receives a callback ID. Instead
      specific function such as
      void tf_io4_v2_register_input_value_callback(TF_IO4V2 *io4_v2, TF_IO4V2InputValueHandler handler, void *user_data);
      must be used. This also means, that you don't have to cast your callback handler to
      void (*)(void)
      and can rely on the compiler warnings if your handler signature is wrong.

      To deregister a callback, pass NULL (C) or nullptr (C++) as handler.

    - Calling device functions in a callback handler is not allowed.
    
    - There is no IP connection. Instead a HAL (Hardware Abstraction Layer) is required.
      The HAL wraps the platform specific SPI communication details. The bindings already
      contain HALs for the Raspberry Pi and Arduino Boards. For other
      platforms, a custom HAL must be implemented (see below)
      
    - The _create function of a bricklet requires passing a pointer to an (initialized) HAL
      instead of an IP connection.
      
    - The error codes are not the same as in the normal C/C++ bindings. All error codes are
      defined in the file bindings/errors.h or in the used HAL.
      const char* tf_strerror(int error_code)
      returns a description for the given error code.
      
Demo program
------------

A demo program for all yet supported platforms is contained in the zip file.
The folder source/demo contains the logic of the program, the hardware specific
part can be found in the source folder.

The demo program can be used with an Raspberry Pi (Zero) and a HAT (Zero) Brick or
with a custom circuit with an Arduino.

To use the program, you have to change the UIDs to those of your bricklets. The UIDs are
shown in the Brick Viewer. Also the bindings print a list of all found devices while
initializing.

The program for the Raspberry Pi can be compiled with make on the Pi itself, or
cross-compiled on another PC with 
make CROSS_COMPILE=arm-linux-gnueabihf-
For this to work, the arm-linux-gnueabihf-gcc (cross) compiler must be installed.

The Arduino programs can be compiled with the Arduino IDE. For ESP32 based systems
you have to install the package "esp32 by Espressif Systems" in the board manager.

Depending on your wiring, the port mapping in the used .ino file must be changed.

The Arduino IDE requires the following directory layout:
(append _esp32 if you use an ESP32 board)

arduino(_esp32)
├── arduino(_esp32).ino
└── src
    ├── bindings
    │   └── Content of the source/bindings folder
    ├── demo
    │   └── Content of the source/demo folder
    └── hal_arduino(_esp32)
        └── Content of the source/hal_arduino(_esp32) folder
        
Attention: Both demos implement a simplified error handling only.

Notes for implementing a custom HAL
-----------------------------------

If you want to use the bindings on another platform, you have to implement
a custom HAL. The HAL abstracts the platform specific way of communicating
over SPI.

The following steps are necessary to implement a custom HAL:

First define a TF_HalContext struct. It holds all data necessary for the SPI
communication. Typically an instance of TF_HalCommon, as well as a Pointer to
an array of port mapping information is stored here. The format of the port mapping
entries can be customized. See the port struct in hal_arduino_esp32.h and hal_linux.h
for examples.

Bricklets are identified by their UID as well as the port under that they are reachable.
A port typically maps to the chip select pin that must be toggled to transfer data over
SPI to the bricklet. Some HAL functions receive a port ID, this is normally an index
into the array of port information.

The next step after defining the TF_HalContext struct is implementing its initialization function,
that handles the following tasks:
    - Initialize the TF_HalCommon instance with tf_hal_common_init
    
    - Prepare the SPI communication
      When your initialization function returns, SPI communication must be possible to all attached devices.
      All chip select pins must be set to HIGH (e.g. disabled) See below for details about the SPI communication.
      
    - Call tf_hal_finish_init
      This is normally the last step in the initialization. SPI communication must be possible here.
      The function expects the number of usable ports as well as a timeout in micro seconds, for how long
      the bindungs should try to reach a device under one of the ports.
      tf_hal_finish_init then builds a list of reachable devices and stores it in the TF_HalCommon instance.
      
Finally all functions defined in bindings/hal_common.h between 
// BEGIN - To be implemented by the specific HAL
and
// END - To be implemented by the specific HAL
must be implemented.

    - int tf_hal_destroy(TF_HalContext *hal);
      Ends the SPI commmunication.
      Attention: The shutdown behaviour of the example HALs is currently untested.
    
    - int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable);
      Sets the chip select pin of the port with the given port_id.
      Depending on the platform, more work has to be done here. For example on
      an Arduino, begin/endTransaction must be called to make sure, that the SPI
      configuration is applied. The bindings make sure, that only one chip select
      pin is enabled at the same time.
    
    - int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, uint32_t length);
      Transmit length bytes of data from the write_buffer to the bricklet while receiving the same
      amount of bytes (as SPI is bi-directional) into the read_buffer. The buffers are always big enough
      to read/write length bytes.
    
    - uint32_t tf_hal_current_time_us(TF_HalContext *hal);
      Return the current time in microseconds. The time does not have to map to a "real" time,
      it only has to be monotonic (except overflows).

    - void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us);
      Block for the given time in microseconds.
    
    - TF_HalCommon *tf_hal_get_common(TF_HalContext *hal);
      Return the TF_HalCommon instance from the specific TF_HalContext.
    
    - char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id);
      Returns a port name (typically a letter from 'A' to 'Z') for the given port ID.
      This name will be patched into the result of get_identity() calls if a device
      is directly connected to the host.
    
    - void tf_hal_log_message(const char *msg);
      Log the given message. Depending on the platform you can use a serial console (Arduino) or
      the standard output (Linux). Writing the log to a file is also possible.
      Attention: This function may not assume that the HAL was initialized successfully, to be able
      to log errors that occurred while initializing the HAL.
    
    - const char* tf_hal_strerror(int rc);
      Returns an error description for the given error code. The bindings contain the function
      tf_strerror, that handles most error codes. If this function encounters unknown error codes, it calls
      tf_hal_strerror of the HAL, so error codes defined for the specific HAL must be handled here.
  
Details about the SPI communication
-----------------------------------

The communication over SPI uses Mode 3:
  - CPOL=1: Clock polarity is inverted: HIGH when inactive
  - CPHA=1: Clock phase is shifted: Data is read on falling edge
Data is transmitted MSB first, the default clock frequency is 1.4 MHz.
The logic level of all signals is 3.3V.

Due to a bug with the XMC microcontroller used by the Bricklets, they don't correctly
go into a floating state on the MISO signal. This results in interference when multiple
Bricklets are used on the same SPI bus. To be able to use multiple bricklets, a
tri-state buffer chip controlled by the chip select signal has to be used.
