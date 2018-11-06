//! The IP Connection manages the communication between the API bindings and the Brick Daemon or a WIFI/Ethernet Extension.
use std::{
    collections::HashMap,
    error::Error,
    io::{Read, Write},
    net::{IpAddr, Shutdown, SocketAddr, TcpStream},
    str::{self, FromStr},
    sync::{
        atomic::{AtomicBool, AtomicUsize, Ordering},
        mpsc::{Receiver, Sender, *},
        Arc,
    },
    thread::{self, JoinHandle},
    time::Duration,
};

use crate::{byte_converter::*, converting_callback_receiver::*, converting_receiver::*};

use hmac::{Hmac, Mac};
use rand::{self, FromEntropy, Rng};
use sha1::Sha1;

/// The IP Connection manages the communication between the API bindings and the Brick Daemon or a WIFI/Ethernet Extension.
/// Before Bricks and Bricklets can be controlled using their API an IP Connection has to be created and its TCP/IP connection has to be established.
#[derive(Debug)]
pub struct IpConnection {
    pub(crate) req: IpConRequestSender,
    //pub(crate) socket_thread_tx: Sender<SocketThreadRequest>,
    socket_thread: Option<JoinHandle<()>>,
}

#[derive(Debug, Clone)]
pub struct IpConRequestSender {
    pub(crate) socket_thread_tx: Sender<SocketThreadRequest>,
    connection_state: Arc<AtomicUsize>,
    auto_reconnect_enabled: Arc<AtomicBool>,
    current_timeout_ms: Arc<AtomicUsize>,
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Hash)]
pub(crate) struct PacketHeader {
    uid: u32,
    length: u8,
    function_id: u8,
    sequence_number: u8,
    response_expected: bool,
    error_code: u8,
}

impl PacketHeader {
    pub(crate) fn with_payload(uid: u32, function_id: u8, sequence_number: u8, response_expected: bool, payload_len: u8) -> PacketHeader {
        PacketHeader { uid, length: PacketHeader::SIZE as u8 + payload_len, function_id, sequence_number, response_expected, error_code: 0 }
    }

    pub(crate) const SIZE: usize = 8;
}

