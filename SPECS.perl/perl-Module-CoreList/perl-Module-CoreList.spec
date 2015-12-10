Name:           perl-Module-CoreList
# Epoch to compete with perl.spec
Epoch:          1
Version:        5.20150820
Release:        4%{?dist}
Summary:        What modules are shipped with versions of perl
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-CoreList/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Module-CoreList-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
# File::Copy not used
# Run-time:
# feature not used at tests
# Getopt::Long not used at tests
BuildRequires:  perl(List::Util)
# Pod::Usage not used at tests
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.88
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.00
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(List::Util)
Requires:       perl(version) >= 0.88

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(version\\)$

%description
Module::CoreList provides information on which core and dual-life modules
are shipped with each version of perl.

%package tools
Summary:        Tool for listing modules shipped with perl
Group:          Development/Tools
Requires:       perl(feature)
Requires:       perl(version) >= 0.88
Requires:       perl-Module-CoreList = %{epoch}:%{version}-%{release}
# The files were distributed with perl.spec's subpackage
# perl-Module-CoreList <= 1:5.020001-309
Conflicts:      perl-Module-CoreList < 1:5.20140914

%description tools
This package provides a corelist(1) tool which can be used to query what
modules were shipped with given perl version.


%prep
%setup -q -n Module-CoreList-%{version}

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

%files tools
%doc README
%{_bindir}/corelist
%{_mandir}/man1/corelist.*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:5.20150820-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:5.20150820-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1:5.20150820-2
- 为 Magic 3.0 重建

* Tue Aug 25 2015 Tom Callaway <spot@fedoraproject.org> - 1:5.20150820-1
- 5.20150820 bump

* Tue Jul 21 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150720-1
- 5.20150720 bump

* Mon Jun 22 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150620-1
- 5.20150620 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.20150520-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20150520-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:5.20150520-2
- Perl 5.22 rebuild

* Tue Jun 02 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150520-1
- 5.20150520 bump

* Tue Apr 21 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150420-1
- 5.20150420 bump

* Mon Mar 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150320-1
- 5.20150320 bump

* Mon Feb 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150220-1
- 5.20150220 bump

* Mon Feb 16 2015 Tom Callaway <spot@fedoraproject.org> - 1:5.20150214-1
- 5.20150214 bump

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20150120-1
- 5.20150120 bump

* Fri Jan 02 2015 Petr Pisar <ppisar@redhat.com> - 1:5.20141220-1
- 5.20141220 bump

* Tue Nov 25 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141120-1
- 5.20141120 bump

* Tue Oct 21 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141020-1
- 5.20141020 bump

* Wed Oct 08 2014 Petr Pisar <ppisar@redhat.com> - 1:5.20141002-1
- 5.20141002 bump

* Wed Sep 17 2014 Petr Pisar <ppisar@redhat.com> 1:5.20140914-1
- Specfile autogenerated by cpanspec 1.78.
