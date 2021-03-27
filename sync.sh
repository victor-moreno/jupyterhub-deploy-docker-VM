#!/bin/bash
if [ "$1" == "from" ]; then
  rsync -av --exclude=data titan:remote/jhub/ ./
elif [ "$1" == "to" ]; then
  rsync -av ./ --exclude=data titan:remote/jhub/
else
  echo "from or to"
fi

