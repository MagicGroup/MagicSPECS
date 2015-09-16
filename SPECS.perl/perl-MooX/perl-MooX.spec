Name:           perl-MooX
Version:        0.101
Release:        5%{?dist}
Summary:        Using Moo and MooX:: packages the most lazy way
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooX/
Source0:        http://www.cpan.org/authors/id/G/GE/GETTY/MooX-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::OptList) >= 0.107
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Import::Into) >= 1.000003
BuildRequires:  perl(Module::Runtime) >= 0.013
BuildRequires:  perl(Moo) >= 0.091004
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

BuildRequires:  perl(Test::More) >= 0.96
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Using Moo and MooX:: packages the most lazy way

%prep
%setup -q -n MooX-%{version}

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
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.101-5
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.101-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.101-2
- Add BR: perl(lib), perl(FindBin).
- BR: perl(ExtUtils::MakeMaker) >= 6.30.

* Sat Mar 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> 0.101-1
- Initial Fedora package.
