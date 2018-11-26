//! Generic device functionality which is used by all bricks and bricklets.

use crate::{
    base58::*,
    byte_converter::FromByteSlice,
    converting_callback_receiver::ConvertingCallbackReceiver,
    converting_receiver::{BrickletError, BrickletRecvTimeoutError, ConvertingReceiver},
    ip_connection::{IpConnection, Request, SocketThreadRequest},
    low_level_traits::*,
};
use std::sync::{
    mpsc::{channel, Sender},
    Arc, Mutex,
};

#[derive(Debug, Copy, Clone, PartialEq)]
pub(crate) enum ResponseExpectedFlag {
    InvalidFunctionId,
    False,
    True,
    AlwaysTrue,
}

impl From<bool> for ResponseExpectedFlag {
    fn from(b: bool) -> Self {
        if b {
            ResponseExpectedFlag::True
        } else {
            ResponseExpectedFlag::False
        }
    }
}

#[derive(Clone)]
pub(crate) struct Device {
    pub api_version: [u16; 3],
    pub response_expected: [ResponseExpectedFlag; 256],
    pub internal_uid: u32,
    pub req_tx: Sender<SocketThreadRequest>,
    pub high_level_locks: Vec<Arc<Mutex<()>>>,
}

/// This error is returned if the response expected status was queried for an unknown function.
#[derive(Debug, Copy, Clone)]
pub struct GetResponseExpectedError(u8);

impl std::error::Error for GetResponseExpectedError {}

impl std::fmt::Display for GetResponseExpectedError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Can not get response expected: Invalid function id {}", self.0)
    }
}

/// This error is returned if the response expected status of a function could not be changed.
#[derive(Debug, Copy, Clone)]
pub enum SetResponseExpectedError {
    /// The function id was unknown. Maybe the wrong UID was used?
    InvalidFunctionId(u8),
    /// This function must always respond, as the response contains result data.
    IsAlwaysTrue(u8),
}

impl std::error::Error for SetResponseExpectedError {}

impl std::fmt::Display for SetResponseExpectedError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            SetResponseExpectedError::InvalidFunctionId(fid) => write!(f, "Can not set response expected: Invalid function id {}", fid),
            SetResponseExpectedError::IsAlwaysTrue(_fid) => write!(f, "Can not set response expected: function always responds."),
        }
    }
}

impl Device {
    pub(crate) fn new(api_version: [u16; 3], uid: &str, ip_connection: &IpConnection, high_level_function_count: u8) -> Device {
        Device {
            api_version,
            internal_uid: uid.base58_to_u32().unwrap(),
            req_tx: ip_connection.req.socket_thread_tx.clone(),
            response_expected: [ResponseExpectedFlag::InvalidFunctionId; 256],
            high_level_locks: vec![Arc::new(Mutex::new(())); high_level_function_count as usize],
        }
    }

    pub(crate) fn get_response_expected(&self, function_id: u8) -> Result<bool, GetResponseExpectedError> {
        match self.response_expected[function_id as usize] {
            ResponseExpectedFlag::False => Ok(false),
            ResponseExpectedFlag::True => Ok(true),
            ResponseExpectedFlag::AlwaysTrue => Ok(true),
            ResponseExpectedFlag::InvalidFunctionId => Err(GetResponseExpectedError(function_id)),
        }
    }

    pub(crate) fn set_response_expected(&mut self, function_id: u8, response_expected: bool) -> Result<(), SetResponseExpectedError> {
        if self.response_expected[function_id as usize] == ResponseExpectedFlag::AlwaysTrue {
            Err(SetResponseExpectedError::IsAlwaysTrue(function_id))
        } else if self.response_expected[function_id as usize] == ResponseExpectedFlag::InvalidFunctionId {
            Err(SetResponseExpectedError::InvalidFunctionId(function_id))
        } else {
            self.response_expected[function_id as usize] = ResponseExpectedFlag::from(response_expected);
            Ok(())
        }
    }

    pub(crate) fn set_response_expected_all(&mut self, response_expected: bool) {
        for resp_exp in self.response_expected.iter_mut() {
            if *resp_exp == ResponseExpectedFlag::True || *resp_exp == ResponseExpectedFlag::False {
                *resp_exp = ResponseExpectedFlag::from(response_expected);
            }
        }
    }

    pub(crate) fn set<T: FromByteSlice>(&self, function_id: u8, payload: Vec<u8>) -> ConvertingReceiver<T> {
        let (sent_tx, sent_rx) = channel();
        if self.response_expected[function_id as usize] == ResponseExpectedFlag::False {
            let (tx, rx) = channel();
            self.req_tx
                .send(SocketThreadRequest::Request(
                    Request::Set { uid: self.internal_uid, function_id, payload, response_sender: None },
                    sent_tx,
                ))
                .expect("The socket thread queue was disconnected from the ip connection. This is a bug in the rust bindings.");
            let timeout = sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
            let _ = tx.send(Err(BrickletError::SuccessButResponseExpectedIsDisabled));
            ConvertingReceiver::new(rx, timeout)
        } else {
            let (tx, rx) = channel();
            self.req_tx
                .send(SocketThreadRequest::Request(
                    Request::Set { uid: self.internal_uid, function_id, payload, response_sender: Some(tx) },
                    sent_tx,
                ))
                .expect("The socket thread queue was disconnected from the ip connection. This is a bug in the rust bindings.");
            let timeout = sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
            ConvertingReceiver::new(rx, timeout)
        }
    }

