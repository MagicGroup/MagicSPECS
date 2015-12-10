Name:           perl-Bytes-Random-Secure
Version:        0.28
Release:        6%{?dist}
Summary:        Perl extension to generate cryptographically-secure random bytes
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Bytes-Random-Secure/
Source0:        http://www.cpan.org/modules/by-module/Bytes/Bytes-Random-Secure-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Crypt::Random::Seed)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Math::Random::ISAAC)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(MIME::QuotedPrint) >= 3.03
BuildRequires:  perl(Scalar::Util) >= 1.21
BuildRequires:  perl(Statistics::Basic)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(warnings)
Requires:       perl(Scalar::Util) >= 1.21
Requires:       perl(MIME::QuotedPrint) >= 3.03
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Scalar::Util\\)$
%global __requires_exclude %__requires_exclude|^perl\\(MIME::QuotedPrint\\)$
%description
Bytes::Random::Secure provides two interfaces for obtaining crypto-quality
random bytes. The simple interface is built around plain functions. For
greater control over the Random Number Generator's seeding, there is an
Object Oriented interface that provides much more flexibility.

%prep
%setup -q -n Bytes-Random-Secure-%{version}

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
%doc Changes README examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.28-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.28-5
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.28-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-2
- Perl 5.22 rebuild

* Sun Jan 18 2015 David Dick <ddick@cpan.org> - 0.28-1
- Initial release
