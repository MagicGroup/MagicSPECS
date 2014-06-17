Name:		perl-Test-Vars
Version:	0.002
Release:	3%{?dist}
Summary:	Detects unused variables
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Vars/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Test-Vars-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl >= 4:5.10.0
BuildRequires:	perl(B)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(parent)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Spelling), hunspell-en
BuildRequires:	perl(Test::Synopsis)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Test::Vars finds unused variables in order to keep the source code tidy.

%prep
%setup -q -n Test-Vars-%{version}

# Placate rpmlint about script interpreters in examples
sed -i -e '1s|^#!perl|#!/usr/bin/perl|' example/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t"

%files
%doc Changes README example/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Vars.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.002-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.002-2
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Paul Howarth <paul@city-fan.org> - 0.002-1
- Update to 0.002
  - Fix compatibility with Perl 5.16 (CPAN RT#72133)
- Drop upstreamed patch for 5.16 compatibility

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Paul Howarth <paul@city-fan.org> - 0.001-5
- Fix compatibility with Perl 5.16 (CPAN RT#72133)
- Don't need to remove empty directories from buildroot

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.001-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug  8 2011 Paul Howarth <paul@city-fan.org> - 0.001-2
- Sanitize for Fedora submission
- Clean up for modern rpm

* Mon Aug  8 2011 Paul Howarth <paul@city-fan.org> - 0.001-1
- Initial RPM version
