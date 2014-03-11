Summary: A library for accessing various audio file formats
Summary(zh_CN.UTF-8): 访问多种音频文件格式的库
Name: audiofile
Version: 0.3.6
Release: 1%{?dist}
Epoch: 1
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://www.68k.org/~michael/audiofile/audiofile-%{version}.tar.gz
URL: http://www.68k.org/~michael/audiofile/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
BuildRequires: libtool

%description
The Audio File library is an implementation of the Audio File Library
from SGI, which provides an API for accessing audio file formats like
AIFF/AIFF-C, WAVE, and NeXT/Sun .snd/.au files. This library is used
by the EsounD daemon.

Install audiofile if you are installing EsounD or you need an API for
any of the sound file formats it can handle.

%description -l zh_CN.UTF-8
访问多种音频文件格式的库，

%package devel
Summary: Development files for Audio File applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig >= 1:0.8

%description devel
The audiofile-devel package contains libraries, include files, and
other resources you can use to develop Audio File applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags} CXXFLAGS="$CXXFLAGS -Wno-unused-but-set-variable" LDFLAGS="$LDFLAGS -lm"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f docs/Makefile*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc COPYING TODO README ChangeLog docs
%{_bindir}/sfconvert
%{_bindir}/sfinfo
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/*

%changelog
* Sun Mar 02 2014 Liu Di <liudidi@gmail.com> - 1:0.3.6-1
- 更新到 0.3.6

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1:0.3.3-3
- 为 Magic 3.0 重建

* Thu Mar 29 2012 Liu Di <liudidi@gmail.com> - 1:0.3.3-2
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 1:0.3.1-1
- 更新到 0.3.1

