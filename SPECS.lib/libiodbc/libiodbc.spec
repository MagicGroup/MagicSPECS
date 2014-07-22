
## admin gui build currently busted, FIXME?
#define _enable_gui --enable-gui

Summary: iODBC Driver Manager
Summary(zh_CN.UTF-8): iODBC 驱动管理器
Name: libiodbc
Version: 3.52.9
Release: 1%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2 or BSD
URL: http://www.iodbc.org/
Source0: http://downloads.sourceforge.net/project/iodbc/iodbc/%{version}/libiodbc-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Patch1: libiodbc-3.52.9-multilib.patch

%{?_enable_gui:BuildRequires: gtk2-devel}
BuildRequires: chrpath

%description
The iODBC Driver Manager is a free implementation of the SAG CLI and
ODBC compliant driver manager which allows developers to write ODBC
compliant applications that can connect to various databases using
appropriate backend drivers.

%description -l zh_CN.UTF-8
iODBC 驱动管理器。

%package devel
Summary: Header files and libraries for iODBC development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release} 
Requires: pkgconfig
%description devel
This package contains the header files and libraries needed to develop
programs that use the driver manager.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package admin
Summary: Gui administrator for iODBC development
Summary(zh_CN.UTF-8): iODBC 开发使用的图形界面管理器
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
%description admin
This package contains a Gui administrator program for maintaining
DSN information in odbc.ini and odbcinst.ini files.

%description admin -l zh_CN.UTF-8
iODBC 开发使用的图形界面管理器.

%prep
%setup -q

%patch1 -p1 -b .multilib

# fix header permissions
chmod -x include/*.h


%build
# --disable-libodbc to minimize conflicts with unixODBC
%configure \
  --enable-odbc3 \
  --with-iodbc-inidir=%{_sysconfdir} \
  --enable-pthreads \
  --disable-libodbc \
  --disable-static \
  --includedir=%{_includedir}/libiodbc \
  %{?_enable_gui} %{!?_enable_gui:--disable-gui}

make %{?_smp_mflags}


%install
rm -rf %{buildroot} 

make install DESTDIR=%{buildroot}

# nuke rpaths
chrpath --delete %{buildroot}%{_bindir}/iodbctest
chrpath --delete %{buildroot}%{_bindir}/iodbctestw

# unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la
rm -rf %{buildroot}%{_datadir}/libiodbc/samples
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE* README
%doc etc/odbc*.ini.sample
%{_bindir}/iodbctest
%{_bindir}/iodbctestw
%{_libdir}/libiodbc.so.2*
%{_libdir}/libiodbcinst.so.2*
%{_mandir}/man1/iodbctest.1*
%{_mandir}/man1/iodbctestw.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/iodbc-config
%{_includedir}/libiodbc/
%{_libdir}/libiodbc.so
%{_libdir}/libiodbcinst.so
%{_mandir}/man1/iodbc-config.1*
%{_libdir}/pkgconfig/libiodbc.pc

%if 0%{?_enable_gui:1}
%files admin
%defattr(-,root,root,-)
%{_bindir}/iodbcadm-gtk
%{_libdir}/libdrvproxy.so*
%{_libdir}/libiodbcadm.so*
%{_mandir}/man1/iodbcadm-gtk.1*
%endif

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 3.52.9-1
- 更新到 3.52.9

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.52.7-5
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Liu Di <liudidi@gmail.com> - 3.52.7-4
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 3.52.7-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.7-1
- libiodbc-3.52.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-4
- -devel: install headers to /usr/include/libiodbc/ to better avoid
  conflicts and need for bogus unixODBC-devel dep

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-3
- capitalize Name,Summary,Version tags
- -devel: capitalize Summary
- fix spurious permissions on header files
- refresh upstream source
- -admin,-devel: add %%defattr(...)

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-2
- iodbc-config multilib patch

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 3.52.6-1
- first try, based on upstream src.rpm

