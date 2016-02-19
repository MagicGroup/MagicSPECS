Name:           perl-Test-MockModule
Version:	0.11
Release:	3%{?dist}
Summary:        Override subroutines in a module for unit testing
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-MockModule/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GF/GFRANKS/Test-MockModule-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(CGI)
BuildRequires:  perl(Test::More), perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n Test-MockModule-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes
%license LICENSE
%{perl_vendorlib}/Test
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.11-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.11-2
- 更新到 0.11

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10-1
- 更新到 0.10

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.05-19
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.05-18
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.05-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-14
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.05-12
- Add BR: perl(CGI) (Fix FTBFS: BZ 661082).

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-11
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-7
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-6
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-5
- license tag fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-4
- bump for fc6

* Wed Jul 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-3
- add missing BuildRequires

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-1
- Initial package for Fedora Extras
