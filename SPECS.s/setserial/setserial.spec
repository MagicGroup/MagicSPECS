%define	_bindir	/bin

Summary: A utility for configuring serial ports
Name: setserial
Version: 2.17
Release: 29%{?dist}
Source: http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0: setserial-2.17-fhs.patch
Patch1: setserial-2.17-rc.patch
Patch2: setserial-2.17-readme.patch
Patch3: setserial-2.17-spelling.patch
Patch4: setserial-hayesesp.patch
License: GPL+
Group: Applications/System
URL: http://setserial.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x

BuildRequires: groff

%description
Setserial is a basic system utility for displaying or setting serial
port information. Setserial can reveal and allow you to alter the I/O
port and IRQ that a particular serial device is using, and more.

%prep
%setup -q
# Use FHS directory layout.
%patch0 -p1 -b .fhs

# Fixed initscript.
%patch1 -p1 -b .rc

# Corrected readme file.
%patch2 -p1 -b .readme

# Fixed spelling in help output.
%patch3 -p1 -b .spelling

# Don't require hayesesp.h (bug #564947).
%patch4 -p1 -b .hayesesp
rm -f config.cache

%build
%configure
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
make install DESTDIR=${RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README rc.serial
%{_bindir}/setserial
%{_mandir}/man*/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.17-29
- 为 Magic 3.0 重建

* Mon Feb 06 2012 Liu Di <liudidi@gmail.com> - 2.17-28
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 2.17-26
- Added comments for all patches.

* Mon Feb 15 2010 Tim Waugh <twaugh@redhat.com> 2.17-25
- Don't require hayesesp.h (bug #564947).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Tim Waugh <twaugh@redhat.com> 2.17-22
- Rebuild for GCC 4.3.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 2.17-21
- More specific license tag.

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 2.17-20
- Fixed mandir in fhs patch (bug #226411).
- Don't run strip (bug #226411).
- Fixed readme patch to talk about Fedora not Red Hat Linux (bug #226411).
- Fixed build root tag (bug #226411).
- Use SMP make flags (bug #226411).
- Avoid %%makeinstall (bug #226411).
- Fixed summary (bug #226411).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.17-19.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.17-19.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.17-19.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.17-19
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.17-18
- Rebuilt.

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 2.17-17
- Spec file tidying by Robert Scheck (bug #135182).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com> 2.17-14
- Build requires groff (bug #111088).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 10 2003 Tim Waugh <twaugh@redhat.com> 2.17-11
- Fix spelling mistake (bug #80896).

* Wed Nov 20 2002 Tim Powers <timp@redhat.com> 2.17-10
- rebuild in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Tim Waugh <twaugh@redhat.com> 2.17-7
- Don't strip binaries explicitly (bug #62566).

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Sep 11 2001 Tim Waugh <twaugh@redhat.com> 2.17-5
- Fix init script (bug #52862).
- Avoid temporary file vulnerability in init script.
- Update README: it's --add, not -add.

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de> 2.17-4
- add ExcludeArch: s390 s390x

* Wed May 30 2001 Tim Waugh <twaugh@redhat.com> 2.17-3
- Sync description with specspo.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com> 2.17-2
- automatic rebuild

* Wed Jun 14 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.17.
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Feb 11 1999 Michael Maher <mike@redhat.com>
- fixed bug #363

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sat Jun 20 1998 Jeff Johnson <jbj@redhat.com>
- upgraded to 2.1.14

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- pulled into distribution
- used setserial-2.12_CTI.tgz instead of setserial-2.12.tar.gz (former is
  all that sunsite has) - not sure what the difference is.

* Thu Sep 25 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- added %%attr's
- added sanity check for RPM_BUILD_ROOT
- setserial is now installed into /bin, where util-linux puts it and all
  startup scripts expect it.
