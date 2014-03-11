Summary: A tool for determining compilation options
Summary(zh_CN.UTF-8): 决定编译选项的工具
Name: pkgconfig
Version: 0.25
Release: 3%{?dist}
Epoch: 1
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Source:  http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
BuildRequires: glib2-devel
BuildRequires: popt-devel

# don't call out to glib-config, since our glib-config is a pkg-config wrapper
Patch2:  pkg-config-0.21-compat-loop.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=16095
Patch3: pkg-config-lib64-excludes.patch
# workaround for breakage with autoconf 2.66
# https://bugzilla.redhat.com/show_bug.cgi?id=611781
Patch4: pkg-config-dnl.patch

Provides: pkgconfig(pkg-config) = %{version}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%description -l zh_CN.UTF-8
pkgconfig 工具决定编译选项。它为每一个需要的库读取配置文件，然后输出
必要的编译器和链接器标记。

%prep
%setup -n pkg-config-%{version} -q
%patch2 -p1 -b .compat-loop
%patch3 -p0 -b .lib64
%patch4 -p1 -R -b .dnl

%build
%configure \
        --disable-shared \
        --with-installed-glib \
        --with-installed-popt \
        --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig

# we include this below, already
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/pkg-config

%files
%defattr(-,root,root)
%doc AUTHORS README COPYING pkg-config-guide.html
%{_mandir}/*/*
%{_bindir}/*
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%{_datadir}/aclocal/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:0.25-3
- 为 Magic 3.0 重建

* Fri Nov 23 2007 Liu Di <liudidi@gmail.com> 0 1:0.22-1mgc
- update to 0.22

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 1:0.21-1mgc
- update to 0.21

* Tue Aug 2 2005 KanKer <kanker@163.com>
- rebuild
