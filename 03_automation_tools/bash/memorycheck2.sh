#! /bin/bash

FREE_MEM=$(free -m | grep Mem | awk '{print $4}')
echo "DEBUG: Memory is currently $FREE_MEM"

if [ "$FREE_MEM" = "3.0Gi" ]; then
  echo "Warning: Memory is at 3.0Gi"
fi
