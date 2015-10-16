#!/bin/sh
# Connects to localhost:4223 by default, use --host and --port to change this

# Trigger enumerate with authentication
tinkerforge --secret "My Authentication Secret" enumerate &

echo "Press key to exit"; read dummy

kill -- -$$ # Stop callback dispatch in background
