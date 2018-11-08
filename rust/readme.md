# Tinkerforge Rust Bindings

[![Latest version](https://img.shields.io/crates/v/tinkerforge.svg)](https://crates.io/crates/tinkerforge)
[![Documentation](https://docs.rs/tinkerforge/badge.svg)](https://docs.rs/tinkerforge)
[![Minimum rustc version](https://img.shields.io/badge/rustc-beta-yellow.svg)](https://github.com/tinkerforge/generators/blob/master/rust/readme.md#rust-version-requirements)
[![License](https://img.shields.io/crates/l/tinkerforge.svg)](https://github.com/tinkerforge/generators/blob/master/rust/readme.md#license)

This crate provides API bindings for [Tinkerforge](https://www.tinkerforge.com) bricks and bricklets.

## How to install

Add `tinkerforge = "2.0"` to the `[dependencies]` of your project's Cargo.toml.

## How to use

First, import the IP connection and any devices you want to use: 
```rust
use tinkerforge::{ip_connection::*, temperature_bricklet::*}
```
You can than create instances like this:
```rust
let ipcon = IpConnection::new();
let t = TemperatureBricklet::new("UID", &ipcon);
```
where `"UID"` is the unique identifier of your brick or bricklet. Once the IP connection is established using:
```rust
ipcon.connect((HOST, PORT)).recv()??;
```
you can use the device's API, for example:
```rust
let temperature = t.get_temperature().recv()? as f32 / 100.0;
```

Further examples can be found [here](http://www.tinkerforge.com/en/doc/Software/API_Bindings_Rust.html).

## Rust version requirements

The 2.0 release currently requires a Beta version of rustc, which can be installed with: `rustup install beta`

When the 2018 edition of Rust (1.31) is released as stable (see the [roadmap](https://internals.rust-lang.org/t/rust-2018-release-schedule-and-extended-beta/8076)), the bindings can be compiled with it.

## License

Licensed under either of

 * CC0 1.0 Universal ([LICENSE-CC0](https://github.com/tinkerforge/generators/blob/master/rust/LICENSE-CC0) or https://creativecommons.org/publicdomain/zero/1.0/legalcode)
 * Apache License, Version 2.0, ([LICENSE-APACHE](https://github.com/tinkerforge/generators/blob/master/rust/LICENSE-APACHE) or https://www.apache.org/licenses/LICENSE-2.0)
 * MIT license ([LICENSE-MIT](https://github.com/tinkerforge/generators/blob/master/rust/LICENSE-MIT) or https://opensource.org/licenses/MIT)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be triple licensed as above, without any
additional terms or conditions.