%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%global WITH_SELINUX 0
%endif
Summary: A GNU file archiving program
Name: tar
Epoch: 2
Version: 1.26
Release: 15%{?dist}
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/tar/
Source0: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/pub/gnu/tar/tar-%{version}.tar.xz.sig
#Manpage for tar and gtar, a bit modified help2man generated manpage
Source2: tar.1
#Stop issuing lone zero block warnings
Patch1: tar-1.14-loneZeroWarning.patch
#Fix extracting sparse files to a filesystem like vfat,
#when ftruncate may fail to grow the size of a file.(#179507)
Patch2: tar-1.15.1-vfatTruncate.patch
#change inclusion defaults of tar to "--wildcards --anchored
#--wildcards-match-slash" for compatibility reasons (#206841)
#Add support for selinux, acl and extended attributes
#Patch3: tar-1.24-xattrs.patch
Patch4: tar-1.17-wildcards.patch
#ignore errors from setting utime() for source file
#on read-only filesystem (#500742)
Patch5: tar-1.22-atime-rofs.patch
#oldarchive option was not working(#594044)
Patch6: tar-1.23-oldarchive.patch
#temporarily disable sigpipe.at patch (fails at build in koji, passes manually)
Patch7: tar-sigpipe.patch
#partially revert upstream commit 4bde4f3 (#717684)
Patch8: tar-1.24-openat-partial-revert.patch
# fix for bad cooperation of -C and -u options (#688567)
Patch9: tar-1.26-update-with-change-directory.patch
# fix rawhide buildfailure with undefined gets
Patch10: tar-1.26-stdio.in.patch
# Prepare gnulib for xattrs and apply xattrs & acls & selinux (#850291)
Patch11: tar-1.26-xattrs-gnulib-prepare.patch
Patch12: tar-1.26-xattrs.patch
# fix regression with --keep-old-files option (#799252)
Patch13: tar-1.26-add-skip-old-files-option.patch

BuildRequires: autoconf automake texinfo gettext libacl-devel rsh
# allow proper tests for extended attributes
BuildRequires: attr acl

%if %{WITH_SELINUX}
BuildRequires: libselinux-devel policycoreutils
%endif
Provides: bundled(gnulib)
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package.

%prep
%setup -q
%patch1 -p1 -b .loneZeroWarning
%patch2 -p1 -b .vfatTruncate
%patch4 -p1 -b .wildcards
%patch5 -p1 -b .rofs
%patch6 -p1 -b .oldarchive
%patch7 -p1 -b .fail
%patch8 -p1 -b .openat
%patch9 -p1 -b .update_and_changedir
%patch10 -p1 -b .gets  %{?_rawbuild}
%patch11 -p1 -b .xattrs_gnulib_prep
%patch12 -p1 -b .xattrs2
%patch13 -p1 -b .skip-old-files

autoreconf

%build
%if %{WITH_SELINUX} == 0
export CONFIGURE_PARAMS+="--without-selinux"
%endif

%configure --bindir=/bin --libexecdir=/sbin $CONFIGURE_PARAMS
make

%install
make DESTDIR=$RPM_BUILD_ROOT bindir=/bin libexecdir=/sbin install

ln -s tar $RPM_BUILD_ROOT/bin/gtar
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -c -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1
ln -s tar.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/gtar.1

# XXX Nuke unpackaged files.
rm -f $RPM_BUILD_ROOT/sbin/rmt

%find_lang %name

%check
rm -f $RPM_BUILD_ROOT/test/testsuite
TESTSUITEFLAGS=-v make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_infodir}/tar.info.gz ]; then
   /sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/tar.info.gz ]; then
      /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir || :
   fi
fi

