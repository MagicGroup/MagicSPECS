Name:           perl-JSON
Summary:        Parse and convert to JSON (JavaScript Object Notation)
Version:        2.90
Release:        1%{?dist}
License:        GPL+ or Artistic

Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MAKAMAKA/JSON-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/JSON/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Tie::IxHash)


%{?perl_default_filter:
%filter_from_provides /^perl(JSON::\(Backend::PP\|backportPP::Boolean\|Boolean\|PP\|PP::IncrParser\))/d
%filter_from_requires /^perl(JSON::backportPP)$/d
%perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(JSON::(Backend::PP|backportPP::Boolean|Boolean|PP|PP::IncrParser)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(JSON::backportPP\\)

%{?perl_default_subpackage_tests}

%description
This module converts between JSON (JavaScript Object Notation) and Perl
data structure into each other. For JSON, see http://www.crockford.com/JSON/.

%prep
%setup -q -n JSON-%{version}

# make rpmlint happy...
find .  -type f -exec chmod -c -x {} +
find t/ -type f -exec perl -pi -e 's|^#! perl|#!%{__perl}|' {} +
sed -i 's/\r//' README t/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Nov 03 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.90-1
- Update to 2.90

* Sun Oct 20 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.61-1
- Update to 2.61

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.59-2
- Perl 5.18 rebuild

* Sun Jun 09 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.59-1
- Update to 2.59

* Sun May 26 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.58-1
- Update to 2.58

* Sun Apr 07 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.57-1
- Update to 2.57
- Remove no-longer-used macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Petr Šabata <contyk@redhat.com> - 2.53-7
- Add some missing and remove some obsolete deps

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.53-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 2.53-3
- update filtering macros for rpm 4.9

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.53-2
- Perl mass rebuild

* Sun May 22 2011 Paul Howarth <paul@city-fan.org> 2.53-1
- update to 2.53
  - fixed to_json (CPAN RT#68359)
  - backport JSON::PP 2.27200 (fixed incr_parse decoding string more correctly
    - CPAN RT#68032)
  - made Makefile.PL skip an installing XS question when set $ENV{PERL_ONLY} or
    $ENV{NO_XS} (CPAN RT#66820)

* Tue Mar  8 2011 Paul Howarth <paul@city-fan.org> 2.51-1
- update to 2.51 (#683052)
  - import JSON::PP 2.27105 as BackportPP
  - fix documentation (CPAN RT#64738)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> 2.50-1
- update to 2.50 (#665621)
  - JSON::PP split off into separate distribution and replaced with
    JSON::backportPP instead for internal use
- BR: perl(Test::Pod)
- drop t/ from %%doc as the tests are in the -tests subpackage
- filter private module perl(JSON::backportPP) from requires
- filter private module perl(JSON::backportPP::Boolean) from provides
- filter private module perl(JSON::Backend::PP) from provides
- filter private module perl(JSON::Boolean) from provides
- filter private module perl(JSON::PP) from provides (really JSON::backportPP)
- filter private module perl(JSON::PP::IncrParser) from provides

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 2.27-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.17-2
- Mass rebuild with perl-5.12.0

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 2.17-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(HTTP::Request)
- dropped old BR on perl(HTTP::Response)
- dropped old requires on perl(HTTP::Daemon)
- dropped old requires on perl(LWP::UserAgent)
- dropped old requires on perl(Scalar::Util)

* Wed Sep 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-5
- adjust filtering so we don't drop the versioned perl(JSON:PP) prov

* Tue Sep 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-4
- bump

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-3
- update filtering 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-1
- auto-update to 2.15 (by cpan-spec-update 0.01)

* Sun Mar 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.14-1
- update to 2.14

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.12-1
- update to 2.12

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.11-1
- update to 2.11

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.09-1
- update to 2.09

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.07-1
- update to 2.x series before F9

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.15-2
- rebuild for new perl

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- update to 1.15

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.14-1
- update to 1.14

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.13-1
- update to 1.13

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.12-1
- update to 1.12
- add t/ to %%doc

* Wed Apr 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-2
- bump

* Tue Apr 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Apr 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.10-1
- Specfile autogenerated by cpanspec 1.69.1.
