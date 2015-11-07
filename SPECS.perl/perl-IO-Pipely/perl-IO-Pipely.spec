Name:           perl-IO-Pipely
Version:        0.005
Release:        7%{?dist}
Summary:        Portably create pipe() or pipe-like handles, one way or another
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Pipely/
Source0:        http://www.cpan.org/authors/id/R/RC/RCAPUTO/IO-Pipely-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base) >= 2.18
BuildRequires:  perl(Carp) >= 1.26
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter) >= 5.68
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fcntl) >= 1.06
BuildRequires:  perl(IO::Socket) >= 1.31
BuildRequires:  perl(Scalar::Util) >= 1.29
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol) >= 1.06
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(base) >= 2.18
Requires:       perl(Exporter) >= 5.68
Requires:       perl(Fcntl) >= 1.06
Requires:       perl(IO::Socket) >= 1.31
Requires:       perl(Symbol) >= 1.06

%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(base\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Exporter\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Fcntl\\)$
%global __requires_exclude %__requires_exclude|^perl\\(IO::Socket\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Symbol\\)$

%description
IO::Pipely provides a couple functions to portably create one- and two-way
pipes and pipe-like socket pairs. It acknowledges and works around known
platform issues so you don't have to.

%prep
%setup -q -n IO-Pipely-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc CHANGES LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.005-7
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.005-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-4
- Perl 5.22 rebuild

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.005-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 22 2013 Petr Šabata <contyk@redhat.com> 0.005-1
- Initial package submitted for review
