Summary: Tools to support ATM networking under Linux
Summary(zh_CN.UTF-8): 在 Linux 下支持 ATM 网络的工具
Name: linux-atm
Version: 2.5.2
Release: 4%{?dist}
License: BSD, GPLv2+, LGPLv2+
URL: http://linux-atm.sourceforge.net/
Group: System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Older kernel headers had broken ATM includes
BuildRequires: glibc-kernheaders >= 2.4-9.1.88
BuildRequires: byacc automake libtool flex
Source: http://downloads.sf.net/linux-atm/linux-atm-%{version}.tar.gz
# Patch from Debian to sanify syslogging
Patch2: linux-atm-2.5.0-open-macro.patch
Patch3: linux-atm-2.5.0-disable-ilmidiag.patch
Patch4: linux-atm-path.patch

%description
Tools to support ATM networking under Linux.

%description -l zh_CN.UTF-8
在 Linux 下支持 ATM 网络的工具

%package libs
Summary: Linux ATM API library
Summary(zh_CN.UTF-8): %{name} 的共享库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
This package contains the ATM library required for userspace ATM tools.

%description libs -l zh_CN.UTF-8
%{name} 的共享库。

%package libs-devel
Summary: Development files for Linux ATM API library
Summary(zh_CN.UTF-8): %{name}-libs 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: linux-atm-libs = %{version}
Requires: glibc-kernheaders >= 2.4-9.1.88

%description libs-devel
This package contains header files and libraries for development using the
Linux ATM API.

%description libs-devel -l zh_CN.UTF-8
%{name}-libs 的开发包。

%prep
%setup -q
%patch2 -p1
%patch3 -p1
#%patch4 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT _doc
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libatm.la
install -m 0644 src/config/hosts.atm $RPM_BUILD_ROOT/etc/
# Selectively sort what we want included in %%doc
mkdir _doc
cp -a doc/ src/config/init-redhat/ src/extra/ANS/ _doc/
rm -f _doc/Makefile* _doc/*/Makefile* _doc/doc/*.sgml

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files 
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS ChangeLog COPYING* NEWS README THANKS _doc/*
%config(noreplace) /etc/atmsigd.conf
%config /etc/hosts.atm
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*
/lib/firmware/*

%files libs
%defattr(-, root, root, 0755)
%{_libdir}/libatm.so.*

%files libs-devel
%defattr(-, root, root, 0755)
%{_includedir}/*
%{_libdir}/libatm.a
%{_libdir}/libatm.so

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.5.2-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.5.2-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Liu Di <liudidi@gmail.com> - 2.5.2-2
- 为 Magic 3.0 重建


