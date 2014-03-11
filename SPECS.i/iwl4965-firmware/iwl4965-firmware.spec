%define iwl4965_v1         228.57.1.21
%define iwl4965_v2         228.61.2.24
%define iwl4965_list       %{iwl4965_v1} %{iwl4965_v2}

Name:           iwl4965-firmware
Version:        %{iwl4965_v2}
Release:        4%{?dist}
Summary:        Firmware for Intel® PRO/Wireless 4965 A/G/N network adaptors

Group:          System Environment/Kernel
License:        Redistributable, no modification permitted
URL:            http://intellinuxwireless.org/
Source0:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-4965-ucode-%{iwl4965_v1}.tgz
Source1:        http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-4965-ucode-%{iwl4965_v2}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch


%description
This package contains the firmware required by the iwl4965 driver for Linux.
Usage of the firmware is subject to the terms and conditions contained
inside the provided LICENSE file. Please read it carefully.


%prep
%setup -c -q
%setup -c -q -D -T -a 1


# Change permission
find . -type f -exec chmod 0644 {} ';'

pushd iwlwifi-4965-ucode-%{version}
# Change encoding
sed -i 's/\r//'  LICENSE.iwlwifi-4965-ucode README.iwlwifi-4965-ucode
# Rename docs
mv LICENSE.iwlwifi-4965-ucode ../LICENSE
mv README.iwlwifi-4965-ucode ../README
# Preserve timestamp
touch -r *.ucode ../LICENSE ../README
popd


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
for f in %{iwl4965_list} ; do
pushd iwlwifi-4965-ucode-$f
install -pm 0644 *.ucode $RPM_BUILD_ROOT/lib/firmware/
popd
done



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 228.61.2.24-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 228.61.2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 228.61.2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 John W. Linville <linville@redhat.com> - 228.61.2.24-1
- Update v2 to 228.61.2.24

* Tue Apr 14 2009 kwizart < kwizart at gmail.com > - 228.57.2.23-5
- Reintroduce dist tag

* Tue Apr 14 2009 John W. Linville <linville@redhat.com> - 228.57.2.23-4
- Resync with F-10 version of the package
- Update v2 to 228.57.2.23 - Should fix #457154

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 228.57.2.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 kwizart < kwizart at gmail.com > - 228.57.2.21-3
- Remove ppc/ppc64 from ExcludedArches

* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 228.57.2.21-2
- Bump to keep the old 4.44.17 firmware dropped.

* Fri Jul 11 2008 kwizart < kwizart at gmail.com > - 228.57.2.21-1
- Update firmware v1 to 228.57.1.21
- Add firmware v2 to 228.57.2.21

* Tue Apr  8 2008 kwizart < kwizart at gmail.com > - 4.44.1.20-2
- Drop the old 4.44.17 firmware

* Tue Dec 18 2007 kwizart < kwizart at gmail.com > - 4.44.1.20-1
- Update v1 to 4.44.1.20
- Improve keep timestramps
- Obsoletes iwlwifi-4965-ucode

* Mon Aug 27 2007 kwizart < kwizart at gmail.com > - 4.44.1.18-2
- Remove ExcludeArch for ppc ppc64

* Fri Aug 17 2007 kwizart < kwizart at gmail.com > - 4.44.1.18-1
- Update to 4.44.1.18
- Bundle the previous 4.44.17 firmware

* Tue Jul 24 2007 kwizart < kwizart at gmail.com > - 4.44.17-1
- Update to 4.44.17

* Thu Jul 19 2007 kwizart < kwizart at gmail.com > - 4.44.15-6
- Uses versionned firmwares (with alternative method)

* Mon Jul 16 2007 kwizart < kwizart at gmail.com > - 4.44.15-5
- Renamed back to iwl4965-firmware
- Dropped obsoletes iwlwifi-firmware

* Sun Jul 15 2007 kwizart < kwizart at gmail.com > - 4.44.15-4
- Renamed LICENSE README
- Drop Provides: iwlwifi-firmware

* Sun Jul 15 2007 kwizart < kwizart at gmail.com > - 4.44.15-3
- Renamed to iwlwifi-4965-firmware
- Provides/Obsolete iwlwifi-firmware
- Drop the dist tag

* Wed Jul 13 2007 kwizart < kwizart at gmail.com > - 4.44.15-2
- Change to ExcludeArch as this can work with koji
- Drop LICENSE.iwlwifi-4965-ucode from /lib/firmware

* Wed Jul 13 2007 kwizart < kwizart at gmail.com > - 4.44.15-1
- Initial package.
