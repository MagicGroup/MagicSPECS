Name:           perl-Locale-SubCountry
Version:        1.47
Release:        3%{?dist}
Summary:        ISO 3166-2 two letter subcountry codes
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Locale-SubCountry
Source0:        http://search.cpan.org/CPAN/authors/id/K/KI/KIMRYAN/Locale-SubCountry-%{version}.tar.gz
BuildArch:      noarch 
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Exporter)
BuildRequires:  perl(locale)
# Tests
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple)
# Optional test
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module allows you to convert the full name for a countries administrative
region to the code commonly used for postal addressing. The reverse look-up
can also be done. Sub country codes are defined in "ISO 3166-2:1998, Codes for
the representation of names of countries and their subdivisions".

Sub countries are termed as states in the US and Australia, provinces in
Canada and counties in the UK and Ireland.

%prep
%setup -q -n Locale-SubCountry-%{version}
find examples -type f -exec chmod -c -x {} +
for i in Changes lib/Locale/SubCountry.pm; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > new
    mv new $i
done
sed -i -e $'1 i =encoding utf8\\\n' lib/Locale/SubCountry.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.47-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.47-2
- 为 Magic 3.0 重建

* Thu Jan 26 2012 Petr Pisar <ppisar@redhat.com> - 1.47-1
- 1.47 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.41-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.41-7
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.41-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.41-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.41-1
- update to 1.41
- chmod -x everything

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.38-2
- rebuild for new perl

* Tue Dec 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.38-1
- update to 1.38
- minor specfile tweaks

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.37-2
- bump for mass rebuild

* Wed Jul  5 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.37-1
- bump release for f-e build

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.37-0.1
- add additional buildreq's

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.37-0
- Initial spec file for F-E
