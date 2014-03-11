Name:           iwl6000g2a-firmware
Version:        17.168.5.3
Release:        2%{?dist}
Summary:        Firmware for Intel(R) Wireless WiFi Link 6005 Series Adapters

Group:          System Environment/Kernel
License:        Redistributable, no modification permitted
URL:            http://intellinuxwireless.org/
Source0:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-6000g2a-ucode-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       udev


%description
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl6000g2a hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%prep
%setup -c -q

# Change permission
find . -type f -exec chmod 0644 {} ';'

pushd iwlwifi-6000g2a-ucode-%{version}
# Change encoding
sed -i 's/\r//'  LICENSE.iwlwifi-6000g2a-ucode README.iwlwifi-6000g2a-ucode
# Rename docs
mv LICENSE.iwlwifi-6000g2a-ucode ../LICENSE
mv README.iwlwifi-6000g2a-ucode ../README
# Preserve timestamp
touch -r *.ucode ../LICENSE ../README
popd


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
pushd iwlwifi-6000g2a-ucode-%{version}
install -pm 0644 *.ucode $RPM_BUILD_ROOT/lib/firmware/
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*.ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 17.168.5.3-2
- 为 Magic 3.0 重建

* Tue Aug  9 2011 John W. Linville <linville@redhat.com> - 17.168.5.3-1
- Update to version 17.168.5.3 from upstream

* Mon Feb 14 2011 John W. Linville <linville@redhat.com> - 17.168.5.2-1
- Update to version 17.168.5.2 from upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.168.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 John W. Linville <linville@redhat.com> - 17.168.5.1-1
- Initial import
