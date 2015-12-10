%define real_name kmldonkey
Name:           kde4-kmldonkey
Version:        2.0.7
Release:        6%{?dist}
Summary:        Advanced GUI frontend for the MLDonkey P2P core.
Summary(zh_CN): MLDonkey P2P 核心的高级界面前端。
Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPL
URL:            http://kmldonkey.org/
Source0:        https://api.opensuse.org:443/public/source/home:eduardhc/kmldonkey-kde4/kmldonkey-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  desktop-file-utils
BuildRequires: qt4-devel 
Requires: qt4 

BuildRequires: kdelibs4-devel >= 4.0
Requires: kdelibs4

Requires:       mldonkey
Conflicts:      mldonkey-ed2k-support

%description
KMLDonkey is a frontend for MLDonkey, a powerful P2P file sharing tool,
designed for the KDE desktop.
Feature Overview:
  * A flexible, powerful and KDE Style Guide compliant graphical interface.
  * A complete implementation of the MLDonkey GUI protocol, meaning
    KMLDonkey can do everything the original GUI does.
  * A convenient and configurable on-demand MLDonkey launcher.
  * Real-time graphical bandwidth and network statistics.
  * MobileMule middleware for controlling your MLDonkey using your Java
    enabled mobile phone.
  * Embedded previewing of all downloads using KParts viewers.
  * Embedded web browser providing P2P related web services such as
    availability and fake checks.
  * KDE panel applet for statistics and easy access to the GUI.
  * KIOSlave for opening current and complete downloads in all KDE
    applications (eg. "mldonkey:/Default/downloading/")

%description -l zh_CN
KMLDonkey 是 MLDonkey 一个 KDE 桌面的前端，MLDonkey 是一个很强的 P2P 
文件分享工具。

%package devel
Summary:      Header files for %{name}
Summary(zh_CN): %{name} 的头文件
Group:	      Development/Libraries
Group(zh_CN): 开发/库
License:      GPL
Requires:     %{name} = %{version}

%description devel
Header files for %{name}

%description devel -l zh_CN
%{name} 的头文件

%prep
%setup -q -n %{real_name}-%{version}

%build
mkdir build
cd build
%cmake_kde4 ..
make

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

## Unpackaged files
# these are safe to remove -- Rex
#rm -f %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%{kde4_bindir}/*
%{kde4_appsdir}/%{real_name}
%{kde4_datadir}/applications/*
%{kde4_iconsdir}/*/*/*/*
%{kde4_servicesdir}/*
%{kde4_libdir}/lib*.so.*
%{kde4_plugindir}/plasma_*_kmldonkey.so

%files devel
%{kde4_includedir}/kmldonkey/*
%{kde4_libdir}/*.so

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.0.7-6
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.0.7-5
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.0.7-4
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.0.7-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.7-2
- 为 Magic 3.0 重建

* Sun Aug 12 2007 Ni Hui <shuizhuyuanluo@126.com> -0.10.1-4.1mgc
- add a shareinfo-filename patch to fix the unsuitable encoding of the shared files

* Sat Aug 11 2007 Liu Di <liudidi@gmail.com> - 0.10.1-4mgc
- change chinese language file

* Sat May 13 2006 Liu Di <liudidi@gmail.com>
- rebuild for MagicLinux 2.0

* Fri Nov 25 2005 sejishikong <sejishikong@263.net> 
- Rebuild for Magiclinux 2.0rc1,update to 0.10.1

* Sun Jan 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.10-0.lvn.3
- fix .desktop naming (applet hardcodes looking for kmldonkey.desktop)

* Wed Jan 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.10-0.lvn.2
- -devel subpkg
- qt/kdelibs Req's for fc2/fc3

* Mon Nov 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.10-0.lvn.1
- 0.10 final

* Mon Sep 13 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.10-0.lvn.0.1.pre4
- update to 0.10pre4

* Mon Jun 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.1-0.lvn.1
- Initial RPM release.
