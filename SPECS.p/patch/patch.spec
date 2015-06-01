%define WITH_SELINUX 0
Summary: Utility for modifying/upgrading files
Summary(zh_CN.UTF-8): 修改/更新文件的工具
Name: patch
Version:	2.7.5
Release:	1%{?dist}
License: GPLv2+
URL: http://www.gnu.org/software/patch/patch.html
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz
Patch100: patch-selinux.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
BuildRequires: ed

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%description -l zh_CN.UTF-8
修改/更新文件的工具。

%prep
%setup -q

%if %{WITH_SELINUX}
# SELinux support.
%patch100 -p1 -b .selinux
%endif

%build
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
%ifarch sparcv9
CFLAGS=`echo $CFLAGS|sed -e 's|-fstack-protector||g'`
%endif
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Apr 15 2015 Liu Di <liudidi@gmail.com> - 2.7.5-1
- 更新到 2.7.5

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.6.1-11
- 为 Magic 3.0 重建

* Sat Jan 21 2012 Liu Di <liudidi@gmail.com> - 2.6.1-10
- 为 Magic 3.0 重建

* Wed Feb 16 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-9
- Let --posix cause --no-backup-if-mismatch (bug #678016).

* Thu Feb 10 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-8
- Incorporate upstream fix for CVE-2010-4651 patch so that a target
  name given on the command line is not validated (bug #667529).

* Tue Feb  8 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-7
- Applied upstream patch to fix CVE-2010-4651 so that malicious
  patches cannot create files above the current directory
  (bug #667529).

* Tue Jan  4 2011 Tim Waugh <twaugh@redhat.com> 2.6.1-6
- Use smp_mflags correctly (bug #665770).

* Mon Aug 16 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-5
- Another fix for the selinux patch (bug #618215).

* Fri Aug  6 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-4
- Fixed interpretation of return value from getfilecon().
- Fixed argument type for --get (bug #553624).

* Fri Aug  6 2010 Dennis Gilmore <dennis@ausil.us>
- using -fstack-projector causes weirdness on 32 bit sparc so disabling for now

* Tue Jul 27 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-3
- Fixed argument type for --get (bug #553624).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-2
- Added comments for all patches.
- Ship COPYING file.
- Removed sparc ifdefs in spec file.

* Mon Jan  4 2010 Tim Waugh <twaugh@redhat.com> 2.6.1-1
- 2.6.1 (bug #551569).  No longer need best-name patch.

* Thu Dec 24 2009 Tim Waugh <twaugh@redhat.com> 2.6-2
- Applied upstream patch to prevent incorrect filename being chosen
  when adding a new file (bug #549122).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 2.6-1
- 2.6.  No longer need stderr, suffix, stripcr, parse, allow-spaces,
  ifdef, program_name, or posix-backup patches.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Tim Waugh <twaugh@redhat.com> 2.5.4-39
- Fixed operation when SELinux is disabled (bug #498102).  Patch from
  Jan Kratochvil.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Tim Waugh <twaugh@redhat.com> 2.5.4-37
- Don't set SELinux file context if it is already correct.

* Mon Nov 24 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-36
- Better summary.

* Mon Jun 30 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-35
- Don't fail if setfilecon() returns EPERM (bug #453365), although the
  setfilecon man page suggests that ENOTSUP will be returned in this
  case.

* Mon Jun 16 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-34
- Only write simple backups for each file once during a run
  (bug #234822).

* Thu Jun 12 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-33
- Fix selinux patch and apply it.  Build requires libselinux-devel.

* Fri Feb  8 2008 Tim Waugh <twaugh@redhat.com> 2.5.4-32
- Applied patch from 2.5.9 to allow spaces in filenames (bug #431887).

* Mon Dec  3 2007 Tim Waugh <twaugh@redhat.com> 2.5.4-31
- Convert spec file to UTF-8 (bug #226233).
- Use _bindir macro in %%files (bug #226233).
- Parallel make (bug #226233).
- Better defattr declaration (bug #226233).

* Thu Oct  4 2007 Tim Waugh <twaugh@redhat.com>
- Beginnings of an SELinux patch (bug #165799); not applied yet.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 2.5.4-30
- Added dist tag.
- More specific license tag.
- Fixed summary.
- Better buildroot tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.4-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-29
- Remove SELinux patch for now (bug #167822).

* Wed Sep  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-27
- Applied patch from Ulrich Drepper to fix string overread (bug #167675).

* Tue Sep  6 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-26
- Preserve SELinux file contexts (bug #165799).

* Thu Aug 11 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-25
- Fixed CRLF detection (bug #154283).

* Wed May  4 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-24
- Reverted last change (bug #154283, bug #156762).

* Fri Apr 29 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-23
- Applied patch from Toshio Kuratomi to avoid problems with DOS-format
  newlines (bug #154283).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-22
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 2.5.4-21
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 2.5.4-18
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuilt in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Tim Waugh <twaugh@redhat.com> 2.5.4-12
- Fix error reporting when given bad options (bug #62981).

* Tue Mar  5 2002 Tim Waugh <twaugh@redhat.com> 2.5.4-11
- s/Copyright:/License:/.
- Fix -D behaviour (bug #60688).

* Tue May 29 2001 Tim Waugh <twaugh@redhat.com> 2.5.4-10
- Merge Mandrake patch:
  - fix possible segfault

* Fri Dec  1 2000 Tim Waugh <twaugh@redhat.com>
- Rebuild because of fileutils bug.

* Thu Nov  2 2000 Tim Waugh <twaugh@redhat.com>
- use .orig as default suffix, as per man page and previous behaviour
  (bug #20202).
- use better patch for this, from maintainer.

* Wed Oct  4 2000 Tim Waugh <twaugh@redhat.com>
- actually use the RPM_OPT_FLAGS

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%makeinstall, %%{_tmppath} and %%{_mandir}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL

* Wed Feb 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.5.4
- Fix up LFS support on Alpha (Bug #5732)

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Jun 06 1999 Alan Cox <alan@redhat.com>
- Fix the case where stderr isnt flushed for ask(). Now the 'no such file'
  appears before the skip patch question, not at the very end, Doh!

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- (ultra?) sparc was getting large file system support.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- bump release to preserve newer than back-ported 4.2.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- Fix for problem #682 segfault.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- added buildroot

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.5

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
