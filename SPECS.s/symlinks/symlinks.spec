Summary: A utility which maintains a system's symbolic links
Name: symlinks
URL: ftp://metalab.unc.edu/pub/Linux/utils/file/
Version: 1.4
Release: 6%{?dist}
Group: Applications/System
License: Copyright only
Source0: http://ibiblio.org/pub/Linux/utils/file/%{name}-%{version}.tar.gz
# Taken from http://packages.debian.org/changelogs/pool/main/s/symlinks/symlinks_1.2-4.2/symlinks.copyright
Source1: symlinks-LICENSE.txt
Patch1: symlinks-coverity-readlink.patch
Patch2: symlinks-coverity-overrun-dynamic.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The symlinks utility performs maintenance on symbolic links.  Symlinks
checks for symlink problems, including dangling symlinks which point
to nonexistent files.  Symlinks can also automatically convert
absolute symlinks to relative symlinks.

Install the symlinks package if you need a program for maintaining
symlinks on your system.

%prep
%setup -q
cp %{SOURCE1} .

# Fix off-by-one error in call to readlink.
%patch1 -p1 -b .coverity-readlink

# Fix possible buffer overrun found by coverity.
%patch2 -p1 -b .coverity-overrun-dynamic

%build
make CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS)" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 755 symlinks $RPM_BUILD_ROOT%{_bindir}
install -m 644 symlinks.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc symlinks-LICENSE.txt
%{_bindir}/symlinks
%{_mandir}/man8/symlinks.8*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.4-6
- 为 Magic 3.0 重建

* Sat Feb 11 2012 Liu Di <liudidi@gmail.com> - 1.4-5
- 为 Magic 3.0 重建

* Fri May 20 2011 Tim Waugh <twaugh@redhat.com> 1.4-4
- Applied patches from Jiri Popelka:
  - Fix off-by-one error in call to readlink.
  - Fix possible buffer overrun found by coverity.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 13 2009 Tim Waugh <twaugh@redhat.com> 1.4-2
- 1.4.  All patches now upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2-32
- fix license tag

* Mon Feb 11 2008 Tim Waugh <twaugh@redhat.com> 1.2-31
- Rebuild for GCC 4.3.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 1.2-30
- Rebuilt.

* Fri Feb 23 2007 Tim Waugh <twaugh@redhat.com> 1.2-29
- Use smp_mflags (bug #226445).
- Better default attributes (bug #226445).
- Make setup macro quiet (bug #226445).
- Clean build root in %%install section (bug #226445).

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 1.2-28
- Fixed build root (bug #226445).

* Tue Feb  6 2007 Tim Waugh <twaugh@redhat.com> 1.2-27
- Fixed summary (bug #226445).
- Added token URL tag (bug #226445).

* Tue Jan 30 2007 Florian La Roche <laroche@redhat.com> - 1.2-26
- do not strip away debuginfo

* Thu Jan 18 2007 Tim Waugh <twaugh@redhat.com> - 1.2-25
- Build with LFS support (bug #206407).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2-24.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.2-24
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1.2-23
- s/Copyright:/License:/.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 16 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch from #89655

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.2-17
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Tue May 30 2000 Preston Brown <pbrown@redhat.com>
- fix up help output (#10236)

* Thu Feb 10 2000 Preston Brown <pbrown@redhat.com>
- do not link statically

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against the latest glibc in the sparc tree

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- changed build root to /var/tmp, not /var/lib
- updated to version 1.2

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- build-rooted
