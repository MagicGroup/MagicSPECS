Name:		perl-MooseX-Types-Stringlike
Summary:	Moose type constraints for strings or string-like objects
Version:	0.003
Release:	7%{?dist}
License:	ASL 2.0
URL:		http://search.cpan.org/dist/MooseX-Types-Stringlike/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/MooseX-Types-Stringlike-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
# Module Runtime
BuildRequires:	perl(MooseX::Types)
BuildRequires:	perl(MooseX::Types::Moose)
BuildRequires:	perl(overload)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Moose)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(version)
# Optional Test Requirements
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.120900
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides a more general version of the Str type. If coercions are
enabled, it will accept objects that overload stringification and coerces them
into strings.

%prep
%setup -q -n MooseX-Types-Stringlike-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::Types::Stringlike.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.003-7
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.003-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-4
- Perl 5.22 rebuild

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Paul Howarth <paul@city-fan.org> - 0.003-1
- Update to 0.003
  - New ArrayRefOfStringlike, ArrayRefOfStringable types to facilitate coercion
    of lists

* Thu Mar 27 2014 Paul Howarth <paul@city-fan.org> - 0.002-1
- Initial RPM version
