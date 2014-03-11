Name:           iwl100-firmware
Version:        39.31.5.1
Release:        3%{?dist}
Summary:        Firmware for Intel(R) Wireless WiFi Link 100 Series Adapters

Group:          System Environment/Kernel
License:        Redistributable, no modification permitted
URL:            http://intellinuxwireless.org/
Source0:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-100-ucode-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       udev


%description
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl100 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%prep
%setup -c -q

# Change permission
find . -type f -exec chmod 0644 {} ';'

pushd iwlwifi-100-ucode-%{version}
# Change encoding
sed -i 's/\r//'  LICENSE.iwlwifi-100-ucode README.iwlwifi-100-ucode
# Rename docs
mv LICENSE.iwlwifi-100-ucode ../LICENSE
mv README.iwlwifi-100-ucode ../README
# Preserve timestamp
touch -r *.ucode ../LICENSE ../README
popd


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
pushd iwlwifi-100-ucode-%{version}
install -pm 0644 *.ucode $RPM_BUILD_ROOT/lib/firmware/
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*.ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 39.31.5.1-3
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 39.31.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 John W. Linville <linville@redhat.com> - 39.31.5.1-1
- Initial import
