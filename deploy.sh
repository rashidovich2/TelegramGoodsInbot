#!/bin/bash

# Connect to VPS
ssh user@your_vps_ip << EOF

# Update packages
sudo apt-get update -y

# Install Python and pip
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y

# Clone your project (replace with your repository)
git clone https://github.com/your_username/your_project.git

# Navigate to your project directory
cd your_project

# Install necessary Python modules
pip3 install aiogram colorlog requests bs4 beautifulsoup4 pyQiwiP2P aiohttp APScheduler==3.9.1 colorama async_class yoomoney geopy coinbase base58 tronpy

# Run your Python script (replace with your script)
python3 your_script.py

EOF
