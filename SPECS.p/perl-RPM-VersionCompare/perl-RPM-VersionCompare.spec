Name:           perl-RPM-VersionCompare
Version:        0.1.1
Release:        9%{?dist}
Summary:        Compare RPM version strings
License:        GPLv3+
Group:          Development/Libraries
URL:            http://ppisar.fedorapeople.org/RPM-VersionCompare/
Source0:        http://ppisar.fedorapeople.org/RPM-VersionCompare/RPM-VersionCompare-v%{version}.tar.gz
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(version) >= 0.77
BuildRequires:  pkgconfig
BuildRequires:  rpm-devel
# Tests only:
BuildRequires:  perl(Test::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This module provides functions to compare RPM version strings. No function
is exported by default. If possible, calls are passed to native librpm
library. Otherwise Python extension provided with RPM sources is re-
-implemented.

%prep
%setup -q -n RPM-VersionCompare-v%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes COPYING
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/RPM*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.1.1-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.1.1-4
- Perl 5.16 rebuild

* Mon Mar 26 2012 Petr Pisar <ppisar@redhat.com> - 0.1.1-3
- Rebuild against RPM 4.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Petr Pisar <ppisar@redhat.com> - 0.1.1-1
- 0.1.1 bump
- Fixes parsing epoch longer than one character (bug #725608)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1.0-2
- Perl mass rebuild

* Fri May 27 2011 Petr Pisar <ppisar@redhat.com> 0.1.0-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr
