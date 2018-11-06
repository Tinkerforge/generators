use std::{error::Error, io, thread};
use tinkerforge::ipconnection::{
    ConnectReason, EnumerateAnswer, EnumerationType, IpConRequestSender, IpConnection,
};

const HOST: &str = "127.0.0.1";
const PORT: u16 = 4223;
const SECRET: &str = "My Authentication Secret!";

fn authenticate(reason: ConnectReason, request_sender: &IpConRequestSender) {
    match reason {
        ConnectReason::Request => println!("Connected by request"),
        ConnectReason::AutoReconnect => println!("Auto-Reconnected"),
    }

    // Authenticate first...
    match request_sender.authenticate(SECRET) {
        Ok(rx) => {
            if let Ok(_) = rx.recv() {
                println!("Authentication succeded");

                // ...then trigger enumerate
                request_sender.enumerate();
            } else {
                println!(
                    "Authentication request sent, but got no response. Maybe your secret is wrong?"
                )
            }
        }
        Err(e) => println!("Could not authenticate: {}", e),
    }
}

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

    // Get Connect Listener
    let connect_listener = ipc.get_connect_event_listener();
    
    // Spawn thread to react to connect events. This thread must not be terminated or joined,
    // as it will end when the IP connection (and the listener's sender) is dropped.
    let request_sender = ipc.get_request_sender();
    thread::spawn(move || {
        for reason in connect_listener {
            authenticate(reason, &request_sender)
        }
    });

    // Get Enumerate Listener
    let enumerate_listener = ipc.get_enumerate_event_listener();

    // Spawn thread to react to enumerate events. This thread must not be terminated or joined,
    // as it will end when the IP connection (and the listener's sender) is dropped.
    thread::spawn(move || {
        for answer in enumerate_listener {
            print_enumerate_answer(&answer);
        }
    });

    ipc.connect(HOST, PORT).recv()??; // Connect to brickd

    println!("Press enter to exit.");
    let mut _input = String::new();
    io::stdin().read_line(&mut _input)?;
    ipc.disconnect();
    Ok(())
}
