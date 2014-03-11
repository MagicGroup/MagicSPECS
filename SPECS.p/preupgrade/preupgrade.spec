Summary: Prepares a system for an upgrade
Name: preupgrade
Version: 1.1.10
Release: 3%{?dist}
License: GPLv2+
Source: https://fedorahosted.org/releases/p/r/preupgrade/%{name}-%{version}.tar.bz2
Source1: http://mirrors.fedoraproject.org/releases.txt
URL: https://fedorahosted.org/preupgrade/
BuildArch: noarch
Requires: python >= 2.1, rpm-python, rpm >= 0:4.1.1
Requires: pygtk2-libglade, gtk2 >= 2.16.6
Requires: python-urlgrabber >= 3.9.1-4
Requires: yum-metadata-parser, yum >= 3.2.24
Requires: usermode
Requires: createrepo >= 0.9.7-7
Requires: util-linux >= 2.15.1
BuildRequires: intltool
BuildRequires: desktop-file-utils, python
Conflicts: yaboot < 1.3.14-8

%description
preupgrade prepares your Fedora system for upgrading to a newer version
by examining your system, downloading all the files needed for the upgrade,
and then setting up your system to perform the upgrade after rebooting.

%prep
%setup -q

%build
# no op

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
ln -s consolehelper $RPM_BUILD_ROOT/%{_bindir}/%{name}
ln -s consolehelper $RPM_BUILD_ROOT/%{_bindir}/%{name}-cli
# NOTE: we ship this *only* for PackageKit - it is ignored by preupgrade!
# preupgrade itself pulls data from {$PWD,$PWD/data}/releases.txt or
# http://mirrors.fedoraproject.org/releases.txt
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/preupgrade/releases.list

%find_lang %name

