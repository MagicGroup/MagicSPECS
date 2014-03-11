Name:           mcs
Version:        0.7.2
Release:        3%{?dist}
Summary:        A configuration file abstraction library
Summary(zh_CN.UTF-8): 配置文件抽象层库

Group:          Applications/System
Group(zh_CN.UTF-8):	应用程序/系统
License:        BSD
URL:            http://atheme.org/projects/mcs.shtml
Source0:        http://distfiles.atheme.org/lib%{name}-%{version}.tbz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libmowgli-devel >= 0.4.0

%description
mcs is a library and set of userland tools which abstract the storage of
configuration settings away from userland applications.

It is hoped that by using mcs, that the applications which use it will
generally have a more congruent feeling in regards to settings.

There have been other projects like this before (such as GConf), but unlike
those projects, mcs strictly handles abstraction. It does not impose any
specific data storage requirement, nor is it tied to any desktop environment or
software suite.

%description -l zh_CN.UTF-8
配置文件抽象层库。

%package libs
Summary:        Library files for the mcs configuration system
Summary(zh_CN.UTF-8):	%name 的共享库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库

%description libs
mcs is a library and set of userland tools which abstract the storage of
configuration settings away from userland applications.

It is hoped that by using mcs, that the applications which use it will
generally have a more congruent feeling in regards to settings.

There have been other projects like this before (such as GConf), but unlike
those projects, mcs strictly handles abstraction. It does not impose any
specific data storage requirement, nor is it tied to any desktop environment or
software suite.

This package contains the libraries necessary for programs using mcs.

%description libs -l zh_CN.UTF-8
%name 的共享库。

%package devel
Summary:        Development files for the mcs configuration system
Summary(zh_CN.UTF-8): %name 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库

Requires:       mcs-libs = %{version}-%{release}
Requires:       pkgconfig

%description devel
mcs is a library and set of userland tools which abstract the storage of
configuration settings away from userland applications.

It is hoped that by using mcs, that the applications which use it will
generally have a more congruent feeling in regards to settings.

There have been other projects like this before (such as GConf), but unlike
those projects, mcs strictly handles abstraction. It does not impose any
specific data storage requirement, nor is it tied to any desktop environment or
software suite.

This package contains the files necessary for writing programs that use mcs.

%description devel -l zh_CN.UTF-8
%name 的开发包。

%prep
%setup -q -n libmcs-%{version}

# Make the build system more verbose
perl -pi -e 's/^\.SILENT:.*$//' buildsys.mk.in

# The build generates a wrong SONAME, fix it.
perl -pi -e "s/-soname=.*'/-soname=\\\$\{LIB\}.\\\$\{LIB_MAJOR\}'/" configure

%build
%configure \
    --disable-gconf \
    --disable-kconfig \
    --disable-dependency-tracking

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo "gconf" > $RPM_BUILD_ROOT%{_sysconfdir}/mcs-backend
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/mcs-backend
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%config(noreplace) %{_sysconfdir}/mcs-backend
%{_libdir}/*.so.*
%{_libdir}/mcs

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/libmcs
%{_libdir}/pkgconfig/libmcs.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.7.2-3
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 0.7.2-2
- 为 Magic 3.0 重建

* Tue Nov 01 2011 Liu Di <liudidi@gmail.com> - 0.7.2-1
- 更新到 0.7.2
