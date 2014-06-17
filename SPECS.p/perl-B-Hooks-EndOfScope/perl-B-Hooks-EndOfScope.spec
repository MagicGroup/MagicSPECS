Name:		perl-B-Hooks-EndOfScope
Version:	0.11
Release:	6%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Summary:	Execute code after scope compilation finishes
Url:		http://search.cpan.org/dist/B-Hooks-EndOfScope
Source0:	http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/B-Hooks-EndOfScope-%{version}.tar.gz
Patch0:		B-Hooks-EndOfScope-0.10-shellbangs.patch
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Sub::Exporter)
BuildRequires:	perl(Variable::Magic) >= 0.48
# Test suite
BuildRequires:	perl(Test::More) >= 0.89
# Release tests
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module allows you to execute code when Perl has finished compiling the
surrounding scope.

%prep
%setup -q -n B-Hooks-EndOfScope-%{version}

# Remove shellbangs from tests to placate rpmlint
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
 RELEASE_TESTING=1

%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/B/
%{_mandir}/man3/B::Hooks::EndOfScope.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.11-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.11-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (a minor efficiency improvement)
- Bump perl(Variable::Magic) version requirement to 0.48

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10 (stop propagating our magic through localisation)
- Package LICENSE file
- Downgrade ExtUtils::MakeMaker version requirement to 6.30
- Upgrade Test::More version requirement to 0.89
- Drop Test::Pod version requirement for EPEL-6 spec compatibility
- BR: perl(Test::EOL) and perl(Test::NoTabs) for additional test coverage
- Clean up for modern rpmbuild since we have no branches prior to EPEL-6
  - Don't specify BuildRoot:
  - Skip cleaning of buildroot in %%install
  - Remove %%clean section
  - Drop redundant %%defattr
- Remove shellbangs from tests to placate rpmlint

* Tue Jan 17 2012 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09 (improve distribution metadata)
- Run release tests too
- BR: perl(Pod::Coverage::TrustPod), perl(Test::Pod) and
  perl(Test::Pod::Coverage) for release tests
- Spec clean-up:
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use tabs
  - Split buildreqs by Build/Module/Tests/Release tests

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.08-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.08-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- auto-update to 0.08 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Variable::Magic) (0.31 => 0.34)

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update for submission

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
