package main

import (
	"fmt"
	"github.com/Tinkerforge/go-api-bindings/ipconnection"
)

const ADDR string = "localhost:4223"
const SECRET string = "My Authentication Secret!"

func main() {
	ipcon := ipconnection.New()
	defer ipcon.Close()

	// Disable auto reconnect mechanism, in case we have the wrong secret. If the authentication is successful, reenable it.
	ipcon.SetAutoReconnect(false)

	ipcon.RegisterConnectCallback(func(reason ipconnection.ConnectReason) {
		if reason == ipconnection.ConnectReasonRequest {
			fmt.Println("Connected by request")
		} else if reason == ipconnection.ConnectReasonAutoReconnect {
			fmt.Println("Auto-Reconnected")
		}

		// Authenticate first...
		err := ipcon.Authenticate(SECRET)
		if err != nil {
			fmt.Println("Could not authenticate:", err)
			return
		}

		fmt.Println("Authentication succeded")
		ipcon.SetAutoReconnect(true) // ...reenable auto reconnect mechanism, as described above,
		ipcon.Enumerate()            // then trigger enumerate.
	})

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

	ipcon.Connect(ADDR) // Connect to brickd.
	defer ipcon.Disconnect()

	fmt.Println("Press enter to exit.")
	fmt.Scanln()
}
