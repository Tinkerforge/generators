//! A wrapper for [`Receiver`](std::sync::mpsc::Receiver), which converts received byte vectors to structured data.
//! This variant of [`ConvertingReceiver`](crate::converting_receiver::ConvertingReceiver) is used for event listeners.

use crate::byte_converter::FromByteSlice;
use std::{
    error::Error,
    marker::PhantomData,
    sync::mpsc::{Receiver, *},
    time::Duration,
};

/// Error type which is returned if a [`recv_forever`](crate::converting_callback_receiver::ConvertingCallbackReceiver::recv_forever) call fails.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum CallbackRecvError {
    /// The queue was disconnected. This usually happens if the ip connection is destroyed.
    QueueDisconnected,
    /// The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?
    MalformedPacket,
}

impl std::fmt::Display for CallbackRecvError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for CallbackRecvError {
    fn description(&self) -> &str {
        match self {
            CallbackRecvError::QueueDisconnected => "The queue was disconnected. This usually happens if the ip connection is destroyed.",
            CallbackRecvError::MalformedPacket =>
                "The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?",
        }
    }
}

/// Error type which is returned if a [`recv_timeout`](crate::converting_callback_receiver::ConvertingCallbackReceiver::recv_timeout) call fails.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum CallbackRecvTimeoutError {
    /// The queue was disconnected. This usually happens if the ip connection is destroyed.
    QueueDisconnected,
    /// The request could not be answered before the timeout was reached.
    QueueTimeout,
    /// The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?
    MalformedPacket,
}

impl std::fmt::Display for CallbackRecvTimeoutError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for CallbackRecvTimeoutError {
    fn description(&self) -> &str {
        match self {
            CallbackRecvTimeoutError::QueueDisconnected =>
                "The queue was disconnected. This usually happens if the ip connection is destroyed.",
            CallbackRecvTimeoutError::QueueTimeout => "The request could not be answered before the timeout was reached.",
            CallbackRecvTimeoutError::MalformedPacket =>
                "The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?",
        }
    }
}

/// Error type which is returned if a [`try_recv`](crate::converting_callback_receiver::ConvertingCallbackReceiver::try_recv) call fails.
#[derive(Copy, Clone, Debug, PartialEq)]
pub enum CallbackTryRecvError {
    /// The queue was disconnected. This usually happens if the ip connection is destroyed.
    QueueDisconnected,
    /// There are currently no answers available.
    QueueEmpty,
    /// The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?
    MalformedPacket,
}

impl std::fmt::Display for CallbackTryRecvError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { write!(f, "{}", self.description()) }
}

impl std::error::Error for CallbackTryRecvError {
    fn description(&self) -> &str {
        match self {
            CallbackTryRecvError::QueueDisconnected =>
                "The queue was disconnected. This usually happens if the ip connection is destroyed.",
            CallbackTryRecvError::QueueEmpty => "There are currently no answers available.",
            CallbackTryRecvError::MalformedPacket =>
                "The received packet had an unexpected length. Maybe a function was called on a wrong brick or bricklet?",
        }
    }
}

/// A wrapper for [`Receiver`], which converts received byte vectors to structured data. This variant of
/// [`ConvertingReceiver`](crate::converting_receiver::ConvertingReceiver) is used for event listeners.
///
/// This receiver wraps a [`Receiver`] receiving raw bytes. Calling [`recv_forever`], [`recv_timeout`] or [`try_recv`]
/// will call equivalent methods on the wrapped [`Receiver`] and then convert the received bytes
/// to a instance of `T`.
///
///
/// # Type parameters
///
/// * `T` - Type which is created from received byte vectors. Must implement [`FromByteSlice`](crate::byte_converter::FromByteSlice)
///
/// # Errors
///
/// Returned errors are equivalent to those returned from methods of a [`Receiver`].
/// If the received answer can not be interpreted as the result type `T`, a `MalformedPacket`
/// error is raised.
///
/// [`Receiver`]: std::sync::mpsc::Receiver
/// [`recv_forever`]: #method.recv_forever
/// [`recv_timeout`]: #method.recv_timeout
/// [`try_recv`]: #method.try_recv
pub struct ConvertingCallbackReceiver<T: FromByteSlice> {
    receiver: Receiver<Vec<u8>>,
    phantom: PhantomData<T>,
}

impl<T: FromByteSlice> ConvertingCallbackReceiver<T> {
    /// Creates a new converting callback receiver which wraps the given [`Receiver`](std::sync::mpsc::Receiver).
    pub fn new(receiver: Receiver<Vec<u8>>) -> ConvertingCallbackReceiver<T> {
        ConvertingCallbackReceiver { receiver, phantom: PhantomData }
    }

