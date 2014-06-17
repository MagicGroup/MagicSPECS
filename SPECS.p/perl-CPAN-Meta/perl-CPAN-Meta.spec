Name:           perl-CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Version:        2.140640
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CPAN-Meta/
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.008
BuildRequires:  perl(JSON::PP) >= 2.27200
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4414
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(version) >= 0.88
# Main test suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.20
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More) >= 0.88
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.

%prep
%setup -q -n CPAN-Meta-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes CONTRIBUTING history LICENSE README Todo t/
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta.3*
%{_mandir}/man3/CPAN::Meta::Converter.3*
%{_mandir}/man3/CPAN::Meta::Feature.3*
%{_mandir}/man3/CPAN::Meta::History.3*
%{_mandir}/man3/CPAN::Meta::Prereqs.3*
%{_mandir}/man3/CPAN::Meta::Spec.3*
%{_mandir}/man3/CPAN::Meta::Validator.3*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.140640-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.140640-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.140640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Paul Howarth <paul@city-fan.org> - 2.140640-1
- Update to 2.140640
  - Improved bad version handling during META conversion
  - When downgrading multiple licenses to version 1.x META formats, if all the
    licenses are open source, the downgraded license will be "open_source", not
    "unknown"
  - Added a 'load_string' method that guesses whether the string is YAML or
    JSON
- Drop obsoletes/provides for old tests sub-package
- Classify buildreqs by usage
- Package upstream's CONTRIBUTING file
- Make %%files list more explicit

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 2.132830-1
- Update to 2.132830
  - Fixed incorrectly encoded META.yml
  - META validation used to allow a scalar value when a list (i.e. array
    reference) was required for a field; this has been tightened and
    validation will now fail if a scalar value is given
  - Installation on Perls < 5.12 will uninstall older versions installed
    due to being bundled with ExtUtils::MakeMaker
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
  - Dropped ExtUtils::MakeMaker configure_requires dependency to 6.17
  - CPAN::Meta::Prereqs now has a 'merged_requirements' method for combining
    requirements across multiple phases and types
  - Invalid 'meta-spec' is no longer a fatal error: instead, it will usually
    be treated as spec version "1.0" (prior to formalization of the meta-spec
    field); conversion has some heuristics for guessing a version depending on
    other fields if 'meta-spec' is missing or invalid
- Don't need to remove empty directories from the buildroot

* Thu Sep  5 2013 Paul Howarth <paul@city-fan.org> - 2.132140-1
- update to latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.120921-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-2
- Build-require Data::Dumper for tests

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.120921-1
- update to latest upstream version

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 2.120900-1
- update to latest upstream version

* Sun Mar 04 2012 Iain Arnell <iarnell@gmail.com> 2.120630-1
- update to latest upstream version

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 2.120530-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 2.120351-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.113640-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.113640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.113640-1
- update to latest version, which deprecated Version::Requirements

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 2.112621-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 2.112150-1
- update to latest upstream version

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.110930-2
- Perl mass rebuild

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 2.110930-1
- update to latest upstream version

* Sat Apr 02 2011 Iain Arnell <iarnell@gmail.com> 2.110910-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 2.110580-1
- update to latest upstream version
- drop BR perl(Storable)

* Sat Feb 26 2011 Iain Arnell <iarnell@gmail.com> 2.110550-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 2.110440-1
- update to latest upstream
- drop BR perl(autodie)
- drop BR perl(Data::Dumper)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 2.110350-1
- update to latest upstream version

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.102400-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 29 2010 Iain Arnell <iarnell@gmail.com> 2.102400-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.102400)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0.20)
- added a new br on perl(IO::Dir) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Storable) (version 0)
- added a new br on perl(autodie) (version 0)
- added a new br on perl(version) (version 0.82)

* Thu Aug 05 2010 Iain Arnell <iarnell@gmail.com> 2.102160-1
- update to latest upstream

* Wed Jun 16 2010 Iain Arnell <iarnell@gmail.com> 2.101670-1
- update to latest upstream

* Mon Jun 14 2010 Iain Arnell <iarnell@gmail.com> 2.101610-1
- update to latest upstream

* Tue Jun 01 2010 Iain Arnell <iarnell@gmail.com> 2.101461-2
- rebuild for perl-5.12

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 2.101461-1
- Specfile autogenerated by cpanspec 1.78.
- drop explicit requirements
