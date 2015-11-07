# Perl and RPM versioning don't work the same :-(
%global extraversion 01

Name:		perl-Test-Unit-Lite
Epoch:		1
Version:	0.12
Release:	23%{?dist}
Summary:	Unit testing without external dependencies
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Unit-Lite/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DE/DEXTER/Test-Unit-Lite-%{version}%{?extraversion}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Taint::Runtime)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter unwanted provides and requires (rpm 4.9 onwards)
%global __provides_exclude ^perl\\(Test::Unit::(Debug|HarnessUnit|Result|TestCase|TestRunner|TestSuite)\\)$
%global __requires_exclude ^perl\\(Test::Unit::Test(Runner|Suite)\\)

%description
This framework provides a lighter version of Test::Unit framework. It
implements some of the Test::Unit classes and methods needed to run test
units. Test::Unit::Lite tries to be compatible with public API of
Test::Unit. It doesn't implement all classes and methods at 100% and only
those necessary to run tests are available.

%prep
%setup -q -n Test-Unit-Lite-%{version}%{?extraversion}

# Filter unwanted provides and (prior to rpm 4.9)
# Unwanted requires not actually detected prior to rpm 4.9
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Evx 'perl\\(Test::Unit::(Debug|HarnessUnit|Result|TestCase|TestRunner|TestSuite)\\)'"
%define __perl_provides %{provfilt}

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Unit::Lite.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1:0.12-23
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:0.12-22
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1:0.12-21
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.12-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.12-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.12-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.12-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.12-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:0.12-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:0.12-13
- Perl 5.16 rebuild

* Sun Mar 25 2012 Paul Howarth <paul@city-fan.org> - 1:0.12-12
- Update to 0.1201
  - Repackaged with newer Module::Builder

* Sat Mar 24 2012 Paul Howarth <paul@city-fan.org> - 1:0.12-11
- Add buildreqs for Perl core modules that could be dual-lived
- Don't need to remove empty directories from buildroot
- Drop %%defattr, redundant since rpm 4.4

* Sat Sep 24 2011 Paul Howarth <paul@city-fan.org> - 1:0.12-10
- BR: perl(Carp) and perl(Cwd)
- Make %%files list more explicit
- Reduce requires filtering to what's actually needed
- Don't use macros for commands

* Wed Jun 22 2011 Petr Pisar <ppisar@redhat.com> - 1:0.12-9
- Do not require private modules

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.12-8
- Perl mass rebuild

* Thu May  5 2011 Paul Howarth <paul@city-fan.org> - 1:0.12-7
- Fix provides filter for rpm 4.9
- BR: perl(Taint::Runtime) for additional test coverage
- Include upstream LICENSE file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.12-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.12-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:0.12-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1:0.12-1
- Auto-update to 0.12 (by cpan-spec-update 0.01)
- Add epoch of 1 (0.1101 => 0.12)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Allisson Azevedo <allisson@gmail.com> - 0.1101-2
- Added filter provides

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> - 0.1101-1
- Initial rpm release
