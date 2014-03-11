Name:           perl-Contextual-Return
Version:        0.003002
Release:        4%{?dist}
Summary:        Create context-sensitive return values
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Contextual-Return
Source0:        http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/Contextual-Return-%{version}.tar.gz
BuildArch:      noarch 
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More), perl(Want), perl(version)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This module allows you to define return values of a perl sub that are
appropriate given the calling context.


%prep
%setup -q -n Contextual-Return-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}


%check



%files
%doc Changes README
%{perl_vendorlib}/Contextual/
%{_mandir}/man3/Contextual::Return.3pm*
%{_mandir}/man3/Contextual::Return::Failure.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.003002-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.003002-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.003002-2
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Iain Arnell <iarnell@gmail.com> 0.003002-1
- update to latest upstream version

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> 0.003001-1
- update to latest upstream version
- drop explicit provides filtering; perl_default_filter already includes DB

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 0.2.1-11
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.2.1-10
- Perl mass rebuild

* Tue Apr 19 2011 Paul Howarth <paul@city-fan.org> - 0.2.1-9
- Filter provides in a way that works with rpm >= 4.9
- Fix typo in %%summary
- Fix argument order for find with -depth
- Run the whole test suite
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop buildroot specification and cleaning, no longer needed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2.1-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.2.1-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.2.1-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.2.1-2
- rebuild for new perl

* Fri Mar 30 2007 Chris Weyl <cweyl@alumni.drew.edu> v0.2.1-1
- update to v0.2.1

* Sat Mar 10 2007 Chris Weyl <cweyl@alumni.drew.edu> v0.2.0-1
- update to v0.2.0
- misc spec cleanups
- add br on perl(ExtUtils::MakeMaker) to satisfy any perl/perl-devel split

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-2
- bump for mass rebuild

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-1
- bump rel for f-e release

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-0.1
- filter unwanted provides
- add additional BR, the better to test with

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.1.0-0
- Initial spec file for F-E
