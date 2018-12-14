package main

import (
	"fmt"
	"tinkerforge/ipconnection"
)

const ADDR string = "localhost:4223"

func main() {
	ipcon := ipconnection.New()
	defer ipcon.Close()

	ipcon.Connect(ADDR) // Connect to brickd.
	defer ipcon.Disconnect()
	// Don't use device before ipcon is connected.

	ipcon.RegisterEnumerateCallback(func(response ipconnection.EnumerateResponse) {
		fmt.Printf("UID:               %s\n", response.UID)
		switch response.EnumerationType {
		case ipconnection.EnumerationTypeAvailable:
			fmt.Printf("Enumeration Type:  Available\n")
		case ipconnection.EnumerationTypeConnected:
			fmt.Printf("Enumeration Type:  Connected\n")
		case ipconnection.EnumerationTypeDisconnected:
			fmt.Printf("Enumeration Type:  Disconnected\n")
			return
		}

		fmt.Printf("Connected UID:     %s\n", response.ConnectedUID)
		fmt.Printf("Position:          %c\n", response.Position)
		fmt.Printf("Hardware Version:  %d.%d.%d\n", response.HardwareVersion[0], response.HardwareVersion[1], response.HardwareVersion[2])
		fmt.Printf("Firmware Version:  %d.%d.%d\n", response.FirmwareVersion[0], response.FirmwareVersion[1], response.FirmwareVersion[2])
		fmt.Printf("Device Identifier: %d\n", response.DeviceIdentifier)
		fmt.Println("")
	})
	ipcon.Enumerate()
	fmt.Println("Press enter to exit.")
	fmt.Scanln()
}
