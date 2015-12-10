%global __libtoolize :
%global with_python3 0%{?fedora} || 0%{?rhel} >= 7

Summary: A utility for determining file types
Name: file
Version: 5.14
Release: 19%{?dist}
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
# Upstream says it's up to distributions to add a way to support local-magic.
Patch0: file-localmagic.patch
# sent upstream - should be included in next upstream release
Patch1: file-5.10-strength.patch
Patch2: file-5.10-sticky-bit.patch
Patch3: file-4.17-rpm-name.patch
Patch4: file-5.04-volume_key.patch
Patch5: file-5.04-man-return-code.patch
Patch6: file-5.04-generic-msdos.patch
Patch7: file-5.14-x86boot.patch
Patch8: file-5.14-perl.patch
Patch9: file-5.14-elfspace.patch
Patch10: file-5.14-bad-fsmagic-space.patch
Patch11: file-5.14-no-magic.patch
Patch12: file-5.14-journald.patch
Patch13: file-5.14-magic_load.patch
Patch14: file-5.14-CVE-2014-1943.patch
URL: http://www.darwinsys.com/file/
Requires: file-libs = %{version}-%{release}
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package libs
Summary: Libraries for applications using libmagic
Group:   Applications/File
License: BSD

%description libs

Libraries for applications using libmagic.

%package devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%package -n python-magic
Summary: Python 2 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python2-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python-magic
This package contains the Python 2 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%if %{with_python3}
%package -n python3-magic
Summary: Python 3 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python3-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python3-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif

%prep

# Don't use -b -- it will lead to poblems when compiling magic file!
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

iconv -f iso-8859-1 -t utf-8 < doc/libmagic.man > doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

%if %{with_python3}
rm -rf %{py3dir}
cp -a python %{py3dir}
%endif

%build
# Fix config.guess to find aarch64 - #925339
autoreconf -fi

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure --enable-fsect-man5 --disable-rpath
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/src/.libs
make
cd python
CFLAGS="%{optflags}" %{__python} setup.py build
%if %{with_python3}
cd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/file

make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# local magic in /etc/magic
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp -a ./magic/magic.local ${RPM_BUILD_ROOT}%{_sysconfdir}/magic

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/file/magic

