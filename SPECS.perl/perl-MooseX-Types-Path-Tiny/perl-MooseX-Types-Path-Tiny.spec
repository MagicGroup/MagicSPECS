Name:		perl-MooseX-Types-Path-Tiny
Summary:	Path::Tiny types and coercions for Moose
Version:	0.011
Release:	6%{?dist}
License:	ASL 2.0
URL:		http://search.cpan.org/dist/MooseX-Types-Path-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-Path-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(Module::Build::Tiny) >= 0.037
# Module Runtime
BuildRequires:	perl(if)
BuildRequires:	perl(Moose) >= 2
BuildRequires:	perl(MooseX::Types)
BuildRequires:	perl(MooseX::Types::Moose)
BuildRequires:	perl(MooseX::Types::Stringlike)
BuildRequires:	perl(namespace::autoclean)
BuildRequires:	perl(Path::Tiny)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(File::pushd)
BuildRequires:	perl(Moose::Conflicts)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.96
# Optional Test Requirements
BuildRequires:	perl(CPAN::Meta) >= 2.120900
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(namespace::autoclean)

%description
This module provides Path::Tiny types for Moose. It handles two important
types of coercion:

 * Coercing objects with overloaded stringification

 * Coercing to absolute paths

It also can check to ensure that files or directories exist.

%prep
%setup -q -n MooseX-Types-Path-Tiny-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::Types::Path::Tiny.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.011-6
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.011-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.011-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-3
- Perl 5.22 rebuild

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.011-2
- Perl 5.20 mass

* Mon Sep  8 2014 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011
  - Documentation amendments
  - Add missing prereq declaration
- Use %%license
- Add explicit dependency on perl(namespace::autoclean)

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Paul Howarth <paul@city-fan.org> - 0.010-2
- Incorporate feedback from package review (#1081966)
  - BR: perl(Moose::Conflicts) for test suite

* Thu Mar 27 2014 Paul Howarth <paul@city-fan.org> - 0.010-1
- Initial RPM version
