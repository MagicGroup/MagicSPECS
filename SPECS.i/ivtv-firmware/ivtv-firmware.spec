%define version_enc 2.06.039
%define version_dec 2.02.023

Summary: Firmware for the Hauppauge PVR 250/350/150/500/USB2 model series
Summary(zh_CN.UTF-8): Hauppauge PVR 250/350/150/500/USB2 系列型号的固件
Name: ivtv-firmware
Version: 20080701
Release: 24
Epoch: 2
License: Redistributable, no modification permitted
Group: System Environment/Kernel
Group(zh_CN.UTF-8): 系统环境/内核
URL: http://dl.ivtvdriver.org/ivtv/firmware/
Source0: http://dl.ivtvdriver.org/ivtv/firmware/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Obsoletes: ivtv-firmware-audio <= 0.0.1
Provides: ivtv-firmware-audio = 0.0.1
Obsoletes: %{name}-dec < %{version_dec}
Provides: %{name}-dec = %{version_dec}
Obsoletes: %{name}-enc < %{version_enc}
Provides: %{name}-enc = %{version_enc}

%description
This package contains the firmware for WinTV Hauppauge PVR
250/350/150/500/USB2 cards.

%description -l zh_CN.UTF-8
WinTV Hauppauge PVR 250/350/150/500/USB2 系列型号的固件。

%prep
%setup -q -c

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}/lib/firmware

install -p *.fw %{buildroot}%{_prefix}/lib/firmware/
install -p v4l-cx2341x-init.mpg %{buildroot}%{_prefix}/lib/firmware/v4l-cx2341x-init.mpg
# license requires that the licenses go in the same place as the firmware
for f in license-*.txt
do
  install -p $f %{buildroot}%{_prefix}/lib/firmware/%{name}-$f
done

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc license-*.txt
%{_prefix}/lib/firmware/*.fw
%{_prefix}/lib/firmware/v4l-cx2341x-init.mpg
%{_prefix}/lib/firmware/%{name}-license-*.txt

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2:20080701-24
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2:20080701-23
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20080701-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20080701-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20080701-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20080701-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20080701-18
- Update to 20080701.

* Wed Mar  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20070217-17
- Many fixes by Jarod Wilson.
- Rip out legacy support.

* Sat Feb  2 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20070217-16
- Place licenses next to firmware images.

* Sat Dec 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20070217-15.1
- Own directories from legacy paths.

* Wed Oct 24 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20070217-15
- Add v4l-cx2341x-init.mpg as a pseudo-firmware.

* Wed Feb 28 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2:20070217-13
- Modify versioning to follow date.

* Mon May 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update firmwares to recommended versions.
- Merge in audio firmware.

* Tue Jan  4 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build for audio firmware.

* Thu Oct 28 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update firmware to 1.8a.
- split package into enc/dec firmwares.
- version acording to origin, note that the two firmwares have
  different versions, so none is really suitable for the main package.

* Wed Mar  3 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Change versioning (previous was based on Windows driver).
- need to bump epoch for that :(

* Sat Feb 28 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.8 (22035).

* Mon Dec 29 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.