%files -f %{name}.lang
%doc AUTHORS ChangeLog ChangeLog.1 COPYING NEWS README THANKS TODO
%ifos linux
/bin/tar
/bin/gtar
%{_mandir}/man1/tar.1*
%{_mandir}/man1/gtar.1*
%else
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man*/*
%endif

%{_infodir}/tar.info*

%changelog
* Thu Nov 29 2012 Ondrej Vasik <ovasik@redhat.com> - 2:1.26-15
- add missing --full-time option to manpage

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> - 2:1.26-14
- fix bad behaviour of --keep-old-files and add --skip-old-files option
  (#799252)

* Wed Oct 10 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-13
- fix badly written macro for building --without-selinux
- allow to build tar in difference CoverityScan by forcing the '.gets' patch to
  be applied even in the run without patches

* Fri Oct 05 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-12
- repair the xattr-gnulib-prepare patch to allow build tar without SELinux
  support
- fedora-review compliance -> remove trailing white-spaces, remove macro from
  comment, remove BR of gawk;coreutils;gzip that should be covered automatically
  by minimum build environment, do not `rm -rf' buildroot at the beginning of
  install phase (needed only in EPEL), remove BuildRoot definition, remove
  defattr macro, s/define/global/
- do not use ${VAR} syntax for bash variables, use just $VAR

* Wed Aug 22 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-11
- fix manpage to reflect #850291 related commit

* Tue Aug 21 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-10
- prepare Gnulib for new xattrs (#850291)
- new version of RH xattrs patch (#850291)
- enable verbose mode in testsuite to allow better debugging on error

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-8
- force the fchown() be called before xattrs_set() (#771927)

* Sat Jun 16 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-7
- store&restore security.capability extended attributes category
  (#771927)
- fix build failure with undefined gets

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 2:1.26-6
- add virtual provides for bundled(gnulib) copylib (#821790)

* Thu Apr 04 2012 Pavel Raiskup <praiskup@redhat.com> 2:1.26-5
- fix for bad cooperation of the '-C' (change directory) and '-u' (update
  package) options (#688567)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 2:1.26-3
- Man page heading formatting fixes.

* Mon Sep 26 2011 Kamil Dudka <kdudka@redhat.com> 2:1.26-2
- restore basic functionality of --acl, --selinux, and --xattr (#717684)

* Sat Mar 12 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.26-1
- new upstream release 1.26
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-5
- drop unnecessary hard dependency on info package(#671157)

* Mon Jan 03 2011 Ondrej Vasik <ovasik@redhat.com> 2:1.25-4
- mention that some compression options might not work if
  the external program is not available(#666755)

* Wed Dec 08 2010 Kamil Dudka <kdudka@redhat.com> 2:1.25-3
- correctly store long sparse file names in PAX archives (#656834)

* Tue Nov 23 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-2
- fix issue with --one-file-system and --listed-incremental
  (#654718)

* Mon Nov 08 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.25-1
- new upstream release 1.25

* Mon Oct 25 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.24-1
- new upstream release 1.24, use .xz archive

* Wed Sep 29 2010 jkeating - 2:1.23-8
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-7
- match non-stripped file names (#637085)

* Mon Sep 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.23-6
- fix exclusion of long file names with --xattrs (#634866)
- do not crash with --listed-incremental (#635318)

* Mon Aug 16 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-5
- add support for security.NTACL xattrs (#621215)

* Tue Jun 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-4
- recognize old-archive/portability options(#594044)

* Wed Apr 07 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-3
- allow storing of extended attributes for fifo and block
  or character devices files(#573147)

* Mon Mar 15 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-2
- update help2maned manpage

* Fri Mar 12 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.23-1
- new upstream release 1.23, remove applied patches

* Wed Mar 10 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-17
- CVE-2010-0624 tar, cpio: Heap-based buffer overflow
  by expanding a specially-crafted archive (#572149)
- realloc within check_exclusion_tags() caused invalid write
  (#570591)
- not closing file descriptors for excluded files/dirs with
  exlude-tag... options could cause descriptor exhaustion
  (#570591)

* Sat Feb 20 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-16
- support for "lustre.*" extended attributes (#561855)

* Thu Feb 04 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-15
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)

* Wed Feb 03 2010 Kamil Dudka <kdudka@redhat.com> 2:1.22-14
- allow also build with SELinux support

* Mon Feb 01 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-13
- allow build without SELinux support(#556679)

* Tue Jan 05 2010 Ondrej Vasik <ovasik@redhat.com> 2:1.22-12
- do not fail with POSIX 2008 glibc futimens() (#552320)
- temporarily disable fix for #531441, causing stack smashing
  with newer glibc(#551206)

* Tue Dec 08 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-11
- fix segfault with corrupted metadata in code_ns_fraction
  (#531441)
- commented patches and sources

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-10
- store xattrs for symlinks (#525992) - by Kamil Dudka
- update tar(1) manpage (#539787)
- fix memory leak in xheader (#518079)

* Wed Nov 18 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-9
- store SELinux context for symlinks (#525992)

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-8
- provide symlink manpage for gtar

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-7
- do process install-info only without --excludedocs(#515923)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-5
- Fix restoring of directory default acls(#511145)
- Do not patch generated autotools files

* Thu Jun 25 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-4
- Report record size only if the archive refers to a device
  (#487760)
- Do not sigabrt with new gcc/glibc because of writing to
  struct members of gnutar header at once via strcpy

* Fri May 15 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-3
- ignore errors from setting utime() for source file
  on read-only filesystem (#500742)

* Fri Mar 06 2009 Kamil Dudka <kdudka@redhat.com> 2:1.22-2
- improve tar-1.14-loneZeroWarning.patch (#487315)

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.22-1
- New upstream release 1.22, removed applied patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 05 2009 Ondrej Vasik <ovasik@redhat.com> 2:1.21-1
- New upstream release 1.21, removed applied patches
- add support for -I option, fix testsuite failure

* Thu Dec 11 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-6
- add BuildRequires for rsh (#475950)

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-5
- fix off-by-one errors in xattrs patch (#472355)

* Mon Nov 10 2008 Kamil Dudka <kdudka@redhat.com> 2:1.20-4
- fixed bug #465803: labels with --multi-volume (upstream patch)

* Fri Oct 10 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-3
- Fixed wrong documentation for xattrs options (#466517)
- fixed bug with null file terminator and change dirs
  (upstream)

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-2
- patch fuzz clean up

* Mon May 26 2008 Ondrej Vasik <ovasik@redhat.com> 2:1.20-1
- new upstream release 1.20 (lzma support, few new options
  and bugfixes)
- heavily modified xattrs patches(as tar-1.20 now uses automake
  1.10.1)

* Tue Feb 12 2008 Radek Brich <rbrich@redhat.com> 2:1.19-3
- do not print getfilecon/setfilecon warnings when SELinux is disabled
  or SELinux data are not available (bz#431879)
- fix for GCC 4.3

* Mon Jan 21 2008 Radek Brich <rbrich@redhat.com> 2:1.19-2
- fix errors in man page
  * fix definition of --occurrence (bz#416661, patch by Jonathan Wakely)
  * update meaning of -l: it has changed from --one-filesystem
    to --check-links (bz#426717)
- update license tag, tar 1.19 is GPLv3+

* Mon Dec 17 2007 Radek Brich <rbrich@redhat.com> 2:1.19-1
- upgrade to 1.19
- updated xattrs patch, removed 3 upstream patches

* Wed Dec 12 2007 Radek Brich <rbrich@redhat.com> 2:1.17-5
- fix (non)detection of xattrs
- move configure stuff from -xattrs patch to -xattrs-conf,
  so the original patch could be easily read
- fix -xattrs patch to work with zero length files and show
  warnings when xattrs not available (fixes by James Antill)
- possible corruption (#408621) - add warning to man page
  for now, may be actually fixed later, depending on upstream

* Tue Oct 23 2007 Radek Brich <rbrich@redhat.com> 2:1.17-4
- upstream patch for CVE-2007-4476
  (tar stack crashing in safer_name_suffix)

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-3
- gawk build dependency

* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-2
- updated license tag
- fixed CVE-2007-4131 tar directory traversal vulnerability (#251921)

* Thu Jun 28 2007 Radek Brich <rbrich@redhat.com> 2:1.17-1
- new upstream version
- patch for wildcards (#206841), restoring old behavior
- patch for testsuite
- update -xattrs patch
- drop 13 obsolete patches

* Tue Feb 06 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-26
- fix spec file to meet Fedora standards (#226478)

* Mon Jan 03 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-25
- fix non-failsafe install-info use in scriptlets (#223718)

* Wed Jan 03 2007 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-24
- supply tar man page (#219375)

* Tue Dec 12 2006 Florian La Roche <laroche@redhat.com> 2:1.15.1-23
- fix CVE-2006-6097 GNU tar directory traversal (#216937)

* Sat Dec 10 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-22
- fix some rpmlint spec file issues

* Wed Oct 25 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-21
- build with dist-tag

* Mon Oct 09 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-20
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Wed Oct 04 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-19
- another fix of tar-1.15.1-xattrs.patch from James Antill

* Sun Oct 01 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-18
- fix tar-1.15.1-xattrs.patch (#208701)

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 2:1.15.1-17
- start new epoch, downgrade to solid stable 1.15.1-16 (#206979),
- all patches are backported

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-2
- apply patches, which were forgotten during upgrade

* Wed Sep 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.91-1
- upgrade, which also fix incremental backup (#206121)

* Fri Sep 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-7
- fix tar-debuginfo package (#205615)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-6
- add xattr support (#200925), patch from james.antill@redhat.com

* Mon Jul 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-5
- fix incompatibilities in appending files to the end
  of an archive (#199515)

* Tue Jul 18 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-4
- fix problem with unpacking archives in a directory for which
  one has write permission but does not own (such as /tmp) (#149686)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.15.90-3.1
- rebuild

* Thu Jun 29 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-3
- fix typo in tar.1 man page

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-2
- exclude listed02.at from testsuite again, because it
  still fails on s390

* Tue Apr 25 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.90-1
- upgrade

* Mon Apr 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-16
- fix problem when options at the end of command line were
  not recognized (#188707)

* Thu Apr 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-15
- fix segmentation faul introduced with hugeSparse.patch

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-14
- fix problems with extracting large sparse archive members (#185460)

* Fri Feb 17 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-13
- fix heap overlfow bug CVE-2006-0300 (#181773)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.15.1-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Peter Vrabec <pvrabec@redhat.com> 1.15.1-12
- fix extracting sparse files to a filesystem like vfat,
  when ftruncate may fail to grow the size of a file.(#179507)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-11
- correctly pad archive members that shrunk during archiving (#172373)

* Tue Sep 06 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-10
- provide man page (#163709, #54243, #56041)

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-9
- silence newer option (#164902)

* Wed Jul 27 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-8
- A file is dumpable if it is sparse and both --sparse
  and --totals are specified (#154882)

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-7
- exclude listed02.at from testsuite

* Fri Jul 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-6
- remove tar-1.14-err.patch, not needed (158743)

* Fri Apr 15 2005 Peter Vrabec <pvrabec@redhat.com> 1.15.1-5
- extract sparse files even if the output fd is not seekable.(#154882)
- (sparse_scan_file): Bugfix. offset had incorrect type.

* Mon Mar 14 2005 Peter Vrabec <pvrabec@redhat.com>
- gcc4 fix (#150993) 1.15.1-4

* Mon Jan 31 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 1.15.1-3

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix tests/testsuite

* Fri Jan 07 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to 1.15.1

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- patch to stop issuing lone zero block warnings
- rebuilt

* Mon Oct 11 2004 Peter Vrabec <pvrabec@redhat.com>
- URL added to spec file
- spec file clean up

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Jeff Johnson <jbj@jbj.org> 1.14-1
- upgrade to 1.14.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.13.25-13
- rebuilt because of crt breakage on ppc64.
- dump automake15 requirement.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.13.25-10
- fix broken buildrquires on autoconf253

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 1.13.25-9
- rebuild from CVS.

* Fri Aug 23 2002 Phil Knirsch <pknirsch@redhat.com> 1.13.25-8
- Included security patch from errata release.

* Mon Jul  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-7
- Fix argv NULL termination (#64869)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-4
- Fix build with autoconf253 (LIBOBJ change; autoconf252 worked)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-2
- Don't include hardlinks to sockets in a tar file (#54827)

* Thu Sep 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.25-1
- 1.13.25

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.22-1
- Update to 1.13.22, adapt patches

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-6
- Fix #52084

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.13.19-5
- Fix build with current autoconf (stricter checking on AC_DEFINE)
- Fix segfault when tarring directories without having read permissions
  (#40802)

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't depend on librt.

* Fri Feb 23 2001 Trond Eivind Glomsröd <teg@redhat.com>
- langify

* Thu Feb 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the man page (#28915)

* Wed Feb 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.19, nukes -I and fixes up -N
- Add -I back in as an alias to -j with a nice loud warning

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.18
- Update man page to reflect changes

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix the "ignore failed read" option (Bug #8330)

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix hang on tar tvzf - <something.tar.gz, introduced by
  exit code fix (Bug #15448), Patch from Tim Waugh <twaugh@redhat.com>

* Fri Aug 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- really fix exit code (Bug #15448)

* Mon Aug  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix exit code (Bug #15448), patch from Tim Waugh <twaugh@redhat.com>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix the exclude bug (#9201)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Sun Jan  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.17
- remove dotbug patch (fixed in base)
- update download URL

* Fri Jan  7 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix a severe bug (tar xf any_package_containing_. would delete the
  current directory)

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.3.16
- unset LINGUAS before running configure

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 1.13.14
- Update man page to know about -I / --bzip
- Remove dependancy on rmt - tar can be used for anything local
  without it.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache.
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
