#![forbid(unsafe_code)]
#![allow(clippy::too_many_arguments)]
#![allow(unstable_name_collisions)]
#![cfg_attr(feature = "fail-on-warnings", deny(warnings))]
#![cfg_attr(feature = "fail-on-warnings", deny(clippy::all))]
#![doc(html_root_url = "https://docs.rs/tinkerforge/0.1.0")]

//! Rust API bindings for [Tinkerforge](https://www.tinkerforge.com) bricks and bricklets.

mod bindings;
pub use crate::bindings::*;
pub mod base58;
pub mod byte_converter;
pub mod converting_callback_receiver;
pub mod converting_high_level_callback_receiver;
pub mod converting_receiver;
pub mod device;
pub mod ipconnection;
pub mod low_level_traits;
