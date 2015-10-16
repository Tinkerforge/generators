#!/bin/sh
# Connects to localhost:4223 by default, use --host and --port to change this

# Trigger enumerate
tinkerforge enumerate &

echo "Press key to exit"; read dummy

kill -- -$$ # Stop callback dispatch in background
