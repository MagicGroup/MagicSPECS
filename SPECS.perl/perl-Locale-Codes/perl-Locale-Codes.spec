Name:           perl-Locale-Codes
Version:	3.36
Release:	2%{?dist}
Summary:        Distribution of modules to handle locale codes
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Locale-Codes/
Source0:        http://www.cpan.org/authors/id/S/SB/SBECK/Locale-Codes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(utf8)
# Tests
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Inject not detected module version
Provides:       perl(Locale::Codes) = %{version}

# Filter under-specified privdes
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Locale::Codes\\)$

# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)

%description
Locale-Codes is a distribution containing a set of modules. The modules
each deal with different types of codes which identify parts of the locale
including languages, countries, currency, etc.

%prep
%setup -q -n Locale-Codes-%{version}
chmod -x examples/*

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
%doc examples Changes LICENSE README README.first
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.36-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.36-1
- 更新到 3.36

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.31-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.31-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 3.31-1
- 3.31 bump

* Wed Mar 05 2014 Petr Pisar <ppisar@redhat.com> - 3.30-1
- 3.30 bump

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 3.29-1
- 3.29 bump

* Wed Dec 04 2013 Petr Pisar <ppisar@redhat.com> - 3.28-2
- Filter private module Locale::Codes::LangFam_Retired from dependencies

* Tue Dec 03 2013 Petr Pisar <ppisar@redhat.com> - 3.28-1
- 3.28 bump

* Thu Sep 12 2013 Petr Pisar <ppisar@redhat.com> - 3.27-2
- Filter dependencies on private modules

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 3.27-1
- 3.27 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.26-2
- Perl 5.18 rebuild

* Fri Jun 07 2013 Petr Pisar <ppisar@redhat.com> - 3.26-1
- 3.26 bump

* Fri Mar 01 2013 Petr Pisar <ppisar@redhat.com> - 3.25-1
- 3.25 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Petr Pisar <ppisar@redhat.com> - 3.24-1
- 3.24 bump

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 3.23-2
- Add missing deps
- Drop command macros
- Modernize spec

* Tue Sep 04 2012 Petr Pisar <ppisar@redhat.com> - 3.23-1
- 3.23 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.22-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 3.22-1
- 3.22 bump

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 3.21-2
- The POD tests do not run by default anymore
- Switch build script from Module::Build to EU::MM

* Fri Mar 02 2012 Petr Pisar <ppisar@redhat.com> - 3.21-1
- 3.21 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 3.20-1
- 3.20 bump

* Thu Sep 01 2011 Petr Pisar <ppisar@redhat.com> - 3.18-1
- 3.18 bump

* Thu Jun 30 2011 Petr Pisar <ppisar@redhat.com> 3.17-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr
