//! A wrapper for [`Receiver`](std::sync::mpsc::Receiver), which converts received byte vectors to structured data.
use std::{
    error::Error,
    marker::PhantomData,
    sync::mpsc::*,
    time::{Duration, Instant},
};

use crate::byte_converter::FromByteSlice;

/// Error type for interactions with Tinkerforge bricks or bricklets.
#[derive(Debug, Copy, Clone)]
pub enum BrickletError {
    /// A parameter was invalid or had an unexpected length
    InvalidParameter,
    /// The brick or bricklet does not support the requested function.
    FunctionNotSupported,
    /// Currently unused
    UnknownError,
    /// The request can not be fulfulled, as there is currently no connection to a brick daemon.
    NotConnected,
    /// The request was sent, but response expected is disabled, so no response can be received. This is not an error.
    SuccessButResponseExpectedIsDisabled,
}

impl From<u8> for BrickletError {
    fn from(byte: u8) -> BrickletError {
        match byte {
            1 => BrickletError::InvalidParameter,
            2 => BrickletError::FunctionNotSupported,
            _ => BrickletError::UnknownError,
        }
    }
}

impl std::fmt::Display for BrickletError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for BrickletError {
    fn description(&self) -> &str {
        match self {
            BrickletError::InvalidParameter => "A parameter was invalid or had an unexpected length.",
            BrickletError::FunctionNotSupported => "The brick or bricklet does not support the requested function.",
            BrickletError::UnknownError => "UnknownError, Currently unused",
            BrickletError::NotConnected => "The request can not be fulfulled, as there is currently no connection to a brick daemon.",
            BrickletError::SuccessButResponseExpectedIsDisabled =>
                "The request was sent, but response expected is disabled, so no response can be received. This is not an error.",
        }
    }
}

/// A wrapper for [`Receiver`], which converts received byte vectors to structured data.
///
/// This receiver wraps a [`Receiver`] receiving raw bytes. Calling [`recv`] or [`try_recv`]
/// will call equivalent methods on the wrapped [`Receiver`] and then convert the received bytes
/// to a instance of `T`.
///
/// ### Note
///
/// Calling [`recv`] will not block indefinitely. Instead the timeout passed to the [`new`](#method.new) method is used for
/// a call of [`recv_timeout`](std::sync::mpsc::Receiver::recv_timeout)
///
/// # Type parameters
///
/// * `T` - Type which is created from received byte vectors. Must implement [`FromByteSlice`](crate::byte_converter::FromByteSlice)
///
/// # Errors
///
/// Returned errors are equivalent to those returned from methods of a [`Receiver`]. Additionally errors
/// raised by the brick or bricklet, such as `InvalidParameter`, `FunctionNotSupported` and `UnknownError`
/// will be returned. If the received response can not be interpreted as the result type `T`, a `MalformedPacket`
/// error is raised.
/// ### Note
/// If the device is configured to send no response for a result-less setter, the Error `SuccessButResponseExpectedIsDisabled`
/// will be returned. This indicates, that the request was sent to the device, but no further guarantees can be made.
///
/// [`Receiver`]: std::sync::mpsc::Receiver
/// [`recv`]: #method.recv
/// [`try_recv`]: #method.try_recv
pub struct ConvertingReceiver<T: FromByteSlice> {
    receiver: Receiver<Result<Vec<u8>, BrickletError>>,
    sent_time: Instant,
    timeout: Duration,
    phantom: PhantomData<T>,
}

/// Error type which is returned if a ConvertingReceiver::recv call fails.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum BrickletRecvTimeoutError {
    /// The queue was disconnected. This usually happens if the ip connection is destroyed.
    QueueDisconnected,
    /// The request could not be responded to before the timeout was reached.
    QueueTimeout,
    /// A parameter was invalid or had an unexpected length.
    InvalidParameter,
    /// The brick or bricklet does not support the requested function.
    FunctionNotSupported,
    /// Currently unused
    UnknownError,
    /// The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?
    MalformedPacket,
    /// The request can not be fulfulled, as there is currently no connection to a brick daemon.
    NotConnected,
    /// The request was sent, but response expected is disabled, so no response can be received. This is not an error.
    SuccessButResponseExpectedIsDisabled,
}

impl std::fmt::Display for BrickletRecvTimeoutError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for BrickletRecvTimeoutError {
    fn description(&self) -> &str {
        match self {
            BrickletRecvTimeoutError::QueueDisconnected =>
                "The queue was disconnected. This usually happens if the ip connection is destroyed.",
            BrickletRecvTimeoutError::QueueTimeout => "The request could not be responded to before the timeout was reached.",
            BrickletRecvTimeoutError::InvalidParameter => "A parameter was invalid or had an unexpected length.",
            BrickletRecvTimeoutError::FunctionNotSupported => "The brick or bricklet does not support the requested function.",
            BrickletRecvTimeoutError::UnknownError => "UnknownError, Currently unused",
            BrickletRecvTimeoutError::MalformedPacket =>
                "The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?",
            BrickletRecvTimeoutError::NotConnected =>
                "The request can not be fulfulled, as there is currently no connection to a brick daemon.",
            BrickletRecvTimeoutError::SuccessButResponseExpectedIsDisabled =>
                "The request was sent, but response expected is disabled, so no response can be received. This is not an error.",
        }
    }
}

