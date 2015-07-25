# tests require working /dev/tty - disabled by default for koji
# see https://rt.cpan.org/Public/Bug/Display.html?id=54807
%bcond_with     check

Name:           perl-IO-Prompt
Summary:        Interactively prompt for user input
%global cpanver 0.997002
Version:        0.997.002
Release:        6%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DC/DCONWAY/IO-Prompt-%{cpanver}.tar.gz 
URL:            http://search.cpan.org/dist/IO-Prompt
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with check}
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Term::ReadKey)
BuildRequires:  perl(Want)
# Tests:
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
An object-oriented way to prompt for user input -- and control how the user is
prompted.

This module is no longer being maintained. Use the IO::Prompter module instead.

%prep
%setup -q -n IO-Prompt-%{cpanver}
find examples -type f -exec chmod -x {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
%if %{with check}
    make test
%else
    echo "Not running tests unless --with check is specified"
%endif

%files
%doc Changes README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.997.002-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.997.002-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Petr Pisar <ppisar@redhat.com> - 0.997.002-1
- 0.997002 bump
- Drop tests sub-package
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.997.001-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 05 2011 Iain Arnell <iarnell@gmail.com> 0.997.001-1
- update to latest upstream version
- apply patch to fix rt#69084
- remove unnecessary explicit requires

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.997-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.997-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.997-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.997-3
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.997-2
- conditionalize tests -- they fail in koji

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.997-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(IO::Handle) (version 0)
- added a new req on perl(POSIX) (version 0)
- added a new req on perl(Term::ReadKey) (version 0)
- added a new req on perl(Want) (version 0)
- added a new req on perl(version) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.99.4-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.99.4-3
- rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.99.4-2
- bump for mass rebuild

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.99.4-1
- bump spec for f-e release 

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.99.4-0.1
- added additional test modules as BR for better testing...

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> v0.99.4-0
- Initial spec file for F-E
