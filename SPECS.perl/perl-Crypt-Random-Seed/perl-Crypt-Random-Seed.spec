Name:           perl-Crypt-Random-Seed
Version:        0.03
Release:        4%{?dist}
Summary:        Simple method to get strong randomness
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-Random-Seed/
Source0:        http://www.cpan.org/modules/by-module/Crypt/Crypt-Random-Seed-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Crypt::Random::TESHA2)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.45
BuildRequires:  perl(warnings)
Requires:       perl(Crypt::Random::TESHA2)
Requires:       perl(IO::Socket)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A simple mechanism to get strong randomness. The main purpose of this
module is to provide a simple way to generate a seed for a PRNG such as
Math::Random::ISAAC, for use in cryptographic key generation, or as the
seed for an upstream module such as Bytes::Random::Secure. Flags for
requiring non-blocking sources are allowed, as well as a very simple method
for plugging in a source.

%prep
%setup -q -n Crypt-Random-Seed-%{version}

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
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README TODO examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.03-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.03-2
- Perl 5.22 rebuild

* Sun Jan 18 2015 David Dick <ddick@cpan.org> - 0.03-1
- Initial release
