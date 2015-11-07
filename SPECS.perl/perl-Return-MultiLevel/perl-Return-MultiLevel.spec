Name:           perl-Return-MultiLevel
Version:        0.04
Release:        5%{?dist}
Summary:        Return across multiple call levels
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Return-MultiLevel/
Source0:        http://www.cpan.org/modules/by-module/Return/Return-MultiLevel-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Munge) >= 0.07
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.48
BuildRequires:  perl(parent)
# Not including Scope::Upper as it is only required it the user specifies a specific ENV variable
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
Requires:       perl(Data::Munge) >= 0.07
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Data::Munge\\)$
%description
This module provides a way to return immediately from a deeply nested call
stack. This is similar to exceptions, but exceptions don't stop
automatically at a target frame (and they can be caught by intermediate
stack frames using eval). In other words, this is more like
setjmp(3)/longjmp(3) than die.

%prep
%setup -q -n Return-MultiLevel-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
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
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.04-5
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.04-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-2
- Perl 5.22 rebuild

* Fri Oct 03 2014 David Dick <ddick@cpan.org> - 0.04-1
- Initial release
