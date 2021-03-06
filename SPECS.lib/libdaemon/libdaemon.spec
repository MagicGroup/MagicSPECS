Name: libdaemon
Version: 0.14
Release: 7%{?dist}
Summary: Library for writing UNIX daemons
Summary(zh_CN.UTF-8): 编写 UNIX 下服务的库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+
URL: http://0pointer.de/lennart/projects/libdaemon/
Source0: http://0pointer.de/lennart/projects/libdaemon/%{name}-%{version}.tar.gz

# Requires lynx to build the docs
BuildRequires:  lynx

%description
libdaemon is a lightweight C library which eases the writing of UNIX daemons.
It consists of the following parts:
* A wrapper around fork() which does the correct daemonization
  procedure of a process
* A wrapper around syslog() for simpler and compatible log output to
  Syslog or STDERR
* An API for writing PID files
* An API for serializing UNIX signals into a pipe for usage with
  select() or poll()
* An API for running subprocesses with STDOUT and STDERR redirected
  to syslog.

%description -l zh_CN.UTF-8
编写 UNIX 下服务的库。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Libraries and header files for libdaemon development
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: libdaemon = %{version}-%{release}

%description devel
The libdaemon-devel package contains the header files and libraries
necessary for developing programs using libdaemon.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;

rm $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/README
rm $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/README.html
rm $RPM_BUILD_ROOT/%{_datadir}/doc/libdaemon/style.css
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%doc doc/README.html doc/style.css
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.14-4
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.14-3
- 为 Magic 3.0 重建

