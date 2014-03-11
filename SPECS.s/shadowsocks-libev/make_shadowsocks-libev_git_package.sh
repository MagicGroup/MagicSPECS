#!/bin/bash
git clone https://github.com/madeye/shadowsocks-libev.git || exit 1
mv shadowsocks-libev shadowsocks-libev-git$1
tar --remove-files -cJvf shadowsocks-libev-git$1.tar.xz shadowsocks-libev-git$1
