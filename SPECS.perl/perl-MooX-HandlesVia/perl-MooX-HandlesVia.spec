Name:           perl-MooX-HandlesVia
Version:        0.001008
Release:        5%{?dist}
Summary:        NativeTrait-like behavior for Moo
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooX-HandlesVia/
Source0:        http://www.cpan.org/authors/id/M/MA/MATTP/MooX-HandlesVia-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Class::Method::Modifiers)
BuildRequires:  perl(Data::Perl) >= 0.002006
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moo) >= 1.003000
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(MooX::Types::MooseLike::Base) >= 0.23
BuildRequires:  perl(Role::Tiny::With)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(strictures) >= 1
BuildRequires:  perl(warnings)

# Redundant to BR: perl(Data::Perl)
BuildRequires:  perl(Data::Perl::Role::Bool)
BuildRequires:  perl(Data::Perl::Role::Code)
BuildRequires:  perl(Data::Perl::Role::Collection::Array)
BuildRequires:  perl(Data::Perl::Role::Collection::Hash)
BuildRequires:  perl(Data::Perl::Role::Counter)
BuildRequires:  perl(Data::Perl::Role::Number)
BuildRequires:  perl(Data::Perl::Role::String)

Requires:       perl(Data::Perl) >= 0.002006
Requires:       perl(Moo) >= 1.003000
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
MooX::HandlesVia is an extension of Moo's 'handles' attribute
functionality. It provides a means of proxying functionality from an
external class to the given atttribute. This is most commonly used as a way
to emulate 'Native Trait' behavior that has become commonplace in Moose
code, for which there was no Moo alternative.

%prep
%setup -q -n MooX-HandlesVia-%{version}

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
%doc Changes LICENSE TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.001008-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.001008-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.001008-2
- Perl 5.22 rebuild

* Sat Apr 04 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001008-1
- Upstream update.

* Tue Feb 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001007-1
- Upstream update.

* Mon Jan 26 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.001006-1
- Upstream update.

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.001005-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.001005-2
- Reflect review.
- Do not package dist.ini, README.mkdn, META.json.

* Fri Mar 21 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.001005-1
- Initial Fedora package.
