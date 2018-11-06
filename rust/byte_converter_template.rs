//! Traits for (de)serialization of structs to byte vectors.
use byteorder::*;
use crate::converting_receiver::BrickletError;

/// A trait to serialize the implementing type to a byte vector.
pub trait ToBytes {
    /// Serialize the implementing type to a byte vector.
    fn to_le_bytes(_: Self) -> Vec<u8>;

    /// Try to serialize the implementing type to a byte vector. If the type is shorter than max_len, it will be padded with zero bytes. Currently this method is only used for strings. Other types use the standard implementation, which calls [`to_le_bytes`] without further checks or padding.
    /// # Errors
    /// Returns an InvalidArgument error if the type was too long.
    /// 
    /// [`to_le_bytes`]: #ToBytes.to_le_bytes
    fn try_to_le_bytes(var: Self, _max_len: usize) -> Result<Vec<u8>, BrickletError> where Self: std::marker::Sized {
        Ok(Self::to_le_bytes(var))
    }
}

/// A trait to deserialize the implemeting type from a byte slice.
pub trait FromByteSlice {
    /// Deserialize the implementing type from a byte slice.
    fn from_le_bytes(bytes: &[u8]) -> Self;
    /// Returns how many bytes are expected to deserialize a instance of the implementing type. Currently this method is only used for strings.
    fn bytes_expected() -> usize;
}

impl ToBytes for () {
    fn to_le_bytes(_: ()) -> Vec<u8> {
        vec![]
    }
}

impl FromByteSlice for () {
    fn from_le_bytes(_: &[u8]) { }

    fn bytes_expected() -> usize { 0 }
}


impl ToBytes for bool {
    fn to_le_bytes(b: bool) -> Vec<u8> {
        vec![b as u8]
    }
}

impl FromByteSlice for bool {
    fn from_le_bytes(bytes: &[u8]) -> bool {
        bytes[0] != 0
    }

    fn bytes_expected() -> usize { 1 }
}


impl ToBytes for u8 {
    fn to_le_bytes(num: u8) -> Vec<u8> {
        vec![num]
    }
}

impl FromByteSlice for u8 {
    fn from_le_bytes(bytes: &[u8]) -> u8 {
        bytes[0]
    }

    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for i8 {
    fn to_le_bytes(num: i8) -> Vec<u8> {
        vec![num as u8]
    }
}

impl FromByteSlice for i8 {
    fn from_le_bytes(bytes: &[u8]) -> i8 {
        bytes[0] as i8
    }

    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for u16 {
    fn to_le_bytes(num: u16) -> Vec<u8> {
        let mut buf = vec![0; 2];
        LittleEndian::write_u16(&mut buf, num);
        buf
    }
}

impl FromByteSlice for u16 {
    fn from_le_bytes(bytes: &[u8]) -> u16 {
        LittleEndian::read_u16(bytes)
    }

    fn bytes_expected() -> usize { 2 }
}

impl ToBytes for i16 {
    fn to_le_bytes(num: i16) -> Vec<u8> {
        let mut buf = vec![0; 2];
        LittleEndian::write_i16(&mut buf, num);
        buf
    }
}

impl FromByteSlice for i16 {
    fn from_le_bytes(bytes: &[u8]) -> i16 {
        LittleEndian::read_i16(bytes)
    }

    fn bytes_expected() -> usize { 2 }
}

impl ToBytes for u32 {
    fn to_le_bytes(num: u32) -> Vec<u8> {
        let mut buf = vec![0; 4];
        LittleEndian::write_u32(&mut buf, num);
        buf
    }
}

impl FromByteSlice for u32 {
    fn from_le_bytes(bytes: &[u8]) -> u32 {
        LittleEndian::read_u32(bytes)
    }

    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for i32 {
    fn to_le_bytes(num: i32) -> Vec<u8> {
        let mut buf = vec![0; 4];
        LittleEndian::write_i32(&mut buf, num);
        buf
    }
}

impl FromByteSlice for i32 {
    fn from_le_bytes(bytes: &[u8]) -> i32 {
        LittleEndian::read_i32(bytes)
    }

    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for u64 {
    fn to_le_bytes(num: u64) -> Vec<u8> {
        let mut buf = vec![0; 8];
        LittleEndian::write_u64(&mut buf, num);
        buf
    }
}

impl FromByteSlice for u64 {
    fn from_le_bytes(bytes: &[u8]) -> u64 {
        LittleEndian::read_u64(bytes)
    }

    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for i64 {
    fn to_le_bytes(num: i64) -> Vec<u8> {
        let mut buf = vec![0; 8];
        LittleEndian::write_i64(&mut buf, num);
        buf
    }
}

impl FromByteSlice for i64 {
    fn from_le_bytes(bytes: &[u8]) -> i64 {
        LittleEndian::read_i64(bytes)
    }

    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for char {
    fn to_le_bytes(c: char) -> Vec<u8> {
        vec![c as u8]
    }
}


impl FromByteSlice for char {
    fn from_le_bytes(bytes: &[u8]) -> char {
          bytes[0] as char
    }

    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for String {
    fn to_le_bytes(s: String) -> Vec<u8> {
        s.into_bytes()
    }

    fn try_to_le_bytes(s: String, max_len: usize) -> Result<Vec<u8>, BrickletError> {
        let bytes = s.into_bytes();
        if bytes.len() > max_len {
            Err(BrickletError::InvalidParameter)
        } else {
            let mut result = vec![0u8; max_len];
            result[0..bytes.len()].copy_from_slice(&bytes);
            Ok(result)
        }        
    }
}

impl FromByteSlice for String {
    fn from_le_bytes(bytes: &[u8]) -> String {
          String::from_utf8(bytes.to_vec()).expect("").replace("\u{0}", "") //TODO: endianess conversion?
    }

    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for f32 {
    fn to_le_bytes(num: f32) -> Vec<u8> {
        let mut buf = vec![0; 4];
        LittleEndian::write_f32(&mut buf, num);
        buf
    }
}

impl FromByteSlice for f32 {
    fn from_le_bytes(bytes: &[u8]) -> f32 {
        LittleEndian::read_f32(bytes)
    }

    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for f64 {
    fn to_le_bytes(num: f64) -> Vec<u8> {
        let mut buf = vec![0; 8];
        LittleEndian::write_f64(&mut buf, num);
        buf
    }
}

impl FromByteSlice for f64 {
    fn from_le_bytes(bytes: &[u8]) -> f64 {
        LittleEndian::read_f64(bytes)
    }

    fn bytes_expected() -> usize { 8 }
}
