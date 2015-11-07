Name:           perl-UNIVERSAL-can
Version:	1.20140328
Release:	3%{?dist}
Summary:        Hack around people calling UNIVERSAL::can() as a function

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/UNIVERSAL-can/
Source0:        http://www.cpan.org/authors/id/C/CH/CHROMATIC/UNIVERSAL-can-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Simple) >= 0.60
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The UNIVERSAL class provides a few default methods so that all objects
can use them. Object orientation allows programmers to override these
methods in subclasses to provide more specific and appropriate behavior.

Some authors call methods in the UNIVERSAL class on potential invocants
as functions, bypassing any possible overriding. This is wrong and you
should not do it. Unfortunately, not everyone heeds this warning and
their bad code can break your good code.


%prep
%setup -q -n UNIVERSAL-can-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
PERL_RUN_ALL_TESTS=1 make test

%files
%doc Changes README
%{perl_vendorlib}/UNIVERSAL/
%{_mandir}/man3/*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.20140328-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.20140328-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.20140328-1
- 更新到 1.20140328

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.15-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.15-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.15-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.15-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.15-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.15-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.15-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.15-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-6
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.15-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.15-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.15-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-2
- rebuild for new perl

* Wed Apr  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Fri Feb 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.
- No longer build requires perl(Test::Exception).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Missing build requirement: perl(Test::Exception).

* Wed Feb  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Tue Dec 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- First build.
