%define name atmel-firmware
%define version 1.3
%define release 6%{?dist}
%define url http://www.thekelleys.org.uk/

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	Distributable
Group:		System Environment/Kernel
Group(zh_CN.UTF-8):	系统环境/内核
URL: 		%{url}
Source0: 	%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Summary: 	Firmware for Atmel at76c50x wireless network chips
Summary(zh_CN.UTF-8):	Atmel at76c50x 无线网络芯片固件
BuildArch: 	noarch

%description
The drivers for Atmel at76c50x wireless network chips in the
Linux 2.6.x kernel and at http://at76c503a.berlios.de/ do not 
include the firmware and this firmware needs to be loaded by 
the host on most cards using these chips. 
This package provides the firmware images which 
should be automatically loaded as needed by the hotplug system. It also 
provides a small loader utility which can be used to accomplish the 
same thing when hotplug is not in use. 

%description -l zh_CN.UTF-8
Atmel at76c50x 无线网络芯片在 Linux 2.6 内核下的驱动固件。

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

mkdir -p -m 755 %{buildroot}/lib/firmware
cp images/* %{buildroot}/lib/firmware
cp images.usb/* %{buildroot}/lib/firmware

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%doc README COPYING
/lib/firmware/*.bin

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.3-6
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.3-4
- 为 Magic 3.0 重建

* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建　
