package main

import (
	"fmt"
	"github.com/tinkerforge/go-api-bindings/ipconnection"
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
		ipcon.SetAutoReconnect(true) //...reenable auto reconnect mechanism, as described below,
		ipcon.Enumerate()            // then trigger enumerate.
	})

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

	ipcon.Connect(ADDR) // Connect to brickd.
	defer ipcon.Disconnect()

	fmt.Println("Press enter to exit.")
	fmt.Scanln()
}
