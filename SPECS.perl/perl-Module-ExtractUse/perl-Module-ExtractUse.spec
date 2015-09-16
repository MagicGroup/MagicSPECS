Name:           perl-Module-ExtractUse
Version:	0.32
Release:	1%{?dist}
Summary:        Find out what modules are used
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-ExtractUse/
Source0:        http://www.cpan.org/modules/by-module/Module/Module-ExtractUse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build) >= 0.37
BuildRequires:  perl(Parse::RecDescent) >= 1.967009
BuildRequires:  perl(Pod::Strip)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl(version)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Module::ExtractUse is basically a Parse::RecDescent grammar to parse Perl
code. It tries very hard to find all modules (whether pragmas, Core, or
from CPAN) used by the parsed code.

%prep
%setup -q -n Module-ExtractUse-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test
./Build test --test_files="xt/*.t"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes README example/
%dir %{perl_vendorlib}/Module/
%{perl_vendorlib}/Module/ExtractUse.pm
%dir %{perl_vendorlib}/Module/ExtractUse/
%{perl_vendorlib}/Module/ExtractUse/Grammar.pm
%{_mandir}/man3/Module::ExtractUse.3pm*
%{_mandir}/man3/Module::ExtractUse::Grammar.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.32-1
- 更新到 0.32

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.28-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.28-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.28-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.28-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.28-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.28-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.28-2
- 为 Magic 3.0 重建

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - Whitespace in use base is valid

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.27-3
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 0.27-2
- Round Module::Build version to 2 digits

* Fri Mar 23 2012 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Removed Test::NoWarnings from a t/23_universal_require.t because it upsets
    the (manual) plan if the tests are skipped

* Thu Mar 22 2012 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Autogenerate the grammar during ./Build (CPAN RT#74879)
  - Added $VERSION to into Module::ExtractUse::Grammar (CPAN RT#75342)
  - Require at least version 1.967009 of Parse::RecDescent (CPAN RT#75130)
  - Fix typos (CPAN RT#75115)
  - Switched to Dist::Zilla
- Drop grammar recompilation, no longer needed
- BR: perl(Test::More)
- Bump perl(Module::Build) version requirement to 0.3601
- Bump perl(Parse::RecDescent) version requirement to 1.967009
- Drop perl(Pod::Strip) and perl(Test::Deep) version requirements
- Package manpage for Module::ExtractUse::Grammar

* Mon Mar 19 2012 Paul Howarth <paul@city-fan.org> - 0.24-3
- Recompile the grammar to work with the new Parse::RecDescent (CPAN RT#74879)

* Tue Mar  6 2012 Paul Howarth <paul@city-fan.org> - 0.24-2
- BR: perl(Carp) and perl(version)
- Don't use macros for commands
- Make %%files list more explicit
- Package example
- Drop %%defattr, redundant since rpm 4.4

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 0.24-1
- Update to 0.24, removing previous grammar hack (rhbz #789976)

* Sat Feb  4 2012 Daniel P. Berrange <berrange@redhat.com> - 0.23-11
- Regenerate grammar for new Parse::RecDescent (rhbz#786849)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-9
- Perl mass rebuild

* Thu Mar 17 2011 Paul Howarth <paul@city-fan.org> - 0.23-8
- Reinstate %%check

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-5
- Mass rebuild with perl-5.12.0 

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.23-1
- Update to 0.23 release

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-2
- rebuild for new perl

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.22-1.fc9
- Specfile autogenerated by cpanspec 1.73.
