Name:           perl-Cache
Version:        2.04
Release:        23%{?dist}
Summary:        The Cache interface

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Cache
Source0:        http://search.cpan.org/CPAN/authors/id/C/CL/CLEISHMAN/Cache-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires:  perl(IO::String) perl(File::NFSLock)
BuildRequires:  perl(Date::Parse) perl(Heap::Fibonacci) perl(Digest::SHA1)
BuildRequires:  perl(Time::HiRes)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The Cache modules are designed to assist a developer in persisting data 
for a specified period of time. Often these modules are used in web 
applications to store data locally to save repeated and redundant 
expensive calls to remote machines or databases.

The Cache interface is implemented by derived classes that store cached 
data in different manners (such as as files on a filesystem, or in memory).


%package -n perl-Cache-Tester
Summary:        Test utility for perl Cache implementations
Requires:       %{name} = %{version}-%{release}

%description -n perl-Cache-Tester
This module is used to run tests against an instance of a Cache implementation
to ensure that it operates as required by the Cache specification.


%prep
%setup -q -n Cache-%{version}

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
%doc Changes design.dia LICENSE README
%exclude %{perl_vendorlib}/Cache/Tester.pm
%exclude %{_mandir}/man3/Cache::Tester.3*
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%files -n perl-Cache-Tester
%defattr(-,root,root)
%{perl_vendorlib}/Cache/Tester.pm
%{_mandir}/man3/Cache::Tester.3*


%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.04-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.04-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.04-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.04-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.04-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.04-18
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.04-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.04-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.04-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.04-14
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 2.04-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.04-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.04-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Iain Arnell <iarnell@gmail.com> 2.04-8
- split Cache::Tester into separate sub-package to avoid runtime dependency on
  Test::More
- use perl_default_filter
- clean up spec for modern rpmbuild

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.04-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.04-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.04-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.04-2.3
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.04-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Sep 20 2006 Patrice Dumas <pertusus@free.fr> 2.04-2
- add missing BuildRequires

* Tue Jul 18 2006 Patrice Dumas <pertusus@free.fr> 2.04-1
- Initial packaging
