use std::{error::Error, io, thread};
use tinkerforge::ipconnection::{IpConnection, EnumerationType, EnumerateAnswer};

const HOST: &str = "127.0.0.1";
const PORT: u16 = 4223;

fn print_enumerate_answer(answer: &EnumerateAnswer) {
    println!("UID:               {}", answer.uid);
    println!("Enumeration Type:  {:?}", answer.enumeration_type);

    if answer.enumeration_type == EnumerationType::Disconnected {
        println!("");
        return;
    }

    println!("Connected UID:     {}", answer.connected_uid);
    println!("Position:          {}", answer.position);
    println!(
        "Hardware Version:  {}.{}.{}",
        answer.hardware_version[0], answer.hardware_version[1], answer.hardware_version[2]
    );
    println!(
        "Firmware Version:  {}.{}.{}",
        answer.firmware_version[0], answer.firmware_version[1], answer.firmware_version[2]
    );
    println!("Device Identifier: {}", answer.device_identifier);
    println!("");
}

fn main() -> Result<(), Box<dyn Error>> {
    let ipc = IpConnection::new(); // Create IP connection

    ipc.connect(HOST, PORT).recv()??; // Connect to brickd

    // Get Enumerate Listener
    let listener = ipc.get_enumerate_event_listener();

    // Spawn thread to react to enumerate events. This thread must not be terminated or joined,
    // as it will end when the IP connection (and the listener's sender) is dropped.
    thread::spawn(move || {
        for answer in listener {
            print_enumerate_answer(&answer);
        }
    });

    // Trigger Enumerate
    ipc.enumerate();

    println!("Press enter to exit.");
    let mut _input = String::new();
    io::stdin().read_line(&mut _input)?;
    ipc.disconnect();
    Ok(())
}
