Name:           perl-Geo-METAR
Version:        1.15
Release:        12%{?dist}
Summary:        Perl module for accessing aviation weather information

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/Geo-METAR/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KO/KOOS/Geo-METAR-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Geo::METAR is Perl module for accessing aviation weather information. 
Referring to things like a cloud altitudes, temperature, wind, dew point,
and so on.)


%prep
%setup -q -n Geo-METAR-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'



%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README TODO examples
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.15-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.15-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.15-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.15-2
- Fix %%doc

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.15-1
- Update to 1.15

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-3
Rebuild for new perl

* Thu Jun  6 2007 kwizart < kwizart at gmail.com > - 1.14-2
- Add BR perl(ExtUtils::MakeMaker)

* Wed Jun  5 2007 kwizart < kwizart at gmail.com > - 1.14-1
- Initial Fedora package
