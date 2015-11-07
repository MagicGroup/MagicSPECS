%define cpan_name Geo-IPfree
%define cpan_version 1.112870
Name:           perl-%{cpan_name}
Version:	1.151940
Release:	2%{?dist}
Summary:        Look up the country of an IPv4 Address
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/%{cpan_name}/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BR/BRICAS/Geo-IPfree-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Memoize)
# Tests only:
BuildRequires:  perl(Test::More) >= 0.47
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This package comes with it's own database to look up the IPv4's country, and
is totally free.

%prep
%setup -q -n %{cpan_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes misc README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.151940-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.151940-1
- 更新到 1.151940

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.1.1.2.8.7.0-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.1.1.2.8.7.0-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.1.1.2.8.7.0-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1.2.8.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Petr Pisar <ppisar@redhat.com> - 1.1.1.2.8.7.0-1
- 1.112870 bump
- Remove BuildRoot and defattr from spec code

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.0.2.8.7.0-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0.2.8.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Petr Pisar <ppisar@redhat.com> - 1.1.0.2.8.7.0-2
- Add BuildRequires needed for tests

* Mon Nov 08 2010 Petr Pisar <ppisar@redhat.com> - 1.1.0.2.8.7.0-1
- 1.102870 bump

* Wed Aug 11 2010 Petr Pisar <ppisar@redhat.com> - 1.1.0.1.6.5.0-1
- 1.101650 bump
- Experimental RPM-extensible version numbering

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.4-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.4-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Allisson Azevedo <allisson@gmail.com> 0.4-1
- Initial rpm release.
