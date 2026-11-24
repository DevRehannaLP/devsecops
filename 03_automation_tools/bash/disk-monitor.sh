#!/bin/bash

set -e

LOG_FILE="$HOME/logs/disk_monitor.log"
TARGET_DIR="/home"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting disk check" >>"$LOG_FILE"

if [ -d "$TARGET_DIR" ]; then
  du -sh "$TARGET_DIR" >>"$LOG_FILE" 2>&1
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Check completed successfully" >>"$LOG_FILE"
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Directory $TARGET_DIR not found" >>"$LOG_FILE"
  exit 1
fi
