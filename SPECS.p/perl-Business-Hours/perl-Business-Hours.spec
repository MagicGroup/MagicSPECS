Summary: 	Calculate business hours in a time period
Name: 		perl-Business-Hours
Version: 	0.10
Release: 	8%{?dist}
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Business-Hours/

Source0: http://search.cpan.org/CPAN/authors/id/R/RU/RUZ/Business-Hours-%{version}.tar.gz
BuildArch: 	noarch

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Set::IntSpan)

# Required by the tests
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.00

%description
A simple tool for calculating business hours in a time period. Over time, 
additional functionality will be added to make it easy to calculate the 
number of business hours between arbitrary dates.

%prep
%setup -q -n Business-Hours-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes LICENSE
%{perl_vendorlib}/Business
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.10-1
- Upstream update.
- Reflect Source0:-URL having changed.
- Spec file cleanup.

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.09-1
- Upstream update.
- Reflect Source0-URL having changed.

* Mon Aug 25 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.08-1
- Upstream update.
- Reflect Source0-URL having changed.

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07-6
- rebuild for new perl

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.07-5
- Update license tag.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.07-4
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-2
- Rebuild for perl-5.8.8.

* Tue Oct 10 2005 Ralf Corsepius <rc040203@freenet.de> - 0.07-1
- Upstream update.
- FE submission.

* Tue Mar 22 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-0.pm.2
- Initial packman version.
