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

impl ToBytes for [bool; 2] {
    fn to_le_bytes(arr: [bool; 2]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 2] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 2] {
        let mut result = [false; 2];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for [bool; 4] {
    fn to_le_bytes(arr: [bool; 4]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 4] {
        let mut result = [false; 4];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 1 }
}

impl ToBytes for [bool; 16] {
    fn to_le_bytes(arr: [bool; 16]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 16] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 16] {
        let mut result = [false; 16];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 2 }
}

impl ToBytes for [bool; 32] {
    fn to_le_bytes(arr: [bool; 32]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 32] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 32] {
        let mut result = [false; 32];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for [bool; 440] {
    fn to_le_bytes(arr: [bool; 440]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 440] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 440] {
        let mut result = [false; 440];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 55 }
}

impl ToBytes for [bool; 448] {
    fn to_le_bytes(arr: [bool; 448]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 448] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 448] {
        let mut result = [false; 448];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 56 }
}

impl ToBytes for [bool; 464] {
    fn to_le_bytes(arr: [bool; 464]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 464] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 464] {
        let mut result = [false; 464];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 58 }
}

impl ToBytes for [bool; 472] {
    fn to_le_bytes(arr: [bool; 472]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 472] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 472] {
        let mut result = [false; 472];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 59 }
}

impl ToBytes for [bool; 480] {
    fn to_le_bytes(arr: [bool; 480]) -> Vec<u8> {
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {0} else {1}];
        for (i, b) in arr.into_iter().enumerate() {
            buf[i / 8] |= (*b as u8) << (i % 8);
        }
        buf
    }
}

impl FromByteSlice for [bool; 480] {
    fn from_le_bytes(bytes: &[u8]) -> [bool; 480] {
        let mut result = [false; 480];
        for (byte, elem) in bytes.into_iter().enumerate() {            
            for i in 0..8 {
                if byte * 8 + i >= result.len() {
                    break;
                }
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }
        }
        result
    }
    fn bytes_expected() -> usize { 60 }
}

impl ToBytes for [u8; 3] {
    fn to_le_bytes(arr: [u8; 3]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 3] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 3] {
        let mut buf = [0u8; 3];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 3 }
}

impl ToBytes for [u8; 4] {
    fn to_le_bytes(arr: [u8; 4]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 4] {
        let mut buf = [0u8; 4];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for [u8; 6] {
    fn to_le_bytes(arr: [u8; 6]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 6] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 6] {
        let mut buf = [0u8; 6];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 6 }
}

impl ToBytes for [u8; 7] {
    fn to_le_bytes(arr: [u8; 7]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 7] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 7] {
        let mut buf = [0u8; 7];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 7 }
}

impl ToBytes for [u8; 8] {
    fn to_le_bytes(arr: [u8; 8]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 8] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 8] {
        let mut buf = [0u8; 8];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for [u8; 12] {
    fn to_le_bytes(arr: [u8; 12]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 12] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 12] {
        let mut buf = [0u8; 12];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 12 }
}

impl ToBytes for [u8; 15] {
    fn to_le_bytes(arr: [u8; 15]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 15] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 15] {
        let mut buf = [0u8; 15];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 15 }
}

impl ToBytes for [u8; 16] {
    fn to_le_bytes(arr: [u8; 16]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 16] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 16] {
        let mut buf = [0u8; 16];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 16 }
}

impl ToBytes for [u8; 32] {
    fn to_le_bytes(arr: [u8; 32]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 32] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 32] {
        let mut buf = [0u8; 32];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 32 }
}

impl ToBytes for [u8; 56] {
    fn to_le_bytes(arr: [u8; 56]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 56] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 56] {
        let mut buf = [0u8; 56];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 56 }
}

impl ToBytes for [u8; 58] {
    fn to_le_bytes(arr: [u8; 58]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 58] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 58] {
        let mut buf = [0u8; 58];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 58 }
}

impl ToBytes for [u8; 60] {
    fn to_le_bytes(arr: [u8; 60]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 60] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 60] {
        let mut buf = [0u8; 60];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 60 }
}

