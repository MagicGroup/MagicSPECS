Name:           perl-Class-DBI-AsForm
Version:        2.42
Release:        34%{?dist}
Summary:        Produce HTML form elements for database columns
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-DBI-AsForm
Source0:        http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/Class-DBI-AsForm-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:	perl(Class::DBI), perl(HTML::Element), perl(Class::DBI::Plugin::Type)
BuildRequires:  perl(DBD::SQLite), perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::More)
BuildRequires:  perl(Pod::Perldoc)
Requires:  perl(Class::DBI)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Patch0:		perl-Class-DBI-AsForm-fix01test.patch

%description
%{summary}.

%prep
%setup -q -n Class-DBI-AsForm-%{version}
%patch0 -p1
perldoc -t perlartistic > Artistic
perldoc -t perlgpl > COPYING
 
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
%doc Artistic COPYING Changes
%{perl_vendorlib}/Class/DBI
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.42-34
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.42-33
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.42-32
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.42-31
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.42-30
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.42-29
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.42-28
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.42-27
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.42-26
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.42-25
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.42-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.42-23
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.42-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.42-21
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.42-20
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.42-19
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.42-18
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.42-16
- minor spec cleanups and rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.42-15
- Perl mass rebuild

* Fri Jun 24 2011 Petr Pisar <ppisar@redhat.com> - 2.42-14
- Adapt to formating changes in HTML-Tree 4.0 (RT#63623, rhbz#715795)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.42-12
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.42-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.42-10
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.42-7
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-6
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-5
- license fix

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-4
- fix broken test

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-3
- fix missing BR

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-2
- bump for fc-6

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.42-1
- bump to 2.42

* Wed Sep  7 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.41-3
- remove redundant BR: perl
- honor %%{_smp_mflags}
- include license text

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.41-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.41-1
- Initial package for Fedora Extras
