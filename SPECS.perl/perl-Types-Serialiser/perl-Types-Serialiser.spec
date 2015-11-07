Name:		perl-Types-Serialiser
Summary:	Simple data types for common serialization formats
Version:	1.0
Release:	5%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Types-Serialiser/
Source0:	http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/Types-Serialiser-%{version}.tar.gz 
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(common::sense)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(overload)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

# Filter bogus provide of JSON::PP::Boolean (for rpm ≥ 4.9)
%global __provides_exclude ^perl\\(JSON::PP::Boolean\\)

%description
This module provides some extra data types that are used by common
serialization formats such as JSON or CBOR. The idea is to have a repository of
simple/small constants and containers that can be shared by different
implementations so they become interoperable between each other.

%prep
%setup -q -n Types-Serialiser-%{version}

# Filter bogus provide of JSON::PP::Boolean (for rpm < 4.9)
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(JSON::PP::Boolean)'"
%define __perl_provides %{provfilt}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%doc Changes COPYING README
%{perl_vendorlib}/Types/
%{_mandir}/man3/Types::Serialiser.3pm*
%{_mandir}/man3/Types::Serialiser::Error.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec  2 2013 Paul Howarth <paul@city-fan.org> - 1.0-1
- Update to 1.0
  - Clarify that the second arg of FREEZE/THAW is the data model/data format
    name, not the serializer
  - Clarify that FREEZE must not modify the data structure to be serialized

* Wed Oct 30 2013 Paul Howarth <paul@city-fan.org> - 0.03-2
- Sanitize for Fedora submission

* Tue Oct 29 2013 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