impl FromByteSlice for PacketHeader {
    fn from_le_bytes(bytes: &[u8]) -> PacketHeader {
        PacketHeader {
            uid: u32::from_le_bytes(bytes),
            length: bytes[4],
            function_id: bytes[5],
            sequence_number: (bytes[6] & 0xf0) >> 4,
            response_expected: (bytes[6] & 0x08) != 0,
            error_code: (bytes[7] & 0xc0) >> 6,
        }
    }

    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for PacketHeader {
    fn to_le_bytes(header: PacketHeader) -> Vec<u8> {
        let mut result = vec![0u8; 8];
        result[0..4].copy_from_slice(&u32::to_le_bytes(header.uid));
        result[4] = header.length;
        result[5] = header.function_id;
        result[6] = header.sequence_number << 4 | (header.response_expected as u8) << 3;
        result[7] = header.error_code << 6;
        result
    }
}

const MAX_PACKET_SIZE: usize = PacketHeader::SIZE + 64 + 8; //header + payload + optional data

#[allow(clippy::needless_pass_by_value)] //All parameters are moved into the thread closure anyway.
fn socket_read_thread_fn(mut tcp_stream: TcpStream, response_tx: Sender<SocketThreadRequest>, session_id: u64) {
    const READ_BUFFER_SIZE: usize = MAX_PACKET_SIZE * 100;
    let mut read_buffer = vec![0; READ_BUFFER_SIZE]; //keep buffer for 100 packets
    let mut read_buffer_level = 0;
    let mut packet_buffer = Vec::with_capacity(MAX_PACKET_SIZE);
    let mut packet_buffer_pending_bytes: usize = 0;
    //tcp_stream.set_read_timeout(Some(Duration::new(0,10_000_000)));
    //tcp_stream.set_nonblocking(true);
    loop {
        //only read if the buffer can fit a packet of max size
        if READ_BUFFER_SIZE - read_buffer_level > MAX_PACKET_SIZE {
            match tcp_stream.read(&mut read_buffer[read_buffer_level..READ_BUFFER_SIZE]) {
                Ok(0) => {
                    //Socket was closed
                    response_tx
                        .send(SocketThreadRequest::SocketWasClosed(session_id, true))
                        .expect("Socket read thread was disconnected from socket thread queue. This is a bug in the rust bindings.");
                    break;
                }
                Ok(bytes_read) => read_buffer_level += bytes_read,
                Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock || e.kind() == std::io::ErrorKind::TimedOut => {}
                Err(_e) => {
                    //TODO: check for non-socket-related errors
                    response_tx
                        .send(SocketThreadRequest::SocketWasClosed(session_id, false))
                        .expect("Socket read thread was disconnected from socket thread queue. This is a bug in the rust bindings.");
                    break;
                }
            }
        }

        loop {
            //Don't have a complete header yet
            if packet_buffer.is_empty() && read_buffer_level < PacketHeader::SIZE {
                break;
            }

            //Read header
            if packet_buffer.is_empty() {
                read_into_packet_buffer(&mut read_buffer, &mut packet_buffer, PacketHeader::SIZE, &mut read_buffer_level);
                let header = PacketHeader::from_le_bytes(&packet_buffer);
                //if header.sequence_number != 0 {
                //    println!("Read header for uid {}, fid {}, seq_num {}", header.uid, header.function_id, header.sequence_number);
                // }
                packet_buffer_pending_bytes = header.length as usize - PacketHeader::SIZE;
            }

            //Read payload
            if packet_buffer_pending_bytes > 0 && read_buffer_level > 0 {
                let to_read = std::cmp::min(packet_buffer_pending_bytes, read_buffer_level);
                read_into_packet_buffer(&mut read_buffer, &mut packet_buffer, to_read, &mut read_buffer_level);
                packet_buffer_pending_bytes -= to_read;
            }

            //Packet complete
            if packet_buffer_pending_bytes == 0 {
                let header = PacketHeader::from_le_bytes(&packet_buffer);

                response_tx
                    .send(SocketThreadRequest::Response(header, packet_buffer[PacketHeader::SIZE..header.length as usize].to_vec()))
                    .expect("Socket read thread was disconnected from socket thread queue. This is a bug in the rust bindings.");
                packet_buffer.clear();
            } else {
                break;
            }
        }
    }
}

/// Type of enumeration of a device.
#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
pub enum EnumerationType {
    /// Device is available (enumeration triggered by user: [`Enumerate`](crate::ipconnection::IpConnection::enumerate())).
    /// This enumeration type can occur multiple times for the same device.
    Available,
    /// Device is newly connected (automatically send by Brick after establishing a communication connection).
    /// This indicates that the device has potentially lost its previous configuration and needs to be reconfigured.
    Connected,
    /// Device is disconnected (only possible for USB connection). In this case only uid and enumerationType are valid.
    Disconnected,
    /// Device returned an unknown enumeration type.
    Unknown,
}

impl From<u8> for EnumerationType {
    fn from(byte: u8) -> EnumerationType {
        match byte {
            0 => EnumerationType::Available,
            1 => EnumerationType::Connected,
            2 => EnumerationType::Disconnected,
            _ => EnumerationType::Unknown,
        }
    }
}

/// Devices send `EnumerateAnswer`s when they are connected, disconnected or when an enumeration was
/// triggered by the user using the [`Enumerate`](crate::ipconnection::IpConnection::enumerate) method.
#[derive(Clone, Debug)]
pub struct EnumerateAnswer {
    /// The UID of the device.
    pub uid: String,
    /// UID where the device is connected to.
    /// For a Bricklet this will be a UID of the Brick where it is connected to.
    /// For a Brick it will be the UID of the bottom Master Brick in the stack.
    /// For the bottom Master Brick in a stack this will be "0".
    /// With this information it is possible to reconstruct the complete network topology.
    pub connected_uid: String,
    /// For Bricks: '0' - '8' (position in stack). For Bricklets: 'a' - 'd' (position on Brick).
    pub position: char,
    /// Major, minor and release number for hardware version.
    pub hardware_version: [u8; 3],
    /// Major, minor and release number for firmware version.
    pub firmware_version: [u8; 3],
    /// A number that represents the device.
    /// The device identifier numbers can be found TODO LINK here. There are also constants for these numbers named following this pattern:
    ///
    /// <device-class>.DEVICE_IDENTIFIER
    ///
    /// For example: MasterBrick.DEVICE_IDENTIFIER or AmbientLightBricklet.DEVICE_IDENTIFIER.
    pub device_identifier: u16,
    /// Type of enumeration. See [`EnumerationType`](crate::ipconnection::EnumerationType)
    pub enumeration_type: EnumerationType,
}

impl FromByteSlice for EnumerateAnswer {
    fn from_le_bytes(bytes: &[u8]) -> EnumerateAnswer {
        EnumerateAnswer {
            uid: str::from_utf8(&bytes[0..8])
                .expect("Could not convert to string. This is a bug in the rust bindings.")
                .replace("\u{0}", ""),
            connected_uid: str::from_utf8(&bytes[8..16])
                .expect("Could not convert to string. This is a bug in the rust bindings.")
                .replace("\u{0}", ""),
            position: bytes[16] as char,
            hardware_version: [bytes[17], bytes[18], bytes[19]],
            firmware_version: [bytes[20], bytes[21], bytes[22]],
            device_identifier: u16::from_le_bytes(&bytes[23..25]),
            enumeration_type: EnumerationType::from(bytes[25]),
        }
    }

