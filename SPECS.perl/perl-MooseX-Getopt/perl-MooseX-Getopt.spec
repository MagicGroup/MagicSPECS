Name:           perl-MooseX-Getopt
Summary:        Moose role for processing command line options
Version:	0.68
Release:	3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Getopt-%{version}.tar.gz
URL:            http://search.cpan.org/dist/MooseX-Getopt/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(Getopt::Long) >= 2.37
BuildRequires:  perl(Getopt::Long::Descriptive) >= 0.081
BuildRequires:  perl(Moose) >= 0.56
BuildRequires:  perl(MooseX::Role::Parameterized)
# MooseX::SimpleConfig -> MooseX::ConfigFromFile -> MooseX::Types::Path::Class -> MooseX::Getopt
%if !0%{?perl_bootstrap}
BuildRequires:  perl(MooseX::SimpleConfig) >= 0.07
%endif
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Requires) >= 0.05
BuildRequires:  perl(Test::Trap)
BuildRequires:  perl(Test::Warn) >= 0.21

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.38-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This is a Moose role which provides an alternate constructor for creating
objects using parameters passed in from the command line.

%prep
%setup -q -n MooseX-Getopt-%{version}

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
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.68-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.68-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.68-1
- 更新到 0.68

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.47-11
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.47-10
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.47-9
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.47-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.47-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.47-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.47-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.47-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.47-3
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.47-2
- 为 Magic 3.0 重建

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 0.47-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.45-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.45-2
- Perl 5.16 rebuild

* Fri May 18 2012 Iain Arnell <iarnell@gmail.com> 0.45-1
- update to latest upstream version

* Fri Apr 20 2012 Iain Arnell <iarnell@gmail.com> 0.40-1
- update to latest upstream version

* Mon Apr 09 2012 Iain Arnell <iarnell@gmail.com> 0.39-2
- avoid circular dependencies (patch from Paul Howarth rhbz#810707)

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 0.39-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.38-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.38-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.38-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.37-2
- Perl mass rebuild

* Thu May 05 2011 Iain Arnell <iarnell@gmail.com> 0.37-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.35-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 0.33-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.33)
- altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- altered br on perl(Test::More) (0.62 => 0.88)
- added a new br on perl(Test::Requires) (version 0.05)
- added a new br on perl(Test::Warn) (version 0.21)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.27)
- altered br on perl(Getopt::Long::Descriptive) (0.077 => 0.081)
- dropped old BR on perl(Scalar::Util)
- dropped old BR on perl(Test::Pod::Coverage)
- altered req on perl(Getopt::Long::Descriptive) (0.077 => 0.081)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.26-1
- add perl_default_filter
- PERL_INSTALL_ROOT => DESTDIR in install
- auto-update to 0.26 (by cpan-spec-update 0.01)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- auto-update to 0.22 (by cpan-spec-update 0.01)
- altered br on perl(Getopt::Long::Descriptive) (0 => 0.077)
- added a new br on perl(Test::Moose) (version 0)
- altered req on perl(Getopt::Long::Descriptive) (0 => 0.077)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- auto-update to 0.20 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Getopt::Long) (2.35 => 2.37)
- added a new req on perl(Getopt::Long) (version 2.37)
- added a new req on perl(Getopt::Long::Descriptive) (version 0)
- added a new req on perl(Moose) (version 0.56)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update to 0.18

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- update to 0.15

* Thu Jul 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-2
- tweak Getopt::Long dep to 2.35; passes tests just fine with 2.35, and that's
  what we have in F-8 perl

* Sat Jun 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13
- switch to Module::Install invocations, rather than Module::Build

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-2
- rebuild for new perl

* Fri Aug 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05
- license tag: GPL -> GPL+

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-2
- bump

* Thu May 03 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update to 0.03

* Fri Apr 20 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- Specfile autogenerated by cpanspec 1.69.1.
