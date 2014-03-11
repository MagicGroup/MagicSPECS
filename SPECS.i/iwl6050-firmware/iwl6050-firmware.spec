Name:           iwl6050-firmware
Version:        41.28.5.1
Release:        4%{?dist}
Summary:        Firmware for Intel(R) Wireless WiFi Link 6050 Series Adapters

Group:          System Environment/Kernel
License:        Redistributable, no modification permitted
URL:            http://intellinuxwireless.org/
Source0:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-6050-ucode-%{version}.tgz
Source1:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-6050-ucode-9.201.4.1.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       udev


%description
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl6050 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%prep
%setup -c -q -a 1

# Change permission
find . -type f -exec chmod 0644 {} ';'

pushd iwlwifi-6050-ucode-%{version}
# Change encoding
%{__sed} -i 's/\r//'  LICENSE.iwlwifi-6050-ucode README.iwlwifi-6050-ucode
# Rename docs
%{__mv} LICENSE.iwlwifi-6050-ucode ../LICENSE
%{__mv} README.iwlwifi-6050-ucode ../README
# Preserve timestamp
touch -r *.ucode ../LICENSE ../README
popd


%build
# Nothing to build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/lib/firmware
%{__install} -pm 0644 */iwlwifi-6050*.ucode %{buildroot}/lib/firmware/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*.ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 41.28.5.1-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 41.28.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 John W. Linville <linville@tuxdriver.com> - 41.28.5.1-2
- need to keep old firmware version available for kernels that need it
- use available macros for standard packaging-related commands

* Thu Dec 16 2010 John W. Linville <linville@tuxdriver.com> - 41.28.5.1-1
- Update for firmware release 41.28.5.1

* Tue Jun  8 2010 John W. Linville <linville@tuxdriver.com> - 9.201.4.1-2
- Cleanse permissions of extracted files

* Tue Jun  8 2010 John W. Linville <linville@tuxdriver.com> - 9.201.4.1-1
- Initial import
