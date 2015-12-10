Name:           perl-MooX-Types-MooseLike
Version:        0.29
Release:        5%{?dist}
Summary:        Some Moosish types and a type builder
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/MooX-Types-MooseLike/
Source0:        http://www.cpan.org/authors/id/M/MA/MATEU/MooX-Types-MooseLike-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Runtime) >= 0.014
# Moose::Meta::TypeConstraint::Class not used at tests
BuildRequires:  perl(Moose::Meta::TypeConstraint::DuckType)
BuildRequires:  perl(Moose::Meta::TypeConstraint::Enum)
# Moose::Meta::TypeConstraint::Role not used at tests
BuildRequires:  perl(Moose::Meta::TypeConstraint::Union)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(Scalar::Util)
# Tests:
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Moo) >= 1.004002
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(overload)
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::More) >= 0.96
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(Module::Runtime) >= 0.014
Requires:   perl(Moose::Meta::TypeConstraint::Class)
Requires:   perl(Moose::Meta::TypeConstraint::DuckType)
Requires:   perl(Moose::Meta::TypeConstraint::Enum)
Requires:   perl(Moose::Meta::TypeConstraint::Role)
Requires:   perl(Moose::Meta::TypeConstraint::Union)
Requires:   perl(Moose::Util::TypeConstraints)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\(Module::Runtime\\)$

%description
See MooX::Types::MooseLike::Base for a list of available base types. Its source
also provides an example of how to build base types, along with both
parameterizable and non-parameterizable.

%prep
%setup -q -n MooX-Types-MooseLike-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.29-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.29-4
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.29-3
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.29-2
- 为 Magic 3.0 重建

* Fri Aug 28 2015 Petr Pisar <ppisar@redhat.com> - 0.29-1
- 0.29 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.20 rebuild

* Fri Aug 29 2014 Petr Pisar <ppisar@redhat.com> - 0.27-1
- 0.27 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 18 2013 Simone Caronni <negativo17@gmail.com> - 0.25-2
- Review fixes.

* Mon Aug 05 2013 Simone Caronni <negativo17@gmail.com> 0.25-1
- Specfile autogenerated by cpanspec 1.78.
