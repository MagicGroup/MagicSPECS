Name:           perl-Data-Page
Version:        2.02
Release:        8%{?dist}
Summary:        Help when paging through sets of results
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Data-Page/
Source0:        http://search.cpan.org/CPAN/authors/id/L/LB/LBROCARD/Data-Page-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Test::Exception), perl(Class::Accessor::Chained::Fast)
BuildRequires:	perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::More)
BuildRequires:  perl(Pod::Perldoc)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Not picked up automatically
Requires:	perl(Class::Accessor::Chained::Fast)

%description
%{summary}.

%prep
%setup -q -n Data-Page-%{version}
perldoc -t perlgpl > COPYING
perldoc -t perlartistic > Artistic

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
%doc README CHANGES COPYING Artistic
%{perl_vendorlib}/Data
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.02-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.02-7
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.02-6
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.02-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.02-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.02-1
- update to 2.02

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.01-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.01-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.01-1
- update to 2.01

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.00-8
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-7
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-6
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-5
- bump for fc6

* Wed Aug 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-4
- perldoc -t

* Thu Aug 25 2005 Paul Howarth <paul@city-fan.org> 2.00-3
- remove redundant BR: perl
- include license text as %%doc
- include CHANGES as %%doc
- use %%{?_smp_mflags} with make
- add BR: Test::Pod::Coverage and Test::Pod for improved test coverage
- add explicit dep perl(Class::Accessor::Chained::Fast)

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.00-1
- Initial package for Fedora Extras
