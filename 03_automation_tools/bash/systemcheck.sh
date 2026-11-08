#!/bin/bash
# ∞ ☬ DevRehannaLP ☬ | DevSecOps ∞ 20261603 1739

echo "=== System Check ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Directory: $(pwd)"
echo "Uptime: $(uptime -p)"
echo "Disk Usage: $(df -h ~ | tail -1 | awk '{print $5}') used"
