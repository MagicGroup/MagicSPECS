Name:           perl-Data-Perl
Version:	0.002009
Release:	1%{?dist}
Summary:        Base classes wrapping fundamental Perl data types
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Perl/
Source0:        http://www.cpan.org/authors/id/M/MA/MATTP/Data-Perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(constant)
BuildRequires:  perl(Class::Method::Modifiers)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(parent)
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Role::Tiny::With)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strictures)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Output)

# rpm's automatick deptracking misses to add this:
Requires:       perl(Exporter)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Data::Perl is a collection of classes that wrap fundamental data types
that exist in Perl. These classes and methods as they exist today are an
attempt to mirror functionality provided by Moose's Native Traits. One
important thing to note is all classes currently do no validation on
constructor input.

%prep
%setup -q -n Data-Perl-%{version}

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
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.002009-1
- 更新到 0.002009

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.002007-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.002007-2
- Reflect initial review.

* Fri Mar 21 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.002007-1
- Initial Fedora package.
