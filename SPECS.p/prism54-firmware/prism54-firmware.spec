%define name prism54-firmware
%define version 1.0
%define release 5%{?dist}

Summary: Firmware for the Linux prism54 driver
Summary(zh_CN.UTF-8): prism54 固件
Name: %{name}
Version: %{version}
Release: %{release}.1
Source0: %{name}-%{version}.tar.bz2
License: Maybe redistributable
Group:	System Environment/Kernel
Group(zh_CN.UTF-8):	系统环境/内核
Url: http://prism54.org/firmware/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch: noarch


%description
Firmware for the Linux Kernel prism54 driver.

%description -l zh_CN.UTF-8
Linux 内核 prism54 驱动的固件。

%prep
%setup -q

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/firmware
install -m 644 *.arm %{buildroot}/lib/firmware/


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
/lib/firmware/*.arm

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.0-5.1
- 为 Magic 3.0 重建

* Tue Aug 04 2015 Liu Di <liudidi@gmail.com> - 1.0-4.1
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Wed Jan 25 2012 Liu Di <liudidi@gmail.com> - 1.0-2
- 为 Magic 3.0 重建


