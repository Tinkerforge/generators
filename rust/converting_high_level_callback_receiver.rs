//! A wrapper for [`Receiver`](std::sync::mpsc::Receiver), which converts received byte vectors to structured data.
//! This variant of [`ConvertingReceiver`](crate::converting_receiver::ConvertingReceiver) is used for high level
//! events, for use cases such as streaming.

use crate::{byte_converter::FromByteSlice, converting_callback_receiver::*, low_level_traits::*};
use std::{marker::PhantomData, time::Duration};

/// A wrapper for [`Receiver`], which converts received byte vectors to structured data. This variant of
/// [`ConvertingReceiver`](crate::converting_receiver::ConvertingReceiver) is used for high level
/// events, for use cases such as streaming.
///
/// This receiver wraps a [`Receiver`] receiving raw bytes. Calling [`recv_forever`], [`recv_timeout`] or [`try_recv`]
/// will call equivalent methods on the wrapped [`Receiver`] and then convert the received bytes
/// to a instance of `T`.
///
///
/// # Type parameters
///
/// * `PayloadT` - Type of the payload which will be streamed. Must be trivially copy- and constructable.
/// * `ResultT` - Type of additional return values which don't change between streaming events of the same stream.
/// * `T` - Type which is created from received byte vectors. Must implement [`FromByteSlice`](crate::byte_converter::FromByteSlice).
/// Also this type has to provide low level steaming information by implementing
/// [`LowLevelRead`](crate::low_level_traits::LowLevelRead) for `PayloadT` and `ResultT`.
///
/// # Errors
///
/// Returned errors are equivalent to those returned from methods of a [`Receiver`].
/// If the received response can not be interpreted as the result type `T`, a `MalformedPacket`
/// error is raised.
///
/// [`Receiver`]: std::sync::mpsc::Receiver
/// [`recv_forever`]: #method.recv_forever
/// [`recv_timeout`]: #method.recv_timeout
/// [`try_recv`]: #method.try_recv
pub struct ConvertingHighLevelCallbackReceiver<
    PayloadT: Default + Copy + Clone,
    ResultT,
    T: FromByteSlice + LowLevelRead<PayloadT, ResultT>,
> {
    receiver: ConvertingCallbackReceiver<T>,
    buf: Vec<PayloadT>,
    currently_receiving_stream: bool,
    message_length: usize,
    chunk_offset: usize,
    phantom: PhantomData<ResultT>,
}

impl<PayloadT: Default + Copy + Clone, ResultT, T: FromByteSlice + LowLevelRead<PayloadT, ResultT>>
    ConvertingHighLevelCallbackReceiver<PayloadT, ResultT, T>
{
    /// Creates a new converting high level callback receiver which wraps the given [`ConvertingCallbackReceiver`](crate::converting_callback_receiver::ConvertingCallbackReceiver).
    pub fn new(receiver: ConvertingCallbackReceiver<T>) -> ConvertingHighLevelCallbackReceiver<PayloadT, ResultT, T> {
        ConvertingHighLevelCallbackReceiver {
            receiver,
            phantom: PhantomData,
            buf: Vec::with_capacity(0),
            currently_receiving_stream: false,
            message_length: 0,
            chunk_offset: 0,
        }
    }

    fn recv_stream_chunk(&mut self, chunk: &T) -> Option<(Vec<PayloadT>, ResultT)> {
        if !self.currently_receiving_stream && chunk.ll_message_chunk_offset() != 0 {
            //currently not receiving and chunk is not start of stream => out of sync
            return None;
        }

        if self.currently_receiving_stream
            && (chunk.ll_message_chunk_offset() != self.chunk_offset || chunk.ll_message_length() != self.message_length)
        {
            //currently receiving, but chunk is not next expected or has wrong length (skipped whole stream) => out of sync
            return None;
        }

        if !self.currently_receiving_stream {
            //initialize
            self.currently_receiving_stream = true;
            self.message_length = chunk.ll_message_length();
            self.chunk_offset = 0;
            self.buf = vec![PayloadT::default(); self.message_length];
        }

        let read_length = std::cmp::min(chunk.ll_message_chunk_data().len(), self.message_length - self.chunk_offset);
        self.buf[self.chunk_offset..self.chunk_offset + read_length].copy_from_slice(&chunk.ll_message_chunk_data()[0..read_length]);
        self.chunk_offset += read_length;

        if self.chunk_offset >= self.message_length {
            //stream complete
            self.currently_receiving_stream = false;
            return Some((self.buf.clone(), chunk.get_result()));
        }
        None
    }

    /// Attempts to return a pending value on this receiver without blocking. This method behaves like [`try_recv`](std::sync::mpsc::Receiver::try_recv).
    ///
    /// # Errors
    ///
    /// Returns an error if the queue was disconnected or currently empty, or if the received packet was malformed.
    pub fn try_recv(&mut self) -> Result<(Vec<PayloadT>, ResultT), CallbackTryRecvError> {
        loop {
            let ll_result = self.receiver.try_recv()?;
            let result_opt = self.recv_stream_chunk(&ll_result);
            if let Some(tup) = result_opt {
                return Ok(tup);
            }
        }
    }

    /// Attempts to wait for a value on this receiver, returning an error if the corresponding channel has hung up. This method behaves like [`recv`](std::sync::mpsc::Receiver::recv).
    ///
    /// # Errors
    ///
    /// Returns an error if the queue was disconnected, or if the received packet was malformed.
    pub fn recv_forever(&mut self) -> Result<(Vec<PayloadT>, ResultT), CallbackRecvError> {
        loop {
            let ll_result = self.receiver.recv_forever()?;
            let result_opt = self.recv_stream_chunk(&ll_result);
            if let Some(tup) = result_opt {
                return Ok(tup);
            }
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
    pub fn recv_timeout(&mut self, timeout: Duration) -> Result<(Vec<PayloadT>, ResultT), CallbackRecvTimeoutError> {
        loop {
            let ll_result = self.receiver.recv_timeout(timeout)?;
            let result_opt = self.recv_stream_chunk(&ll_result);
            if let Some(tup) = result_opt {
                return Ok(tup);
            }
        }
    }

    /* uncomment if https://github.com/rust-lang/rust/issues/46316 has landed
        pub fn recv_deadline(&self, deadline: Instant) -> Result<T, RecvTimeoutError> {
           let bytes = self.receiver.recv_deadline(deadline)?;
            Ok(T::from_le_byte_slice(bytes))        
        }
    */
}

impl<PayloadT: Default + Copy + Clone, ResultT, T: FromByteSlice + LowLevelRead<PayloadT, ResultT>> Iterator
    for ConvertingHighLevelCallbackReceiver<PayloadT, ResultT, T>
{
    type Item = Option<(Vec<PayloadT>, ResultT)>;
    fn next(&mut self) -> Option<Option<(Vec<PayloadT>, ResultT)>> {
        match self.recv_forever() {
            Ok(result) => Some(Some(result)),
            Err(CallbackRecvError::MalformedPacket) => Some(None),
            Err(_e) => None,
        }
    }
}
/*
impl<PayloadT: Default + Copy + Clone, ResultT, T: FromByteSlice + LowLevelRead<PayloadT, ResultT>> IntoIterator for ConvertingHighLevelCallbackReceiver<PayloadT, ResultT, T> {
    fn into_iter(self) -> Iter<T> { self.iter() }
}

impl<T: FromByteSlice> IntoIterator for ConvertingHighLevelCallbackReceiver<T> {
    type Item = T;
    type IntoIter = IntoIter<T>;

    fn into_iter(self) -> IntoIter<T> { IntoIter { rx: self } }
}
*/
