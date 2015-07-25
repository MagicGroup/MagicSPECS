Name:           perl-Class-Trigger
Version:        0.14
Release:        10%{?dist}
Summary:        Mixin to add / call inheritable triggers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-Trigger/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/Class-Trigger-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(IO::Scalar), perl(Test::More), perl(IO::WrapTie)
Requires:  perl(IO::Scalar)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n Class-Trigger-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Class
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.14-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-1
- update

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1
- update to 0.13

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-3
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-2
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-1
- bump to 0.12
- license fix

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-2
- bump for fc6

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.10-1
- bump to 0.10

* Wed Aug 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-3
- fix missing BR: perl(Class::Data::Inheritable)
- use %{_smp_mflags}

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.09-1
- Initial package for Fedora Extras
