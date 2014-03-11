Name:		netxen-firmware
Summary:	QLogic Linux Intelligent Ethernet (3000 and 3100 Series) Adapter Firmware
Version:	4.0.534
Release:	6%{?dist}
License:	Redistributable, no modification permitted
Group:		System Environment/Kernel
Source0:	ftp://ftp.qlogic.com/outgoing/linux/firmware/netxen_nic/phanfw.bin
Source1:	ftp://ftp.qlogic.com/outgoing/linux/firmware/netxen_nic/LICENCE.phanfw
URL:		ftp://ftp.qlogic.com/outgoing/linux/firmware/netxen_nic/
BuildArch:	noarch
Requires:	udev

%description
QLogic Linux Intelligent Ethernet (3000 and 3100 Series) Adapter Firmware.

%prep
%setup -n %{name} -c -T
cp %{SOURCE0} .
cp %{SOURCE1} .

%build
# Firmware, do nothing.

%install
mkdir -p %{buildroot}%{_prefix}/lib/firmware/
install -m0644 phanfw.bin %{buildroot}%{_prefix}/lib/firmware/
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc LICENCE.phanfw
%{_prefix}/lib/firmware/phanfw.bin

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.0.534-6
- 为 Magic 3.0 重建

* Fri Apr 20 2012 Liu Di <liudidi@gmail.com> - 4.0.534-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.534-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Tom Callaway <spot@fedoraproject.org> - 4.0.534-3
- new LICENCE.phanfw
- add Requires: udev

* Mon Dec 13 2010 Tom Callaway <spot@fedoraproject.org> - 4.0.534-2
- update urls

* Mon Dec  6 2010 Tom Callaway <spot@fedoraproject.org> - 4.0.534-1
- initial package
