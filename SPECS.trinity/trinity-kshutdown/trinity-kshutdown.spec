Name: kshutdown
Summary: An advanced shut down utility for KDE
Summary(zh_CN.UTF-8): KDE 下的高级关机工具
Version: 1.0.4
Release: 1%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://kshutdown.sf.net/
Packager: Konrad Twardowski <kdtonline@poczta.onet.pl>
Source0: kshutdown-%version.tar.bz2
Patch1: kshutdown-1.0.4-admin.patch
Buildroot: %_tmppath/kshutdown-%version-%release-root
Requires: kdelibs >= 3.3.0
BuildRequires: kdelibs-devel

%description
KShutDown is an advanced shut down utility for KDE.
Features:
- Turn Off Computer (logout and halt the system)
- Restart Computer (logout and reboot the system)
- Lock Session (lock the screen using a screen saver)
- End Current Session (end the current KDE session and logout the user)
- Extras (additional, user commands)
- Time and delay options
- Command line and DCOP support
- System tray and panel applet
- Visual and sound notifications
- KDE Kiosk support
- And more...

%description -l zh_CN.UTF-8
KDE 下的高级关机工具

%prep
%setup -q
%patch1 -p1
chmod 777 admin/*

%build
make -f admin/Makefile.common
%configure --enable-final
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-ltdefx \-lDCOP \-lkio/g' kshutdown*/Makefile
make

%install
rm -fr %buildroot
make install DESTDIR=%buildroot
magic_rpm_clean.sh
cd %buildroot
find . -type d | sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' > $RPM_BUILD_DIR/file.list.kshutdown
find . -type f | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.kshutdown
find . -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.kshutdown

%clean
rm -fr %buildroot
rm -fr $RPM_BUILD_DIR/kshutdown
rm -fr ../file.list.kshutdown

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f ../file.list.kshutdown

%changelog

