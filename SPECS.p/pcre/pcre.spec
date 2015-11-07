# This is stable release:
#%%global rcversion RC1
Name: pcre
Version:	8.37
Release:	2%{?dist}
%global myversion %{version}%{?rcversion:-%rcversion}
Summary: Perl-compatible regular expression library
Summary(zh_CN.UTF-8): 兼容 Perl 的正则表达式库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: BSD
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Upstream thinks RPATH is good idea.
Patch0: pcre-8.21-multilib.patch
# Refused by upstream, bug #675477
Patch1: pcre-8.32-refused_spelling_terminated.patch
# Reset non-matched groups within capturing group up to forced match,
# bug #1161587, in upstream after 8.36
Patch2: pcre-8.36-Fix-bug-when-there-are-unset-groups-prior-to-ACCEPT-.patch
# Fix unused memory usage on zero-repeat assertion condition, bug #1165626,
# CVE-2014-8964, in upstream after 8.36
Patch3: pcre-8.36-Fix-zero-repeat-assertion-condition-bug.patch
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

%description -l zh_CN.UTF-8
兼容 Perl 的正则表达式库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static library for %{name}
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-devel%{_isa} = %{version}-%{release}

%description static
Library for static linking for %{name}.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package tools
Summary: Auxiliary utilities for %{name}
Summary(zh_CN.UTF-8): %{name} 的工具
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires: %{name}%{_isa} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%description tools -l zh_CN.UTF-8
%{name} 的工具。

%prep
%setup -q -n %{name}-%{myversion}
# Get rid of rpath
%patch0 -p1 -b .multilib
%patch1 -p1 -b .terminated_typos
%patch2 -p1 -b .reset_groups
%patch3 -p1 -b .zero_repeat_assertion
# Because of rpath patch
libtoolize --copy --force && autoreconf -vif
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 s390x sparc64 sparcv9
    --disable-jit \
%else
    --enable-jit \
%endif
    --enable-pcretest-libreadline --enable-utf --enable-unicode-properties \
    --enable-pcre8 --enable-pcre16 --enable-pcre32
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre
magic_rpm_clean.sh

%check
%ifarch s390 s390x ppc
# larger stack is needed on s390, ppc
ulimit -s 10240
%endif
make %{?_smp_mflags} check VERBOSE=yes

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE
%doc AUTHORS NEWS README ChangeLog

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
%{!?_licensedir:%global license %%doc}
%license COPYING LICENCE

%files tools
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.*
%{_mandir}/man1/pcretest.*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 8.37-2
- 更新到 8.37

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 8.36-3.3
- 为 Magic 3.0 重建

* Mon Mar 16 2015 Liu Di <liudidi@gmail.com> - 8.36-3.2
- 为 Magic 3.0 重建

* Thu Feb 19 2015 David Tardon <dtardon@redhat.com> - 8.36-3.1
- rebuild for C++ stdlib API changes in gcc5

