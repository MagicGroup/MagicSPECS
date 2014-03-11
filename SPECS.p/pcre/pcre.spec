# This is stable release:
#%%global rcversion RC1
Name: pcre
Version: 8.30
Release: %{?rcversion:0.}2%{?rcversion:.%rcversion}%{?dist}.1
%global myversion %{version}%{?rcversion:-%rcversion}
Summary: Perl-compatible regular expression library
Group: System Environment/Libraries
License: BSD
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Upstream thinks RPATH is good idea.
Patch0: pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1: pcre-8.30-refused_spelling_terminated.patch
BuildRequires: readline-devel
# New libtool to get rid of rpath
BuildRequires: autoconf, automake, libtool

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary: Static library for %{name}
Group: Development/Libraries

%description static
Library for static linking for %{name}.

%package tools
Summary: Auxiliary utilities for %{name}
Group: Development/Tools

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%prep
%setup -q -n %{name}-%{myversion}
# Get rid of rpath
%patch0 -p1 -b .multilib
%patch1 -p1 -b .terminated_typos
# Because of rpath patch
libtoolize --copy --force && autoreconf
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%configure \
%ifarch s390 s390x
    --disable-jit \
%else
    --enable-jit \
%endif
    --enable-pcretest-libreadline --enable-utf --enable-unicode-properties \
    --enable-pcre8 --enable-pcre16
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

%check
%ifarch s390 ppc
# larger stack is needed on s390, ppc
ulimit -s 10240
%endif
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%doc AUTHORS COPYING LICENCE NEWS README ChangeLog

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man1/pcre-config.*
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc HACKING

