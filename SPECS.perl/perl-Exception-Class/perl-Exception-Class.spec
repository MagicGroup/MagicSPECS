Name:           perl-Exception-Class
Version:	1.39
Release:	1%{?dist}
Summary:        Module that allows you to declare real exception classes in Perl
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Exception-Class/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/Exception-Class-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Class::Data::Inheritable) >= 0.02
BuildRequires:  perl(Devel::StackTrace) >= 1.20
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.46
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Exception::Class allows you to declare exception hierarchies in your
modules in a "Java-esque" manner.

%prep
%setup -q -n Exception-Class-%{version}

chmod a-x lib/Exception/Class.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
export IS_MAINTAINER=1


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.39-1
- 更新到 1.39

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.32-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.32-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.32-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.32-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.32-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Steven Pritchard <steve@kspei.com> 1.32-1
- Update to 1.32.
- License is now Artistic 2.0.
- Switch back to building with ExtUtils::MakeMaker/Makefile.PL.  (Dave
  Rolsky needs to make up his mind.)
- Add README to docs.

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.29-2
- rebuild against perl 5.10.1

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.29-1
- Upstream update (Required by other packages, fix mass rebuild breakdowns).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Steven Pritchard <steve@kspei.com> 1.26-1
- Update to 1.26.
- Bump Devel::StackTrace dependency to 1.20.

* Thu May 31 2008 Steven Pritchard <steve@kspei.com> 1.24-1
- Update to 1.24.
- Bump Devel::StackTrace dependency to 1.17.
- Clean up to match current cpanspec output.
- Improve Summary and description.
- Build with Module::Build.
- BR Test::Pod and Test::Pod::Coverage and define IS_MAINTAINER.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23-6
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.23-5
- rebuild against new perl

* Sat Dec 29 2007 Ralf Corsépius 1.23-4
- BR: perl(Test::More) (BZ 419631).
- Adjust License-tag.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.23-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.23-2
- Canonicalize Source0 URL.
- Fix find option order.
- Drop executable bit from Exception/Class.pm to avoid a rpmlint warning.

* Fri Feb 03 2006 Steven Pritchard <steve@kspei.com> 1.23-1
- Update to 1.23

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 1.22-1
- Update to 1.22

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 1.21-3
- Remove explicit core module dependencies
- Add COPYING and Artistic

* Wed Aug 17 2005 Steven Pritchard <steve@kspei.com> 1.21-2
- Minor spec cleanup

* Tue Aug 16 2005 Steven Pritchard <steve@kspei.com> 1.21-1
- Specfile autogenerated.