/// Error type which is returned if a [`try_recv`](crate::converting_receiver::ConvertingReceiver::try_recv) call fails.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum BrickletTryRecvError {
    /// The queue was disconnected. This usually happens if the ip connection is destroyed.
    QueueDisconnected,
    /// There are currently no responses available.
    QueueEmpty,
    /// A parameter was invalid or had an unexpected length.
    InvalidParameter,
    /// The brick or bricklet does not support the requested function.
    FunctionNotSupported,
    /// Currently unused
    UnknownError,
    /// The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?
    MalformedPacket,
    /// The request can not be fulfulled, as there is currently no connection to a brick daemon.
    NotConnected,
    /// The request was sent, but response expected is disabled, so no response can be received. This is not an error.
    SuccessButResponseExpectedIsDisabled,
}

impl std::fmt::Display for BrickletTryRecvError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for BrickletTryRecvError {
    fn description(&self) -> &str {
        match self {
            BrickletTryRecvError::QueueDisconnected =>
                "The queue was disconnected. This usually happens if the ip connection is destroyed.",
            BrickletTryRecvError::QueueEmpty => "There are currently no responses available.",
            BrickletTryRecvError::InvalidParameter => "A parameter was invalid or had an unexpected length.",
            BrickletTryRecvError::FunctionNotSupported => "The brick or bricklet does not support the requested function.",
            BrickletTryRecvError::UnknownError => "UnknownError, Currently unused",
            BrickletTryRecvError::MalformedPacket =>
                "The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?",
            BrickletTryRecvError::NotConnected =>
                "The request can not be fulfulled, as there is currently no connection to a brick daemon.",
            BrickletTryRecvError::SuccessButResponseExpectedIsDisabled =>
                "The request was sent, but response expected is disabled, so no response can be received. This is not an error.",
        }
    }
}

impl<T: FromByteSlice> ConvertingReceiver<T> {
    /// Creates a new converting receiver which wraps the given [`Receiver`](std::sync::mpsc::Receiver). [`recv`](#method.recv) calls will time out after the given timeout.
    pub fn new(receiver: Receiver<Result<Vec<u8>, BrickletError>>, timeout: Duration) -> ConvertingReceiver<T> {
        ConvertingReceiver { receiver, sent_time: Instant::now(), timeout, phantom: PhantomData }
    }

    /// Attempts to return a pending value on this receiver without blocking. This method behaves like [`try_recv`](std::sync::mpsc::Receiver::try_recv).
    ///
    /// # Errors
    ///
    /// Returns an error on the following conditions:
    /// * There is no connection to a brick daemon.
    /// * The brick or bricklet returns an error.
    /// * The queue was disconnected or currently empty.
    /// * Response expected was disabled for a result-less setter. This is not an error.
    pub fn try_recv(&self) -> Result<T, BrickletTryRecvError> {
        let recv_result = self.receiver.try_recv();
        match recv_result {
            Ok(Ok(bytes)) =>
                if T::bytes_expected() == bytes.len() {
                    Ok(T::from_le_byte_slice(&bytes))
                } else {
                    Err(BrickletTryRecvError::MalformedPacket)
                },
            Ok(Err(BrickletError::InvalidParameter)) => Err(BrickletTryRecvError::InvalidParameter),
            Ok(Err(BrickletError::FunctionNotSupported)) => Err(BrickletTryRecvError::FunctionNotSupported),
            Ok(Err(BrickletError::UnknownError)) => Err(BrickletTryRecvError::UnknownError),
            Ok(Err(BrickletError::NotConnected)) => Err(BrickletTryRecvError::NotConnected),
            Ok(Err(BrickletError::SuccessButResponseExpectedIsDisabled)) => Err(BrickletTryRecvError::SuccessButResponseExpectedIsDisabled),
            Err(TryRecvError::Disconnected) => Err(BrickletTryRecvError::QueueDisconnected),
            Err(TryRecvError::Empty) => Err(BrickletTryRecvError::QueueEmpty),
        }
    }

