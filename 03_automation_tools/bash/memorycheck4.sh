#! /bin/bash

FREE_MEM=$(free -m | grep Mem | awk '{print $4}')
echo "DEBUG: Memory is currently $FREE_MEM"

if [ "$FREE_MEM" -lt "1000" ]; then
  echo "Warning: Memory is critically low! Only $FREE_MEM MB remaining."
else
  echo "All clear! System memory is healthy at $FREE_MEM."
fi