impl ToBytes for [u8; 61] {
    fn to_le_bytes(arr: [u8; 61]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 61] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 61] {
        let mut buf = [0u8; 61];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 61 }
}

impl ToBytes for [u8; 62] {
    fn to_le_bytes(arr: [u8; 62]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 62] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 62] {
        let mut buf = [0u8; 62];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 62 }
}

impl ToBytes for [u8; 64] {
    fn to_le_bytes(arr: [u8; 64]) -> Vec<u8> {
        arr.to_vec()
    }
}

impl FromByteSlice for [u8; 64] {
    fn from_le_bytes(bytes: &[u8]) -> [u8; 64] {
        let mut buf = [0u8; 64];
        buf.copy_from_slice(bytes);
        buf
    }
    fn bytes_expected() -> usize { 64 }
}

impl ToBytes for [char; 4] {
    fn to_le_bytes(arr: [char; 4]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8]
    }
}

impl FromByteSlice for [char; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 4] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char]
    }
    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for [i8; 32] {
    fn to_le_bytes(arr: [i8; 32]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8]
    }
}

impl FromByteSlice for [i8; 32] {
    fn from_le_bytes(bytes: &[u8]) -> [i8; 32] {
        [bytes[0] as i8, bytes[1] as i8, bytes[2] as i8, bytes[3] as i8, bytes[4] as i8, bytes[5] as i8, bytes[6] as i8, bytes[7] as i8, bytes[8] as i8, bytes[9] as i8, bytes[10] as i8, bytes[11] as i8, bytes[12] as i8, bytes[13] as i8, bytes[14] as i8, bytes[15] as i8, bytes[16] as i8, bytes[17] as i8, bytes[18] as i8, bytes[19] as i8, bytes[20] as i8, bytes[21] as i8, bytes[22] as i8, bytes[23] as i8, bytes[24] as i8, bytes[25] as i8, bytes[26] as i8, bytes[27] as i8, bytes[28] as i8, bytes[29] as i8, bytes[30] as i8, bytes[31] as i8]
    }
    fn bytes_expected() -> usize { 32 }
}

impl ToBytes for [char; 56] {
    fn to_le_bytes(arr: [char; 56]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8]
    }
}

impl FromByteSlice for [char; 56] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 56] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char]
    }
    fn bytes_expected() -> usize { 56 }
}

impl ToBytes for [char; 58] {
    fn to_le_bytes(arr: [char; 58]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8]
    }
}

impl FromByteSlice for [char; 58] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 58] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char]
    }
    fn bytes_expected() -> usize { 58 }
}

impl ToBytes for [char; 59] {
    fn to_le_bytes(arr: [char; 59]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8, arr[58] as u8]
    }
}

impl FromByteSlice for [char; 59] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 59] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char, bytes[58] as char]
    }
    fn bytes_expected() -> usize { 59 }
}

impl ToBytes for [char; 60] {
    fn to_le_bytes(arr: [char; 60]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8, arr[58] as u8, arr[59] as u8]
    }
}

impl FromByteSlice for [char; 60] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 60] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char, bytes[58] as char, bytes[59] as char]
    }
    fn bytes_expected() -> usize { 60 }
}

impl ToBytes for [char; 61] {
    fn to_le_bytes(arr: [char; 61]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8, arr[58] as u8, arr[59] as u8, arr[60] as u8]
    }
}

impl FromByteSlice for [char; 61] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 61] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char, bytes[58] as char, bytes[59] as char, bytes[60] as char]
    }
    fn bytes_expected() -> usize { 61 }
}

impl ToBytes for [char; 62] {
    fn to_le_bytes(arr: [char; 62]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8, arr[58] as u8, arr[59] as u8, arr[60] as u8, arr[61] as u8]
    }
}

impl FromByteSlice for [char; 62] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 62] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char, bytes[58] as char, bytes[59] as char, bytes[60] as char, bytes[61] as char]
    }
    fn bytes_expected() -> usize { 62 }
}

