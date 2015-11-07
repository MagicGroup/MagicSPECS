Name:           perl-Class-DBI
Version:	3.0.17
Release:	26%{?dist}
Summary:        Simple Database Abstraction
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-DBI/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/Class-DBI-v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Class::Accessor), perl(Class::Data::Inheritable)
BuildRequires:  perl(Class::Trigger), perl(Ima::DBI), perl(UNIVERSAL::moniker)
BuildRequires:  perl-DBD-Pg, perl(DBD::SQLite), perl(Date::Simple)
BuildRequires:  perl(Time::Piece::MySQL), perl(Clone), perl(version), perl(Test::More)
BuildRequires:  perl(Pod::Perldoc)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Class::Accessor), perl(Ima::DBI)

%description
%{summary}.

%prep
%setup -q -n Class-DBI-v%{version}
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
# This test fails because no postgresql and mysql servers are running
# in the build environment.
# 

%files
%doc Changes COPYING Artistic
%{perl_vendorlib}/Class/
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.0.17-26
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 3.0.17-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 3.0.17-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 3.0.17-23
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 3.0.17-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.0.17-21
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.0.17-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0.17-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0.17-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0.17-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.0.17-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 3.0.17-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.0.17-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.0.17-13
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Tom Callaway <spot@fedoraproject.org> - 3.0.17-12
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.0.17-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0.17-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.0.17-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.0.17-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.17-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.17-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.17-1
- bump to 3.0.17

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.16-2
- license fix

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.16-1
- bump to 3.0.16

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.15-1
- bump to 3.0.15

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.14-1
- bump to 3.0.14

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.13-1
- bump to 3.0.13

* Wed Aug 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.96-6
- comment out , since it fails.

* Sun Aug 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.96-4
- BR: perl(Time::Piece::MySQL)
- Requires: perl(Class::Accessor), perl(Ima::DBI)

* Wed Aug 24 2005 Paul Howarth <paul@city-fan.org> 0.96-3
- include license text
- remove redundant BR: perl
- add BR: perl(Date::Simple) for more test coverage

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.96-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.96-1
- Initial package for Fedora Extras