* Thu Nov 20 2014 Petr Pisar <ppisar@redhat.com> - 8.36-3
- Fix CVE-2014-8964 (unused memory usage on zero-repeat assertion condition)
  (bug #1165626)

* Fri Nov 07 2014 Petr Pisar <ppisar@redhat.com> - 8.36-2
- Reset non-matched groups within capturing group up to forced match
  (bug #1161587)

* Tue Oct 07 2014 Petr Pisar <ppisar@redhat.com> - 8.36-1
- 8.36 bump

* Tue Sep 16 2014 Petr Pisar <ppisar@redhat.com> - 8.36-0.1.RC1
- 8.36 RC1 bump
- Enable JIT on aarch64

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Petr Pisar <ppisar@redhat.com> - 8.35-6
- Fix compile-time loop for recursive reference within a group with an
  indefinite repeat (bug #1128577)

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> - 8.35-5
- fix license handling

* Mon Jul 14 2014 Petr Pisar <ppisar@redhat.com> - 8.35-4
- Fix empty-matching possessive zero-repeat groups in interpreted mode
  (bug #1119241)
- Fix memory leaks in pcregrep (bug #1119257)
- Fix compiler crash for zero-repeated groups with a recursive back reference
  (bug #1119272)

* Thu Jun 19 2014 Petr Pisar <ppisar@redhat.com> - 8.35-3
- Fix bad starting data when char with more than one other case follows
  circumflex in multiline UTF mode (bug #1110620)
- Fix not including VT in starting characters for \s if pcre_study() is used
  (bug #1111045)
- Fix character class with a literal quotation (bug #1111054)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.35-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Petr Pisar <ppisar@redhat.com> - 8.35-2
- Do no rely on wrapping signed integer while parsing {min,max} expression
  (bug #1086630)

* Wed Apr 09 2014 Petr Pisar <ppisar@redhat.com> - 8.35-1
- 8.35 bump
- Run tests in parallel

* Fri Mar 14 2014 Petr Pisar <ppisar@redhat.com> - 8.35-0.1.RC1
- 8.35-RC1 bump

* Tue Mar 11 2014 Petr Pisar <ppisar@redhat.com> - 8.34-4
- Fix max/min quantifiers in ungreedy mode (bug #1074500)

* Tue Jan 21 2014 Dan Horák <dan[at]danny.cz> - 8.34-3
- enlarge stack for tests on s390x

* Thu Jan 09 2014 Petr Pisar <ppisar@redhat.com> - 8.34-2
- Fix jitted range check (bug #1048097)

* Mon Dec 16 2013 Petr Pisar <ppisar@redhat.com> - 8.34-1
- 8.34 bump

* Wed Oct 16 2013 Petr Pisar <ppisar@redhat.com> - 8.33-3
- Disable strict-aliasing on PPC64 (bug #881232)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.33-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Petr Pisar <ppisar@redhat.com> - 8.33-2
- Disable unsupported JIT on aarch64 (bug #969693)

* Thu May 30 2013 Petr Pisar <ppisar@redhat.com> - 8.33-1
- 8.33 bump

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.3.RC1
- Fix passing too small output vector to pcre_dfa_exec (bug #963284)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.2.RC1
- Fix bad handling of empty lines in pcregrep tool (bug #961789)
- Fix possible pcretest crash with a data line longer than 65536 bytes

* Thu May 02 2013 Petr Pisar <ppisar@redhat.com> - 8.33-0.1.RC1
- 8.33-RC1 bump

* Mon Jan 28 2013 Petr Pisar <ppisar@redhat.com> - 8.32-4
- Fix forward search in JIT when link size is 3 or greater
- Fix buffer over-read in UTF-16 and UTF-32 modes with JIT

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 8.32-3
- Adjust autoreconf to fix FTBFS on F-19

* Mon Jan 07 2013 Petr Pisar <ppisar@redhat.com> - 8.32-2
- Make inter-subpackage dependencies architecture specific (bug #892187)

* Fri Nov 30 2012 Petr Pisar <ppisar@redhat.com> - 8.32-1
- 8.32 bump

* Thu Nov 29 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.2.RC1
- Inter-depend sub-packages to prevent from mixing different versions

* Tue Nov 13 2012 Petr Pisar <ppisar@redhat.com> - 8.32-0.1.RC1
- 8.32-RC1 bump

* Mon Sep 03 2012 Petr Pisar <ppisar@redhat.com> - 8.31-2
- Set re_nsub in regcomp() properly (bug #853990)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.31-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Petr Pisar <ppisar@redhat.com> - 8.31-1
- 8.31 bump

* Tue Jun 05 2012 Petr Pisar <ppisar@redhat.com> - 8.31-0.1.RC1
- 8.31-RC1 bump

* Sat May 12 2012 Tom Callaway <spot@fedoraproject.org> - 8.30-7
- disable jit for sparcv9 and sparc64

* Fri May 11 2012 Petr Pisar <ppisar@redhat.com> - 8.30-6
- Fix spelling in manual pages (bug #820978)

* Mon Apr 23 2012 Petr Pisar <ppisar@redhat.com> - 8.30-5
- Possessify high ASCII (bug #815217)
- Fix ovector overflow (bug #815214)

* Fri Apr 20 2012 Petr Pisar <ppisar@redhat.com> - 8.30-4
- Possesify \s*\R (bug #813237)

* Thu Apr 05 2012 Petr Pisar <ppisar@redhat.com> - 8.30-3
- Fix look-behind assertion in UTF-8 JIT mode (bug #810314)

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

* Thu Jun 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.9-5
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
