Name:           perl-Test-Simple
Summary:        Basic utilities for writing tests
Version:        1.001003
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Simple
Source0:        http://search.cpan.org/CPAN/authors/id/E/EX/EXODIST/Test-Simple-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Pipe)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util) >= 1.13
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::Harness) >= 2.03
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(overload)
Requires:       perl(Scalar::Util) >= 1.13
Requires:       perl(Test::Harness) >= 2.03

## testing
#Requires:       perl-tests
#Requires:       /usr/bin/prove

%{?perl_default_filter}

%description
This package provides the bulk of the core testing facilities. For more
information, see perldoc for Test::Simple, Test::More, etc.

This package is the CPAN component of the dual-lifed core package Test-Simple.

%prep
%setup -q -n Test-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

#cd %%{_libexecdir}/perl5-tests/perl-tests/
#prove -I %%{buildroot}/blib -r t/

%files
%doc Changes README examples/ t/
%dir %{perl_vendorlib}/Test/
%{perl_vendorlib}/Test/Builder.pm
%{perl_vendorlib}/Test/Builder/
%{perl_vendorlib}/Test/More.pm
%{perl_vendorlib}/Test/Simple.pm
%doc %{perl_vendorlib}/Test/Tutorial.pod
%{_mandir}/man3/Test::Builder.3pm*
%{_mandir}/man3/Test::Builder::IO::Scalar.3pm*
%{_mandir}/man3/Test::Builder::Module.3pm*
%{_mandir}/man3/Test::Builder::Tester.3pm*
%{_mandir}/man3/Test::Builder::Tester::Color.3pm*
%{_mandir}/man3/Test::More.3pm*
%{_mandir}/man3/Test::Simple.3pm*
%{_mandir}/man3/Test::Tutorial.3pm*

%changelog
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
