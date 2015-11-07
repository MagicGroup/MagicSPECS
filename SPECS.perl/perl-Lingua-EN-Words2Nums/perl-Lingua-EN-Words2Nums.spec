Name:           perl-Lingua-EN-Words2Nums
Version:        0.18
Release:        5%{?dist}
Summary:        Convert English text to numbers
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Lingua-EN-Words2Nums/
Source0:        http://www.cpan.org/authors/id/J/JO/JOEY/Lingua-EN-Words2Nums-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
This module converts English text into numbers. It supports both ordinal
and cardinal numbers, negative numbers, and very large numbers.

%prep
%setup -q -n Lingua-EN-Words2Nums-%{version}
chmod -c a-x testnum

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README samples testnum TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.18-5
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.18-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Petr Šabata <contyk@redhat.com> 0.18-1
- Initial packaging.
