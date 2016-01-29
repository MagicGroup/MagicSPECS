Name:           libifp
Version:        1.0.0.2
Release:        10%{?dist}
Summary:        A general-purpose library-driver for iRiver's iFP portable audio players
Summary(zh_CN.UTF-8): 一个iRiver的iFP可移动音频播放器的多用途的驱动库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
License:        GPL
URL:            http://ifp-driver.sourceforge.net/
Source0:        http://dl.sourceforge.net/ifp-driver/%{name}-%{version}.tar.gz
Source1:        libifp.hotplug
Source2:        10-libifp.rules
# autoconf-2.69 breaks configure.in (likely configure.in is the broken part)
# Upstream is dead, so fix it here:
Patch0:         libifp-1.0.0.2-fix-broken-configure.in.diff
Patch1:         libifp-1.0.0.2-fix-broken-configure-again.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libusb-devel doxygen

%description
libifp is a general-purpose library-driver for iRiver's iFP (flash-based)
portable audio players. The source code is pure C and is fairly portable.

Also included is a console app that uses the library.

%description -l zh_CN.UTF-8
libifp是一个iRiver的iFP(基于闪存)可移动音频播放器的多用途的驱动库。源码是纯C
的，所以好移植。

也包括了一个使用这个库的命令行应用

%package        devel
Summary:        Headers and libraries for developing with libifp
Summary(zh_CN.UTF-8):	使用libifp开发所需要的头文件和库
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains headers and libraries for developing apps that use
libifp.

%description devel -l zh_CN.UTF-8
这个包包含了使用libifo开发应用所需要的头文件和库。

%prep
%autosetup 

%build
autoreconf -fisv
%configure --with-libusb --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
install -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/libifp-hotplug
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/udev/rules.d/10-libifp.rules
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_sbindir}/*
/usr/lib/udev/rules.d/*.rules

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_mandir}/man3/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.0.0.2-10
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.0.2-9
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.0.0.2-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.0.2-7
- 为 Magic 3.0 重建

* Mon Oct 29 2012 Liu Di <liudidi@gmail.com> - 1.0.0.2-6
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.0.0.2-5
- 为 Magic 3.0 重建

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.0.2-2
- Rebuild for Fedora Extras 5

* Mon Aug 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.0.2-1
- Upstream update
- Disabled build of static libraries

* Thu Jul 14 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.0.1-2
- Modified for new udev

* Thu Jul  7 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net>
- Added Per Bjornsson's hotplug files

* Wed Jun 29 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.0.1-1
- Initial RPM release