    /// Attempts to return a pending value on this receiver without blocking. This method behaves like [`try_recv`](std::sync::mpsc::Receiver::try_recv).
    ///
    /// # Errors
    ///
    /// Returns an error if the queue was disconnected or currently empty, or if the received packet was malformed.
    pub fn try_recv(&self) -> Result<T, CallbackTryRecvError> {
        let recv_result = self.receiver.try_recv();
        match recv_result {
            Ok(bytes) =>
                if T::bytes_expected() == bytes.len() {
                    Ok(T::from_le_bytes(&bytes))
                } else {
                    Err(CallbackTryRecvError::MalformedPacket)
                },
            Err(TryRecvError::Disconnected) => Err(CallbackTryRecvError::QueueDisconnected),
            Err(TryRecvError::Empty) => Err(CallbackTryRecvError::QueueEmpty),
        }
    }

    /// Attempts to wait for a value on this receiver, returning an error if the corresponding channel has hung up. This method behaves like [`recv`](std::sync::mpsc::Receiver::recv).
    ///
    /// # Errors
    ///
    /// Returns an error if the queue was disconnected or currently empty, or if the received packet was malformed.
    pub fn recv_forever(&self) -> Result<T, CallbackRecvError> {
        let recv_result = self.receiver.recv();
        match recv_result {
            Ok(bytes) =>
                if T::bytes_expected() == bytes.len() {
                    Ok(T::from_le_bytes(&bytes))
                } else {
                    Err(CallbackRecvError::MalformedPacket)
                },
            Err(RecvError) => Err(CallbackRecvError::QueueDisconnected),
        }
    }

    /// Attempts to wait for a value on this receiver, returning an error if the corresponding channel has hung up, or if it waits more than timeout.
    /// This method behaves like [`recv_timeout`](std::sync::mpsc::Receiver::recv_timeout).
    ///
    /// # Errors
    ///
    /// Returns an error on one of the following conditions:
    /// * The queue was disconnected.
    /// * The received packet was malformed.
    /// * Blocked longer than the configured time out.
    pub fn recv_timeout(&self, timeout: Duration) -> Result<T, CallbackRecvTimeoutError> {
        let recv_result = self.receiver.recv_timeout(timeout);
        match recv_result {
            Ok(bytes) =>
                if T::bytes_expected() == bytes.len() {
                    Ok(T::from_le_bytes(&bytes))
                } else {
                    Err(CallbackRecvTimeoutError::MalformedPacket)
                },
            Err(RecvTimeoutError::Disconnected) => Err(CallbackRecvTimeoutError::QueueDisconnected),
            Err(RecvTimeoutError::Timeout) => Err(CallbackRecvTimeoutError::QueueTimeout),
        }
    }

    /* uncomment if https://github.com/rust-lang/rust/issues/46316 has landed
        pub fn recv_deadline(&self, deadline: Instant) -> Result<T, RecvTimeoutError> {
           let bytes = self.receiver.recv_deadline(deadline)?;
            Ok(T::from_le_bytes(bytes))        
        }
    */
    pub fn iter(&self) -> Iter<T> { Iter { rx: self } }

    pub fn try_iter(&self) -> TryIter<T> { TryIter { rx: self } }
}

pub struct Iter<'a, T: 'a + FromByteSlice> {
    rx: &'a ConvertingCallbackReceiver<T>,
}

pub struct TryIter<'a, T: 'a + FromByteSlice> {
    rx: &'a ConvertingCallbackReceiver<T>,
}

pub struct IntoIter<T: FromByteSlice> {
    rx: ConvertingCallbackReceiver<T>,
}

impl<'a, T: FromByteSlice> Iterator for Iter<'a, T> {
    type Item = T;

    fn next(&mut self) -> Option<T> { self.rx.recv_forever().ok() }
}

impl<'a, T: FromByteSlice> Iterator for TryIter<'a, T> {
    type Item = T;

    fn next(&mut self) -> Option<T> { self.rx.try_recv().ok() }
}

impl<'a, T: FromByteSlice> IntoIterator for &'a ConvertingCallbackReceiver<T> {
    type Item = T;
    type IntoIter = Iter<'a, T>;

    fn into_iter(self) -> Iter<'a, T> { self.iter() }
}

impl<T: FromByteSlice> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<T> { self.rx.recv_forever().ok() }
}

impl<T: FromByteSlice> IntoIterator for ConvertingCallbackReceiver<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;

    fn into_iter(self) -> IntoIter<T> { IntoIter { rx: self } }
}
