Name:           perl-Lingua-EN-Number-IsOrdinal
Version:        0.05
Release:        4%{?dist}
Summary:        Detect if English number is ordinal or cardinal
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Lingua-EN-Number-IsOrdinal/
Source0:        http://www.cpan.org/authors/id/R/RK/RKITOVER/Lingua-EN-Number-IsOrdinal-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Lingua::EN::FindNumber)
# Tests only
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Try::Tiny)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
This module will tell you if a number, either in words or as digits, is a
cardinal or ordinal number.

%prep
%setup -q -n Lingua-EN-Number-IsOrdinal-%{version}

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
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.05-4
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.05-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Petr Šabata <contyk@redhat.com> - 0.05-1
- 0.05 bump

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-2
- Perl 5.22 rebuild

* Fri Nov 21 2014 Petr Šabata <contyk@redhat.com> 0.04-1
- Initial packaging.
