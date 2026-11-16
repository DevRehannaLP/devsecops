#!/bin/bash
USERS="Rehanna Bob Alice root"
for TARGET in $USERS; do
  echo "Scanning user: $TARGET"
  if [ "$TARGET" == "Rehanna" ]; then
    echo "Welcome back, Admin.System are go."
  else
    echo "Unknown user. Access denied."
    exit 1
  fi
done
