Summary: Firmware for Intel® PRO/Wireless 2200 network adaptors
Name: ipw2200-firmware
Version: 3.1
Release: 8%{?dist}
License: Redistributable, no modification permitted
Group: System Environment/Kernel
URL: http://ipw2200.sourceforge.net/firmware.php
# License agreement must be displayed before download (referer protection)
Source0: ipw2200-fw-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
# This is so that the noarch packages only appears for these archs
ExclusiveArch: noarch i386 x86_64

%description
This package contains the firmware files required by the ipw2200 driver for
Linux. Usage of the firmware is subject to the terms and conditions contained
in /lib/firmware/LICENSE.ipw2200. Please read it carefully.


%prep
%setup -q -n ipw2200-fw-%{version}


%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/lib/firmware
# Terms state that the LICENSE *must* be in the same directory as the firmware
%{__install} -p -m 0644 *.fw %{buildroot}/lib/firmware/
%{__install} -p -m 0644 LICENSE.ipw2200-fw %{buildroot}/lib/firmware/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc /lib/firmware/LICENSE.ipw2200-fw
/lib/firmware/*.fw


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.1-8
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.1-7
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 3.1-6
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  7 2010 John W. Linville <linville@redhat.com> - 3.1-4
- Add dist tag

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net> 3.1-2
- Bump release, the added dist tag in F-10 broke the update path (#505162).

* Fri Mar 20 2009 John W. Linville <linville@redhat.com> - 3.1-1
- Update for release 3.1 of firmware

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 24 2008 Matthias Saou <http://freshrpms.net> 3.0-10
- Remove LICENSE file from %%doc (was +x), mark the other as %%doc (#440553).
- Remove the included older 2.4 firmware, since 3.0 has been required by all
  kernels for a long while now.

* Tue Mar 20 2007 Matthias Saou <http://freshrpms.net> 3.0-9
- Add "noarch" to the ExclusiveArchs since plague chokes otherwise.

* Mon Mar  5 2007 Matthias Saou <http://freshrpms.net> 3.0-8
- Change group and license fields to reflect latest firmware guidelines.

* Mon Feb 26 2007 Matthias Saou <http://freshrpms.net> 3.0-7
- Move from a symlink to using a copy for the LICENSE (cleaner and easier).

* Sat Feb 24 2007 Matthias Saou <http://freshrpms.net> 3.0-6
- Fix group and license tags.
- Add (partially useful) exclusivearch.
- Quiet %%setup.

* Wed Feb 14 2007 Matthias Saou <http://freshrpms.net> 3.0-5
- Don't mark the LICENSE in /lib/firmware as %%doc since it could be excluded
  when using --excludedocs, symlink a file in %%doc to it instead.
- Remove 2.2 and 2.3 firmwares since only 2.4 and 3.0 are required for FC5+.

* Wed Feb 14 2007 Matthias Saou <http://freshrpms.net> 3.0-4
- Minor spec file cleanup for Fedora inclusion.

* Tue Oct 17 2006 Matthias Saou <http://freshrpms.net> 3.0-3
- Move the LICENSE as LICENSE.ipw2200 in the firmware directory to fully
  comply to the Intel redistribution terms and conditions.

* Sun Jun 25 2006 Matthias Saou <http://freshrpms.net> 3.0-2
- Fix inclusion of the 3.0 firmware files.

* Sat Jun 24 2006 Dag Wieers <dag@wieers.com> - 3.0-1
- Updated to release 3.0.

* Mon Jan  2 2006 Matthias Saou <http://freshrpms.net> 2.4-2
- Convert spec file to UTF-8.

* Thu Oct 27 2005 Matthias Saou <http://freshrpms.net> 2.4-1
- Update to 2.4, but keep 2.2 and 2.3 included too.

* Tue May 31 2005 Matthias Saou <http://freshrpms.net> 2.3-2
- Also bundle 2.2 firmware : The recent driver downgrade required this :-/

* Wed May 25 2005 Matthias Saou <http://freshrpms.net> 2.3-1
- Update to 2.3, required by latest FC4 dev and 2.6.12rc.

* Thu Apr 21 2005 Matthias Saou <http://freshrpms.net> 2.2-3
- Remove all symlinks, the only useful location is /lib/firmware now.
- No longer rename all firmware files, recent ipw2200 modules expect the
  default names now (tested w/ FC3 2.6.11 updates and FC4test).

* Thu Feb 17 2005 Matthias Saou <http://freshrpms.net> 2.2-2
- Rename all files from ipw-2.2-* to ipw2200_* as required.

* Wed Feb  9 2005 Matthias Saou <http://freshrpms.net> 2.2-1
- Update to 2.2, required by latest FC kernels.

* Wed Nov  3 2004 Matthias Saou <http://freshrpms.net> 2.0-1
- Update to 2.0.
- Now put the files in /lib/firmware and symlinks in other dirs.

* Wed Jun 16 2004 Matthias Saou <http://freshrpms.net> 1.2-1
- Initial RPM release, based on the ipw2100-firmware spec file.