    fn bytes_expected() -> usize { 26 }
}

#[derive(Debug, Clone)]
pub(crate) enum Request {
    Set { uid: u32, function_id: u8, payload: Vec<u8>, response_sender: Option<Sender<Result<Vec<u8>, BrickletError>>> },
    Get { uid: u32, function_id: u8, payload: Vec<u8>, response_sender: Sender<Result<Vec<u8>, BrickletError>> },
    RegisterCallback { uid: u32, function_id: u8, response_sender: Sender<Vec<u8>> },
    RegisterConnectCallback(Sender<ConnectReason>),
    RegisterDisconnectCallback(Sender<DisconnectReason>),
    RegisterEnumerateCallback(Sender<Vec<u8>>),
}

impl Request {
    pub(crate) fn get_header(&self, sequence_number: u8) -> PacketHeader {
        match self {
            Request::Set { uid, function_id, payload, response_sender } =>
                PacketHeader::with_payload(*uid, *function_id, sequence_number, response_sender.is_some(), payload.len() as u8),
            Request::Get { uid, function_id, payload, .. } =>
                PacketHeader::with_payload(*uid, *function_id, sequence_number, true, payload.len() as u8),
            Request::RegisterCallback { .. } =>
                unreachable!("Can not create header for callback registration. This is a bug in the rust bindings."),
            Request::RegisterConnectCallback(_) =>
                unreachable!("Can not create header for callback registration. This is a bug in the rust bindings."),
            Request::RegisterDisconnectCallback(_) =>
                unreachable!("Can not create header for callback registration. This is a bug in the rust bindings."),
            Request::RegisterEnumerateCallback(_) =>
                unreachable!("Can not create header for callback registration. This is a bug in the rust bindings."),
        }
    }
}

fn read_into_packet_buffer(read_buffer: &mut Vec<u8>, packet_buffer: &mut Vec<u8>, bytes_to_read: usize, read_buffer_level: &mut usize) {
    //packet_buffer.copy_from_slice(&read_buffer[0..bytes_to_read]);
    packet_buffer.extend(read_buffer.drain(0..bytes_to_read));
    //for i in 0..bytes_to_read {
    //    packet_buffer.push(read_buffer[i]);
    //}
    read_buffer.extend_from_slice(&vec![0u8; bytes_to_read]);
    *read_buffer_level -= bytes_to_read;
}

fn cancel_request(request: Request) {
    let response_sender_opt = match request {
        Request::RegisterCallback { .. } => unreachable!("Can not cancel callback registration. This is a bug in the rust bindings."),
        Request::RegisterConnectCallback(_) => unreachable!("Can not cancel callback registration. This is a bug in the rust bindings."),
        Request::RegisterDisconnectCallback(_) => unreachable!("Can not cancel callback registration. This is a bug in the rust bindings."),
        Request::RegisterEnumerateCallback(_) => unreachable!("Can not cancel callback registration. This is a bug in the rust bindings."),
        Request::Set { response_sender, .. } => response_sender,
        Request::Get { response_sender, .. } => Some(response_sender),
    };
    if let Some(response_sender) = response_sender_opt {
        let _ = response_sender.send(Err(BrickletError::NotConnected));
    }
}

fn register_callback(
    uid: u32,
    function_id: u8,
    response_sender: Sender<Vec<u8>>,
    registered_callbacks: &mut HashMap<(u32, u8), Vec<Sender<Vec<u8>>>>,
) {
    let key = (uid, function_id);
    let val = response_sender;

    registered_callbacks.entry(key).or_default().push(val);
}

/// This enum specifies the reason of a successful connection.
/// It is generated from the [Connect event listener](`crate::ipconnection::IpConnection::get_connect_event_listener)
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum ConnectReason {
    /// Connection established after request from user.
    Request,
    /// Connection after auto-reconnect.
    AutoReconnect,
}

/// This enum specifies the reason of a connections termination.
/// It is generated from the [Disconnect event listener](`crate::ipconnection::IpConnection::get_disconnect_event_listener)
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum DisconnectReason {
    /// Disconnect was requested by user.
    Request,
    /// Disconnect because of an unresolvable error.
    Error,
    /// Disconnect initiated by Brick Daemon or WIFI/Ethernet Extension.
    Shutdown,
}

fn is_socket_really_connected(stream: &mut TcpStream) -> Result<bool, std::io::Error> {
    stream.set_nonblocking(true)?;
    let mut buf = [0u8; 1];
    let result = match stream.peek(&mut buf) {
        Ok(0) => Ok(false),
        Ok(_) => Ok(true),
        Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => Ok(true),
        Err(_) => Ok(false),
    };
    stream.set_nonblocking(false)?;
    result
}

fn create_socket(addr: IpAddr, port: u16) -> std::io::Result<(TcpStream, TcpStream)> {
    let mut tcp_stream = TcpStream::connect_timeout(&SocketAddr::new(addr, port), Duration::new(30, 0))?;

    tcp_stream.set_read_timeout(Some(Duration::new(5, 0)))?;
    tcp_stream.set_write_timeout(Some(Duration::new(5, 0)))?;
    tcp_stream.set_nodelay(true)?;

    if !is_socket_really_connected(&mut tcp_stream)? {
        return Err(std::io::Error::new(std::io::ErrorKind::ConnectionReset, "was not really connected"));
    };

    let stream_copy = tcp_stream.try_clone()?;
    Ok((tcp_stream, stream_copy))
}

#[allow(clippy::needless_pass_by_value)] //All parameters are moved into the thread closure anyway.
fn socket_thread_fn(
    work_queue_rx: Receiver<SocketThreadRequest>,
    work_queue_tx: Sender<SocketThreadRequest>,
    connection_state: Arc<AtomicUsize>,
) {
    let mut registered_callbacks = HashMap::<(u32, u8), Vec<Sender<Vec<u8>>>>::new();
    let mut connect_callbacks = Vec::new();
    let mut disconnect_callbacks = Vec::new();
    let mut enumerate_callbacks = Vec::new();
    let mut session_id = 0u64;
    let mut timeout = Duration::new(2, 500_000_000);
    let mut auto_reconnect_enabled = true;
    let mut auto_reconnect_allowed = true;
    let mut is_auto_reconnect = false;

    'thread: loop {
        connection_state.store(0, Ordering::SeqCst);
        let mut seq_num: u8 = 1;
        let mut send_buffer = Vec::with_capacity(MAX_PACKET_SIZE);
        let mut response_queues = HashMap::<(u32, u8, u8), Vec<Sender<Result<Vec<u8>, BrickletError>>>>::new();
        let mut disconnect_reason = DisconnectReason::Error;

        //wait for ip address and port
        let (addr, port, connection_request_done_tx) = 'wait_for_connect: loop {
            match work_queue_rx.recv() {
                Ok(SocketThreadRequest::Request(Request::RegisterCallback { uid, function_id, response_sender }, sent_tx)) => {
                    register_callback(uid, function_id, response_sender, &mut registered_callbacks);
                    sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings.")
                }
                Ok(SocketThreadRequest::Request(Request::RegisterConnectCallback(response_sender), sent_tx)) => {
                    connect_callbacks.push(response_sender);
                    sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings.")
                }
                Ok(SocketThreadRequest::Request(Request::RegisterDisconnectCallback(response_sender), sent_tx)) => {
                    disconnect_callbacks.push(response_sender);
                    sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings.")
                }
                Ok(SocketThreadRequest::Request(Request::RegisterEnumerateCallback(response_sender), sent_tx)) => {
                    enumerate_callbacks.push(response_sender);
                    sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings.")
                }
                Ok(SocketThreadRequest::Request(req, sent_tx)) => {
                    cancel_request(req);
                    sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings.")
                }
                Ok(SocketThreadRequest::Terminate) => break 'thread,
                Ok(SocketThreadRequest::Connect(addr, port, tx)) => {
                    is_auto_reconnect = false;
                    break 'wait_for_connect (addr, port, Some(tx));
                }
                Ok(SocketThreadRequest::Disconnect(tx)) =>
                    if !is_auto_reconnect {
                        let _ = tx.send(Err(DisconnectErrorNotConnected));
                    } else {
                        auto_reconnect_allowed = false;
                    },
                Ok(SocketThreadRequest::SocketWasClosed(_, _)) => {} //Ignore: There is no socket that could be closed yet.
                Ok(SocketThreadRequest::Response(_, _)) => {}        //ignore network data, the thread creating it is not running yet
                Ok(SocketThreadRequest::SetTimeout(t)) => timeout = t,
                Ok(SocketThreadRequest::TriggerAutoReconnect(addr, port)) => {
                    if !auto_reconnect_allowed {
                        continue 'wait_for_connect;
                    }
                    is_auto_reconnect = true;
                    break 'wait_for_connect (addr, port, None);
                }
                Ok(SocketThreadRequest::SetAutoReconnect(ar_enabled)) => auto_reconnect_enabled = ar_enabled,
                Err(_) => {
                    println!("Disconnected from Queue.");
                    break 'thread;
                }
            }
        };

