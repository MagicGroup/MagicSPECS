Name:           perl-Test-Class
Version:        0.38
Release:        7%{?dist}
Summary:        Easily create test classes in an xUnit/JUnit style
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Class/
Source0:        http://www.cpan.org/authors/id/A/AD/ADIE/Test-Class-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Module::Build)
# Run-time:
BuildRequires:  perl(Attribute::Handlers) >= 0.77
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(MRO::Compat) >= 0.11
BuildRequires:  perl(Storable) >= 2.04
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder) >= 0.78
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(IO::File) >= 1.09
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::Exception) >= 0.25
BuildRequires:  perl(Test::More) >= 0.78
# Optional tests:
BuildRequires:  perl(Contextual::Return)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Attribute::Handlers) >= 0.77
Requires:       perl(MRO::Compat) >= 0.11
Requires:       perl(Storable) >= 2.04
Requires:       perl(Test::Builder) >= 0.78

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Attribute::Handlers|MRO::Compat|Storable|Test::Builder)\\)$

%description
Test::Class provides a simple way of creating classes and objects to test
your code in an xUnit style.

%prep
%setup -q -n Test-Class-%{version}

# Fix up broken permissions
find -type f -exec chmod -x {} \;

# There's a non-ISO char, iconv isn't able to convert
%{__perl} -pi -e 's/Mart.*n/Martín/' < Changes > Changes~
mv Changes~ Changes

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.38-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.38-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.38-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.38-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.38-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.38-2
- 为 Magic 3.0 重建

* Wed Feb 20 2013 Petr Pisar <ppisar@redhat.com> - 0.38-1
- 0.38 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.36-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.36-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.36-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 10 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.36-1
- Update to 0.36 (Fix FTBFS: BZ 661059).
- Update Source0-URL.
- Cleanup BuildRequires/Requires, spec-file overhaul.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.33-2
- rebuild against perl 5.10.1

* Mon Sep 21 2009 Steven Pritchard <steve@kspei.com> 0.33-1
- Update to 0.33.
- Update Source0 URL.
- Add LICENSE.
- BR Test::Pod, Test::CPAN::Meta, and Test::MinimumVersion and define
  AUTOMATED_TESTING for better test coverage.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.
- BR Test::Builder.
- Add versioned dependencies to Test::Builder::Tester and Test::More.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 0.30-1
- Update to 0.30.

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.28-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28.
- Update License tag.
- Bump Test::Exception requirement to 0.25.

* Mon Jul 16 2007 Steven Pritchard <steve@kspei.com> 0.24-1
- Specfile autogenerated by cpanspec 1.71.
- BR Contextual::Return, Test::Builder::Tester, and Test::More.
- Drop explicit perl BR.
