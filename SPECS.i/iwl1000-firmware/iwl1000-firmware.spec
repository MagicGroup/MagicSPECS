%define iwl1000_v3         128.50.3.1
%define iwl1000_v5         39.31.5.1
%define iwl1000_list       %{iwl1000_v3} %{iwl1000_v5}

Name:           iwl1000-firmware
Epoch:          1
Version:        %{iwl1000_v5}
Release:        2%{?dist}
Summary:        Firmware for Intel® PRO/Wireless 1000 B/G/N network adaptors

Group:          System Environment/Kernel
License:        Redistributable, no modification permitted
URL:            http://intellinuxwireless.org/
Source0:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-1000-ucode-%{iwl1000_v5}.tgz
Source1:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-1000-ucode-%{iwl1000_v3}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       udev


%description
This package contains the firmware required by the iwlagn driver
for Linux to support the iwl1000 hardware.  Usage of the firmware
is subject to the terms and conditions contained inside the provided
LICENSE file. Please read it carefully.

%prep
%setup -c -q
%setup -c -q -D -T -a 1

pushd iwlwifi-1000-ucode-%{version}
# Change encoding
sed -i 's/\r//'  LICENSE.iwlwifi-1000-ucode README.iwlwifi-1000-ucode
# Rename docs
mv LICENSE.iwlwifi-1000-ucode ../LICENSE
mv README.iwlwifi-1000-ucode ../README
# Preserve timestamp
touch -r *.ucode ../LICENSE ../README
popd


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
for f in %{iwl1000_list} ; do
pushd iwlwifi-1000-ucode-$f
install -pm 0644 *.ucode $RPM_BUILD_ROOT/lib/firmware/
popd
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*.ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1:39.31.5.1-2
- 为 Magic 3.0 重建

* Wed Apr  6 2011 John W. Linville <linville@tuxdriver.com> - 39.31.5.1-1
- Update for upstream version 39.31.5.1
- Add logic to preserve version 128.50.3.1 for use by older kernels
- Add Epoch tag to account for Intel's bizarre release numbering

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 128.50.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 10 2009 John W. Linville <linville@tuxdriver.com> - 128.50.3.1-2
- Add Requires for udev

* Wed Sep 16 2009 John W. Linville <linville@tuxdriver.com> - 128.50.3.1-1
- Initial import