        //connect to received or last ip and port
        session_id += 1;
        connection_state.store(2, Ordering::SeqCst);

        let (mut tcp_stream, stream_copy) = match create_socket(addr, port) {
            Ok((a, b)) => (a, b),
            Err(e) => {
                if let Some(tx) = connection_request_done_tx {
                    let _ = tx.send(Err(ConnectError::IoError(e)));
                }
                work_queue_tx
                    .send(SocketThreadRequest::TriggerAutoReconnect(addr, port))
                    .expect("Socket thread was still running, but it's work queue was destroyed. This is a bug in the rust bindings.");
                continue 'thread;
            }
        };

        let socket_read_thread = {
            let local_tx_copy = work_queue_tx.clone();
            thread::spawn(move || {
                socket_read_thread_fn(stream_copy, local_tx_copy, session_id);
            })
        };

        //we have a connection, notify requester, connection state and all registered event listeners
        if let Some(tx) = connection_request_done_tx {
            let _ = tx.send(Ok(()));
        }

        connection_state.store(1, Ordering::SeqCst);
        {
            let connect_reason = if is_auto_reconnect { ConnectReason::AutoReconnect } else { ConnectReason::Request };
            connect_callbacks.retain(|queue| queue.send(connect_reason).is_ok());
        }

        'connection: loop {
            match work_queue_rx.recv_timeout(Duration::new(5, 0)) {
                Ok(SocketThreadRequest::Request(request, sent_tx)) => {
                    let mut notify_sender = true;
                    match request {
                        Request::RegisterCallback { uid, function_id, response_sender } =>
                            register_callback(uid, function_id, response_sender, &mut registered_callbacks),
                        Request::RegisterConnectCallback(response_sender) => connect_callbacks.push(response_sender),
                        Request::RegisterDisconnectCallback(response_sender) => disconnect_callbacks.push(response_sender),
                        Request::RegisterEnumerateCallback(response_sender) => enumerate_callbacks.push(response_sender),
                        req => {
                            if let Request::Set { uid: 0, function_id: 128, response_sender: None, .. } = req {
                                //FIXME: when response_sender is none, the sender can not be notified anyway.
                                notify_sender = false;
                            }
                            let header = req.get_header(seq_num);
                            let sent_seq_num = seq_num;
                            seq_num += 1;
                            if seq_num == 16 {
                                seq_num = 1;
                            }
                            send_buffer.clear();
                            send_buffer.extend_from_slice(&PacketHeader::to_le_bytes(header));

                            let (uid, function_id, payload, response_sender_opt) = match req {
                                Request::Set { uid, function_id, payload, response_sender } => (uid, function_id, payload, response_sender),
                                Request::Get { uid, function_id, payload, response_sender } =>
                                    (uid, function_id, payload, Some(response_sender)),
                                Request::RegisterCallback { .. } =>
                                    unreachable!("Can not extract params from callback registration. This is a bug in the rust bindings."),
                                Request::RegisterConnectCallback(_) =>
                                    unreachable!("Can not extract params from callback registration. This is a bug in the rust bindings."),
                                Request::RegisterDisconnectCallback(_) =>
                                    unreachable!("Can not extract params from callback registration. This is a bug in the rust bindings."),
                                Request::RegisterEnumerateCallback(_) =>
                                    unreachable!("Can not extract params from callback registration. This is a bug in the rust bindings."),
                            };

                            if response_sender_opt.is_some() {
                                let key = (uid, function_id, sent_seq_num);
                                let val = response_sender_opt.unwrap();
                                response_queues.entry(key).or_default().push(val);
                            }
                            send_buffer.extend_from_slice(&payload);
                            if tcp_stream.write_all(&send_buffer).is_err() {
                                if auto_reconnect_enabled {
                                    let _ = work_queue_tx.send(SocketThreadRequest::TriggerAutoReconnect(addr, port));
                                }
                                break 'connection;
                            }
                        }
                    }
                    if notify_sender {
                        sent_tx.send(timeout).expect("Request sent queue was dropped. This is a bug in the rust bindings."); //Notify caller that the request is sent
                    }
                }
                Ok(SocketThreadRequest::Terminate) => {
                    break 'thread;
                }
                Ok(SocketThreadRequest::Connect(_, _, tx)) => {
                    let _ = tx.send(Err(ConnectError::AlreadyConnected));
                }
                Ok(SocketThreadRequest::TriggerAutoReconnect(_, _)) => {}
                Ok(SocketThreadRequest::Disconnect(tx)) => {
                    let _ = tcp_stream.shutdown(Shutdown::Both); //we are closing the connection anyway, so ignore errors here
                    let _ = tx.send(Ok(()));
                    disconnect_reason = DisconnectReason::Request;
                    break 'connection;
                }
                Ok(SocketThreadRequest::SocketWasClosed(sid, was_shutdown)) if sid == session_id => {
                    if auto_reconnect_enabled {
                        let _ = work_queue_tx.send(SocketThreadRequest::TriggerAutoReconnect(addr, port));
                    }
                    disconnect_reason = if was_shutdown { DisconnectReason::Shutdown } else { DisconnectReason::Error };
                    break 'connection;
                }
                Ok(SocketThreadRequest::SocketWasClosed(_, _)) => {
                    /* The socket read thread sends this message also when we closed the session by request. Ignore it here as it is obsolete.*/
                }
                Ok(SocketThreadRequest::Response(header, payload)) => {
                    if header.sequence_number == 0 {
                        if header.function_id == 253 {
                            enumerate_callbacks.retain(|queue| queue.send(payload.clone()).is_ok());
                        } else {
                            //callback
                            let key = (header.uid, header.function_id);
                            if let Some(queue_vec) = registered_callbacks.get_mut(&key) {
                                queue_vec.retain(|queue| queue.send(payload.clone()).is_ok())
                            }
                        }
                    } else {
                        //response for getter or setter
                        let key = (header.uid, header.function_id, header.sequence_number);
                        let mut should_remove_val = false;
                        if let Some(queue_vec) = response_queues.get_mut(&key) {
                            let queue = queue_vec.remove(0);
                            if header.error_code != 0 {
                                let _ = queue.send(Err(BrickletError::from(header.error_code)));
                            } else {
                                let _ = queue.send(Ok(payload));
                            }
                            should_remove_val = queue_vec.is_empty();
                        };
                        if should_remove_val && response_queues.contains_key(&key) {
                            response_queues.remove(&key);
                        }
                    }
                }
                Ok(SocketThreadRequest::SetTimeout(t)) => timeout = t,
                Ok(SocketThreadRequest::SetAutoReconnect(ar_enabled)) => auto_reconnect_enabled = ar_enabled,
                Err(RecvTimeoutError::Timeout) => {
                    let (_tx, _rx) = channel();
                    let _ = work_queue_tx.send(SocketThreadRequest::Request(
                        Request::Set { uid: 0, function_id: 128, payload: vec![], response_sender: None },
                        _tx,
                    ));
                }
                Err(_) => {
                    println!("Disconnected from Queue. This is a bug in the rust bindings.");
                    break 'thread;
                }
            }
        }
        socket_read_thread.join().expect("The socket read thread paniced or could not be joined. This is a bug in the rust bindings.");
        disconnect_callbacks.retain(|queue| queue.send(disconnect_reason).is_ok());
    }
    connection_state.store(0, Ordering::SeqCst);
    disconnect_callbacks.retain(|queue| queue.send(DisconnectReason::Request).is_ok());
}

