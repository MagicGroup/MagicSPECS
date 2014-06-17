Name:           perl-DateTime-Precise
Version:        1.05
Release:        19%{?dist}

Summary:        Perform common time and date operations with additional GPS operations

Group:          Development/Libraries
License:        Public Domain
URL:            http://search.cpan.org/dist/DateTime-Precise
Source0:        http://search.cpan.org/CPAN/authors/id/B/BZ/BZAJAC/DateTime-Precise-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?filter_setup:
%filter_from_provides /perl(bigfloat)/d
%filter_from_provides /perl(bigint)/d
%filter_from_requires /perl(DateTime::Math\/bigfloat.pl)/d
%filter_from_requires /perl(DateTime::Math\/bigint.pl)/d
%?perl_default_filter
}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(big(float|int)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(DateTime::Math/big(float|int)\\.pl\\)

%description
The purpose of this library was to replace our dependence on Unix epoch time,
which, being limited to a range of about 1970 to 2030, is inadequate for our
purposes (we have data as old as 1870). This date library effectively handles
dates from A.D. 1000 to infinity, and would probably work all the way back to 0
(ignoring, of course, the switch-over to the Gregorian calendar). The useful
features of Unix epoch time (ease of date difference calculation and date
comparison, strict ordering) are preserved, and elements such as
human-legibility are added. The library handles fractional seconds and some
date/time manipulations used for the Global Positioning Satellite system.


%prep
%setup -q -n DateTime-Precise-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/DateTime::Precise.3pm.gz


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.05-19
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.05-18
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.05-17
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.05-16
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 1.05-14
- update filtering for rpm 4.9

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-13
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-12
- Perl 5.14 mass rebuild

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 1.05-11
- update requires/provides filtering to use standard macros

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.05-4
- rebuild for new perl

* Wed Jan 30 2008 Xavier Bachelot <xavier@bachelot.org> - 1.05-3
- Fix License: tag.
- Remove '| :' for %%check section.

* Fri Dec 21 2007 Xavier Bachelot <xavier@bachelot.org> - 1.05-2
- Clean up spec.

* Thu Jul 27 2006 Xavier Bachelot <xavier@bachelot.org> - 1.05-1
- Initial build.
