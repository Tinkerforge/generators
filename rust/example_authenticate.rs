use std::{error::Error, io, thread};
use tinkerforge::ip_connection::{ConnectReason, EnumerateResponse, EnumerationType, IpConnection, IpConnectionRequestSender};

const HOST: &str = "localhost";
const PORT: u16 = 4223;
const SECRET: &str = "My Authentication Secret!";

fn authenticate(reason: ConnectReason, request_sender: &mut IpConnectionRequestSender) {
    match reason {
        ConnectReason::Request => println!("Connected by request"),
        ConnectReason::AutoReconnect => println!("Auto-Reconnected"),
    }

    // Authenticate first...
    match request_sender.authenticate(SECRET) {
        Ok(rx) => {
            if let Ok(_) = rx.recv() {
                println!("Authentication succeded");

                //Reenable auto reconnect mechanism, as described below.
                request_sender.set_auto_reconnect(true);

                // ...then trigger enumerate
                request_sender.enumerate();
            } else {
                println!("Authentication request sent, but got no response. Maybe your secret is wrong?")
            }
        }
        Err(e) => println!("Could not authenticate: {}", e),
    }
}

fn print_enumerate_response(response: &EnumerateResponse) {
    println!("UID:               {}", response.uid);
    println!("Enumeration Type:  {:?}", response.enumeration_type);

    if response.enumeration_type == EnumerationType::Disconnected {
        println!("");
        return;
    }

    println!("Connected UID:     {}", response.connected_uid);
    println!("Position:          {}", response.position);
    println!("Hardware Version:  {}.{}.{}", response.hardware_version[0], response.hardware_version[1], response.hardware_version[2]);
    println!("Firmware Version:  {}.{}.{}", response.firmware_version[0], response.firmware_version[1], response.firmware_version[2]);
    println!("Device Identifier: {}", response.device_identifier);
    println!("");
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut ipcon = IpConnection::new(); // Create IP connection

    // Disable auto reconnect mechanism, in case we have the wrong secret. If the authentication is successful, reenable it.
    ipcon.set_auto_reconnect(false);
    
    // Get Connect Receiver
    let connect_receiver = ipcon.get_connect_receiver();

    // Spawn thread to react to connect events. This thread must not be terminated or joined,
    // as it will end when the IP connection (and the receiver's sender) is dropped.
    let mut request_sender = ipcon.get_request_sender();
    thread::spawn(move || {
        for reason in connect_receiver {
            authenticate(reason, &mut request_sender)
        }
    });

    // Get Enumerate Receiver
    let enumerate_receiver = ipcon.get_enumerate_receiver();

    // Spawn thread to react to enumerate events. This thread must not be terminated or joined,
    // as it will end when the IP connection (and the receiver's sender) is dropped.
    thread::spawn(move || {
        for response in enumerate_receiver {
            print_enumerate_response(&response);
        }
    });

    ipcon.connect((HOST, PORT)).recv()??; // Connect to brickd

    println!("Press enter to exit.");
    let mut _input = String::new();
    io::stdin().read_line(&mut _input)?;
    ipcon.disconnect();
    Ok(())
}