/// This error is raised if a [`connect`](crate::ipconnection::IpConnection::connect) call fails.
#[derive(Debug)]
pub enum ConnectError {
    /// Could not parse the given ip address.
    CouldNotParseIpAddress(String),
    /// An [`IoError`](std::io::Error) was raised while creating the socket.
    IoError(std::io::Error),
    /// Already connected. Disconnect before connecting somewhere else.
    AlreadyConnected,
    /// Could not create tcp socket (Failed to set no delay flag).
    CouldNotSetNoDelayFlag,
    /// Could not create tcp socket (Failed to clone tcp stream).
    CouldNotCloneTcpStream,
    /// Connect succeeded, but the socket was disconnected immediately.
    /// This usually happens if the first auto-reconnect succeeds immediately, but should be handled within the reconnect logic.    
    NotReallyConnected,
}

impl std::error::Error for ConnectError {
    /*fn description(&self) -> &str {  }*/
}

impl std::fmt::Display for ConnectError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        if let ConnectError::IoError(e) = self {
            e.fmt(f)
        } else {
            write!(
                f,
                "{}",
                match self {
                    ConnectError::CouldNotParseIpAddress(addr) => format!("Could not parse ip address: {}", addr),
                    ConnectError::IoError(_e) => unreachable!("Could not query io error description. This is a bug in the rust bindings."),
                    ConnectError::AlreadyConnected => "Already connected. Disconnect before connecting somewhere else.".to_owned(),
                    ConnectError::CouldNotSetNoDelayFlag =>
                        "Could not create tcp socket (Failed to set no delay flag). This is a bug in the rust bindings.".to_owned(),
                    ConnectError::CouldNotCloneTcpStream =>
                        "Could not create tcp socket (Failed to clone tcp stream). This is a bug in the rust bindings.".to_owned(),
                    ConnectError::NotReallyConnected =>
                        "Connect succeeded, but the socket was disconnected immediately. This is a bug in the rust bindings.".to_owned(),
                }
            )
        }
    }
}

