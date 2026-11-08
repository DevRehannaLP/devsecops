#!/bin/bash
# System Information Script - displays key system details
# Author: DevRehannaLP

echo "============================="
echo "    SYSTEM INFORMATION REPORT"
echo "============================="

echo "User: $USER"
echo "Hostname: $HOSTNAME"
echo "Date: $(date)"
echo "OS: $(uname -o)"
echo "Disk Usage: $(df -h / | tail -1 | awk '{print $4}') available"
echo "Memory: $(free -h | awk '/^Mem/ {print $3 " used / " $2 " total"}')"
echo "Uptime: $(uptime -p)"
echo "============================="
