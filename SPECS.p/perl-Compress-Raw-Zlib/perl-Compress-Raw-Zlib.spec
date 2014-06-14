Name:           perl-Compress-Raw-Zlib
Version:        2.065
Release:        2%{?dist}
Summary:        Low-level interface to the zlib compression library
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Compress-Raw-Zlib/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/Compress-Raw-Zlib-%{version}.tar.gz
BuildRequires:  perl(AutoLoader)
# XSLoader or DynaLoader; choose wisely
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
# Dual-lived module needs rebuilding early in the boot process
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
BuildRequires:  zlib-devel
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# see above
Requires:       perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
The Compress::Raw::Zlib module provides a Perl interface to the zlib
compression library, which is used by IO::Compress::Zlib.

%prep
%setup -q -n Compress-Raw-Zlib-%{version}

%build
BUILD_ZLIB=False 
OLD_ZLIB=False
ZLIB_LIB=%{_libdir}
ZLIB_INCLUDE=%{_includedir}
export BUILD_ZLIB OLD_ZLIB ZLIB_LIB ZLIB_INCLUDE

perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/Compress/
%{perl_vendorarch}/Compress/
%{_mandir}/man3/Compress::Raw::Zlib.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.065-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Paul Howarth <paul@city-fan.org> - 2.065-1
- Update to 2.065
  - Resolve c++ build failure in core (CPAN RT#92657)
  - gcc -g3: final link failed: Memory exhausted (CPAN RT#88936)

* Sun Feb  2 2014 Paul Howarth <paul@city-fan.org> - 2.064-1
- Update to 2.064
  - Handle non-PVs better (CPAN RT#91558)
  - Z_OK instead of Z_BUF_ERROR (CPAN RT#92521)

* Sun Nov  3 2013 Paul Howarth <paul@city-fan.org> - 2.063-1
- Update to 2.063
  - gcc -g3: final link failed: Memory exhausted (CPAN RT#88936)
  - Compress::Raw::Zlib uses AutoLoader for no reason (CPAN RT#88260)
  - Typo in Compress::Zlib _combine function documentation (CPAN RT#89305)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.062-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Mon Aug 12 2013 Paul Howarth <paul@city-fan.org> - 2.062-1
- Update to 2.062
  - Typo fix (CPAN RT#86417)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.061-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.061-2
- Perl 5.18 rebuild

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 2.061-1
- Update to 2.061
  - Include zlib 1.2.8 source
  - Typo fix (CPAN RT#85431)
  - Silence compiler warning by making 2nd parameter to DispStream a const char*

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.060-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Paul Howarth <paul@city-fan.org> - 2.060-1
- Update to 2.060 (mention SimpleZip in POD)

* Sun Nov 25 2012 Paul Howarth <paul@city-fan.org> - 2.059-1
- Update to 2.059
  - Copy-on-write support (CPAN RT#81353)

* Tue Nov 13 2012 Paul Howarth <paul@city-fan.org> - 2.058-1
- Update to 2.058
  - Compress::Raw::Zlib needs to use PERL_NO_GET_CONTEXT (CPAN RT#80319)
  - Install to 'site' instead of 'perl' when perl version is 5.11+
    (CPAN RT#79812)
  - Update to ppport.h that includes SvPV_nomg_nolen (CPAN RT#78079)

* Sat Aug 11 2012 Paul Howarth <paul@city-fan.org> - 2.056-1
- Update to 2.056
  - Fix C++ build issue

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.055-1
- Update to 2.055
  - Fix misuse of magic in API (CPAN RT#78079)
  - Include zlib 1.2.7 source
- BR: perl(Exporter) and perl(lib)
- BR: perl(Test::NoWarnings) except when bootstrapping
- Drop redundant explicit require for perl(Exporter)
- Drop BR: perl(bytes), not dual-lived

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.054-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.054-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.054-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.054-2
- Omit optional Test::Pod tests on bootstrap

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 2.054-1
- Update to 2.054
  - Fix build issue on Win32 (CPAN RT#77030)

* Sun May  6 2012 Paul Howarth <paul@city-fan.org> - 2.053-1
- Update to 2.053
  - Include zlib 1.2.7 source

* Sun Apr 29 2012 Paul Howarth <paul@city-fan.org> - 2.052-1
- Update to 2.052
  - Fix build issue when Perl is built with C++
- Don't need to remove empty directories from buildroot

* Thu Feb 23 2012 Paul Howarth <paul@city-fan.org> - 2.051-1
- Update to 2.051
  - Fix bug in Compress::Raw::Zlib on 64-bit Windows (CPAN RT#75222)

* Tue Feb 21 2012 Paul Howarth <paul@city-fan.org> - 2.050-1
- Update to 2.050
  - Fix build failure on Irix and Solaris (CPAN RT#75151)

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.049-1
- Update to 2.049
  - Include zlib 1.2.6 source

* Sun Jan 29 2012 Paul Howarth <paul@city-fan.org> - 2.048-1
- Update to 2.048
  - Allow flush to be called multiple times without any intermediate call to
    deflate and still return Z_OK
  - Added support for zlibCompileFlags
  - Set minimum Perl version to 5.6
  - Set minimum zlib version to 1.2.0
- Don't use macros for commands

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 2.045-2
- Rebuild for gcc 4.7 in Rawhide

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.045-1
- Update to 2.045
  - Moved FAQ.pod into Zlib.pm

* Sun Dec  4 2011 Paul Howarth <paul@city-fan.org> - 2.044-1
- Update to 2.044
  - Moved FAQ.pod under the lib directory so it can get installed

* Mon Nov 21 2011 Paul Howarth <paul@city-fan.org> - 2.043-1
- Update to 2.043 (no changes)

* Fri Nov 18 2011 Paul Howarth <paul@city-fan.org> - 2.042-1
- Update to 2.042 (no changes)

* Sat Oct 29 2011 Paul Howarth <paul@city-fan.org> - 2.040-1
- Update to 2.040
  - Croak if attempt to freeze/thaw compression object (CPAN RT#69985)
- BR: perl(Carp)

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.037-4
- Install to vendorlib so that our debuginfo does not conflict with that of
  the main perl package

* Thu Jul 28 2011 Karsten Hopp <karsten@redhat.com> 2.037-3
- Bump and rebuild as it got compiled with the old perl on ppc

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-2
- Perl mass rebuild

* Wed Jun 22 2011 Paul Howarth <paul@city-fan.org> - 2.037-1
- Update to 2.037 (no changes)

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 2.036-2
- Perl mass rebuild

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 2.036-1
- 2.036 bump (added offset parameter to CRC32)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.035-3
- Perl mass rebuild

* Fri Jun 17 2011 Paul Howarth <paul@city-fan.org> - 2.035-2
- Perl mass rebuild

* Sat May  7 2011 Paul Howarth <paul@city-fan.org> - 2.035-1
- Update to 2.035 (no changes)

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 2.034-1
- 2.034 bump
- Buildroot and defattr cleanup
- Correcting BRs/Rs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.033-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.033-3
- remove epoch again, it's actually rpmdev bug
 https://fedorahosted.org/rpmdevtools/ticket/13

* Fri Jan 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.033-2
- re-add epoch. rpmdev-vercmp "0" 2.032 2 "" 2.033 1 -> 2.032

* Thu Jan 13 2011 Paul Howarth <paul@city-fan.org> - 2.033-1
- Update to 2.033 (fixed typos and spelling errors - Perl RT#81782)
- Drop redundant Obsoletes and Epoch tags
- Simplify provides filter

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 0:2.032-2
- BuildRequire perl(Test::Pod) for tests

* Fri Jan 07 2011 Petr Pisar <ppisar@redhat.com> - 0:2.032-1
- 2.032 bump

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.030-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 26 2010 Petr Sabata <psabata@redhat.com> - 0:2.030-1
- 2.030 version bump

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.027-1
- update

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0:2.024-3
- Mass rebuild with perl-5.12.0

* Mon Mar 29 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.024-2
- split again from main package for updated version

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-2
- Bump release to beat F-7 version

* Sun Jul 01 2007 Robin Norwood <rnorwood@redhat.com> - 2.005-1
- update to 2.005.

* Tue Jun 05 2007 Robin Norwood <rnorwood@redhat.com> - 2.004-1
- Initial build from CPAN

