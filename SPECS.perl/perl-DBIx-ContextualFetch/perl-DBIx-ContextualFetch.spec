Name:           perl-DBIx-ContextualFetch
Version:        1.03
Release:        22%{?dist}
Summary:        Add contextual fetches to DBI
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBIx-ContextualFetch
Source0:        http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/DBIx-ContextualFetch-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(DBI)
BuildRequires:  perl(DBD::SQLite), perl(Test::Pod::Coverage), perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(DBI)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DBI::(st|db)\\)

%description
%{summary}.

%prep
%setup -q -n DBIx-ContextualFetch-%{version}

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
%doc Changes
%{perl_vendorlib}/DBIx
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.03-22
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.03-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-20
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.03-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-18
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.03-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Iain Arnell <iarnell@gmail.com> 1.03-14
- update filtering for rpm 4.9

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-13
- Perl mass rebuild

* Tue Feb 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-12
- new filter with RPM4.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.03-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-5
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-4
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-3
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-2
- bump for fc6

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-1
- bump to 1.03

* Wed Aug 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.02-3
- more cleanups

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.02-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.02-1
- Initial package for Fedora Extras
