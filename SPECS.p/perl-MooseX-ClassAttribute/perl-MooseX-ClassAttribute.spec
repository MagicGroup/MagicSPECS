Name:           perl-MooseX-ClassAttribute
Summary:        Declare class attributes Moose-style
Version:        0.26
Release:        7%{?dist}
License:        Artistic 2.0
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/MooseX-ClassAttribute-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/MooseX-ClassAttribute/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Moose) >= 1.23
BuildRequires:  perl(MooseX::AttributeHelpers)
BuildRequires:  perl(MooseX::Role::Parameterized)
BuildRequires:  perl(namespace::autoclean) >= 0.11
BuildRequires:  perl(namespace::clean) >= 0.20
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires) >= 0.05

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.26-4
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module allows you to declare class attributes in exactly the same way as
object attributes, using class_has() instead of has().

You can use any feature of Moose's attribute declarations, including overriding
a parent's attributes, delegation (handles), and attribute metaclasses, and it
should just work. The one exception is the "required" flag, which is not
allowed for class attributes.

The accessor methods for class attribute may be called on the class directly,
or on objects of that class. Passing a class attribute to the constructor will
not set it.

%prep
%setup -q -n MooseX-ClassAttribute-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check
make test


%files
%doc README Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.26-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.26-5
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.26-4
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.26-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.24-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream
- new BR perl(Test::Fatal)
- new BR perl(Test::Requires) >= 0.05
- new BR perl(MooseX::AttributeHelpers)
- new BR perl(MooseX::Role::Parameterized)
- updated R/BR perl(Moose) >= 1.15

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to 0.16
- license change from "GPL+ or Artistic" to "Artistic 2.0"

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- Mass rebuild with perl-5.12.0

* Fri Apr 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.13)
- altered br on perl(Module::Build) (0.340201 => 0.36)
- altered br on perl(Moose) (0.89 => 0.98)
- altered br on perl(Test::More) (0 => 0.88)
- added a new br on perl(namespace::autoclean) (version 0)
- dropped old BR on perl(MooseX::AttributeHelpers)
- added a new req on perl(Moose) (version 0.98)
- added a new req on perl(namespace::autoclean) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.10-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- add perl_default_filter
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered br on perl(Module::Build) (0 => 0.340201)
- altered br on perl(Moose) (0.74 => 0.89)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- auto-update to 0.08 (by cpan-spec-update 0.01)
- added a new br on perl(Scalar::Util) (version 0)
- altered br on perl(Moose) (0 => 0.74)
- altered br on perl(MooseX::AttributeHelpers) (0 => 0.13)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Allisson Azevedo <allisson@gmail.com> 0.07-1
- Initial RPM release