impl ToBytes for [char; 63] {
    fn to_le_bytes(arr: [char; 63]) -> Vec<u8> {
        vec![arr[0] as u8, arr[1] as u8, arr[2] as u8, arr[3] as u8, arr[4] as u8, arr[5] as u8, arr[6] as u8, arr[7] as u8, arr[8] as u8, arr[9] as u8, arr[10] as u8, arr[11] as u8, arr[12] as u8, arr[13] as u8, arr[14] as u8, arr[15] as u8, arr[16] as u8, arr[17] as u8, arr[18] as u8, arr[19] as u8, arr[20] as u8, arr[21] as u8, arr[22] as u8, arr[23] as u8, arr[24] as u8, arr[25] as u8, arr[26] as u8, arr[27] as u8, arr[28] as u8, arr[29] as u8, arr[30] as u8, arr[31] as u8, arr[32] as u8, arr[33] as u8, arr[34] as u8, arr[35] as u8, arr[36] as u8, arr[37] as u8, arr[38] as u8, arr[39] as u8, arr[40] as u8, arr[41] as u8, arr[42] as u8, arr[43] as u8, arr[44] as u8, arr[45] as u8, arr[46] as u8, arr[47] as u8, arr[48] as u8, arr[49] as u8, arr[50] as u8, arr[51] as u8, arr[52] as u8, arr[53] as u8, arr[54] as u8, arr[55] as u8, arr[56] as u8, arr[57] as u8, arr[58] as u8, arr[59] as u8, arr[60] as u8, arr[61] as u8, arr[62] as u8]
    }
}

impl FromByteSlice for [char; 63] {
    fn from_le_bytes(bytes: &[u8]) -> [char; 63] {
        [bytes[0] as char, bytes[1] as char, bytes[2] as char, bytes[3] as char, bytes[4] as char, bytes[5] as char, bytes[6] as char, bytes[7] as char, bytes[8] as char, bytes[9] as char, bytes[10] as char, bytes[11] as char, bytes[12] as char, bytes[13] as char, bytes[14] as char, bytes[15] as char, bytes[16] as char, bytes[17] as char, bytes[18] as char, bytes[19] as char, bytes[20] as char, bytes[21] as char, bytes[22] as char, bytes[23] as char, bytes[24] as char, bytes[25] as char, bytes[26] as char, bytes[27] as char, bytes[28] as char, bytes[29] as char, bytes[30] as char, bytes[31] as char, bytes[32] as char, bytes[33] as char, bytes[34] as char, bytes[35] as char, bytes[36] as char, bytes[37] as char, bytes[38] as char, bytes[39] as char, bytes[40] as char, bytes[41] as char, bytes[42] as char, bytes[43] as char, bytes[44] as char, bytes[45] as char, bytes[46] as char, bytes[47] as char, bytes[48] as char, bytes[49] as char, bytes[50] as char, bytes[51] as char, bytes[52] as char, bytes[53] as char, bytes[54] as char, bytes[55] as char, bytes[56] as char, bytes[57] as char, bytes[58] as char, bytes[59] as char, bytes[60] as char, bytes[61] as char, bytes[62] as char]
    }
    fn bytes_expected() -> usize { 63 }
}

impl ToBytes for [u16; 2] {
    fn to_le_bytes(arr: [u16; 2]) -> Vec<u8> {
        let mut buf = vec![0,4];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 2] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 2] {
        let mut buf = [0u16; 2];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 4 }
}

impl ToBytes for [u16; 4] {
    fn to_le_bytes(arr: [u16; 4]) -> Vec<u8> {
        let mut buf = vec![0,8];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 4] {
        let mut buf = [0u16; 4];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for [u16; 5] {
    fn to_le_bytes(arr: [u16; 5]) -> Vec<u8> {
        let mut buf = vec![0,10];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 5] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 5] {
        let mut buf = [0u16; 5];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 10 }
}

impl ToBytes for [u16; 27] {
    fn to_le_bytes(arr: [u16; 27]) -> Vec<u8> {
        let mut buf = vec![0,54];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 27] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 27] {
        let mut buf = [0u16; 27];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 54 }
}

