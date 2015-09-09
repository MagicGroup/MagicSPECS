#!/bin/sh
@PYTHON3@ -c "import PyQt5" &> /dev/null
if [ $? -eq 0 ]; then
  exec @PYTHON3@ -m PyQt5.uic.pyuic ${1+"$@"}
else
  exec @PYTHON2@ -m PyQt5.uic.pyuic ${1+"$@"}
fi
