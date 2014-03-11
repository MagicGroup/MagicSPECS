Name:		rt61pci-firmware
Version:	1.2
Release:	6%{?dist}
Summary:	Firmware for Ralink庐 RT2561/RT2661 A/B/G network adaptors
Summary(zh_CN.UTF-8): Ralink RT2561/RT2661 A/B/G 网卡的固件
Group:		System Environment/Kernel
Group(zh_CN.UTF-8):	系统环境/内核
License:	Redistributable, no modification permitted
URL:		http://www.ralinktech.com
Source0:	http://www.ralinktech.com.tw/data/RT61_Firmware_V%{version}.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Obsoletes: rt61-firmware < %{version}-%{release}
Provides: rt61-firmware = %{version}-%{release}


%description
This package contains the firmware required by the rt61pci driver for Linux.
Usage of the firmware is subject to the terms and conditions contained
inside the provided LICENSE.ralink-firmware.txt file.
Please read it carefully.

%description -l zh_CN.UTF-8
Ralink RT2561/RT2661 A/B/G 网卡的固件

%prep
%setup -q -n RT61_Firmware_V%{version}
sed -i 's/\r//' LICENSE.ralink-firmware.txt

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
install -pm 0644 *.bin $RPM_BUILD_ROOT/lib/firmware

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE.ralink-firmware.txt
/lib/firmware/*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.2-6
- 为 Magic 3.0 重建

* Sun Feb 05 2012 Liu Di <liudidi@gmail.com> - 1.2-5
- 为 Magic 3.0 重建


