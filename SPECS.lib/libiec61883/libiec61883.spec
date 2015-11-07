Summary:        Streaming library for IEEE1394
Summary(zh_CN.UTF-8): IEEE 1394 的流媒体库
Name:           libiec61883
Version:        1.2.0
Release:        6%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
Source:         http://linux1394.org/dl/%{name}-%{version}.tar.gz
Patch0:         libiec61883-1.2.0-installtests.patch
Patch1:         libiec61883-channel-allocation-without-local-node-rw.patch
URL:            http://linux1394.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
ExcludeArch:    s390 s390x

# Works only with newer libraw1394 versions
BuildRequires:  libraw1394-devel >= 1.2.1
Requires:       libraw1394 >= 1.2.1

%description

The libiec61883 library provides an higher level API for streaming DV,
MPEG-2 and audio over IEEE1394.  Based on the libraw1394 isochronous
functionality, this library acts as a filter that accepts DV-frames,
MPEG-2 frames or audio samples from the application and breaks these
down to isochronous packets, which are transmitted using libraw1394.

%description -l zh_CN.UTF-8
IEEE 1394 的流媒体库。

%package devel
Summary:        Development files for libiec61883
Summary(zh_CN.UTF-8):	%name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig, libraw1394-devel >= 1.2.1

%description devel
Development files needed to build applications against libiec61883

%description devel -l zh_CN.UTF-8
%name 的开发包。

%package utils
Summary:        Utilities for use with libiec61883
Summary(zh_CN.UTF-8): 使用 %name 的工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Requires:       %{name} = %{version}-%{release}

%description utils
Utilities that make use of iec61883

%description utils -l zh_CN.UTF-8
使用 %name 的工具。

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/libiec61883.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libiec61883.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libiec61883.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libiec61883.so
%dir %{_includedir}/libiec61883
%{_includedir}/libiec61883/*.h
%{_libdir}/pkgconfig/libiec61883.pc

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.2.0-6
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.2.0-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.0-4
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建


