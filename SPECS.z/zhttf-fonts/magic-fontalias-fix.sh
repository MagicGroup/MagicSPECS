#!/bin/sh

if [ ! -f /usr/share/fonts/ttf/zh_CN/fonts.dir ];then
	mkfontscale /usr/share/fonts/ttf/zh_CN/
	mkfontdir /usr/share/fonts/ttf/zh_CN/
fi
if [ ! -f /usr/share/fonts/pcf/zh_CN/fonts.dir ];then
	mkfontscale /usr/share/fonts/pcf/zh_CN/
	mkfontdir /usr/share/fonts/pcf/zh_CN/
fi
if ! `grep sungtil /usr/share/fonts/ttf/zh_CN/fonts.dir >/dev/null` && ! `grep kaitim /usr/share/fonts/ttf/zh_CN/fonts.dir >/dev/null` ;then
	j=0
	for i in `< /usr/share/fonts/ttf/zh_CN/fonts.dir`;do
  		if [ $j = "0" ];then
		j=$(($i + 3))
		echo "$j" >/usr/share/fonts/ttf/zh_CN/fonts.dir.tmp
		break
  	fi
	done
	sed -e '1d' /usr/share/fonts/ttf/zh_CN/fonts.dir >>/usr/share/fonts/ttf/zh_CN/fonts.dir.tmp
	echo 'wqy-zenhei.ttf -arphic-ar pl sungtil gb-medium-r-normal--0-0-0-0-p-0-iso10646-1' >>/usr/share/fonts/ttf/zh_CN/fonts.dir.tmp
	echo 'wqy-zenhei.ttf -arphic-ar pl kaitim gb-medium-r-normal--0-0-0-0-p-0-iso10646-1' >>/usr/share/fonts/ttf/zh_CN/fonts.dir.tmp
	echo 'wqy-zenhei.ttf -arphic-ar pl kaitim big5-medium-r-normal--0-0-0-0-p-0-iso10646-1' >>/usr/share/fonts/ttf/zh_CN/fonts.dir.tmp
	mv -f /usr/share/fonts/ttf/zh_CN/fonts.dir.tmp /usr/share/fonts/ttf/zh_CN/fonts.dir
fi
