%define git 1
%define vcsdate 20151031

Name:		libcec
Version:	2.1.4
Release:	6%{?dist}
Summary:	Library and utilities for HDMI-CEC device control
Summary(zh_CN.UTF-8): HDMI-CEC 设备控制的库和工具

License:	GPLv2+
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://libcec.pulse-eight.com/
Source0:	%{name}-%{gitdate}.tar.xz
Source1:	make_libcec_git_package.sh
BuildRequires:	pkgconfig(libudev)

%description
With libcec you can access your Pulse-Eight CEC adapter.

%description -l zh_CN.UTF-8
HDMI-CEC 设备控制的库和工具。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}
Provides:	cec-devel = %{version}

%description devel
With libcec you can access your Pulse-Eight CEC adapter.

This package contains the files for developing applications which
will use libcec.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{gitdate}

%build
autoreconf -ifv
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
rm %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post 
/usr/sbin/ldconfig

%postun
/usr/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/cec-client
%{_bindir}/cec-config
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.1.4-6
- 更新到 20151031 日期的仓库源码

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.1.4-5
- 为 Magic 3.0 重建

* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 2.1.4-4
- 更新到 20140714 日期的仓库源码

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.5-0.git20120709.1.1
- 为 Magic 3.0 重建

