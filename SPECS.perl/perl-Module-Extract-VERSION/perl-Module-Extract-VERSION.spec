Name:		perl-Module-Extract-VERSION
Version:	1.01
Release:	15%{?dist}
Summary:	Extract a module version without running code
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Module-Extract-VERSION/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Module-Extract-VERSION-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.00
%if "%{?rhel}" != "4"
BuildRequires:	perl(Test::Prereq)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Filter bogus provide for perl(ExtUtils::MakeMaker::_version) (rpm 4.9 onwards)
%global __provides_exclude ^perl\\(ExtUtils::MakeMaker::_version\\)

%description
This module lets you pull out of module source code the version number for the
module. It assumes that there is only one $VERSION in the file.

%prep
%setup -q -n Module-Extract-VERSION-%{version}

# Filter bogus provide for perl(ExtUtils::MakeMaker::_version) (prior to rpm 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Fvx 'perl(ExtUtils::MakeMaker::_version)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Extract::VERSION.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.01-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.01-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.01-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.01-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.01-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.01-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.01-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.01-5
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.01-4
- BR: perl(Carp)

* Fri Aug 12 2011 Paul Howarth <paul@city-fan.org> - 1.01-3
- Filter bogus provide for perl(ExtUtils::MakeMaker::_version) (#728286)

* Thu Aug  4 2011 Paul Howarth <paul@city-fan.org> - 1.01-2
- Sanitize for Fedora submission

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.01-1
- Initial RPM version
