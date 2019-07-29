package main

import (
	"fmt"

	"github.com/Tinkerforge/go-api-bindings/ipconnection"
)

const ADDR string = "localhost:4223"

func main() {
	ipcon := ipconnection.New()
	defer ipcon.Close()

	ipcon.Connect(ADDR) // Connect to brickd.
	defer ipcon.Disconnect()
	// Don't use device before ipcon is connected.

	ipcon.RegisterEnumerateCallback(func(uid string, connectedUID string, position rune, hardwareVersion [3]uint8, firmwareVersion [3]uint8, deviceIdentifier uint16, enumerationType ipconnection.EnumerationType) {
		fmt.Printf("UID:               %s\n", uid)
		switch enumerationType {
		case ipconnection.EnumerationTypeAvailable:
			fmt.Printf("Enumeration Type:  Available\n")
		case ipconnection.EnumerationTypeConnected:
			fmt.Printf("Enumeration Type:  Connected\n")
		case ipconnection.EnumerationTypeDisconnected:
			fmt.Printf("Enumeration Type:  Disconnected\n")
			return
		}

		fmt.Printf("Connected UID:     %s\n", connectedUID)
		fmt.Printf("Position:          %c\n", position)
		fmt.Printf("Hardware Version:  %d.%d.%d\n", hardwareVersion[0], hardwareVersion[1], hardwareVersion[2])
		fmt.Printf("Firmware Version:  %d.%d.%d\n", firmwareVersion[0], firmwareVersion[1], firmwareVersion[2])
		fmt.Printf("Device Identifier: %d\n", deviceIdentifier)
		fmt.Println("")
	})

	ipcon.Enumerate()
	fmt.Println("Press enter to exit.")
	fmt.Scanln()
}
