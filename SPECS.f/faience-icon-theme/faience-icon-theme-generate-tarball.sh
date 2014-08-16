#!/bin/sh

# Regenerate faience-icon-theme tarball without copyrighted trademarks

name=faience-icon-theme_0.5
theme_name=Faience

# unpack the zip archive
unzip $name -d $name

# unpack the icon tarballs
cd $name
tar -xzf $theme_name.tar.gz
tar -xzf $theme_name-Azur.tar.gz
tar -xzf $theme_name-Claire.tar.gz
tar -xzf $theme_name-Ocre.tar.gz

# remove nonfree and unneeded icons
find $theme_name*/ -name '*flash*' -exec rm -rf {} ';'
find $theme_name*/ -name '*amazon*' -exec rm -rf {} ';'
find $theme_name*/ -name '*gmail*' -exec rm -rf {} ';'
find $theme_name*/ -name '*chromium*' -exec rm -rf {} ';'
find $theme_name*/ -name '*dropbox*' -exec rm -rf {} ';'
find $theme_name*/ -name '*evernote*' -exec rm -rf {} ';'
find $theme_name*/ -name '*facebook*' -exec rm -rf {} ';'
find $theme_name*/ -name '*firefox*' -exec rm -rf {} ';'
find $theme_name*/ -name '*google*' -exec rm -rf {} ';'
find $theme_name*/ -name '*twitter*' -exec rm -rf {} ';'
find $theme_name*/ -name '*gtwitter*' -exec rm -rf {} ';'
find $theme_name*/ -name '*launchpad*' -exec rm -rf {} ';'
find $theme_name*/ -name '*mandriva*' -exec rm -rf {} ';'
find $theme_name*/ -name '*mendeley*' -exec rm -rf {} ';'
find $theme_name*/ -name '*thunderbird*' -exec rm -rf {} ';'
find $theme_name*/ -name '*nixnote*' -exec rm -rf {} ';'
find $theme_name*/ -name '*ppa*' -exec rm -rf {} ';'
find $theme_name*/ -name '*rpmdrake*' -exec rm -rf {} ';'
find $theme_name*/ -name '*skype*' -exec rm -rf {} ';'
find $theme_name*/ -name '*softwarecenter*' -exec rm -rf {} ';'
find $theme_name*/ -name '*steam*' -exec rm -rf {} ';'
find $theme_name*/ -name '*susehelpcenter*' -exec rm -rf {} ';'
find $theme_name*/ -name '*twitux*' -exec rm -rf {} ';'
find $theme_name*/ -name '*ubuntu*' -exec rm -rf {} ';'
find $theme_name*/ -name '*wunderlist*' -exec rm -rf {} ';'
find $theme_name*/ -name '*Wunderlist*' -exec rm -rf {} ';'
find $theme_name*/ -name '*yahoo*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-archlinux-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-debian-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-frugalware-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-gentoo-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-linux-mint-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-opensuse-symbolic*' -exec rm -rf {} ';'
find $theme_name*/ -name '*start-here-slackware-symbolic*' -exec rm -rf {} ';'

# Delete dead icon symlinks
find -L . -type l -exec rm {} \;

# remove faenza-icon-theme dep
sed -i "s/Inherits=Faenza,gnome,hicolor/Inherits=gnome,hicolor/" $theme_name/index.theme

# remove old icon tarballs
rm -f $theme_name.tar.gz
rm -f $theme_name-Azur.tar.gz
rm -f $theme_name-Claire.tar.gz
rm -f $theme_name-Ocre.tar.gz

# create new icon tarballs
tar -czf $theme_name.tar.gz $theme_name/
tar -czf $theme_name-Azur.tar.gz $theme_name-Azur/
tar -czf $theme_name-Claire.tar.gz $theme_name-Claire/
tar -czf $theme_name-Ocre.tar.gz $theme_name-Ocre/

# remove extracted icon dirs
rm -rf $theme_name
rm -rf $theme_name-Azur
rm -rf $theme_name-Claire
rm -rf $theme_name-Ocre

# create the tarball and clean directory
cd ..
tar -cf - $name/ | xz -9 -c - > $name.tar.xz 
rm -rf $name

echo "tarball created"
exit
