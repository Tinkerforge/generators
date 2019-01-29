use std::{error::Error, io, thread};
use tinkerforge::ip_connection::{EnumerateResponse, EnumerationType, IpConnection};

const HOST: &str = "localhost";
const PORT: u16 = 4223;

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
    let ipcon = IpConnection::new(); // Create IP connection

    ipcon.connect((HOST, PORT)).recv()??; // Connect to brickd

    let receiver = ipcon.get_enumerate_callback_receiver();

    // Spawn thread to react to enumerate callback messages.
    // This thread must not be terminated or joined,
    // as it will end when the IP connection (and the receiver's sender) is dropped.
    thread::spawn(move || {
        for response in receiver {
            print_enumerate_response(&response);
        }
    });

    // Trigger Enumerate
    ipcon.enumerate();

    println!("Press enter to exit.");
    let mut _input = String::new();
    io::stdin().read_line(&mut _input)?;
    ipcon.disconnect();
    Ok(())
}
