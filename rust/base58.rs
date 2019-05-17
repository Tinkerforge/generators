//! Parses Base58 encoded brick and bricklet uids.
use std::{
    error::Error,
    fmt::{Display, Formatter},
};

const ALPHABET: &str = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

const ERROR_INVALID_CHAR: &str = "UID contains an invalid character.";
const ERROR_TOO_BIG: &str = "UID is too big to fit into a u64";
const ERROR_EMPTY: &str = "UID is empty or a value that mapped to zero";

///Error type of Base58 parser.
#[derive(Debug, Copy, Clone)]
pub enum Base58Error {
    ///Is returned if the parse finds an invalid character. Contains the character and it's index in the string.
    InvalidCharacter,
    UidToBig, //FIXME: (breaking change) Spelling
    UidEmpty
}

impl Display for Base58Error {
    fn fmt(&self, f: &mut Formatter) -> std::fmt::Result {
        match *self {
            Base58Error::InvalidCharacter => write!(f, "{}", ERROR_INVALID_CHAR),
            Base58Error::UidToBig => write!(f, "{}", ERROR_TOO_BIG),
            Base58Error::UidEmpty => write!(f, "{}", ERROR_EMPTY)
        }
    }
}

impl Error for Base58Error {
    fn description(&self) -> &str {
        match *self {
            Base58Error::InvalidCharacter => ERROR_INVALID_CHAR,
            Base58Error::UidToBig => ERROR_TOO_BIG,
            Base58Error::UidEmpty => ERROR_EMPTY
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
        let mut result_u64: u64 = 0;
        let radix: u64 = ALPHABET.len() as u64;
        let mut digit: u32 = 0;
        // Remove 1s from the left as they are leading zeros in base 58
        let filtered = self.as_bytes().iter().skip_while(|c| **c == '1' as u8).collect::<Vec<&u8>>();
        for (idx, &&character) in filtered.iter().enumerate().rev() {
            match ALPHABET.as_bytes().iter().enumerate().find(|(_i, c)| **c == character).map(|(i, _c)| i) {
                None => return Err(Base58Error::InvalidCharacter),
                Some(i) => {
                    if digit > 0 && radix.pow(digit - 1) > (u64::max_value() / radix) {
                        return Err(Base58Error::UidToBig); //pow overflow
                    }
                    let opt = radix.pow(digit).checked_mul(i as u64);
                    if opt.is_none() {
                        return Err(Base58Error::UidToBig); //mul overflow
                    }
                    if u64::max_value() - opt.unwrap() < result_u64 {
                        return Err(Base58Error::UidToBig); //add overflow
                    }
                    result_u64 += opt.unwrap();
                }
            }
            digit += 1;
        }

        let result = if result_u64 > u32::max_value().into() {
                let value1 = result_u64 & 0xFF_FF_FF_FF;
                let value2 = (result_u64 >> 32) & 0xFF_FF_FF_FF;
                ((value1 & 0x00_00_0F_FF)
                |(value1 & 0x0F_00_00_00) >> 12
                |(value2 & 0x00_00_00_3F) << 16
                |(value2 & 0x00_0F_00_00) << 6
                |(value2 & 0x3F_00_00_00) << 2) as u32
            }
            else {
                result_u64 as u32
            };
        if result == 0 {
            Err(Base58Error::UidEmpty)
        } else {
            Ok(result)
        }
    }
}

impl Base58 for String {
    fn base58_to_u32(&self) -> Result<u32, Base58Error> { self.as_str().base58_to_u32() }
}
