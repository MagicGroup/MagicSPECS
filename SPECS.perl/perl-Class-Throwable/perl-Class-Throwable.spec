Name:           perl-Class-Throwable
Version:	0.13
Release:	2%{?dist}
Summary:        A minimal lightweight exception class
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-Throwable/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KM/KMX/Class-Throwable-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)

%global __provides_exclude ^perl\\((DB|TestException)\\)
%global __requires_exclude ^perl\\(base\\)

%description
This module implements a minimal lightweight exception object. It is
meant to be a compromise between more basic solutions like Carp which
can only print information and cannot handle exception objects, and more
complex solutions like Exception::Class which can be used to define
complex inline exceptions and has a number of module dependencies. 

%prep
%setup -q -n Class-Throwable-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make 

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} ';' 2>/dev/null
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::Throwable.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.13-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.13-1
- 更新到 0.13

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10-9
- Perl mass rebuild

* Tue Apr 19 2011 Paul Howarth <paul@city-fan.org> - 0.10-8
- Filter bogus provides of perl(DB) and perl(TestException)
- Filter doc-file-dependency perl(base)
- Fix argument order for find with -depth

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.10-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan  6 2008 Gabriel Somlo <somlo at cmu.edu> 0.10-1
- Initial Fedora package