cd python
%{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%if %{with_python3}
cd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc COPYING ChangeLog README
%{_bindir}/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/magic

%files libs
%doc COPYING ChangeLog README
%{_libdir}/*so.*
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/file
%{_datadir}/misc/*

%files devel
%{_libdir}/*.so
%{_includedir}/magic.h
%{_mandir}/man3/*

%files -n python-magic
%doc python/README COPYING python/example.py
%{python_sitelib}/magic.py
%{python_sitelib}/magic.pyc
%{python_sitelib}/magic.pyo
%if 0%{?fedora} || 0%{?rhel} >= 6
%{python_sitelib}/*egg-info
%endif

%if %{with_python3}
%files -n python3-magic
%doc python/README COPYING python/example.py
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/magic*.pyc
%{python3_sitelib}/__pycache__/magic*.pyo
%endif

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 5.14-19
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 5.14-18
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 5.14-17
- 为 Magic 3.0 重建

* Tue Feb 25 2014 Jan Kaluza <jkaluza@redhat.com> - 5.14-16
- fix potential memory leak introduced in previous commit

* Tue Feb 18 2014 Jan Kaluza <jkaluza@redhat.com> - 5.14-15
- fix #1065837 - fix for CVE-2014-1943

* Wed Jan 15 2014 Jan Kaluza <jkaluza@redhat.com> - 5.14-14
- fix #1051598 - reverse the order of shebang vs. package keyword detection
  in Perl by increasing strength of all Perl patterns

* Mon Sep 09 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-13
- fix #1001689 - fix segfault when calling magic_load twice

* Thu Aug 22 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-12
- fix #985072 - add support for journald files

* Thu Aug  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 5.14-11
- Build python-magic for python3 where applicable.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-9
- fix #980446 - do not segfault when no magic is loaded

* Mon Jun 17 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-8
- replace sitearch with sitelib

* Mon Jun 17 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-7
- build python-magic as noarch

* Wed May 15 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-6
- fix #962678 - do not exit if no magic file is loaded, we can still provide
  useful info without magic file

* Mon May 13 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-5
- fix #925339 - support aarch64

* Mon Apr 08 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-4
- fix #948255 - print white-space in fsmagic, but only when
  we know there will be some more output

* Fri Mar 29 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-3
- fix #928995 - do not print white-space in the end of fsmagic

* Mon Mar 25 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-2
- fix useless space in ELF output which could break libtool

* Fri Mar 22 2013 Jan Kaluza <jkaluza@redhat.com> - 5.14-1
- fix #891856 - update to file-5.14
- fix #909754 - magic number for Python-3.3
- fix #912271 - do not report dwarf debug info packages as 'stripped'
- fix #882321 - do not print 'unknown capability' for ELF capabilities for
  architectures which File does not support
- fix #866000 - show proper build id for ELF binaries
- fix #860139 - better dump file recognition on big endian architectures
- remove file-static subpackage
- move python-magic .py files to python_sitearch

* Mon Mar 11 2013 Jan Kaluza <jkaluza@redhat.com> - 5.11-9
- fix #919466 - fix memory leak in get_default_magic

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-7
- removed duplicated patterns for backups generated by "dump" tool
- recognize volume_key escrow packets
- mention exit code in manpage
- remove weak msdos patterns

* Wed Nov 21 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-6
- clean up the spec file

* Tue Aug 14 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-5
- fix #847936 - decompress bzip2 properly when using -z param
- fix #847937 - read magic patterns also from ~/.magic.mgc

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-3
- removed buildroot, defattr

* Thu Jun 21 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-2
- detect names of RPM packages
- detect swap on ia64 architecture

* Mon Feb 27 2012 Jan Kaluza <jkaluza@redhat.com> - 5.11-1
- fix #796130 - update to file-5.11
- fix #796209 - recognize VDI images
- fix #795709 - recognize QED images

* Wed Jan 18 2012 Jan Kaluza <jkaluza@redhat.com> - 5.10-5
- fix detection of ASCII text files with setuid, setgid, or sticky bits

* Tue Jan 10 2012 Jan Kaluza <jkaluza@redhat.com> - 5.10-4
- fix #772651 - decrease strength of newly added "C source" patterns

* Tue Jan 03 2012 Jan Kaluza <jkaluza@redhat.com> - 5.10-3
- fix #771292 - do not show 'using regular magic file' warning for /etc/magic,
  because this file is not supposed to be compiled

* Mon Jan 02 2012 Jan Kaluza <jkaluza@redhat.com> - 5.10-2
- fix #770006 - detect tnef files

* Mon Jan 02 2012 Jan Kaluza <jkaluza@redhat.com> - 5.10-1
- fix #771030 - update to file-5.10

* Mon Jan 02 2012 Jan Kaluza <jkaluza@redhat.com> - 5.09-3
- fix #720321 - added /etc/magic config file to let users define their local
  magic patterns

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.09-2
- Rebuilt for glibc bug#747377

* Thu Sep 29 2011 Jan Kaluza <jkaluza@redhat.com> - 5.09-1
- fix #739286 - update to file-5.09

* Thu Aug 04 2011 Jan Kaluza <jkaluza@redhat.com> - 5.08-1
- fix #728181 - update to file-5.08
- remove unused patches

* Tue Jun 14 2011 Jan Kaluza <jkaluza@redhat.com> - 5.07-5
- fix #712991 - include RPM noarch in /usr/share/magic

* Thu Jun 09 2011 Jan Kaluza <jkaluza@redhat.com> - 5.07-4
- fix #711843 - fix postscript detection

* Thu Jun 09 2011 Jan Kaluza <jkaluza@redhat.com> - 5.07-3
- fix #709953 - add support for BIOS version detection

* Mon May 23 2011 Jan Kaluza <jkaluza@redhat.com> - 5.07-2
- backported patches to fix 5.07 regressions
- fix #706231 - fixed ZIP detection
- fix #705183, #705499 - removed weak DOS device driver pattern

* Wed May 11 2011 Jan Kaluza <jkaluza@redhat.com> - 5.07-1
- update to new upstream version 5.07
- remove unused patches

* Tue Mar 01 2011 Jan Kaluza <jkaluza@redhat.com> - 5.05-4
- fix #678458 - support for Python 3.2 compiled files

* Thu Feb 10 2011 Jan Kaluza <jkaluza@redhat.com> - 5.05-3
- fix #676543 - improved TeX and LaTeX recognition
- fix #676041 - detect all supported RPM architectures

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Jan Kaluza <jkaluza@redhat.com> - 5.05-1
- fix #670319 - update to new upstream release 5.05
- removed useless patches

* Mon Jan 10 2011 Jan Kaluza <jkaluza@redhat.com> - 5.04-18
- fix #668304 - support for com32r programs
- distinguish between GFS2 and GFS1 filesystems

* Wed Nov 24 2010 Jan Kaluza <jkaluza@redhat.com> - 5.04-17
- fix #656395 - "string" magic directive supports longer strings

* Wed Aug 25 2010 Jan Kaluza <jkaluza@redhat.com> - 5.04-16
- fix #637785 - support for zip64 format

* Tue Aug 24 2010 Jan Kaluza <jkaluza@redhat.com> - 5.04-15
- fix #626591 - support for WebM format

* Thu Aug 12 2010 Jan Kaluza <jkaluza@redhat.com> - 5.04-14
- fix #623602 - support for Python 2.7 compiled files

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 5.04-13
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 Jan Kaluza <jkaluza@redhat.com> 5.04-12
- fix #599695 - try to get "from" attribute for ELF binaries
  only from core dumps.

* Thu Jul 08 2010 Jan Kaluza <jkaluza@redhat.com> 5.04-11
- added docs for file-libs

* Tue Jun 29 2010 Jan Kaluza <jkaluza@redhat.com> 5.04-10
- fix #608922 - updated z-machine magic

* Fri Jun 11 2010 Jan Kaluza <jkaluza@redhat.com> 5.04-9
- removed excessive HTML/SGML "magic patterns" (#603040)

* Wed Apr 14 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-8
- fix #580046 - the file command returns zero exit code 
                even in case of unexisting file being tested

* Wed Apr 07 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-7
- fix #566305 - "file" may trim too much of command line from core file

* Wed Mar 24 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-6
- fix #550212 - 'file' gives bad meta-data for squashfs-4.0 

* Wed Mar 24 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-5
- fix #575184 - file command does not print separator 
  when --print0 option is used

* Thu Mar 11 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-4
- fix #570785 - "file" misidentifies filesystem type

* Tue Feb 09 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-3
- fix #562840 -  [PATCH] Add matches for ruby modules

* Thu Jan 28 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-2
- fix #533245 -  segfaults on star.ulaw

* Mon Jan 25 2010 Daniel Novotny <dnovotny@redhat.com> 5.04-1
- update to new upstream release 5.04

* Mon Jan 18 2010 Daniel Novotny <dnovotny@redhat.com> 5.03-18
- static library moved to new "-static" subpackage (#556048)

* Fri Dec 25 2009 Robert Scheck <robert@fedoraproject.org> 5.03-17
- removed broken install of example.py (%%doc is much enough)

* Mon Nov 30 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-16
- fixed the patch for multilib (#515767)

* Tue Nov 24 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-15
- BuildRequires: autoconf, automake

* Tue Nov 24 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-14
- BuildRequires: automake because of the Makefile.am patch

* Fri Nov 13 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-13
- fix #537324 -  update spec conditional for rhel

* Thu Nov 05 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-12
- fix #533151 -  file command doesn't recognize deltaisos or rpm-only deltarpms

* Tue Oct 27 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-11
- fix #531082 -  RFE: add detection of Python 3 bytecode
- fix #531127 -  `file' command does not recognize mime type `image/vnd.djvu'

* Wed Oct 21 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-10
- fix #530083 -  file -s is not able to detect swap signature on ppc

* Tue Aug 25 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-9
- fix #515767 -  multilib: file /usr/share/misc/magic.mgc conflicts

* Thu Aug 06 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-8
- rebuild for #515767 -  multilib: file /usr/share/misc/magic.mgc conflicts

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-6
- fix #510429 -  file is confused by string "/* (if any) */" 
       in C header and claims it "Lisp/Scheme program text"

* Wed Jul 22 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-5
- #513079 -  RFE: file - recognize xfs metadump images

* Fri Jul 10 2009 Adam Jackson <ajax@redhat.com> 5.03-4
- Clean up %%description.

* Tue Jun 16 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-4
- one more PostScript font magic added (#505762),
  updated font patch

* Tue Jun 16 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-3
- added magic for three font issues (PostScript fonts)
  (#505758, #505759, #505765)

* Thu May 14 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-2
- fix #500739 - Disorganized magic* file locations in file-libs

* Mon May 11 2009 Daniel Novotny <dnovotny@redhat.com> 5.03-1
- new upstream version

* Tue May 05 2009 Daniel Novotny <dnovotny@redhat.com> 5.02-1
- new upstream version; drop upstreamed patches; this fixes #497913

* Wed Apr 29 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-8
- fix #498036 - Elang JAM file definition breaks detection of postscript-files

* Mon Apr 20 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-7
- fix previous patch:
  the name of the format is a bit different (MDUMP -> MDMP)

* Fri Apr 17 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-6
- fix #485835 (MDUMP files)

* Mon Mar 23 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-5
- added two font definitions (#491594, #491595)
  and a fix for file descriptor leak when MAGIC_COMPRESS used (#491596)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-3
- fix #486105 -  file-5.00-2.fc11 fails to recognise a file 
  (and makes rpmbuild fail)

* Mon Feb 16 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-2
- fix #485141 -  rpm failed while checking a French Word file

* Mon Feb 09 2009 Daniel Novotny <dnovotny@redhat.com> 5.00-1
- upgrade to 5.00
- drop upstreamed patches, rebase remaining patch

* Wed Jan 14 2009 Daniel Novotny <dnovotny@redhat.com> 4.26-9
- fix #476655 detect JPEG-2000 Code Stream Bitmap

* Mon Jan 12 2009 Daniel Novotny <dnovotny@redhat.com> 4.26-8
- fix #479300 - add btrfs filesystem magic

* Mon Dec 15 2008 Daniel Novotny <dnovotny@redhat.com> 4.26-7
- fix the LaTex issue in bz#474156

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.26-6
- Rebuild for Python 2.6

* Thu Dec 04 2008 Daniel Novotny <dnovotny@redhat.com> - 4.26-5
- fix #470811 - Spurious perl auto-requires

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.26-4
- Rebuild for Python 2.6

* Thu Oct 16 2008 Daniel Novotny <dnovotny@redhat.com> 4.26-3
- fix #465994 file --mime-encoding seems broken

* Tue Oct 07 2008 Daniel Novotny <dnovotny@redhat.com> 4.26-2
- fix #463809: rpmbuild rpmfcClassify: Assertion fails on some binary files
  (false positive test on "DOS device driver" crashed file(1)
   and rpmbuild(8) failed)  

* Mon Sep 15 2008 Daniel Novotny <dnovotny@redhat.com> 4.26-1
- new upstream version: fixes #462064

* Mon Jul 21 2008 Tomas Smetana <tsmetana@redhat.com> - 4.25-1
- new upstream version; drop upstreamed patches

* Fri Jun 06 2008 Tomas Smetana <tsmetana@redhat.com> - 4.24-4
- add GFS2 filesystem magic; thanks to Eric Sandeen
- add LVM snapshots magic (#449755); thanks to Jason Farrell

* Wed Jun 04 2008 Tomas Smetana <tsmetana@redhat.com> - 4.24-3
- drop patches that do nothing in recent build system
- create the text magic file during installation

* Tue Jun 03 2008 Tomas Smetana <tsmetana@redhat.com> - 4.24-2
- rebuild because of egg-info

* Tue Jun 03 2008 Tomas Smetana <tsmetana@redhat.com> - 4.24-1
- new upstream version

* Tue Mar 11 2008 Tomas Smetana <tsmetana@redhat.com> - 4.23-5
- fix EFI detection patch

* Fri Feb 01 2008 Tomas Smetana <tsmetana@redhat.com> - 4.23-4
- fix mismatching gzip files and text files as animations

* Fri Feb 01 2008 Tomas Smetana <tsmetana@redhat.com> - 4.23-3
- fix #430927 - detect ext4 filesystems

* Thu Jan 31 2008 Tomas Smetana <tsmetana@redhat.com> - 4.23-2
- fix #430952 - wrong handling of ELF binaries

* Tue Jan 29 2008 Tomas Smetana <tsmetana@redhat.com> - 4.23-1
- new upstream version; update patches; drop unused patches

* Thu Jan 24 2008 Tomas Smetana <tsmetana@redhat.com> - 4.21-5
- build a separate python-magic package; thanks to Terje Rosten

* Thu Dec 06 2007 Tomas Smetana <tsmetana@redhat.com> - 4.21-4
- add PE32/PE32+ magic

* Wed Aug 15 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.21-3
- resolves: #172015: no longer reports filename of crashed app when run on core files.
- resolves: #249578: Weird output from "file -i"
- resolves: #234817: file reports wrong filetype for microsoft word file

* Wed Jul  4 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.21-2
- resolves: #246700: RPM description isn't related to product
- resolves: #238789: file-devel depends on %%{version}
  but not on %%{version}-%%{release}
- resolves: #235267: for core files, file doesn't display the executable name

* Tue May 29 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.21-1
- upgrade to new upstream 4.21
- resolves: #241034: CVE-2007-2799 file integer overflow

* Wed Mar  7 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.20-1
- upgrade to new upstream 4.20

* Tue Feb 20 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.19-4
- rpath in file removal

* Mon Feb 19 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.19-3
- Resolves: #225750 - Merge Review: file

* Thu Jan 25 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.19-2
- Resolves: #223297 - file does not recognize OpenOffice "native" formats
- Resolves: #224344 - Magic rules should be in file-libs

* Tue Jan  9 2007 Martin Bacovsky <mbacovsk@redhat.com> - 4.19-1
- Resolves: #208880 - Pointless file(1) error message while detecting ELF 64-bit file
    thanks to <jakub@redhat.com> for patch
- Resolves: #214992 - file-devel should own %%_includedir/* %%_libdir/lib*.so
- Resolves: #203548 - a -devel package should be split out for libmagic
- upgrade to new upstream 4.19
- patch revision and cleaning
- split package to file, file-devel and file-libs

* Wed Aug 23 2006 Martin Bacovsky <mbacovsky@redhat.com> - 4.17-8
- fix recognition of perl script with embed awk (#203610) 

* Fri Aug 18 2006 Martin Bacovsky <mbacovsk@redhat.com> - 4.17-7
- fix recognition of bash script with embed awk (#202185)

* Thu Aug 03 2006 Martin Bacovsky <mbacovsk@redhat.com> - 4.17-6
- fix gziped empty file (#72986)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.17-5.1
- rebuild

* Mon Jul 10 2006 Radek Vokal <rvokal@redhat.com> 4.17-5
- fix powerpoint mine (#190373) <vonsch@gmail.com>

* Wed May 24 2006 Radek Vokal <rvokal@redhat.com> 4.17-4
- /usr/share/file is owned by package (#192858)
- fix magic for Clamav files (#192406)

* Fri Apr 21 2006 Radek Vokal <rvokal@redhat.com> 4.17-3
- add support for OCFS or ASM (#189017)

* Tue Mar 14 2006 Radek Vokal <rvokal@redhat.com> 4.17-2
- fix segfault when compiling magic
- add check for wctype.h
- fix for flac and mp3 files

* Mon Mar 13 2006 Radek Vokal <rvokal@redhat.com> 4.17-1
- upgrade to file-4.17, patch clean-up

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.16-6.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.16-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb 04 2006 Radek Vokal <rvokal@redhat.com> 4.16-6
- xen patch, recognizes Xen saved domain

* Fri Jan 13 2006 Radek Vokal <rvokal@redhat.com> 4.16-5
- fix for 64bit arrays

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Radek Vokal <rvokal@redhat.com> - 4.16-4
- printf utf8 filenames and don't use isprint() (#174348)

* Tue Nov 08 2005 Radek Vokal <rvokal@redhat.com> - 4.16-3
- remove .la files (#172633)

* Mon Oct 31 2005 Radek Vokal <rvokal@redhat.com> - 4.16-2
- fix core files output, show "from" (#172015)

* Tue Oct 18 2005 Radek Vokal <rvokal@redhat.com> - 4.16-1
- upgrade to upstream

* Mon Oct 03 2005 Radek Vokal <rvokal@redhat.com> - 4.15-4
- file output for Berkeley DB gains Cracklib (#168917)

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> - 4.15-3
- small fix in previously added patch, now it works for multiple params

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> - 4.15-2
- print xxx-style only once (#168617)

* Tue Aug 09 2005 Radek Vokal <rvokal@redhat.com> - 4.15-1
- upgrade to upstream 

* Tue Aug 09 2005 Radek Vokal <rvokal@redhat.com> - 4.14-4
- mime for mpeg and aac files fixed (#165323)

* Fri Aug 05 2005 Radek Vokal <rvokal@redhat.com> - 4.14-3
- mime for 3ds files removed, conflicts with text files (#165165)

* Fri Jul 22 2005 Radek Vokal <rvokal@redhat.com> - 4.14-2
- fixed mime types recognition (#163866) <mandriva.org>

* Thu Jul 14 2005 Radek Vokal <rvokal@redhat.com> - 4.14-1
- sync with upstream, patch clean-up

* Mon Jul 04 2005 Radek Vokal <rvokal@redhat.com> - 4.13-5
- fixed reiserfs check (#162378)

* Mon Apr 11 2005 Radek Vokal <rvokal@redhat.com> - 4.13-4
- check Cyrus files before Apple Quicktime movies (#154342) 

* Mon Mar 07 2005 Radek Vokal <rvokal@redhat.com> - 4.13-3
- check for shared libs before fs dump files (#149868)

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> - 4.13-2
- gcc4 rebuilt

* Tue Feb 15 2005 Radek Vokal <rvokal@redhat.com> - 4.13-1
- new version, fixing few bugs, patch clean-up
- consistent output for bzip files (#147440)

* Mon Jan 24 2005 Radek Vokal <rvokal@redhat.com> - 4.12-3
- core64 patch fixing output on core files (#145354) <kzak@redhat.com>
- minor change in magic patch

* Mon Jan 03 2005 Radek Vokal <rvokal@redhat.com> - 4.12-2
- fixed crashes in threaded environment (#143871) <arjanv@redhat.com>

* Thu Dec 02 2004 Radek Vokal <rvokal@redhat.com> - 4.12-1
- upgrade to file-4.12
- removed Tim's patch, tuned magic patch

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 4.10-4
- Convert libmagic.3 to UTF-8

* Thu Nov 18 2004 Radek Vokal <rvokal@redhat.com> 4.10-3
- set of patches from debian.org
- new magic types (#128763)
- zlib added to BuildReq (#125294)

* Tue Oct 12 2004 Tim Waugh <twaugh@redhat.com> 4.10-2
- Fixed occasional segfault (bug #131892).

* Wed Aug 11 2004 Radek Vokal <rvokal@redhat.com>
- zlib patch deleted, note patch deleted, rh patch updated, debian patch updated
- upgrade to file-4.10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 10 2004 Jakub Jelinek <jakub@redhat.com>
- fix ELF note handling (#109495)

* Tue Mar 23 2004 Karsten Hopp <karsten@redhat.de> 4.07-3 
- add docs (#115966)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 18 2004 Jeff Johnson <jbj@jbj.org> 4.07-1
- upgrade to 4.07.
- deal gracefully with unreadable files (#113207).
- detect PO files (from Debian).

* Tue Dec 16 2003 Jeff Johnson <jbj@jbj.org> 4.06-1
- upgrade to file-4.06.

* Mon Nov 10 2003 Tim Waugh <twaugh@redhat.com> 4.02-4
- Minimal fix for busy loop problem (bug #109495).

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 4.05-1
- upgrade to 4.05.

* Thu Oct  9 2003 Jeff Johnson <jbj@jbj.org> 4.02-3
- use zlib rather than exec'ing gzip.

-* Thu Aug 28 2003 Dan Walsh <dwalsh@redhat.com>
-- Add Selinux support.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig to post/postun

* Mon Apr 21 2003 Jeff Johnson <jbj@redhat.com> 4.02-1
- upgrade to file-4.02.

* Thu Feb 27 2003 Jeff Johnson <jbj@redhat.com> 3.39-9
- check size read from elf header (#85297).

* Tue Feb 18 2003 Matt Wilson <msw@redhat.com> 3.39-8
- add FHS compatibility symlink from /usr/share/misc/magic -> ../magic
  (#84509)

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 3.39-7
- the "real" fix to the vorbis/ogg magic details (#82810).

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> 3.39-6
- avoid vorbis/ogg magic details (#82810).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 3.39-5
- rebuilt

* Sun Jan 12 2003 Nalin Dahyabhai <nalin@redhat.com> 3.39-4
- PT_NOTE, take 3

* Fri Jan 10 2003 Nalin Dahyabhai <nalin@redhat.com> 3.39-3
- don't barf in ELF headers with align = 0

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 3.39-2
- don't get lost when looking at PT_NOTE sections

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 3.39-1
- update to 3.39.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.37-6
- Don't use an old magic.mime 
- Add mng detection (#64229)

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.37-5
- Rebuild

* Mon Jan 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.37-4
- Fix missing include of <stdint.h> (#58209)

* Tue Dec 11 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.37-2
- Add CFLAGS to handle large files (#53576)

* Mon Dec 10 2001 Trond Eivind Glomsrød <teg@redhat.com> 3.37-1
- 3.37
- s/Copyright/License/
- build with --enable-fsect-man5, drop patch
- disable two old patches

* Fri Jul 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- revert a patch to Magdir/elf, which breaks many libtool scripts
  in several rpm packages

* Mon Jun 25 2001 Crutcher Dunnavant <crutcher@redhat.com>
- iterate to 3.35

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Nov 26 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.33.

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- Bill made the patch but didn't apply it. :)

* Mon Aug 14 2000 Bill Nottingham <notting@redhat.com>
- 'ASCII text', not 'ASCII test' (#16168)

* Mon Jul 31 2000 Jeff Johnson <jbj@redhat.com>
- fix off-by-1 error when creating filename for use with -i.
- include a copy of GNOME /etc/mime-types in %%{_datadir}/magic.mime (#14741).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- install magic as man5/magic.5 with other formats (#11172).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 14 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Apr 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.30

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- add ia64 patch from rth

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages
- update to 3.28

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- identify ELF stripped files correctly (#4665).
- use SPARC (not sparc) consistently throughout (#4665).
- add entries for MS Office files (#4665).

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- diddle magic so that *.tfm files are identified correctly.

* Tue Jul  6 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.27.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- experimental support for realmedia files added

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binary.

* Fri Nov 27 1998 Jakub Jelinek <jj@ultra.linux.cz>
- add SPARC V9 magic.

* Tue Nov 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.26.

* Mon Aug 24 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.25.
- detect gimp XCF versions.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.24
- buildrooted

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Mon Mar 31 1997 Erik Troan <ewt@redhat.com>
- Fixed problems caused by 64 bit time_t.

* Thu Mar 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Improved recognition of Linux kernel images.
