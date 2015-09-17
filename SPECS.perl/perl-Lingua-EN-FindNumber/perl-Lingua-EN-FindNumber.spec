Name:           perl-Lingua-EN-FindNumber
Version:        1.31
Release:        1%{?dist}
Summary:        Locate (written) numbers in English text
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Lingua-EN-FindNumber/
Source0:        http://www.cpan.org/authors/id/N/NE/NEILB/Lingua-EN-FindNumber-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Lingua::EN::Words2Nums)
# Tests only
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
This module provides a regular expression for finding numbers in
English text. It also provides functions for extracting and
manipulating such numbers.

%prep
%setup -q -n Lingua-EN-FindNumber-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 24 2015 Petr Šabata <contyk@redhat.com> - 1.31-1
- 1.31 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.30-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Petr Šabata <contyk@redhat.com> 1.30-1
- Initial packaging.
