# For versioned provides
%global T_T_Version 0.114
%global T_u_o_Version 0.16

Name:           perl-Test-Simple
Summary:        Basic utilities for writing tests
Version:        1.001014
Release:        349%{?dist}
# CC0: lib/ok.pm
# Public Domain: lib/Test/Tutorial.pod
# GPL+ or Artistic: the rest of the distribution
License:        (GPL+ or Artistic) and CC0 and Public Domain
URL:            http://search.cpan.org/dist/Test-Simple
Source0:        http://search.cpan.org/CPAN/authors/id/E/EX/EXODIST/Test-Simple-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.75
# Module Runtime
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(Scalar::Util) >= 1.13
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Test::Harness) >= 2.03
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Pipe)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(threads)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(overload)
Requires:       perl(PerlIO)
Requires:       perl(Scalar::Util) >= 1.13
Requires:       perl(Term::ANSIColor)
Requires:       perl(Test::Harness) >= 2.03
Requires:       perl(threads::shared)

# Test-Tester and Test-use-ok integrated at version 1.001010
Obsoletes:      perl-Test-Tester < 0.109-7
Provides:       perl-Test-Tester = %{T_T_Version}-1%{?dist}
Obsoletes:      perl-Test-use-ok < 0.11-7
Provides:       perl-Test-use-ok = %{T_u_o_Version}-1%{?dist}

%{?perl_default_filter}

%description
This package provides the bulk of the core testing facilities. For more
information, see perldoc for Test::Simple, Test::More, etc.

This package is the CPAN component of the dual-lifed core package Test-Simple.

%prep
%setup -q -n Test-Simple-%{version}

# Ensure version consistency for provides
perl -Ilib -MTest::Tester -MTest::use::ok -e '
  die "Inconsistent Test::Tester version: expected %{T_T_Version} / got $Test::Tester::VERSION\n"
    unless $Test::Tester::VERSION == %{T_T_Version};
  die "Inconsistent Test::use::ok version: expected %{T_u_o_Version} / got $Test::use::ok::VERSION\n"
    unless $Test::use::ok::VERSION == %{T_u_o_Version};'

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
make test AUTHOR_TESTING=1

%files
%doc Changes README examples/ t/
%dir %{perl_vendorlib}/Test/
%{perl_vendorlib}/ok.pm
%{perl_vendorlib}/Test/Builder.pm
%{perl_vendorlib}/Test/Builder/
%{perl_vendorlib}/Test/More.pm
%{perl_vendorlib}/Test/Simple.pm
%{perl_vendorlib}/Test/Tester.pm
%{perl_vendorlib}/Test/Tester/
%doc %{perl_vendorlib}/Test/Tutorial.pod
%{perl_vendorlib}/Test/use/
%{_mandir}/man3/ok.3*
%{_mandir}/man3/Test::Builder.3*
%{_mandir}/man3/Test::Builder::IO::Scalar.3*
%{_mandir}/man3/Test::Builder::Module.3*
%{_mandir}/man3/Test::Builder::Tester.3*
%{_mandir}/man3/Test::Builder::Tester::Color.3*
%{_mandir}/man3/Test::More.3*
%{_mandir}/man3/Test::Simple.3*
%{_mandir}/man3/Test::Tester.3*
%{_mandir}/man3/Test::Tester::Capture.3*
%{_mandir}/man3/Test::Tester::CaptureRunner.3*
%{_mandir}/man3/Test::Tutorial.3*
%{_mandir}/man3/Test::use::ok.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.001014-349
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.001014-348
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.001014-347
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001014-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001014-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001014-3
- Perl 5.22 rebuild

* Wed Mar 04 2015 Petr Šabata <contyk@redhat.com> - 1.001014-2
- Correct the license tag

* Wed Jan  7 2015 Paul Howarth <paul@city-fan.org> - 1.001014-1
- Update to 1.001014
  - Fix a unit test that broke on some platforms with spaces in the $^X path
  - Add a test to ensure that the Changes file is updated

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 1.001012-1
- Update to 1.001012
  - Move test that was dropped in the wrong directory

* Tue Dec 23 2014 Paul Howarth <paul@city-fan.org> - 1.001011-1
- Update to 1.001011
  - Fix windows test bug (GH#491)
  - Integrate Test::Tester and Test::use::ok for easier downgrade from trial
  - Remove POD Coverage test
- Obsolete/Provide perl-Test-Tester and perl-Test-use-ok
- Classify buildreqs by usage
- Use features from recent ExtUtils::MakeMaker to simplify spec
- Run tests with AUTHOR_TESTING=1 so we do the threads test too

* Tue Nov  4 2014 Paul Howarth <paul@city-fan.org> - 1.001009-1
- Update to 1.001009
  - Backport cmp_ok fix from alphas (GH#478)

* Thu Oct 16 2014 Paul Howarth <paul@city-fan.org> - 1.001008-1
- Update to 1.001008
  - Fix subtest name when skip_all is used

* Tue Sep  9 2014 Paul Howarth <paul@city-fan.org> - 1.001006-1
- Update to 1.001006
  - Documentation updates
  - Subtests accept args
  - Outdent subtest diag
  - Changed install path for perl 5.12 or higher

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.001003-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 1.001003-1
- Update to 1.001003
  - Documentation updates for maintainer change
- This release by EXODIST -> update source URL
- Drop obsoletes/provides for old tests sub-package

* Tue Nov  5 2013 Paul Howarth <paul@city-fan.org> - 1.001002-1
- Update to 1.001002
  - Restore ability to use regex with test_err and test_out (CPAN RT#89655)
- Drop upstreamed regex patch

* Sat Oct 12 2013 Paul Howarth <paul@city-fan.org> - 0.99-1
- 0.99 bump
- This release by RJBS -> update source URL

* Fri Aug 09 2013 Petr Pisar <ppisar@redhat.com> - 0.98.05-3
- Pass regular expression intact

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.98.05-1
- 0.98_05 bump

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.98-244
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.98-242
- Update dependencies and comments

* Thu Aug 23 2012 Paul Howarth <paul@city-fan.org> - 0.98-241
- Merge tests sub-package back into main package
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands
- Mark Tutorial.pod as %%doc
- Drop explicit dependency on perl-devel

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.98-6
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 0.98-5
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-3
- Change path on vendor, so our debuginfo are not conflicting with
  perl core debuginfos

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-2
- Perl mass rebuild

* Thu Feb 24 2011 Iain Arnell <iarnell@gmail.com> - 0.98-1
- Update to latest upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Iain Arnell <iarnell@gmail.com> - 0.96-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.94-2
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.94-1
- Specfile by Fedora::App::MaintainerTools 0.006