%files static
%{_libdir}/*.a
%doc COPYING LICENCE 

%files tools
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.*
%{_mandir}/man1/pcretest.*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 8.30-2.1
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Petr Pisar <ppisar@redhat.com> - 8.30-2
- Remove old libpcre.so.0 from distribution
- Move library to /usr

* Thu Feb 09 2012 Petr Pisar <ppisar@redhat.com> - 8.30-1
- 8.30 bump
- Add old libpcre.so.0 to preserve compatibility temporarily

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 8.30-0.1.RC1
- 8.30 Relase candidate 1 with UTF-16 support and *API change*
- Enable UTF-16 variant of PCRE library
- The pcre_info() function has been removed from pcre library.
- Loading compiled pattern does not fix endianity anymore. Instead an errror
  is returned and the application can use pcre_pattern_to_host_byte_order() to
  convert the pattern.
- Surrogates (0xD800---0xDFFF) are forbidden in UTF-8 mode now.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.21-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Petr Pisar <ppisar@redhat.com> - 8.21-2
- Fix unmatched subpattern to not become wildcard (bug #769597)
- Fix NULL pointer derefernce in pcre_free_study() (upstream bug #1186)

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 8.21-1
- 8.21 bump

* Thu Dec 08 2011 Karsten Hopp <karsten@redhat.com> 8.21-0.2.RC1
- ppc needs a larger stack similar to s390

* Tue Dec 06 2011 Petr Pisar <ppisar@redhat.com> - 8.21-0.1.RC1
- 8.21-RC1 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 8.20-7
- Fix case-less match if cases differ in encoding length (bug #756675)

* Fri Nov 25 2011 Petr Pisar <ppisar@redhat.com> - 8.20-6
- Fix cache-flush in JIT on PPC

* Tue Nov 22 2011 Petr Pisar <ppisar@redhat.com> - 8.20-5
- Fix repeated forward reference (bug #755969)

* Wed Nov 16 2011 Petr Pisar <ppisar@redhat.com> - 8.20-4
- Fix other look-behind regressions

* Tue Nov 15 2011 Petr Pisar <ppisar@redhat.com> - 8.20-3
- Fix look-behind regression in 8.20

* Tue Nov 15 2011 Dan Horák <dan[at]danny.cz> - 8.20-2
- fix build on s390(x) - disable jit and use larger stack for tests

* Fri Oct 21 2011 Petr Pisar <ppisar@redhat.com> - 8.20-1
- 8.20 bump

* Tue Oct 11 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC3
- 8.20-RC3 bump

* Fri Sep 23 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC2
- 8.20-RC2 bump

* Mon Sep 12 2011 Petr Pisar <ppisar@redhat.com> - 8.20-0.1.RC1
- 8.20-RC1 bump with JIT

* Tue Sep 06 2011 Petr Pisar <ppisar@redhat.com> - 8.13-4
- Fix infinite matching PRUNE (bug #735720)

* Mon Aug 22 2011 Petr Pisar <ppisar@redhat.com> - 8.13-3
- Fix parsing named class in expression (bug #732368)

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-2
- Separate utilities from libraries
- Move pcre-config(1) manual to pcre-devel sub-package
- Remove explicit defattr from spec code
- Compile pcretest with readline support

* Thu Aug 18 2011 Petr Pisar <ppisar@redhat.com> - 8.13-1
- 8.13 bump: Bug-fix version, Unicode tables updated to 6.0.0, new pcregrep
  option --buffer-size to adjust to long lines, new feature is passing of
  *MARK information to callouts.
- Should fix crash back-tracking over unicode sequence (bug #691319)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-4
- Fix caseless reference matching in UTF-8 mode when the upper/lower case
  characters have different lengths (bug #702623)

* Mon May 09 2011 Petr Pisar <ppisar@redhat.com> - 8.12-3
- Fix typos in manual pages (bugs #675476, #675477)
- Clean spec file up

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Petr Pisar <ppisar@redhat.com> - 8.12-1
- 8.12 bump
- Remove accepted pcre-8.11-Fix-typo-in-pcreprecompile-3.patch

* Mon Dec 13 2010 Petr Pisar <ppisar@redhat.com> - 8.11-1
- 8.11 bump
- See ChangeLog for changes. Namely changes have been made to the way
  PCRE_PARTIAL_HARD affects the matching of $, \z, \Z, \b, and \B.
- Fix typo in pcreprecompile(3) manual
- Document why shared library is not under /usr

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 8.10-1
- 8.10 bump (bug #612635)
- Add LICENCE to static subpackage because COPYING refers to it
- Remove useless rpath by using new libtool (simple sed does not work anymore
  because tests need to link against just-compiled library in %%check phase)

* Thu Jul 08 2010 Petr Pisar <ppisar@redhat.com> - 7.8-4
- Add COPYING to static subpackage
- Remove useless rpath

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> - 7.8-1
- Update to 7.8, drop upstreamed patches
- Fix destination of documentation (#427763)
- Use buildroot macro consistently
- Separate the static library, as per current Guidelines
- Satisfy rpmlint

* Fri Jul  4 2008 Tomas Hoger <thoger@redhat.com> - 7.3-4
- Apply Tavis Ormandy's patch for CVE-2008-2371.

* Tue Feb 12 2008 Tomas Hoger <thoger@redhat.com> - 7.3-3
- Backport patch from upstream pcre 7.6 to address buffer overflow
  caused by "a character class containing a very large number of
  characters with codepoints greater than 255 (in UTF-8 mode)"
  CVE-2008-0674, #431660
- Try re-enabling make check again.

* Fri Nov 16 2007 Stepan Kasal <skasal@redhat.com> - 7.3-2
- Remove obsolete ``reqs''
- add dist tag
- update BuildRoot

* Mon Sep 17 2007 Than Ngo <than@redhat.com> - 7.3-1
- bz292501, update to 7.3

* Mon Jan 22 2007 Than Ngo <than@redhat.com> - 7.0-1
- 7.0

* Mon Nov 27 2006 Than Ngo <than@redhat.com> - 6.7-1
- update to 6.7
- fix #217303, enable-unicode-properties
- sane stack limit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Tue May 09 2006 Than Ngo <than@redhat.com> 6.6-1
- update to 6.6
- fix multilib problem

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Aug 24 2005 Than Ngo <than@redhat.com> 6.3-1
- update to 6.3

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 5.0-4
- rebuild

* Fri Feb 11 2005 Joe Orton <jorton@redhat.com> 5.0-3
- don't print $libdir in 'pcre-config --libs' output

* Thu Nov 18 2004 Joe Orton <jorton@redhat.com> 5.0-2
- include LICENCE, AUTHORS in docdir
- run make check
- move %%configure to %%build

* Thu Nov 18 2004 Than Ngo <than@redhat.com> 5.0-1
- update to 5.0
- change License: BSD
- fix header location #64248

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 23 2004 Than Ngo <than@redhat.com> 4.5-2
- add the correct pcre license, #118781

* Fri Mar 12 2004 Than Ngo <than@redhat.com> 4.5-1
- update to 4.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 4.4-1
- 4.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Than Ngo <than@redhat.com> 4.2-1
- update to 4.2

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 3.9-9
- build with utf8, bug #81504

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 3.9-8
- Really remove .la files

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 3.9-7
- remove .la

* Thu Oct 10 2002 Than Ngo <than@redhat.com> 3.9-7
- Typo bug

* Wed Oct  9 2002 Than Ngo <than@redhat.com> 3.9-6
- Added missing so symlink

* Thu Sep 19 2002 Than Ngo <than@redhat.com> 3.9-5.1
- Fixed to build s390/s390x/x86_64

* Wed Jun 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-5
- Fix #65009

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-2
- rebuild

* Fri Jan 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-1
- Update to 3.9

* Wed Nov 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.7-1
- Update to 3.7

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.4-2
- Move libpcre to /lib, grep uses it these days (#41104)

* Wed Apr 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Move this to a separate package, used to be in kdesupport, but it's
  generally useful...
