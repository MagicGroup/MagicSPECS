 
Name: xvidcap
Version: 1.1.7
Release: 7%{?dist}
Summary: xvidcap is a screen videos capture
Summary(zh_CN.UTF-8): 屏幕录像软件 
License: GPL 
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Packager: kde <athena_star {at} 163 {dot} com>
Source0: %{name}-%{version}.tar.gz
Source1: zh_CN.xvidcap.po
Source2: xvidcap.desktop
Patch0: xvidcap_use_kaffeine_to_play.patch
Patch3: xvidcap-1.1.7-new-ffmpeg2.patch
Patch4:	xvidcap-newx.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Url: http://sourceforge.net/projects/xvidcap/
Requires(pre): /usr/bin/msgfmt
Prefix: %{_prefix}

%description
xvidcap is a screen capture enabling you to capture videos off your
X-Window desktop for illustration or documentation purposes. It is
intended to be a standards-based alternative to tools like Lotus
ScreenCam.

%description -l zh_CN.UTF-8
xvidcap 是一个屏幕捕获程序，它使您可以从您的 X-Window 桌面捕获
视频用作插图，或者用来编写文档。它试图成为一个基于标准的、类似
Lotus ScreenCam 这类工具的替代品。

%prep
%setup -q
%patch0 -p1
%patch3 -p1
%patch4 -p1

%build
./configure --prefix=/usr --with-forced-embedded-ffmpeg --enable-libmp3lame --enable-libtheora
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -d -m755 %{buildroot}/usr/share/locale/zh_CN/LC_MESSAGES/
msgfmt %{SOURCE1} -o %{buildroot}/usr/share/locale/zh_CN/LC_MESSAGES/xvidcap.mo
rm -rf %{buildroot}/usr/share/applications/xvidcap.desktop
install -D -m755 %{SOURCE2} %{buildroot}/usr/share/applications/xvidcap.desktop
#install -D -m755 %{SOURCE3} %{buildroot}/usr/share/pixmaps/xvidcap.png
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}
 
%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/dbus-1/*
%{_datadir}/gnome/help/xvidcap/*
%{_datadir}/locale/*
%{_datadir}/omf/*
%{_mandir}/man1/*
%{_datadir}/xvidcap/*
%{_docdir}/*

%changelog
* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.1.7-7
- 为 Magic 3.0 重建

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.1.7-6
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Liu Di <liudidi@gmail.com> - 1.1.7-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.7-4
- 为 Magic 3.0 重建

* Mon Dec 03 2012 Liu Di <liudidi@gmail.com> - 1.1.7-3
- 为 Magic 3.0 重建

* Fri Apr 06 2012 Liu Di <liudidi@gmail.com> - 1.1.7-2
- 为 Magic 3.0 重建

* Fri Aug 03 2007 kde <athena_star {at} 163 {dot} com> - 1.1.6-1mgc
- init the spec file