impl ToBytes for [u16; 29] {
    fn to_le_bytes(arr: [u16; 29]) -> Vec<u8> {
        let mut buf = vec![0,58];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 29] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 29] {
        let mut buf = [0u16; 29];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 58 }
}

impl ToBytes for [u16; 30] {
    fn to_le_bytes(arr: [u16; 30]) -> Vec<u8> {
        let mut buf = vec![0,60];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 30] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 30] {
        let mut buf = [0u16; 30];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 60 }
}

impl ToBytes for [u16; 31] {
    fn to_le_bytes(arr: [u16; 31]) -> Vec<u8> {
        let mut buf = vec![0,62];
        LittleEndian::write_u16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u16; 31] {
    fn from_le_bytes(bytes: &[u8]) -> [u16; 31] {
        let mut buf = [0u16; 31];
        LittleEndian::read_u16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 62 }
}

impl ToBytes for [i16; 3] {
    fn to_le_bytes(arr: [i16; 3]) -> Vec<u8> {
        let mut buf = vec![0,6];
        LittleEndian::write_i16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [i16; 3] {
    fn from_le_bytes(bytes: &[u8]) -> [i16; 3] {
        let mut buf = [0i16; 3];
        LittleEndian::read_i16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 6 }
}

impl ToBytes for [i16; 4] {
    fn to_le_bytes(arr: [i16; 4]) -> Vec<u8> {
        let mut buf = vec![0,8];
        LittleEndian::write_i16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [i16; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [i16; 4] {
        let mut buf = [0i16; 4];
        LittleEndian::read_i16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for [i16; 10] {
    fn to_le_bytes(arr: [i16; 10]) -> Vec<u8> {
        let mut buf = vec![0,20];
        LittleEndian::write_i16_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [i16; 10] {
    fn from_le_bytes(bytes: &[u8]) -> [i16; 10] {
        let mut buf = [0i16; 10];
        LittleEndian::read_i16_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 20 }
}

impl ToBytes for [u32; 4] {
    fn to_le_bytes(arr: [u32; 4]) -> Vec<u8> {
        let mut buf = vec![0,16];
        LittleEndian::write_u32_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u32; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [u32; 4] {
        let mut buf = [0u32; 4];
        LittleEndian::read_u32_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 16 }
}

impl ToBytes for [i32; 2] {
    fn to_le_bytes(arr: [i32; 2]) -> Vec<u8> {
        let mut buf = vec![0,8];
        LittleEndian::write_i32_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [i32; 2] {
    fn from_le_bytes(bytes: &[u8]) -> [i32; 2] {
        let mut buf = [0i32; 2];
        LittleEndian::read_i32_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 8 }
}

impl ToBytes for [u64; 4] {
    fn to_le_bytes(arr: [u64; 4]) -> Vec<u8> {
        let mut buf = vec![0,32];
        LittleEndian::write_u64_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u64; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [u64; 4] {
        let mut buf = [0u64; 4];
        LittleEndian::read_u64_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 32 }
}

impl ToBytes for [u64; 7] {
    fn to_le_bytes(arr: [u64; 7]) -> Vec<u8> {
        let mut buf = vec![0,56];
        LittleEndian::write_u64_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [u64; 7] {
    fn from_le_bytes(bytes: &[u8]) -> [u64; 7] {
        let mut buf = [0u64; 7];
        LittleEndian::read_u64_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 56 }
}

impl ToBytes for [i64; 4] {
    fn to_le_bytes(arr: [i64; 4]) -> Vec<u8> {
        let mut buf = vec![0,32];
        LittleEndian::write_i64_into(&arr, &mut buf);
        buf
    }
}

impl FromByteSlice for [i64; 4] {
    fn from_le_bytes(bytes: &[u8]) -> [i64; 4] {
        let mut buf = [0i64; 4];
        LittleEndian::read_i64_into(&bytes, &mut buf);
        buf
    }
    fn bytes_expected() -> usize { 32 }
}