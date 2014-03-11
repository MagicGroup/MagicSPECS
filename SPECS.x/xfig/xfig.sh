#!/bin/bash

if [ -x /usr/bin/xfig-Xaw3d ]; then
    exec xfig-Xaw3d "$@"
else
    exec xfig-plain "$@"
fi