    pub(crate) fn get_callback_receiver<T: FromByteSlice>(&self, function_id: u8) -> ConvertingCallbackReceiver<T> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.req_tx
            .send(SocketThreadRequest::Request(
                Request::RegisterCallback { uid: self.internal_uid, function_id, response_sender: tx },
                sent_tx,
            ))
            .expect("The socket thread queue was disconnected from the ip connection. This is a bug in the rust bindings.");
        sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        ConvertingCallbackReceiver::new(rx)
    }

    pub(crate) fn get<T: FromByteSlice>(&self, function_id: u8, payload: Vec<u8>) -> ConvertingReceiver<T> {
        let (tx, rx) = channel();
        let (sent_tx, sent_rx) = channel();
        self.req_tx
            .send(SocketThreadRequest::Request(Request::Get { uid: self.internal_uid, function_id, payload, response_sender: tx }, sent_tx))
            .expect("The socket thread queue was disconnected from the ip connection. This is a bug in the rust bindings.");
        let timeout = sent_rx.recv().expect("The sent queue was dropped. This is a bug in the rust bindings.");
        ConvertingReceiver::new(rx, timeout)
    }

    pub(crate) fn set_high_level<
        PayloadT,
        OutputT,
        LlwT: LowLevelWrite<OutputT>,
        ClosureT: FnMut(usize, usize, &[PayloadT]) -> Result<LlwT, BrickletRecvTimeoutError>,
    >(
        &self,
        high_level_function_idx: u8,
        payload: &[PayloadT],
        max_payload_len: usize,
        chunk_len: usize,
        low_level_closure: &mut ClosureT,
    ) -> Result<(usize, OutputT), BrickletRecvTimeoutError> {
        if payload.len() > max_payload_len {
            return Err(BrickletRecvTimeoutError::InvalidParameter);
        }

        let length = payload.len();

        let mut chunk_offset = 0;
        {
            let _lock_guard = self.high_level_locks[high_level_function_idx as usize].lock().unwrap();
            if length == 0 {
                match low_level_closure(length, chunk_offset, &[]) {
                    Ok(low_level_result) => return Ok((low_level_result.ll_message_written(), low_level_result.get_result())),
                    Err(e) => return Err(e),
                }
            }
            let mut written_sum = 0;
            loop {
                match low_level_closure(length, chunk_offset, &payload[chunk_offset..std::cmp::min(chunk_offset + chunk_len, length)]) {
                    Ok(low_level_result) => {
                        let written = low_level_result.ll_message_written();
                        let output = low_level_result.get_result();
                        written_sum += written;
                        if written < chunk_len {
                            return Ok((written_sum, output));
                        }
                        chunk_offset += chunk_len;
                        if chunk_offset >= length {
                            return Ok((written_sum, output));
                        }
                    }
                    Err(e) => return Err(e),
                }
            }
        }
    }

    pub(crate) fn get_high_level<
        PayloadT: Default + Clone + Copy,
        OutputT,
        LlrT: LowLevelRead<PayloadT, OutputT>,
        ClosureT: FnMut() -> Result<LlrT, BrickletRecvTimeoutError>,
    >(
        &self,
        high_level_function_idx: u8,
        low_level_closure: &mut ClosureT,
    ) -> Result<(Vec<PayloadT>, OutputT), BrickletRecvTimeoutError> {
        let mut chunk_offset = 0;
        {
            let _lock_guard = self.high_level_locks[high_level_function_idx as usize].lock().unwrap();
            let mut result = low_level_closure()?;
            let mut out_of_sync = result.ll_message_chunk_offset() != 0;
            let message_length = result.ll_message_length();

            if !out_of_sync {
                let mut buf = vec![PayloadT::default(); message_length];
                let first_read_length = std::cmp::min(result.ll_message_chunk_data().len(), message_length - chunk_offset);
                buf[chunk_offset..chunk_offset + first_read_length].copy_from_slice(&result.ll_message_chunk_data()[0..first_read_length]);
                chunk_offset += first_read_length;
                while chunk_offset < message_length {
                    result = low_level_closure()?;
                    out_of_sync = result.ll_message_chunk_offset() != chunk_offset || result.ll_message_length() != message_length;
                    if out_of_sync {
                        break;
                    }

                    let read_length = std::cmp::min(result.ll_message_chunk_data().len(), message_length - chunk_offset);
                    buf[chunk_offset..chunk_offset + read_length].copy_from_slice(&result.ll_message_chunk_data()[0..read_length]);
                    chunk_offset += read_length;
                }
                if !out_of_sync {
                    return Ok((buf, result.get_result()));
                }
            }

            assert!(out_of_sync);
            while chunk_offset + result.ll_message_chunk_data().len() < message_length {
                result = low_level_closure()?;
            }
            Err(BrickletRecvTimeoutError::MalformedPacket)
        }
    }
}