/// This error is raised if a disconnect request failed, because there was no connection to disconnect
#[derive(Debug)]
pub struct DisconnectErrorNotConnected;

pub(crate) enum SocketThreadRequest {
    Request(Request, Sender<Duration>),
    Connect(IpAddr, u16, Sender<Result<(), ConnectError>>),
    Disconnect(Sender<Result<(), DisconnectErrorNotConnected>>),
    SocketWasClosed(u64, bool),
    Response(PacketHeader, Vec<u8>),
    SetTimeout(Duration),
    TriggerAutoReconnect(IpAddr, u16),
    SetAutoReconnect(bool),
    Terminate,
}

/// This enum is returned from the [`get_connection_state`](crate::ipconnection::IpConnection::get_connection_state) method.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ConnectionState {
    /// No connection is established.
    Disconnected,
    /// A connection to the Brick Daemon or the WIFI/Ethernet Extension is established.
    Connected,
    /// IP Connection is currently trying to connect.
    Pending,
}

impl From<usize> for ConnectionState {
    fn from(num: usize) -> ConnectionState {
        match num {
            1 => ConnectionState::Connected,
            2 => ConnectionState::Pending,
            _ => ConnectionState::Disconnected,
        }
    }
}

struct ServerNonce([u8; 4]);

impl FromByteSlice for ServerNonce {
    fn from_le_bytes(bytes: &[u8]) -> ServerNonce { ServerNonce([bytes[0], bytes[1], bytes[2], bytes[3]]) }

    fn bytes_expected() -> usize { 4 }
}

/// This error is returned if the remote's server nonce could not be queried.
#[derive(Debug, Copy, Clone)]
pub struct AuthenticateError;

impl std::fmt::Display for AuthenticateError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for AuthenticateError {
    fn description(&self) -> &str { "Could not get server nonce" }
}

impl Default for IpConnection {
    fn default() -> Self {
        let (socket_thread_tx, socket_thread_rx) = channel();
        let copy = socket_thread_tx.clone();
        let atomic = Arc::new(AtomicUsize::new(0));
        IpConnection {
            req: IpConRequestSender {
                socket_thread_tx,
                connection_state: Arc::clone(&atomic),
                auto_reconnect_enabled: Arc::new(AtomicBool::new(false)),
                current_timeout_ms: Arc::new(AtomicUsize::new(2500)),
            },
            socket_thread: Some(thread::spawn(move || {
                socket_thread_fn(socket_thread_rx, copy, Arc::clone(&atomic));
            })),
        }
    }
}

impl Drop for IpConnection {
    fn drop(&mut self) {
        let _ = self.req.socket_thread_tx.send(SocketThreadRequest::Terminate);
        if let Some(thread) = self.socket_thread.take() {
            thread.join().expect("Could not join socket thread. This is a bug in the rust bindings.");
        }
    }
}

