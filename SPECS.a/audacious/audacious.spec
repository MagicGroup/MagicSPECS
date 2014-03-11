%define name audacious
%define version 3.4.3
%define testver %{nil}
%if 0%{?testver}
%define release 0.%{testver}.1%{?dist}.2
%else
%define release 1%{?dist}
%endif

Name:		%{name}
Summary:	Audacious
Summary(zh_CN.UTF-8): Audacious 媒体播放器
Version:	%{version}
Release:	%{release}

%if 0%{?testver}
Source: 	http://distfiles.atheme.org/audacious-%{version}-%{testver}.tar.bz2
%else
Source:		http://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2
%endif

Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:		http://www.audacious-media-player.org/
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libguess-devel
BuildRequires:  libmowgli-devel mcs-devel
%description
Audacious is a fork of Beep Media Player(BMP).
Beep Media Player(BMP) is a GTK2 port of the popular X Multimedia
System(XMMS) and more.

%description -l zh_CN.UTF-8
Audacious 是 Beep 媒体播放器 (BMP) 的一个移植。
Beep 媒体播放器 (BMP) 是流行的 X 媒体播放系统 (XMMS) 的 GTK2 移植。

%package	devel
Summary:	Libraries and header files for Audacious.
Summary(zh_CN.UTF-8): Audacious 的库和头文件。
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}

%description	devel
Libraries and header files required for compiling Audacious plugins.

%description devel -l zh_CN.UTF-8
编译 Audacious 插件需要的库和头文件。

%prep
%if 0%{?testver}
%setup -q -n %{name}-%{version}-%{testver}
%else
%setup -q
%endif

%build
%configure CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"  --enable-chardet 

make  %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir} 

%files
%defattr(-, root, root)
%doc AUTHORS COPYING
%{_bindir}/aud*
%{_libdir}/lib*
%{_datadir}/applications/audacious*.desktop
%{_datadir}/audacious/*
%{_datadir}/locale/*
%{_datadir}/man/*
%{_datadir}/icons/hicolor/*/apps/*.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/audacious/*
%{_includedir}/libaudcore/*
%{_includedir}/libaudgui/*
%{_libdir}/pkgconfig/*

%changelog
* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 3.4.3-1
- 更新到 3.4.3

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 3.1-0.beta3.1
- 更新到 3.1 beta3

* Sat Jul 06 2009 Liu Di <liudidi@gmail.com> - 2.0.1-1
- 更新到 2.0.1

* Sun Mar  4 2007 Jiang Tao <jiangtao9999@163.com> 1.3.0
- Update to 1.3.0 final releas.

* Sun Jul 16 2006 Jiang Tao <jiangtao9999@163.com> 1.1.0
- Update to 1.1.0
- Timidity-plug seem to can't work, so disable it.
- Enable the "character set detection support" to support chinese char (--enable-chardet), hope it work fine.
- The po file is too old, I think i neet to get a new .pot.

* Thu Jun 29 2006 Jiang Tao <jiangtao9999@163.com> 1.1.0dr2
- Update to 1.1.0dr2

* Wed Apr 19 2006 Jiang Tao <jiangtao9999@163.com> 1.0.0
- Update to 1.0.0

* Sun Apr 02 2006 Jiang Tao <jiangtao9999@163.com> 0.2.3
- Create spec file and rebuild

