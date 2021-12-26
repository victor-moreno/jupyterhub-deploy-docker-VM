#!/bin/bash
cd /mnt/mimas/remote/jhub
export HOSTNAME=$(`hostname`)
# logins
echo -e "\nFailed logins\n"
/mnt/mimas/remote/jhub/logs/docker-compose logs |grep "Failed login"
# failures
echo -e "\nLogins:\n"
/mnt/mimas/remote/jhub/logs/docker-compose logs |grep "User logged"
