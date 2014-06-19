Name:           perl-MooseX-Params-Validate
Summary:        Extension of Params::Validate using Moose's types
Version:        0.18
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/MooseX-Params-Validate-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/MooseX-Params-Validate/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Devel::Caller)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Moose) >= 0.58
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Moose::Util::TypeConstraints)
BuildRequires:  perl(overload)
BuildRequires:  perl(Params::Validate) >= 0.88
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)

# obsolete/provide old tests sub-package
# can be removed during F21 development cycle
Obsoletes:      %{name}-tests < 0.18-1
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module fills a gap in Moose by adding method parameter validation to
Moose. This is just one of many developing options, it should be considered
the "official" one by any means though.

%prep
%setup -q -n MooseX-Params-Validate-%{version}

# silence rpmlint warning
sed -i -e '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README LICENSE t
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.18-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version
- drop explicit requires
- drop tests sub-package; move tests to main documentation

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.16-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.16-2
- Perl mass rebuild

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-1
- Mass rebuild with perl-5.12.0 & update

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.13)
- dropped old BR on perl(Sub::Name)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.12-2
- rebuild against perl 5.10.1

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- auto-update to 0.12 (by cpan-spec-update 0.01)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Devel::Caller) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Devel::Caller) (version 0)
- added a new req on perl(Moose) (version 0.58)
- added a new req on perl(Params::Validate) (version 0.88)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(Sub::Exporter) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-2
- rebuild against new Moose

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07
- change from Build.PL to Makefile.PL incantation (now using Module::Install)
- update br's

* Tue Jul 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.03-2
- rebuild for new perl

* Mon Oct 22 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update to 0.03
- license tag update: GPL -> GPL+
- add t/ to doc

* Thu Apr 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- update to 0.02

* Thu Apr 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.01-2
- bump

* Wed Apr 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- Specfile autogenerated by cpanspec 1.69.1.
