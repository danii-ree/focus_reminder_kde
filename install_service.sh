#!/bin/bash

# Get the current user and working directory
USER=$(whoami)
WORKING_DIR=$(pwd)

# Create the service file with proper paths
sed "s|%USER%|$USER|g; s|%WORKING_DIR%|$WORKING_DIR|g" focus_reminder.service > /tmp/focus_reminder.service

# Copy the service file to systemd directory
sudo cp /tmp/focus_reminder.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable focus_reminder.service
sudo systemctl start focus_reminder.service

echo "Focus Reminder service has been installed and started."
echo "To check status: systemctl status focus_reminder.service"
echo "To stop: systemctl stop focus_reminder.service"
echo "To disable: systemctl disable focus_reminder.service" 