Name:           perl-Crypt-Random-TESHA2
Version:        0.01
Release:        4%{?dist}
Summary:        Random numbers using timer/schedule entropy
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-Random-TESHA2/
Source0:        http://www.cpan.org/modules/by-module/Crypt/Crypt-Random-TESHA2-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Digest::SHA) >= 5.22
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Statistics::Basic)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.45
BuildRequires:  perl(Time::HiRes) >= 1.98
BuildRequires:  perl(warnings)
Requires:       perl(Digest::SHA) >= 5.22
Requires:       perl(Exporter) >= 5.57
Requires:       perl(Time::HiRes) >= 1.98
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Digest::SHA\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Exporter\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Time::HiRes\\)$
%description
Generate random numbers using entropy gathered from timer /
scheduler jitter.

%prep
%setup -q -n Crypt-Random-TESHA2-%{version}

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
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.01-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.01-2
- Perl 5.22 rebuild

* Sat Jan 17 2015 David Dick <ddick@cpan.org> - 0.01-1
- Initial release
