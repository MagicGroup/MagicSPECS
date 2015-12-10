# Note that this is NOT a relocatable package
Summary: Allows several audio streams to play on a single audio device.
Summary(zh_CN.UTF-8): 允许几个音频流在单个音频设备上播放。
Name:      esound
Version:   0.2.41
Release: 7%{?dist}
#Epoch: 1
License: GPL
URL: ftp://ftp.gnome.org/pub/GNOME/sources/esound
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Source0:   http://ftp.gnome.org/pub/GNOME/sources/esound/esound-%{version}.tar.bz2
Patch1:	   esound-0.2.41-lm.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: docbook-utils, audiofile-devel
BuildRequires: alsa-lib-devel

%description
EsounD, the Enlightened Sound Daemon, is a server process that mixes
several audio streams for playback by a single audio device. For
example, if you're listening to music on a CD and you receive a
sound-related event from ICQ, the two applications won't have to
queue for the use of your sound card.

Install esound if you'd like to let sound applications share your
audio device. You'll also need to install the audiofile package.

%description -l zh_CN.UTF-8
ESounD 是 Enlightened Sound Daemon。它是一个混合几种音频流来由单个
音频设备播放的服务器进程。例如：如果您正在收听光盘上的音乐，然后您
收到了一个来自 ICQ 的使用音效的事件，这两个程序不必排队使用您的声卡。 

如果您想让您的声音程序共享您的音频设备，安装 esound 软件包。
您还应该安装 audiofile 软件包。

%package devel
Summary: Development files for EsounD applications.
Summary(zh_CN.UTF-8): 用于 EsounD 程序的开发文件。
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: esound = %{version}-%{release}
Requires: audiofile-devel
Requires: alsa-lib-devel

%description devel
The esound-devel package includes the libraries, include files and
other resources needed to develop EsounD applications.

%description devel -l zh_CN.UTF-8
esound-devel 软件包包括开发 EsounD 程序所需的库、包含文件和其它资源。

%prep
%setup -q
%patch1 -p1

%build
autoreconf -fisv
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root,-)
%doc AUTHORS COPYING.LIB ChangeLog docs/esound.sgml
%doc NEWS README TIPS TODO
%config(noreplace) /etc/*
%{_bindir}/esd
%{_bindir}/esdcat
%{_bindir}/esdctl
%{_bindir}/esddsp
%{_bindir}/esdfilt
%{_bindir}/esdloop
%{_bindir}/esdmon
%{_bindir}/esdplay
%{_bindir}/esdrec
%{_bindir}/esdsample
%{_libdir}/*.so.*
%{_datadir}/man/man*/*
%{_datadir}/doc/*

%files devel
%defattr(-, root, root,-)
%{_bindir}/esd-config
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.2.41-7
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.2.41-6
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.2.41-5
- 为 Magic 3.0 重建

* Thu Mar 29 2012 Liu Di <liudidi@gmail.com> - 0.2.41-4
- 为 Magic 3.0 重建

* Thu Feb 02 2012 Liu Di <liudidi@gmail.com> - 0.2.41-3
- 为 Magic 3.0 重建

* Fri Nov 18 2011 Liu Di <liudidi@gmail.com> - 0.2.41-2
- 为 Magic 3.0 重建

* Wed Feb 11 2009 Liu Di <liudidi@gmail.com> - 1:0.2.41-1
- 更新到 0.2.41

* Fri Sep 26 2008 Liu Di <liudidi@gmail.com> - 1:0.2.40-1mgc
- 更新到 0.2.40

* Mon Sep 26 2005 KanKer <kanker@163.com>
- rebuild
