#!/bin/sh

if [ "$#" = 2 ]; then
  if [ "$1" = "-U" ]; then
    exec socat stdio "$2"
  elif [ "$2" = "-U" ]; then
    exec socat stdio "$1"
  fi
fi

exec ncat "$@"
