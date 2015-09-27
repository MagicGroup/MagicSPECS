Name: sane-frontends
Version: 1.0.14
Release: 17%{?dist}
Summary: Graphical frontend to SANE
Summary(zh_CN.UTF-8): SANE 的图形前端
URL: http://www.sane-project.org
Source0: ftp://ftp.sane-project.org/pub/sane/%{name}-%{version}/%{name}-%{version}.tar.gz
# Fix array subscript out of bounds errors (#133121).
# Upstream commit 5113e3de39846a8226909088ad5c1aa4969f3030 and commit
# 7336b064653026171a715dfaf803693b638c67a5 (partial)
Patch0: sane-frontends-1.0.14-array-out-of-bounds.patch
# Fix building with sane-backends >= 1.0.20.
# Upstream commit 5e96223e497538d06e18d8e84b774c4a35f654b4 (partial) and commit
# c554cfce37e37a33f94a9051afe2062c4759072b
Patch1: sane-frontends-1.0.14-sane-backends-1.0.20.patch
# Describe correct option names in xcam man page.
# Upstream commit 7e079e377174826453a1041719fb347d69d3ba5f
Patch2: sane-frontends-1.0.14-xcam-man.patch
# Update lib/snprintf.c to current version from LPRng to resolve license issue (#1102522)
Patch3: sane-frontends-1.0.14-update-to-current-lprng-plp_snprintf.patch
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
BuildRequires: gtk2-devel gimp-devel
BuildRequires: sane-backends-devel >= 1.0.19-15
Requires:  sane-backends
Buildroot: %{_tmppath}/%{name}-root
Obsoletes: sane <= 0:1.0.9
Provides: sane = %{?epoch:%{epoch}:}%{version}-%{release}

%description
This packages includes the scanadf and xcam programs.

%description -l zh_CN.UTF-8
SANE 的图形前端。

%prep
%setup -q
%patch0 -p1 -b .array-out-of-bounds
%patch1 -p1 -b .sane-backends-1.0.20
%patch2 -p1 -b .xcam-man
%patch3 -p1 -b .snprintf

%build
%configure --with-gnu-ld --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --mandir=%{_mandir}
make

%install
rm -rf %buildroot
%makeinstall

# Not xscanimage; use xsane instead.
rm -f %{buildroot}%{_bindir}/xscanimage
rm -f %{buildroot}%{_mandir}/man1/xscanimage*
rm -f %{buildroot}%{_datadir}/sane/sane-style.rc
magic_rpm_clean.sh

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,755)
%doc AUTHORS COPYING README
%{_bindir}/*
%{_mandir}/man1/*
# there is no desktop file for xcam because while it is a GUI program it is
# intended to be used from the command line

%changelog
* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 1.0.14-17
- 为 Magic 3.0 重建

* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 1.0.14-16
- 为 Magic 3.0 重建

* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 1.0.14-15
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0.14-14
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 1.0.14-13
- rebuild for gcc 4.7

* Mon Nov 07 2011 Nils Philippsen <nils@redhat.com> - 1.0.14-12
- rebuild (libpng)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 26 2010 Nils Philippsen <nils@redhat.com> - 1.0.14-10
- add missing documentation files AUTHORS, COPYING, README
- don't distribute sane-style.rc
- use %%buildroot consistently
- explain missing xcam.desktop file

* Mon Aug 03 2009 Nils Philippsen <nils@redhat.com> 1.0.14-9
- remove ExcludeArch: s390 s390x

* Fri Jul 31 2009 Nils Philippsen <nils@redhat.com> 1.0.14-8
- replace badcode with array-out-of-bounds patch
- fix compilation with sane-backends-1.0.20

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 02 2009 Nils Philippsen <nils@redhat.com> 1.0.14-6
- don't require libieee2384-devel, libjpeg-devel but require fixed
  sane-backends-devel for building

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.14-5
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.14-4
- Autorebuild for GCC 4.3

* Tue Apr 24 2007 Nils Philippsen <nphilipp@redhat.com> 1.0.14-3
- merge review (#226389):
  - add version info to obsoletes/provides
  - no config files in /usr
  - use %%configure macro
- add dist tag

* Thu Mar 15 2007 Karsten Hopp <karsten@redhat.com> 1.0.14-2
- rebuild with current gtk2 to add png support (#232013)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.14-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.14-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.14-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Nils Philippsen <nphilipp@redhat.com> 1.0.14-1
- version 1.0.14
- fix build requires
- update badcode patch

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.0.13-2
- Rebuild for new GCC.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com> 1.0.13-1
- 1.0.13.

* Mon Sep 27 2004 Tim Waugh <twaugh@redhat.com> 1.0.12-4
- Fixed mistaken array op (bug #133121).

* Sat Jun 19 2004 Jeremy Katz <katzj@redhat.com> - 1.0.12-3
- remove no longer valid requires on old gtk+ and gimp

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1.0.12-1
- 1.0.12.

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- s/ftp.mostang.com/ftp.sane-project.org/.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- BuildReq: libieee1284-devel, it seems to get picked up if available

* Mon Sep 29 2003 Tim Waugh <twaugh@redhat.com>
- Updated URL.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 29 2003 Tim Waugh <twaugh@redhat.com> 1.0.11-1
- 1.0.11.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com> 1.0.10-2
- Don't require a specific version of sane-backends.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 1.0.10-1
- 1.0.10.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Oct 25 2002 Tim Waugh <twaugh@redhat.com> 1.0.9-1
- 1.0.9.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-3
- Don't explicitly strip binaries (bug #62565).

* Wed Jun 12 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-2
- Rebuild to fix bug #66129.

* Tue May 28 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-1
- 1.0.8.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-0.20020522.1
- Update to CVS.  Release expected before the end of the month.
- Don't ship xscanimage any longer.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-2
- Rebuild in new environment.

* Mon Feb  4 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-1
- 1.0.7.

* Sun Jan 27 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-0.beta2.1
- 1.0.7-beta2.

* Wed Jan 23 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-0.beta1.1
- 1.0.7-beta1.
- No longer need the fpe patch.

* Fri Nov 30 2001 Tim Waugh <twaugh@redhat.com> 1.0.6-2
- Fix a floating point exception (bug #56536).

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 1.0.6-1
- 1.0.6.

* Sun Jul  1 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-1
- 1.0.5.
- Change Copyright: to License:.

* Thu Jun  7 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010605
- CVS snapshot 2001-06-05.
- Don't install xscanimage plug-in symlinks.  The old sane package never
  used to do this, and it looks confusing in gimp if you also have
  xsane-gimp (which is better) installed.  xscanimage works stand-alone
  anyhow.

* Sun Jun  3 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010603.1000
- CVS snapshot 2001-06-03 10:00.

* Sat Jun  2 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010530
- Built for Red Hat Linux.
- CVS snapshot 2001-05-30.

* Mon Jan 08 2001 Francis Galiegue <fg@mandrakesoft.com> 1.0.4-2mdk

- Summary now capitalised
- BuildRequires: sane (for sane-config)

