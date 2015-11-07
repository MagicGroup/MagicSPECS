Name:           perl-MooseX-MethodAttributes
Summary:        Introspect your method code attributes
Version:	0.31
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-MethodAttributes-%{version}.tar.gz
URL:            http://search.cpan.org/dist/MooseX-MethodAttributes
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
BuildRequires:  perl(Moose) >= 0.98
BuildRequires:  perl(MooseX::Role::Parameterized)
BuildRequires:  perl(MooseX::Types::Moose) >= 0.21
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(namespace::clean) >= 0.10
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.26-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module allows code attributes of methods to be introspected using
Moose meta method objects.


%prep
%setup -q -n MooseX-MethodAttributes-%{version}

# we don't have Test::CheckDeps
rm -f t/00-check-deps.t

# silence rpmlint warning
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.31-2
- 更新到 0.31

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.30-1
- 更新到 0.30

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.28-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.28-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 0.28-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.27-2
- Perl 5.16 rebuild
- Specify all dependencies

* Mon Feb 20 2012 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.26-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.26-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.25-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- remove explicit requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Aug 28 2010 Iain Arnell <iarnell@gmail.com> 0.24-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.24)
- altered br on perl(ExtUtils::MakeMaker) (6.11 => 6.31)
- altered br on perl(Moose) (0.97 => 0.98)
- added a new br on perl(MooseX::Types::Moose) (version 0.21)
- dropped old BR on perl(MooseX::Types)
- altered req on perl(Moose) (0.97 => 0.98)
- added a new req on perl(MooseX::Types::Moose) (version 0.21)
- dropped old requires on perl(MooseX::Types)
- dropped old requires on perl(namespace::autoclean)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- update by Fedora::App::MaintainerTools 0.004
- updating to latest GA CPAN version (0.20)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.11)
- altered br on perl(Moose) (0.90 => 0.97)
- dropped old BR on perl(MRO::Compat)
- altered req on perl(Moose) (0.90 => 0.97)
- dropped old requires on perl(MRO::Compat)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- add perl_default_filter
- PERL_INSTALL_ROOT => DESTDIR in install
- auto-update to 0.19 (by cpan-spec-update 0.01)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.18-2
- rebuild against perl 5.10.1

* Sat Sep 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- auto-update to 0.18 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.79 => 0.90)
- altered br on perl(MooseX::Types) (0.06 => 0.20)
- altered br on perl(Test::More) (0 => 0.88)
- added a new br on perl(namespace::autoclean) (version 0)
- altered br on perl(namespace::clean) (0 => 0.10)
- altered req on perl(Moose) (0.79 => 0.90)
- altered req on perl(MooseX::Types) (0.06 => 0.20)
- added a new req on perl(namespace::autoclean) (version 0)
- altered req on perl(namespace::clean) (0 => 0.10)

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- auto-update to 0.16 (by cpan-spec-update 0.01)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- auto-update to 0.15 (by cpan-spec-update 0.01)
- added a new br on perl(MRO::Compat) (version 0)
- added a new req on perl(MRO::Compat) (version 0)
- added a new req on perl(Moose) (version 0.79)
- added a new req on perl(MooseX::Types) (version 0.06)
- added a new req on perl(namespace::clean) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- auto-update to 0.14 (by cpan-spec-update 0.01)

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)

* Wed May 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- add br on Test::Exception (missing as a test/br:
  https://rt.cpan.org/Ticket/Display.html?id=46396)
- auto-update to 0.12 (by cpan-spec-update 0.01)

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.70 => 0.79)

* Mon Apr 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-2
- must remember to check summary! *sigh*

* Mon Apr 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- submission

* Mon Apr 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
