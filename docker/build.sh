#!/bin/bash -e

docker buildx build --no-cache -t tinkerforge/builder-generators-debian:1.2.0 .
