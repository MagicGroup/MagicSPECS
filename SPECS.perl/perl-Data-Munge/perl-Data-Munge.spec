Name:           perl-Data-Munge
Version:        0.095
Release:        2%{?dist}
Summary:        Utility functions for working with perl data structures and code references
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Munge/
Source0:        http://www.cpan.org/modules/by-module/Data/Data-Munge-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
# Scalar::Util not used since perl 5.016
# Tests:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module defines a few generally useful utility functions that process
perl data structures and code references.

%prep
%setup -q -n Data-Munge-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.095-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 0.095-1
- 0.095 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.093-2
- Perl 5.22 rebuild

* Sat Jan 17 2015 David Dick <ddick@cpan.org> - 0.093-1
- Fix typo in synopsis

* Sat Nov 22 2014 David Dick <ddick@cpan.org> - 0.091-1
- Work around regex bug in perls < 5.18 that causes spurious test failures.

* Fri Oct 03 2014 David Dick <ddick@cpan.org> - 0.08-1
- Initial release
