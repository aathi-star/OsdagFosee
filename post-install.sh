#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Make the script executable
chmod +x /usr/local/bin/insta-osdag.py

# Run the script
/usr/local/bin/insta-osdag.py

