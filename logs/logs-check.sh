#!/bin/bash
export HOSTNAME=$(hostname)
if [ "$HOSTNAME" == "cuda*" ]; then 
  NODE=cuda
else
  NODE=mimas
fi 
cd /mnt/${NODE}/remote/jhub
# logins
echo -e "\nFailed logins\n"
/mnt/${NODE}/remote/jhub/logs/docker-compose logs |grep "Failed login"
# failures
echo -e "\nLogins:\n"
/mnt/${NODE}/remote/jhub/logs/docker-compose logs |grep "User logged"
