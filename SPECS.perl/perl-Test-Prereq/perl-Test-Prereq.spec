Name:           perl-Test-Prereq
Version:	1.039
Release:	3%{?dist}
Summary:        Check if Makefile.PL has the right pre-requisites
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Prereq/
Source0:        http://www.cpan.org/authors/id/B/BD/BDFOY/Test-Prereq-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Info)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The prereq_ok() function examines the modules it finds in blib/lib/,
blib/script, and the test files it finds in t/ (and test.pl). It figures
out which modules they use, skips the modules that are in the Perl core,
and compares the remaining list of modules to those in the PREREQ_PM
section of Makefile.PL.

%prep
%setup -q -n Test-Prereq-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# t/get_from_prereqs.t requires interactive CPAN module configuration and
# network access.
rm t/get_from_prereqs.t


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.039-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.039-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.039-1
- 更新到 1.039

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.037-19
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.037-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.037-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.037-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.037-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.037-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.037-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.037-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.037-11
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.037-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.037-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.037-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.037-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.037-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.037-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.037-4
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Petr Pisar <ppisar@redhat.com> - 1.037-3
- Disable t/get_from_prereqs.t test because it requires interactive
  configuration <https://rt.cpan.org/Public/Bug/Display.html?id=56785> and
  network access (#539015)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.037-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 1.037-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.036-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Steven Pritchard <steve@kspei.com> 1.036-1
- Update to 1.036.
- Add some dependencies when building with --with-check.

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 1.034-1
- Update to 1.034.

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.033-2
- rebuild for new perl

* Fri Mar 23 2007 Steven Pritchard <steve@kspei.com> 1.033-1
- Update to 1.033.

* Wed Jan 17 2007 Steven Pritchard <steve@kspei.com> 1.032-1
- Update to 1.032.
- Use fixperms macro instead of our own chmod incantation.
- Add LICENSE to docs.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.031-2
- Fix find option order.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.031-1
- Update to 1.031.

* Fri Mar 24 2006 Steven Pritchard <steve@kspei.com> 1.030-1
- Specfile autogenerated by cpanspec 1.64.
- Fix License.
- Drop explicit Requires.
- Disable tests by default (uses network).