%files -f %{name}.lang
%defattr(-, root, root)
%dir %{_datadir}/%{name}
%doc ChangeLog README COPYING
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%{_datadir}/%{name}/*
%{_sbindir}/%{name}
%{_sbindir}/%{name}-cli
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{python_sitelib}/%{name}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.10-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Richard Hughes <richard@hughsie.com> - 1.1.10-1
- New upstream release.
- Recommend downloading the DVD if there is not enough space in /boot
- Do not hardcode --location=none when upgrading to F16

* Tue Mar 15 2011 Richard Hughes <richard@hughsie.com> - 1.1.9-1
- New upstream release.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Richard Hughes <richard@hughsie.com> - 1.1.8-1
- New upstream release.
- Reinvigorate pre-upgrade-cli with the same fixes as the gui tool.
- Translation updates.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jun 05 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.6-2
- Fix description to clarify that skipping releases is ok 
- Update spec to match current guidelines

* Wed May 12 2010 Richard Hughes <richard@hughsie.com> - 1.1.6-1
- New upstream release.
- Generate a valid kickstart when there is no space for the install.img
- Ensure we disable all plugins which could cause issues with downloading
- Translation updates

* Mon Dec 14 2009 Seth Vidal <skvidal at fedoraproject.org> - 1.1.4-1
- fixes 538118 among others

* Fri Nov 13 2009 Will Woods <wwoods@redhat.com> - 1.1.3-1
- Check /boot for enough space to perform upgrade (bug 530541)
- Don't traceback if /boot is RAID (bug 504826)
- Check if /boot is dmraid

* Mon Oct 12 2009 Will Woods <wwoods@redhat.com> - 1.1.2-1
- Proper fix for bug 526208
- Require gtk2 >= 2.16.6

* Fri Oct  9 2009 Seth Vidal <skvidal at fedoraproject.org> - 1.1.1-2
- require yum 3.2.24

* Fri Oct 09 2009 Will Woods <wwoods@redhat.com> - 1.1.1-1
- Fix UI hang on upgrades from F11 (bug 526208)
- Fix unhandled traceback in preupgrade.dev (bug 504826)
- Give preupgrade its own User-Agent string

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Will Woods <wwoods@redhat.com> - 1.1.0-1
- Bump version for 1.1.0 release

* Tue May 5 2009 Will Woods <wwoods@redhat.com> - 1.1.0-0.pre3
- Drop support for /boot on RAID
- Properly enable both main and install repos
- Fix cleanup of interrupted runs
- Require VNC password to be >= 6 chars long, like anaconda (bug #498843)

* Wed Apr 22 2009 Will Woods <wwoods@redhat.com> - 1.1.0-0.pre2
- Disable bootloader installation (bug 496952)
- Fix handling of releases.txt to accept Rawhide again

* Thu Apr 16 2009 Will Woods <wwoods@redhat.com> - 1.1.0-0.pre1
- Try to get new packages for *all* repos, including updates (bug 473966)
- Fix UnicodeDecodeError downloading packages (bug 476862)
- Fix traceback if network isn't up at startup (bug 474177)
- Specify which system to upgrade in kickstart (bug 473016)
- Fix traceback with certain mirrors (bug 487743)
- Fix problems with "excludes=" in yum.conf (bug 491577)

* Mon Dec  8 2008 Will Woods <wwoods@redhat.com> - 1.0.1-1
- Fix yaboot Conflicts: to allow installation on ppc (bug 473065)
- Fix crash with separate /var partition or mdraid root (bug 473782)
- Fix crash with mdraid (software RAID) root (bug 473103)
- CLI: Use the right dir for createrepo 
- CLI: Fix network option parsing, add --dhcp
- CLI: Write network options into ks.cfg (bug 472933)

* Fri Nov 21 2008 Will Woods <wwoods@redhat.com> - 1.0.0-1
- Minor UI fixes
- Add --clean flag
- Use checksums to verify boot image integrity
- Clean up bootloader config when cleaning an interrupted run
- Use 'ybin --bootonce' on ppc rather than changing default boot target
- Be more careful about picking a keymap (bug 471515)
- Add Fedora 10 (Cambridge) to releases.txt

* Mon Nov  3 2008 Will Woods <wwoods@redhat.com> - 0.9.9-1
- Fetch release data from http://mirrors.fedoraproject.org/releases.txt
- Recognize new metadata filenames
- Generate kickstart for all installs
- Automatically upgrade bootloader config during upgrade
- preupgrade-cli: Add --vnc for headless remote installs
- preupgrade-cli: Properly set locale so we don't crash on non-en_US
- preupgrade-cli: Fix --help 

* Thu Oct  2 2008 Will Woods <wwoods@redhat.com> - 0.9.8-2
- Clear cache after user decides not to resume an old run
- Add Fedora 10 Beta to releases.list

* Thu Sep 18 2008 Will Woods <wwoods@redhat.com> - 0.9.8-1
- GUI version prompts to resume interrupted runs
- Checks for available disk space before downloading / rebooting
- Does not change boot target until you hit the Reboot button
- Handle invalid treeinfo gracefully (bug #459935)
- Use UUID=xxx for devices - makes finding devices much more robust
- No more network dialog for missing packages
- Use anaconda's own depsolving tweaks (whiteout/blacklist)
- Use kickstart to automate installs

* Tue May  6 2008 Will Woods <wwoods@redhat.com> - 0.9.3-2
- Add missing Requires on pyxf86config

* Fri May  2 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.3-1
- 0.9.3

* Thu May  1 2008 Seth Vidal <skvidal at fedoraproject.org> 
- make preupgrade clean up its messes in post so it doesn't leave
  cruft on the fs after an upgrade.

* Thu Apr 24 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.2-1
- 0.9.2 
- put cli tool back in 

* Mon Apr 21 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9.1-1
- 0.9.1

* Mon Apr  7 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.9-2
- add dist tag
- fix buildroot
- fix buildarchitectures to buildarch


* Thu Apr  3 2008 Will Woods <wwoods@redhat.com> - 0.9-1
- Remove .desktop file; we'll run from a puplet notification (or by hand)
- Check file size on downloaded boot images to make sure they're the right ones
- More descriptive title for boot item
- Update releases.list - add Fedora 9 Beta
- Add python as a buildreq 

* Wed Mar 26 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.8-1
- remove the cli for now b/c it is broken!

* Mon Mar 24 2008 Will Woods <wwoods@redhat.com> - 0.8-1
- Functionally nearly complete
- Add .desktop file for GUI

* Thu Feb  7 2008 Seth Vidal <skvidal at fedoraproject.org> - 0.1-1
- first pkging attempt
