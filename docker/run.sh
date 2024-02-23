#!/bin/bash

exec docker run --rm -it tinkerforge/builder-generators-debian:1.2.0 bash -c $1
