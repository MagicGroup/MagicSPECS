Name:           perl-Object-Accessor
# Epoch to compete with perl.spec
Epoch:          1
Version:        0.48
Release:        5%{?dist}
Summary:        Interface to create per object accessors
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Object-Accessor/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Object-Accessor-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
%if 0%(perl -e 'print $] > 5.017')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(if)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Params::Check) >= 0.34
# Tie::Scalar is not needed for tests
# Tie::StdScalar is not needed for tests
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if 0%(perl -e 'print $] > 5.017')
Requires:       perl(deprecate)
%endif

%description
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).

%prep
%setup -q -n Object-Accessor-%{version}

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
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.48-3
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.48-2
- Perl 5.18 rebuild

* Wed Jun 19 2013 Jitka Plesnikova <jplesnik@redhat.com> 0.48-1
- Specfile autogenerated by cpanspec 1.78.
