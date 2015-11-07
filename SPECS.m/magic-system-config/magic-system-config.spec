Summary: MagicLinux BugPatch Package
Summary(zh_CN.UTF-8): MagicLinux 补丁包
Name: magic-system-config
Version: 3.0
Release: 3%{?dist}
Source0: %{name}.tar.gz
#already include in alsa-lib
#Source1: asound.conf
Source2: crc-ccitt.h
Source3: nspluginscan.desktop
Packager:yourfeng<yourfeng@eyou.com>
License: GPL
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRoot:%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:chkconfig 
Requires:iptables, portmap, lm_sensors, nfs-utils, xorg-x11-xfs
Requires:initscripts, xinetd
#for CD
#Requires:jre = 1.6.0_10
Obsoletes: mgc-patch

%description
- Enable the alsa's multiple audio stream surport;
- Fix some bugs after the system installation
- add some commands

%description -l zh_CN.UTF-8
- 修正一些安装系统后的bug
- 添加一些命令

%prep
%setup -q -n %{name}

#%build

%install
mkdir -p $RPM_BUILD_ROOT
cp -rf * $RPM_BUILD_ROOT
# add alsa multi-sound stream surport
# install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT/etc/asound.conf
# replace the wrong crc-ccitt.h come from glibc-kernheaders-2.6.8.1-5mgc
#install -D -m644 %{SOURCE2} $RPM_BUILD_ROOT/usr/include/linux/crc-ccitt.h
# search plugins on first boot
mkdir -p $RPM_BUILD_ROOT%{_datadir}/autostart
install -D -m755 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/autostart/nspluginscan.desktop
chmod +x $RPM_BUILD_ROOT/usr/bin/*

%post
#chmod 755 /etc/init.d/rcalsasound
#ln -sf /etc/init.d/rcalsasound /usr/sbin/rcalsasound
echo "DESKTOP=KDE" > /etc/sysconfig/desktop
echo "DISPLAYMANAGER=KDM" >> /etc/sysconfig/desktop
#echo 'options ide-cd dma=1' >>/etc/modules.conf

#determine the default locale var
echo 'LANG=zh_CN.UTF-8' >>/etc/sysconfig/i18n
echo 'LC_ALL=zh_CN.UTF-8' >>/etc/sysconfig/i18n

#add local libdir
echo '/usr/local/lib' >/etc/ld.so.conf.d/magic.conf

pango-querymodules-32 >/etc/pango/pango.modules

#init prograss when the root filesystem is reiserfs, wait for user input
echo 'AUTOFSCK_DEF_CHECK=yes' >/etc/sysconfig/autofsck

#FIXME
# remove some server start links forrunlevel three
# should be removed from the "%post" section of specs
# of each packages
# 以下暂不使用
%if 0
chkconfig iptables off
chkconfig ip6tables off
chkconfig portmap off
chkconfig nfslock off
chkconfig lm_sensors off
chkconfig xfs off
chkconfig netfs off
#chkconfig pcmcia off
chkconfig xinetd off
#chkconfig rawdevices off
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/rc.d/init.d/rcalsasound
%{_sysconfdir}/timezone
%{_bindir}/*
%{_sbindir}/addplug
%{_datadir}/autostart/*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.0-3
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 3.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.6-2
- 为 Magic 3.0 重建

* Tue Apr 19 2011 Liu Di <liudidi@gmail.com> - 2.6-1
- 修改默认 Locale 为 UTF-8

* Tue Sep 09 2008 Liu Di <liudidi@gmail.com> - 2.1-9mgc
- 修改 magic_sudo_add.sh 中 pppoe 的内容

* Sun Jul 20 2008 Liu Di <liudidi@gmail.com> - 2.1-8mgc
- 添加了 addplug 命令以添加系统内所有普通用户的自动挂载

* Sun Feb 17 2008 Liu Di <liudidi@gmail.com> - 2.1-6mgc
- fix java config

* Fri Feb 23 2007 Liu Di <liudidi@gmail.com> - 2.1-3mgc
- remove some scripts, fix java version
- fix nspluginscan

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> -8mgc
- remove asound.conf

* Fri Sep 08 2006 LiuDi <liudidi2gmail.com> -7mgc
- fix pango name

* Sun May 28 2006 KanKer <kanker@163.com> -6mgc
- update jre to 1.5.0.07
- update magic_add_sudo.sh
- move java-profile.sh to here from setup

* Wed May 3 2006 KanKer <kanker@163.com> -5mgc
- update jre to 1.5.0.06

* Sun Jan 15 2006 KanKer <kanker@163.com>
- add magic_sudo_add.sh and magic_sudo_del.sh

* Thu Jan 3 2006 KanKer <kanker@163.com>
- remove pcmcia depends

* Tue Dec 29 2005 KanKer <kanker@163.com>
- set default timezone to Asia/Shanghai

* Mon Dec 19 2005 KanKer <kanker@163.com>
- rename mgc-patch to magic-system-config

* Thu Dec 13 2005 KanKer <kanker@163.com>
- move test.wav to alsa-utils

* Mon Dec 12 2005 KanKer <kanker@163.com>
- fix java chinese display bug

* Tue Nov 24 2005 KanKer <kanker@163.com>
- remove or add some services
- update 2.0

* Tue Nov 3 2005 KanKer <kanker@163.com>
- update jre directory

* Thu Nov 1 2005 KanKer <kanker@163.com>
- fix asound.conf bug

* Wed Aug 3 2005 KanKer <kanker@163.com>
- remove ip6tables and nfslock services
- fixed java chinese display bug

* Mon Jul 25 2005 KanKer <kanker@163.com>
- chmod /tmp to 1777
- remove  java's fonts setting
- set locale gb18030

* Mon Mar 14 2005 KanKer <kanker@163.com>
- add nspluginscan.sh to search plugins on first boot.

* Sun Mar 6 2005 kde <jack@linux.net.cn> 2.0.4.0-1mgc
- add asound.conf

* Wed Dec 1 2004 jackey <jackey.yang@gmail.com>
- Removed all hacks

* Mon Aug 16 2004  yourfeng <yourfeng@eyou.com> 
- yourfeng (release 1)

