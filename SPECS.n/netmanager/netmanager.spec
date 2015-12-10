Name: netmanager
Summary: Networking manager tools
Summary(zh_CN.UTF-8): 一个网络管理工具
Version: 0.1.6
Release: 6%{?dist}
License: GPL v2
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: %{name}-%{version}.tar.gz
Source1: netmanager.desktop
Packager: stronghill <stronghill {at} 163 {dot} com>
Distribution: MagicLinux
URL: http://www.linuxfans.org/
Vendor: MGC Group

%description
Netmanager Tools

Author:
	stronghill

%description -l zh_CN.UTF-8
一个网络管理工具。

%prep
%setup -q

%build
qmake4
make clean
qmake4
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/applications

install -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -m 644 tong.jpg %{buildroot}%{_datadir}/pixmaps/%{name}/tong.jpg
install -m 644 butong.jpg %{buildroot}%{_datadir}/pixmaps/%{name}/butong.jpg
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications
install -m 644 netmanagerzh_CN.UTF-8.qm %{buildroot}%{_datadir}/%{name}/netmanagerzh_CN.UTF-8.qm
install -m 644 netmanagerzh_CN.UTF-8.qm %{buildroot}%{_datadir}/%{name}/netmanagerzh_CN.UTF-8.qm
install -m 644 netmanager.qm %{buildroot}%{_datadir}/%{name}/netmanager.qm
install -m 644 netmanager.ts %{buildroot}%{_datadir}/%{name}/netmanager.ts

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post


%preun


%postun


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/pixmaps/%{name}/*
%{_datadir}/applications/*
%{_datadir}/netmanager/*.qm
%{_datadir}/netmanager/netmanager.ts

%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 0.1.6-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.1.6-5
- 为 Magic 3.0 重建

* Mon Jan 26 2015 Liu Di <liudidi@gmail.com> - 0.1.6-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.1.6-3
- 为 Magic 3.0 重建

* Tue Dec 20 2011 Liu Di <liudidi@gmail.com> - 0.1.6-2mgc
- 为 Magic 3.0 重建
