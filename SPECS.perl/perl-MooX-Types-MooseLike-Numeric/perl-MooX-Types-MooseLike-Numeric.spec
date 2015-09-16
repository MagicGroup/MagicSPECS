Name:           perl-MooX-Types-MooseLike-Numeric
Version:        1.02
Release:        6%{?dist}
Summary:        Moo types for numbers
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooX-Types-MooseLike-Numeric/
Source0:        http://www.cpan.org/authors/id/M/MA/MATEU/MooX-Types-MooseLike-Numeric-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Moo)
BuildRequires:  perl(MooX::Types::MooseLike) >= 0.23
BuildRequires:  perl(MooX::Types::MooseLike::Base)
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

Requires:       perl(MooX::Types::MooseLike) >= 0.23
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Filter under-specified requires
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(MooX::Types::MooseLike\\)$

%description
Moo types for numbers, adapted from MooseX::Types::Common::Numeric.

%prep
%setup -q -n MooX-Types-MooseLike-Numeric-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.02-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-3
- Perl 5.20 rebuild

* Tue Jun 17 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.02-2
- Spec file cosmetics.

* Sun Jun 08 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.02-1
- Initial Fedora package.
