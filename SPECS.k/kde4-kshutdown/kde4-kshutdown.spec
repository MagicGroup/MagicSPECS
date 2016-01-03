%define real_name kshutdown
%define beta %{nil}
Name: kde4-kshutdown
Summary: An advanced shut down utility for KDE
Summary(zh_CN.UTF-8): KDE 下的高级关机工具
Version:	3.2
Release: 3%{?beta}%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://kshutdown.sf.net/
Packager: Konrad Twardowski <kdtonline@poczta.onet.pl>
Source0: http://downloads.sourceforge.net/project/kshutdown/KShutdown/%{version}/kshutdown-source-%{version}%{?beta}.zip
Buildroot: %_tmppath/kshutdown-%version-%release-root
Requires: kdelibs4 >= 3.3.0
BuildRequires: kdelibs4-devel

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
%setup -q -n %{real_name}-%{version}%{?beta}

%build
pushd src
qmake-qt4 -config release
make
cp kshutdown-qt ../kshutdown-qt4
make clean
popd

mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -fr %buildroot
cd build
make install DESTDIR=%buildroot
install -m 0755 ../kshutdown-qt4 %{buildroot}%{kde4_bindir}
magic_rpm_clean.sh

%clean
rm -fr %buildroot
rm -fr $RPM_BUILD_DIR/kshutdown

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{kde4_bindir}/kshutdown*
%{kde4_appsdir}/*
%{kde4_localedir}/*
%{kde4_iconsdir}/hicolor/*/apps/*.* 
%{kde4_xdgappsdir}/*

%changelog
* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 3.2-1
- 更新到 3.2

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.0-0.beta2.1
- 为 Magic 3.0 重建


