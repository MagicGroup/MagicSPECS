Name:           kmldonkey
Version:        0.11
Release:        1%{?dist}
Summary:        Advanced GUI frontend for the MLDonkey P2P core.
Summary(zh_CN): MLDonkey P2P 核心的高级界面前端。
Group:          Applications/Internet
Group(zh_CN):	应用程序/互联网
License:        GPL
URL:            http://kmldonkey.org/
Source0:        http://mirrors.ustc.edu.cn/kde/stable/apps/KDE3.x/network/kmldonkey-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  desktop-file-utils
BuildRequires: qt-devel 
Requires: qt 

BuildRequires: kdelibs-devel >= 3.2
Requires: kdelibs

Requires:       mldonkey
Conflicts:      mldonkey-ed2k-support

Patch0: shareinfo-filename.patch
Patch1:	kmldonkey-0.11-admin.patch

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
%setup -q
%patch0 -p1
%patch1 -p1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
make -f admin/Makefile.common

%configure \
  --disable-rpath \
  --disable-debug --disable-warnings 
#临时措施
for i in kmldonkey/kmldonkey/plugins/debugpage/Makefile kmldonkey/kmldonkey/Makefile kmldonkey/kio_mldonkey/Makefile kmldonkey/scripts/Makefile;do
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-ltdefx \-lDCOP \-lkio \-L\/usr\/lib\/qt\-3\.3\/lib/g' $i
done
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

## Unpackaged files
# these are safe to remove -- Rex
rm -f %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_bindir}/*
%{_datadir}/apps/%{name}
%{_mandir}/man[^3]/*
%{_datadir}/applications/*
%{_datadir}/apps/kicker/applets/mldonkeyapplet.desktop
%{_datadir}/apps/konqueror/servicemenus/*
%{_datadir}/apps/mldonkeyapplet/
%{_datadir}/icons/*/*/*/*
%{_datadir}/services/*
%{_datadir}/servicetypes/*
%{_libdir}/lib*.so.*
%{_libdir}/trinity/*.so*
%{_libdir}/trinity/*.la
%{_docdir}/HTML/en/*

%files devel
%{_includedir}/kmldonkey/*
%{_libdir}/*.so

%changelog
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
