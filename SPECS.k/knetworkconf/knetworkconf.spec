# This spec file was generated using Kpp
# If you find any problems with this spec file please report
# the error to ian geiser <geiseri@msoe.edu>
%define name knetworkconf
%define version 0.6.1
%define release 5%{?dist}

Summary:   A KDE application to configure TCP/IP settings.
Summary(zh_CN.UTF-8): 配置TCP/IP设置的KDE程序。
Name:      %{name}
Version:   %{version}
Release:   %{release}
License: GPL
Url:       http://www.merlinux.org/knetworkconf/
Group:     Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source:    %{name}-%{version}.tar.bz2
Patch0:knetworkconf-magic-only.patch
Patch1:knetworkconf-chinese.patch
Patch2:knetworkconf-0.6.1-admin.patch
BuildRoot:  %{_tmppath}/%{name}-buildroot
Requires: %_bindir/tdesu

%description
KNetworkConf is a KDE application to configure  TCP/IP settings
in a Linux machine. I developed it because I couldn't find any
application to configure TCP/IP settings from within KDE, and I
think this is a "must have" app for a serious Desktop Enviroment
like KDE.
KNetworkConf can configure installed network devices (you can't
add new ones for now), the default gateway,host and domain names,
and add/remove DNS servers. This first version is a standalone
application, but the idea is to make it a KDE Control Center
module and a KApplet to have a fast access to it from the KDE
panel.

%description -l zh_CN.UTF-8
KNetworkConf是一个在Linux机器上配置TCP/IP设置的KDE应用程序。

%prep
%setup 
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
#mkdir -p $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES/
#mv $RPM_BUILD_ROOT/usr/share/locale/zh_CN.GB2312/LC_MESSAGES/knetworkconf.mo $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES/
#rm -rf $RPM_BUILD_ROOT/usr/share/locale/zh_CN.GB2312
mv $RPM_BUILD_ROOT/usr/share/icons/default.kde $RPM_BUILD_ROOT/usr/share/icons/crystalsvg
rm -rf $RPM_BUILD_ROOT/usr/lib/pkgconfig/*

magic_rpm_clean.sh 

%clean
rm -rf $RPM_BUILD_ROOT


%files 
%defattr(-,root,root)
%doc README COPYING AUTHORS LEAME
/usr
%exclude /usr/*/debug*
%exclude /usr/share/doc/HTML/*

%changelog
* Tue Aug 31 2006 KanKer <kanker@163.com> -0.6.1-4mgc
- remove *.pc

* Sat Jan 14 2006 KanKer <kanker@163.com>
- move gateway setting to config file of eth

* Wed Dec 7 2005 KanKer <kanker@163.com>
- fix a bug in networkconfigparser

* Tue Jun 23 2005 KanKer <kanker@163.com>
- update 0.6.1

* Tue May 26 2005 KanKer <kanker@163.com>
- rebuild

* Thu Sep 16 2004 KanKer <kanker@163.com>
- fix spec for magiclinux,make a patch to support magiclinux.
 
* Sun Feb 22 2004 Juan Luis Baptiste <juan.baptiste@kdemail.net> 0.5-1mdk
- 0.5

* Thu Oct 02 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.2-1mdk
- 0.4.2

* Fri Jul 18 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 0.4.1-2mdk
- Rebuild

* Thu Apr 10 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.1-1mdk
- 0.4.1
- find lang macro

* Fri Mar 28 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4-1mdk
- from Juan Luis Baptiste <juancho@linuxmail.org> :
	- Initial release.
