Summary: A file compression and packaging utility compatible with PKZIP
Summary(zh_CN.UTF-8): 与 PKZIP 兼容的文件压缩和打包工具
Name: zip
Version: 3.0
Release: 8%{?dist}
License: BSD
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Source: http://downloads.sourceforge.net/infozip/zip30.tar.gz
URL: http://www.info-zip.org/Zip.html
# This patch will probably be merged to zip 3.1
# http://www.info-zip.org/board/board.pl?m-1249408491/
Patch1: zip-3.0-exec-shield.patch
# Not upstreamed.
Patch2: zip-3.0-currdir.patch
# Not upstreamed.
Patch3: zip-3.0-time.patch
Patch4: man.patch
Patch5: zip-3.0-format-security.patch
Patch6: zipnote.patch

BuildRequires: bzip2-devel
Requires: unzip


%description
The zip program is a compression and file packaging utility.  Zip is
analogous to a combination of the UNIX tar and compress commands and
is compatible with PKZIP (a compression and file packaging utility for
MS-DOS systems).

Install the zip package if you need to compress files using the zip
program.

%description -l zh_CN.UTF-8
与 PKZIP 兼容的文件压缩和打包工具。

%prep
%setup -q -n zip30
%patch1 -p1 -b .exec-shield
%patch2 -p1 -b .currdir
%patch3 -p1 -b .time
%patch4 -p1 -b .man
%patch5 -p1 -b .format-security
%patch6 -p1 -b .zipnote

%build
make -f unix/Makefile prefix=%{_prefix} "CFLAGS_NOOPT=-I. -DUNIX $RPM_OPT_FLAGS" generic_gcc  %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BULD_ROOT%{_mandir}/man1

make -f unix/Makefile prefix=$RPM_BUILD_ROOT%{_prefix} \
        MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install

%files
%defattr(-,root,root,-)
%doc README CHANGES TODO WHATSNEW WHERE LICENSE README.CR
%doc proginfo/algorith.txt
%{_bindir}/zipnote
%{_bindir}/zipsplit
%{_bindir}/zip
%{_bindir}/zipcloak
%{_mandir}/man1/zip.1*
%{_mandir}/man1/zipcloak.1*
%{_mandir}/man1/zipnote.1*
%{_mandir}/man1/zipsplit.1*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 3.0-8
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 3.0-7
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.0-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.0-5
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Liu Di <liudidi@gmail.com> - 3.0-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 24 2010 Karel Klic <kklic@redhat.com> - 3.0-2
- Removed BuildRoot tag
- Removed %%clean section
- Removed trailing whitespaces in the spec file

* Fri Nov 13 2009 Karel Klic <kklic@redhat.com> - 3.0-1
- New upstream version
- Removed zip23.patch, because ZMEM is not used anyway
- Removed zip-2.31-install.patch, problem solved in upstream
- Removed zip23-umask.patch, upstream uses mkstemp which solves the problem
- Removed zip-2.31-near-4GB.patch, because upstream version
  handles large files well
- Removed zip-2.31-configure.patch, configure is better in the current version
- Removed zip-2.3-sf.patch, the error message doesn't exist in upstream anymore
- Removed zip-2.31-umask_mode.patch, which fixes also removed near-4GB patch
- Updated zip-2.31-time.patch for zip 3.0
- Updated exec-shield.patch for zip 3.0
- Updated zip-2.3-currdir.patch for zip 3.0

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.31-6
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Ivana Varekova <varekova@redhat.com> - 2.31-5
- add S_IWOTH option

* Mon Nov  5 2007 Ivana Varekova <varekova@redhat.com> - 2.31-4
- fix "zip does not honor umask setting when creating archives"
- fix "zip segfaults by attempt to archive big file"
- spec file cleanup

* Wed Feb  7 2007 Ivana Varekova <varekova@redhat.com> - 2.31-3
- incorporate the next peckage review comment

* Tue Feb  6 2007 Ivana Varekova <varekova@redhat.com> - 2.31-2
- incorporate the package review

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.31-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.31-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.31-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Ivana Varekova <varekova@redhat.com> 2.31-1
- update to 2.31

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 2.3-30
- rebuilt

* Mon Jan 17 2005 Ivana Varekova <varekova@redhat.com> 2.3-29
- Fix bug #142237 - problem with -d and ./files containing archives

* Mon Jun 21 2004 Lon Hohberger <lhh@redhat.com> 2.3-24
- Extend max file/archive size to 2^32-8193 (4294959103) bytes
- Include better debugging output for configure script

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 19 2004 Lon Hohberger <lhh@redhat.com> 2.3-22
- Fix typos

* Tue Feb 17 2004 Lon Hohberger <lhh@redhat.com> 2.3-21
- Include LICENSE file per bugzilla #116004

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 22 2003 Lon Hohberger <lhh@redhat.com> 2.3-19
- Make temp file have umask 0066 mode (#112516)

* Fri Oct 24 2003 Lon Hohberger <lhh@redhat.com> 2.3-18
- Incorporate Arjan's exec-shield patch for i386

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 19 2002 Tim Powers <timp@redhat.com>
- bump and rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  2 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Don't strip explicitly

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.3-11
- Add URL

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Aug 25 2000 Bill Nottingham <notting@redhat.com>
- add encryption code (#16878)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- rebuild in new environment

* Mon Mar 13 2000 Bill Nottingham <notting@redhat.com>
- spec file cleanups (#10143)

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- fix some perms

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan 11 2000 Bill Nottingham <notting@redhat.com>
- update to 2.3

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- updated text in the spec file

* Fri Jan 15 1999 Cristian Gafton <gafton@redhat.com>
- patch top build on the arm

* Mon Dec 21 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
