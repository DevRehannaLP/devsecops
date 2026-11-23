#!/bin/bash
# ∞ ☬ DevRehannaLP ☬ | DevSecOps ∞ 20261603 1739

echo "=== System Check ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Directory: $(pwd)"
echo "Uptime: $(uptime -p)"
echo "Disk Usage: $(df -h ~ | tail -1 | awk '{print $5}') used"

# Adding to the script to check firewall activity

if sudo ufw status | grep -q "active"; then
  echo -e "\e[32mSECURE (Active)\e[0m"
else
  echo -e "\e[31mWARNING (Inactive)\e[0m"
fi
