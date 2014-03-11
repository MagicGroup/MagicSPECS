Name:           perl-Class-DBI-Loader
Version:        0.34
Release:        15%{?dist}
Summary:        Dynamic definition of Class::DBI sub classes
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-DBI-Loader
Source0:        http://search.cpan.org/CPAN/authors/id/D/DM/DMAKI/Class-DBI-Loader-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:	perl(Lingua::EN::Inflect), perl(Test::Pod::Coverage), perl(Test::Pod)
BuildRequires:  perl(Class::DBI::mysql), perl(Class::DBI::Pg), perl(Class::DBI::SQLite)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Pod::Perldoc)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n Class-DBI-Loader-%{version}
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
# Coverage test fails
mv t/03podcoverage.t .
TEST_POD=1 

%files
%doc Artistic COPYING Changes
%{perl_vendorlib}/Class/DBI
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.34-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.34-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.34-13
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Tom Callaway <spot@fedoraproject.org> - 0.34-12
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.34-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.34-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.34-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.34-2
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.34-1
- license fix
- bump to 0.34

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.33-1
- bump for 0.33

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.32-1
- bump for 0.32

* Fri Sep  9 2005 Paul Howarth <paul@city-fan.org> 0.22-4
- include POD tests in %%check, but disable failing POD coverage test
- remove explicit Class::DBI dep because it's pulled in by other deps
  that are autodetected

* Wed Sep  7 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-3
- remove redundant BR: perl
- honor %%{_smp_mflags}
- include license text

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.22-1
- Initial package for Fedora Extras
