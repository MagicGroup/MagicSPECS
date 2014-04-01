Name:           eeze
Version:	1.7.10
Release:        1%{?dist}
License:        BSD and GPLv2+
Summary:        Device abstraction library
Summary(zh_CN.UTF-8): 设备抽象库
Url:            http://enlightenment.org
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
BuildRequires:  ecore-devel 
BuildRequires:  libeina-devel >= %{version}
BuildRequires:  systemd-devel

%description
Eeze is a library for manipulating devices through udev with a simple and fast
api. It interfaces directly with libudev, avoiding such middleman daemons as 
udisks/upower or hal, to immediately gather device information the instant it 
becomes known to the system.

%description -l zh_CN.UTF-8
设备抽象层库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, test programs and documentation for eeze

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install utildir=%{_libdir}/enlightenment/utils

find %{buildroot} -name '*.la' -delete

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README COPYING NEWS AUTHORS
%{_libdir}/libeeze.so.1*
%{_libdir}/enlightenment/utils/eeze_scanner
%{_bindir}/eeze_disk_ls
%{_bindir}/eeze_mount
%{_bindir}/eeze_umount

%files devel
%{_includedir}/eeze-1
%{_libdir}/pkgconfig/eeze.pc
%{_libdir}/libeeze.so

%changelog
* Sat Mar 29 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Mon Aug 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Update license to GPLv2 and BSD

* Mon Aug 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7
- Clean up spec file

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec
