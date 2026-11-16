#!/bin/bash
TARGET="Bob"
echo "Hello, $TARGET"
if [ "$TARGET" == "Rehanna" ]; then
  echo "Welcome back, Admin.System are go."
else
  echo "Unknown user. Access denied."
fi
