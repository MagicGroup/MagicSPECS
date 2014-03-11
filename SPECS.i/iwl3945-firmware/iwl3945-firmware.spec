Summary: Firmware for Intel® PRO/Wireless 3945 A/B/G network adaptors
Name: iwl3945-firmware
Version: 15.32.2.9
Release: 6%{?dist}
License: Redistributable, no modification permitted
Group: System Environment/Kernel
URL: http://intellinuxwireless.org/
Source0: http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-3945-ucode-%{version}.tgz
Source1: http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-3945-ucode-15.28.1.8.tgz
Source2: http://intellinuxwireless.org/iwlwifi/downloads/iwlwifi-3945-ucode-2.14.4.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
# This is so that the noarch packages don't appear for these archs
ExcludeArch: ppc ppc64
# Renamed (twice) from iwlwifi-fimware as of 2.14.4-1
Provides: iwlwifi-firmware = %{version}-%{release}
Obsoletes: iwlwifi-firmware =< 2.14.4-1
Obsoletes: iwlwifi-3945-firmware =< 2.14.4-1

%description
This package contains the firmware required by the iwl3945 driver for Linux.
Usage of the firmware is subject to the terms and conditions contained
inside the provided LICENSE file. Please read it carefully.


%prep
%setup -q -n iwlwifi-3945-ucode-%{version} -a 1 -a 2
# Give doc files simpler names, since they won't get mixed with others
%{__mv} LICENSE.iwlwifi-3945-ucode LICENSE
%{__mv} README.iwlwifi-3945-ucode README
# Fix end-of-line encoding
%{__sed} -i 's/\r//' LICENSE README
# Put timestamp back (it's the same on all files)
touch -r iwlwifi-3945*.ucode LICENSE README
# Use reasonable permissions for text files
chmod 0644 LICENSE README


%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/lib/firmware
%{__install} -p -m 0644 iwlwifi-3945*.ucode */iwlwifi-3945*.ucode \
    %{buildroot}/lib/firmware/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README
/lib/firmware/*.ucode


%changelog
* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 15.32.2.9-6
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.32.2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  4 2009 John W. Linville <linville@redhat.com> 15.32.2.9-4
- Use of a dist tag is now back in favor...

* Fri Dec  4 2009 John W. Linville <linville@redhat.com> 15.32.2.9-3
- Use reasonable permissions for text files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.32.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 John W. Linville <linville@redhat.com> 15.32.2.9-1
- Update to 15.32.2.9.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.28.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Matthias Saou <http://freshrpms.net> 15.28.2.8-2
- Update the iwlwifi-3945-1.ucode from 2.14.1.5 to 15.28.1.8.

* Wed Oct 22 2008 Matthias Saou <http://freshrpms.net> 15.28.2.8-1
- Update to 15.28.2.8.
- Keep both 2.14.4 (iwlwifi-3945.ucode) and 2.14.1.5 (iwlwifi-3945-1.ucode) as
  the new 15.28.2.8 is now iwlwifi-3945-2.ucode.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net> 2.14.1.5-2
- Update to 2.14.1.5 (newer than 2.14.4...).
- Keep 2.14.4 in the package too.

* Tue Jul 24 2007 Matthias Saou <http://freshrpms.net> 2.14.4-1
- Rename package from iwlwifi-3945-firmware to iwl3945-firmware.
- Add obsoletes.

* Sun Jul 15 2007 Matthias Saou <http://freshrpms.net> 2.14.4-1
- Rename package from iwlwifi-firmware to iwlwifi-3945-firmware.
- Add provides and obsoletes.
- Fix description to reference the right LICENSE file name.
- Change from using dos2unix to chmod/sed/touch, preserve timestamps on docs.

* Sat Jul 14 2007 Matthias Saou <http://freshrpms.net> 2.14.4-1
- Update to 2.14.4.

* Fri May 18 2007 Matthias Saou <http://freshrpms.net> 2.14.3-2
- Bump release (Koji Error importing RPM file. rpm already exists.)

* Fri May 18 2007 Matthias Saou <http://freshrpms.net> 2.14.3-1
- Update to 2.14.3 (upstream name change iwlwifi-ucode -> iwlwifi-3945-ucode).
- Remove the ".iwlwifi-3945-ucode" suffix from included LICENSE and README.
- Use dos2unix on the LICENSE and the README to fix end of line encoding.
- Switch from using ExclusiveArch hack to ExcludeArch hack for Koji build.

* Tue Mar 20 2007 Matthias Saou <http://freshrpms.net> 2.14.1-4
- Add "noarch" to the ExclusiveArchs since plague chokes otherwise.

* Mon Mar  5 2007 Matthias Saou <http://freshrpms.net> 2.14.1-3
- Change group and license fields to reflect latest firmware guidelines.
- Replace "microcode" with "firmware" in summary and description.

* Mon Feb 26 2007 Matthias Saou <http://freshrpms.net> 2.14.1-2
- Initial RPM release.
- Rename from -ucode to -firmware.

