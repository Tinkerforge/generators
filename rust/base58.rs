//! Parses Base58 encoded brick and bricklet uids.
use std::{
    error::Error,
    fmt::{Display, Formatter},
};

const ALPHABET: &str = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

///Error type of Base58 parser.
#[derive(Debug, Copy, Clone)]
pub enum Base58Error {
    ///Is returned if the parse finds an invalid character. Contains the character and it's index in the string.
    InvalidCharacter(usize, u8),
    UidToBig
}

impl Display for Base58Error {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        match *self {
            Base58Error::InvalidCharacter(idx, character) => write!(f, "Invalid character at index {}: {}", idx, character),
            Base58Error::UidToBig => write!(f, "UID was to big to fit into a u64")
        }
    }
}

impl Error for Base58Error {
    fn description(&self) -> &str {
        match *self {
            Base58Error::InvalidCharacter(_, _) => "Invalid character",
            Base58Error::UidToBig => "UID was to big to fit into a u64"
        }
    }
}

///A trait which adds Base58 parsing capabilities to strings. The alphabet used is "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ".
pub trait Base58 {
    /// Parse this string as Base58 encoded uid. Returns an error if a character is found, that is not part of the used alphabet.
    fn base58_to_u32(&self) -> Result<u32, Base58Error>;
}

impl Base58 for str {
    fn base58_to_u32(&self) -> Result<u32, Base58Error> {
        let mut result: u64 = 0;
        let radix: u64 = ALPHABET.len() as u64;
        let mut digit: u32 = 0;
        for (idx, &character) in self.as_bytes().iter().enumerate().rev() {
            match ALPHABET.as_bytes().iter().enumerate().find(|(_i, c)| **c == character).map(|(i, _c)| i) {
                None => return Err(Base58Error::InvalidCharacter(idx, character)),
                Some(i) => {
                    let opt = radix.pow(digit).checked_mul(i as u64);
                    if opt.is_none() {
                        return Err(Base58Error::UidToBig);
                    }
                    result += opt.unwrap();
                }
            }
            digit += 1;
        }
        
        if result > u32::max_value().into() {
            let value1 = result & 0xFF_FF_FF_FF;
            let value2 = (result >> 32) & 0xFF_FF_FF_FF;

            Ok(((value1 & 0x00_00_0F_FF)
               |(value1 & 0x0F_00_00_00) >> 12
               |(value2 & 0x00_00_00_3F) << 16
               |(value2 & 0x00_0F_00_00) << 6
               |(value2 & 0x3F_00_00_00) << 2) as u32)
        }
        else {
            Ok(result as u32)
        }
    }
}

impl Base58 for String {
    fn base58_to_u32(&self) -> Result<u32, Base58Error> { self.as_str().base58_to_u32() }
}
