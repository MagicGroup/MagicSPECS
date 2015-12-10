Name:           perl-Test-Deep
Version:	0.119
Release:	3%{?dist}
Summary:        Extremely flexible deep comparison
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Deep/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Test-Deep-%{version}.tar.gz
Patch0:         perl-Test-Deep-0.103-arrayeach.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util) >= 1.09
# Tests
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings) >= 0.02
BuildRequires:  perl(Test::Tester) >= 0.04
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::Deep gives you very flexible ways to check that the result you
got is the result you were expecting. At it's simplest it compares two
structures by going through each level, ensuring that the values
match, that arrays and hashes have the same elements and that
references are blessed into the correct class. It also handles
circular data structures without getting caught in an infinite loop.

%prep
%setup -q -n Test-Deep-%{version}
%patch0 -p1 -b .arrayeach

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


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.119-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.119-2
- 更新到 0.119

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.117-1
- 更新到 0.117

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.108-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.108-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.108-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.108-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.108-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.108-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.108-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.108-6
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.108-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.108-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Dec 18 2010 Steven Pritchard <steve@kspei.com> 0.108-1
- Update to 0.108.
- Update Source0 URL.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.106-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.106-2
- rebuild against perl 5.10.1

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 0.106-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Lubomir Rintel <lubo.rintel@gooddata.com> 0.103-2
- Fix crash on matching array_each() against non-array

* Wed Jun 04 2008 Steven Pritchard <steve@kspei.com> 0.103-1
- Update to 0.103.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 0.102-1
- Update to 0.102.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.101-1
- Update to 0.101.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.100-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.100-1
- Update to 0.100.

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.099-1
- Update to 0.099.
- Update License tag.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.098-1
- Update to 0.098.

* Fri Aug 10 2007 Steven Pritchard <steve@kspei.com> 0.097-1
- Update to 0.097.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.096-2
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 0.096-1
- Update to 0.096.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.095-2
- Fix find option order.

* Fri Apr 21 2006 Steven Pritchard <steve@kspei.com> 0.095-1
- Update to 0.095.

* Sat Apr 08 2006 Steven Pritchard <steve@kspei.com> 0.093-1
- Specfile autogenerated by cpanspec 1.64.
- Improve description.
- Fix License.
- Remove explicit dependency on Test::Tester and Test::NoWarnings.
