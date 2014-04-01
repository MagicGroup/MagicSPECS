#!/bin/bash
hg clone http://linuxtv.org/hg/dvb-apps/ || exit 1
mv dvb-apps dvb-apps-hg$1
tar Jcvf dvb-apps-hg$1.tar.xz dvb-apps-hg$1
