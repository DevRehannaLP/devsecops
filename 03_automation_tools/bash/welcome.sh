#!/bin/bash
USER_NAME="Rehanna"

echo "Welcome to the automation zone, $USER!"

if [ "$USER" = "root" ]; then
  echo "Warning: You are running this as root!"
else
  echo "Good job running this as a standard user."
fi

MY_HOST=$(hostname)
echo "This script is running on: $MY_HOST"

cat /fakefile.txt
if [ $? -ne 0 ]; then
  echo "Caught an error! The file doesn't exist."
fi
