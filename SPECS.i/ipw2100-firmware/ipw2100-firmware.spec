# $Id: ipw2100-firmware.spec 2095 2004-08-25 15:01:13Z dude $
# Authority: matthias
# Dist: nodist

Summary: Firmware for Intel PRO/Wireless 2100 network adaptors
Summary(zh_CN.UTF-8): Intel PRO/Wireless 2100网卡的固件
Name: ipw2100-firmware
Version: 1.3
Release: 6%{?dist}
License: Distributable
Group: System Environment/Kernel
Group(zh_CN.UTF-8): 系统环境/内核
URL: http://ipw2100.sourceforge.net/firmware.php
# Full path not available because of the end user agreement
Source: ipw2100-fw-1.3.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
This package contains the firmware files required by the ipw-2100 driver for
Linux. Usage of the firmware is subject to the terms contained in :
%{_defaultdocdir}/%{name}-%{version}/LICENSE. Please read it carefully.

%description -l zh_CN.UTF-8
这个包包含了Linux下ipw-2100驱动所需要的固件文件。使用这个固件的限制在：
%{_defaultdocdir}/%{name}-%{version}/LICENSE.请仔细阅读。

%prep
%setup -c


%build


%install
%{__rm} -rf %{buildroot}
# Install all firmware files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/firmware \
             %{buildroot}%{_libdir}/hotplug/firmware
%{__install} -m 0644 *.fw %{buildroot}%{_sysconfdir}/firmware/
%{__install} -m 0644 *.fw %{buildroot}%{_libdir}/hotplug/firmware/

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc LICENSE
%{_sysconfdir}/firmware/*.fw
%{_libdir}/hotplug/firmware/*.fw


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.3-6
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3-5
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1.3-4
- 为 Magic 3.0 重建

* Tue Apr 25 2005 Jaroslaw Polok <jaroslaw.polok@cern.ch> 1.3-1
- Update to 1.3.

* Wed Aug 25 2004 Matthias Saou <http://freshrpms.net> 1.2-1
- Update to 1.2.

* Wed Jun 16 2004 Matthias Saou <http://freshrpms.net> 1.1-1
- Cosmetic spec file changes.

* Tue May 11 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to firmware version 1.1.

* Tue May 11 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Change description to explicitly point to the LICENSE file.

* Sat May  8 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

