Summary: Device information files for HAL
Name: hal-info
Version: 20091130
Release: 3%{?dist}
License: AFL or GPLv2
Group: System Environment/Libraries
URL: http://www.freedesktop.org/Software/hal
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.bz2

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: hal >= 0.5.10
BuildRequires: hal-devel >= 0.5.10

%description 
The hal-info package contains various device information files (also
known as .fdi files) for the hal package.

%prep
%setup -q

%build
%configure --enable-killswitch-dell-wlan=no --enable-killswitch-dell-bluetooth=no --enable-killswitch-dell-wwan=no

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_datadir}/hal/fdi/information/10freedesktop/*.fdi
%{_datadir}/hal/fdi/preprobe/10osvendor/*.fdi

%changelog
* Tue Dec 25 2012 Liu Di <liudidi@gmail.com> - 20091130-3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20091130-2
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090716-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 30 2009 Richard Hughes <rhughes@redhat.com> - 20090716-3
- Remove 30-keymap-olpc.fdi as it's now shipped in olpc-utils
- Fixes #514081

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090716-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Richard Hughes <rhughes@redhat.com> - 20090716-1
- New upstream release to fix some more music players, resume problems and
  keymaps. See http://lists.freedesktop.org/archives/hal/2009-July/013481.html
  for full list.

* Tue Apr 14 2009 Richard Hughes <rhughes@redhat.com> - 20090414-1
- New upstream release to fix a load of HP keymaps.

* Tue Apr 14 2009 Richard Hughes <rhughes@redhat.com> - 20090330-2
- A key labelled "Music" on a Dell USB keyboard shows up in X as "XF86Tools"
  which is wrong. Reassigns the key to be "Media".

* Mon Mar 30 2009 Richard Hughes <rhughes@redhat.com> - 20090330-1
- Update to latest upstream release

* Mon Mar 09 2009 Richard Hughes <rhughes@redhat.com> - 20090309-1
- Update to latest upstream release

* Tue Mar 03 2009 - Bastien Nocera <bnocera@redhat.com> - 20090202-3
- Remove the Dell native killswitches, replaced by the kernel killswitches
  in dell_laptop (#488177)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090202-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Richard Hughes <rhughes@redhat.com> - 20090202-1
- Update to latest upstream release

* Fri Dec 19 2008 Richard Hughes <rhughes@redhat.com> - 20081219-1
- Update to latest upstream release

* Mon Dec 01 2008 Richard Hughes <rhughes@redhat.com> - 20081127-1
- Update to latest upstream release

* Wed Nov 12 2008 Richard Hughes <rhughes@redhat.com> - 20081022-2
- Add a OLPC keymap file, based from one by Ignacio Vazquez-Abrams.

* Mon Oct 22 2008 Richard Hughes <rhughes@redhat.com> - 20081022-1
- Update to latest upstream release

* Mon Oct 13 2008 Richard Hughes <rhughes@redhat.com> - 20081013-1
- Update to latest upstream release

* Wed Oct 01 2008 Richard Hughes <rhughes@redhat.com> - 20081001-2
- Bump for rebuild

* Wed Oct 01 2008 Richard Hughes <rhughes@redhat.com> - 20081001-1
- Update to latest upstream release

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> - 20080813-2
- Add patch for Lenovo 3000 video key

* Wed Aug 13 2008 Matthew Garrett <mjg@redhat.com> - 20080813-1
- update to git snapshot

* Sat Jun 07 2008 Dan Williams <dcbw@redhat.com> - 20080607-1
- Update to git snapshot

* Fri May 09 2008 Richard Hughes <rhughes@redhat.com> - 20080508-1
- Update to latest upstream release

* Thu Apr 24 2008 Dan Williams <dcbw@redhat.com> - 20080317-6
- Add CDMA Novatel S620

* Wed Apr  2 2008 Dan Williams <dcbw@redhat.com> - 20080317-5
- Add more Novatel U727s

* Wed Apr  2 2008 Dan Williams <dcbw@redhat.com> - 20080317-4
- Really fix MC5720 (rh #439753)

* Mon Mar 31 2008 Dan Williams <dcbw@redhat.com> - 20080317-3
- Fix for Sierra MC5720 (rh #439753)

* Fri Mar 28 2008 Dan Williams <dcbw@redhat.com> - 20080317-2
- Fix for Sierra 595U and others (rh #439536)

* Sun Mar 23 2008 Lubomir Kundrak <lkundrak@redhat.com> - 20080317-1
- Update to latest upstream release

* Sat Mar 15 2008 Lubomir Kundrak <lkundrak@redhat.com> - 20080313-1
- Update to latest upstream release
- Fix License tag

* Mon Mar 10 2008 Ray Strode <rstrode@redhat.com> - 20080310-1
- Update to latest upstream release

* Wed Mar  5 2008 Dan Williams <dcbw@redhat.com> - 20080215-2
- Fix modem tags for Kyocera KPC-650

* Fri Feb 15 2008 Dan Williams <dcbw@redhat.com> - 20080215-1
- Update to latest upstream release (mainly for mobile broadband updates)

* Sun Jan 06 2008 Lubomir Kundrak <lkundrak@redhat.com> - 20071212-1
- Update to latest upstream release
- Clean buildroot in %%install

* Tue Oct 30 2007 David Zeuthen <davidz@redhat.com> - 20071030-1
- Update to latest upstream release

* Thu Oct 11 2007 David Zeuthen <davidz@redhat.com> - 20071011-1
- Update to latest upstream release

* Fri Sep 25 2007 David Zeuthen <davidz@redhat.com> - 20070925-1
- Update to latest release.

* Fri Aug 31 2007 David Zeuthen <davidz@redhat.com> - 20070831-1
- Update to latest release.

* Wed Jul 31 2007 David Zeuthen <davidz@redhat.com> - 20070725-1
- Update to latest release.

* Thu May 17 2007 Richard Hughes <rhughes@redhat.com> - 20070516-2
- Oops. My packaging blunder. Apologies.

* Thu May 17 2007 Richard Hughes <rhughes@redhat.com> - 20070516-1
- Update to latest release.

* Tue Apr 17 2007 David Zeuthen <davidz@redhat.com> - 20070402-1
- Initial build.