    /// Attempts to wait for a value on this receiver, returning an error if the corresponding channel has hung up, or if it waits more than timeout.
    /// This method behaves like [`recv_timeout`](std::sync::mpsc::Receiver::recv_timeout).
    ///
    /// # Errors
    ///
    /// Returns an error on one of the following conditions:
    /// * There is no connection to a brick daemon.
    /// * The brick or bricklet returns an error.
    /// * The queue was disconnected.
    /// * Response expected was disabled for a result-less setter. This is not an error.
    /// * Blocked longer than the configured time out.
    pub fn recv(&self) -> Result<T, BrickletRecvTimeoutError> {
        let recv_result = self.receiver.recv_timeout(self.sent_time + self.timeout - Instant::now());
        match recv_result {
            Ok(Ok(bytes)) =>
                if T::bytes_expected() == bytes.len() {
                    Ok(T::from_le_byte_slice(&bytes))
                } else {
                    Err(BrickletRecvTimeoutError::MalformedPacket)
                },
            Ok(Err(BrickletError::InvalidParameter)) => Err(BrickletRecvTimeoutError::InvalidParameter),
            Ok(Err(BrickletError::FunctionNotSupported)) => Err(BrickletRecvTimeoutError::FunctionNotSupported),
            Ok(Err(BrickletError::UnknownError)) => Err(BrickletRecvTimeoutError::UnknownError),
            Ok(Err(BrickletError::NotConnected)) => Err(BrickletRecvTimeoutError::NotConnected),
            Ok(Err(BrickletError::SuccessButResponseExpectedIsDisabled)) =>
                Err(BrickletRecvTimeoutError::SuccessButResponseExpectedIsDisabled),
            Err(RecvTimeoutError::Disconnected) => Err(BrickletRecvTimeoutError::QueueDisconnected),
            Err(RecvTimeoutError::Timeout) => Err(BrickletRecvTimeoutError::QueueTimeout),
        }
    }
    /*
        pub fn recv_timeout(&self, timeout: Duration) -> Result<T, BrickletRecvTimeoutError> {
            let recv_result = self.receiver.recv_timeout(timeout);
            match recv_result {
                Ok(Ok(bytes))                 => if T::bytes_expected() == bytes.len() 
                                                    {Ok(T::from_le_byte_slice(bytes))}
                                                 else 
                                                    {Err(BrickletRecvTimeoutError::MalformedPacket)},
                Ok(Err(BrickletError::InvalidParameter))     => Err(BrickletRecvTimeoutError::InvalidParameter),
                Ok(Err(BrickletError::FunctionNotSupported)) => Err(BrickletRecvTimeoutError::FunctionNotSupported),
                Ok(Err(BrickletError::UnknownError))         => Err(BrickletRecvTimeoutError::UnknownError),
                Ok(Err(BrickletError::NotConnected))         => Err(BrickletRecvTimeoutError::NotConnected),
                Err(RecvTimeoutError::Disconnected)             => Err(BrickletRecvTimeoutError::QueueDisconnected),
                Err(RecvTimeoutError::Timeout)                  => Err(BrickletRecvTimeoutError::QueueTimeout),
            }        
        }
    */
    /* uncomment if https://github.com/rust-lang/rust/issues/46316 has landed
        pub fn recv_deadline(&self, deadline: Instant) -> Result<T, BrickletRecvTimeoutError> {
            let recv_result = self.receiver.recv_deadline(deadline);
            match recv_result {
                Ok(Ok(bytes))                 => Ok(T::from_le_byte_slice(bytes)),
                Ok(Err(InvalidParameter))     => Err(BrickletRecvTimeoutError::InvalidParameter),
                Ok(Err(FunctionNotSupported)) => Err(BrickletRecvTimeoutError::FunctionNotSupported),
                Ok(Err(UnknownError))         => Err(BrickletRecvTimeoutError::UnknownError),
                Err(Disconnected)             => Err(BrickletRecvTimeoutError::QueueDisconnected),
                Err(Timeout)                  => Err(BrickletRecvTimeoutError::QueueTimeout),
            }        
        }
    */
    pub fn iter(&self) -> Iter<T> { Iter { rx: self } }

    pub fn try_iter(&self) -> TryIter<T> { TryIter { rx: self } }
}

pub struct Iter<'a, T: 'a + FromByteSlice> {
    rx: &'a ConvertingReceiver<T>,
}

pub struct TryIter<'a, T: 'a + FromByteSlice> {
    rx: &'a ConvertingReceiver<T>,
}

pub struct IntoIter<T: FromByteSlice> {
    rx: ConvertingReceiver<T>,
}

impl<'a, T: FromByteSlice> Iterator for Iter<'a, T> {
    type Item = T;

    fn next(&mut self) -> Option<T> { self.rx.recv().ok() }
}

impl<'a, T: FromByteSlice> Iterator for TryIter<'a, T> {
    type Item = T;

    fn next(&mut self) -> Option<T> { self.rx.try_recv().ok() }
}

impl<'a, T: FromByteSlice> IntoIterator for &'a ConvertingReceiver<T> {
    type Item = T;
    type IntoIter = Iter<'a, T>;

    fn into_iter(self) -> Iter<'a, T> { self.iter() }
}

impl<T: FromByteSlice> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<T> { self.rx.recv().ok() }
}

impl<T: FromByteSlice> IntoIterator for ConvertingReceiver<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;

    fn into_iter(self) -> IntoIter<T> { IntoIter { rx: self } }
}