impl IpConRequestSender {
    /// Creates a TCP/IP connection to the given `host` and `port`. The host and port can refer to a Brick Daemon or to a WIFI/Ethernet Extension.
    ///
    /// Devices can only be controlled when the connection was established successfully.
    ///
    /// Blocks until the connection is established and throws an exception if there is no Brick Daemon or WIFI/Ethernet Extension listening at the given host and port.
    pub fn connect(&self, host: &str, port: u16) -> Receiver<Result<(), ConnectError>> {
        let (tx, rx) = channel();
        let addr = match IpAddr::from_str(host) {
            Err(std::net::AddrParseError { .. }) => {
                let _ = tx.send(Err(ConnectError::CouldNotParseIpAddress(host.to_owned())));
                return rx;
            }
            Ok(address) => address,
        };

        self.socket_thread_tx
            .send(SocketThreadRequest::Connect(addr, port, tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        rx
    }

    /// Disconnects the TCP/IP connection from the Brick Daemon or the WIFI/Ethernet Extension.
    pub fn disconnect(&self) -> Receiver<Result<(), DisconnectErrorNotConnected>> {
        let (tx, rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Disconnect(tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        rx
    }

    /// This event is triggered whenever the IP Connection got connected to a Brick Daemon or to a WIFI/Ethernet Extension.
    pub fn get_connect_event_listener(&self) -> Receiver<ConnectReason> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(Request::RegisterConnectCallback(tx), sent_tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        rx
    }

    /// This event is triggered whenever the IP Connection got disconnected from a Brick Daemon or to a WIFI/Ethernet Extension.
    pub fn get_disconnect_event_listener(&self) -> Receiver<DisconnectReason> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(Request::RegisterDisconnectCallback(tx), sent_tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        rx
    }

    /// Returns the timeout as set by [`set_timeout`](crate::ipconnection::IpConnection::set_timeout)
    pub fn get_timeout(&self) -> Duration { Duration::from_millis(self.current_timeout_ms.load(Ordering::SeqCst) as u64) }

    /// Sets the timeout for getters and for setters for which the response expected flag is activated.
    ///
    /// Default timeout is 2,5s.
    pub fn set_timeout(&mut self, timeout: Duration) {
        self.socket_thread_tx
            .send(SocketThreadRequest::SetTimeout(timeout))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        let millis = (timeout.as_secs() as usize).saturating_mul(1000).saturating_add(timeout.subsec_nanos() as usize / 1_000_000);
        self.current_timeout_ms.store(millis, Ordering::SeqCst);
    }

    /// Queries the current connection state.
    pub fn get_connection_state(&self) -> ConnectionState { ConnectionState::from(self.connection_state.load(Ordering::SeqCst)) }

    /// Returns true if auto-reconnect is enabled, false otherwise.
    pub fn get_auto_reconnect(&self) -> bool { self.auto_reconnect_enabled.load(Ordering::SeqCst) }

    /// Enables or disables auto-reconnect. If auto-reconnect is enabled, the IP Connection will try to reconnect to
    /// the previously given host and port, if the currently existing connection is lost.
    /// Therefore, auto-reconnect only does something after a successful [`connect`](crate::ipconnection::IpConnection::connect) call.
    ///
    /// Default value is true.
    pub fn set_auto_reconnect(&mut self, auto_reconnect_enabled: bool) {
        self.socket_thread_tx
            .send(SocketThreadRequest::SetAutoReconnect(auto_reconnect_enabled))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        self.auto_reconnect_enabled.store(auto_reconnect_enabled, Ordering::SeqCst);
    }

    /// Broadcasts an enumerate request. All devices will respond with an enumerate event.
    pub fn enumerate(&self) {
        let (tx, rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(Request::Set { uid: 0, function_id: 254, payload: vec![], response_sender: None }, tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
    }

    /// This listener receives enumerate events, as described [here](crate::ipconnection::EnumerateAnswer).
    ///
    pub fn get_enumerate_event_listener(&self) -> ConvertingCallbackReceiver<EnumerateAnswer> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(Request::RegisterEnumerateCallback(tx), sent_tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        ConvertingCallbackReceiver::new(rx)
    }

    /// Performs an authentication handshake with the connected Brick Daemon or WIFI/Ethernet Extension.
    /// If the handshake succeeds the connection switches from non-authenticated to authenticated state
    /// and communication can continue as normal. If the handshake fails then the connection gets closed.
    /// Authentication can fail if the wrong secret was used or if authentication is not enabled at all
    /// on the Brick Daemon or the WIFI/Ethernet Extension.
    ///
    /// See the authentication tutorial for more information.
    ///
    /// New in version 2.1.0.
    pub fn authenticate(&self, secret: &str) -> Result<ConvertingReceiver<()>, AuthenticateError> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(Request::Get { uid: 1, function_id: 1, payload: vec![], response_sender: tx }, sent_tx))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        let timeout = sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        let recv = ConvertingReceiver::<ServerNonce>::new(rx, timeout);
        let server_nonce = match recv.recv() {
            Ok(nonce) => nonce,
            Err(_) => return Err(AuthenticateError),
        };

        let mut rng = rand::prng::ChaChaRng::from_entropy();
        let mut client_nonce = [0u8; 4];
        rng.fill(&mut client_nonce);

        let mut to_hash = [0u8; 8];
        //bytes::copy_memory(to_hash.mut_slice_to(4), )
        to_hash[0..4].copy_from_slice(&server_nonce.0);
        to_hash[4..=7].copy_from_slice(&client_nonce);

        let mut mac = Hmac::<Sha1>::new_varkey(secret.as_bytes()).expect("");
        mac.input(&to_hash);
        let result = mac.result();

        let (auth_sent_tx, auth_sent_rx) = channel();
        let mut payload = [0u8; 24];
        payload[0..4].copy_from_slice(&client_nonce);
        let hashed = result.code();
        payload[4..24].copy_from_slice(&hashed);
        let (auth_tx, auth_rx) = channel();
        self.socket_thread_tx
            .send(SocketThreadRequest::Request(
                Request::Set { uid: 1, function_id: 2, payload: payload.to_vec(), response_sender: Some(auth_tx) },
                auth_sent_tx,
            ))
            .expect("Socket thread has crashed. This is a bug in the rust bindings.");
        let timeout = auth_sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        Ok(ConvertingReceiver::new(auth_rx, timeout))
    }
}

impl IpConnection {
    /// Creates an IP Connection object that can be used to enumerate the available devices. It is also required for the constructor of Bricks and Bricklets.
    pub fn new() -> IpConnection { Default::default() }

    /// Returns a new request sender, to be used in other threads.
    pub fn get_request_sender(&self) -> IpConRequestSender { self.req.clone() }

    /// Creates a TCP/IP connection to the given `host` and `port`. The host and port can refer to a Brick Daemon or to a WIFI/Ethernet Extension.
    ///
    /// Devices can only be controlled when the connection was established successfully.
    ///
    /// Blocks until the connection is established and throws an exception if there is no Brick Daemon or WIFI/Ethernet Extension listening at the given host and port.
    pub fn connect(&self, host: &str, port: u16) -> Receiver<Result<(), ConnectError>> { self.req.connect(host, port) }

    /// Disconnects the TCP/IP connection from the Brick Daemon or the WIFI/Ethernet Extension.
    pub fn disconnect(&self) -> Receiver<Result<(), DisconnectErrorNotConnected>> { self.req.disconnect() }

    /// This event is triggered whenever the IP Connection got connected to a Brick Daemon or to a WIFI/Ethernet Extension.
    pub fn get_connect_event_listener(&self) -> Receiver<ConnectReason> { self.req.get_connect_event_listener() }

    /// This event is triggered whenever the IP Connection got disconnected from a Brick Daemon or to a WIFI/Ethernet Extension.
    pub fn get_disconnect_event_listener(&self) -> Receiver<DisconnectReason> { self.req.get_disconnect_event_listener() }

    /// Returns the timeout as set by [`set_timeout`](crate::ipconnection::IpConnection::set_timeout)
    pub fn get_timeout(&self) -> Duration { self.req.get_timeout() }

    /// Sets the timeout for getters and for setters for which the response expected flag is activated.
    ///
    /// Default timeout is 2,5s.
    pub fn set_timeout(&mut self, timeout: Duration) { self.req.set_timeout(timeout) }

    /// Queries the current connection state.
    pub fn get_connection_state(&self) -> ConnectionState { self.req.get_connection_state() }

    /// Returns true if auto-reconnect is enabled, false otherwise.
    pub fn get_auto_reconnect(&self) -> bool { self.req.get_auto_reconnect() }

    /// Enables or disables auto-reconnect. If auto-reconnect is enabled, the IP Connection will try to reconnect to
    /// the previously given host and port, if the currently existing connection is lost.
    /// Therefore, auto-reconnect only does something after a successful [`connect`](crate::ipconnection::IpConnection::connect) call.
    ///
    /// Default value is true.
    pub fn set_auto_reconnect(&mut self, auto_reconnect_enabled: bool) { self.req.set_auto_reconnect(auto_reconnect_enabled) }

    /// Broadcasts an enumerate request. All devices will respond with an enumerate event.
    pub fn enumerate(&self) { self.req.enumerate() }

    /// This listener receives enumerate events, as described [here](crate::ipconnection::EnumerateAnswer).
    ///
    pub fn get_enumerate_event_listener(&self) -> ConvertingCallbackReceiver<EnumerateAnswer> { self.req.get_enumerate_event_listener() }

    /// Performs an authentication handshake with the connected Brick Daemon or WIFI/Ethernet Extension.
    /// If the handshake succeeds the connection switches from non-authenticated to authenticated state
    /// and communication can continue as normal. If the handshake fails then the connection gets closed.
    /// Authentication can fail if the wrong secret was used or if authentication is not enabled at all
    /// on the Brick Daemon or the WIFI/Ethernet Extension.
    ///
    /// See the authentication tutorial for more information.
    ///
    /// New in version 2.1.0.
    pub fn authenticate(&self, secret: &str) -> Result<ConvertingReceiver<()>, AuthenticateError> { self.req.authenticate(secret) }
}
