Name:           perl-Catalyst-Plugin-ConfigLoader
Summary:        Load config files of various types
Version:	0.34
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Catalyst-Plugin-ConfigLoader-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Plugin-ConfigLoader/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Runtime) >= 5.7008
BuildRequires:  perl(Config::Any) >= 0.20
BuildRequires:  perl(Data::Visitor) >= 0.24
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(MRO::Compat) >= 0.09
BuildRequires:  perl(parent)
BuildRequires:  perl(Test::More)

Requires:       perl(Catalyst::Runtime) >= 5.7008
Requires:       perl(Config::Any) >= 0.20
Requires:       perl(Data::Visitor) >= 0.24
Requires:       perl(MRO::Compat) >= 0.09


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
This module will attempt to load find and load a configuration file of
various types. Currently it supports YAML, JSON, XML, INI and Perl formats.

%prep
%setup -q -n Catalyst-Plugin-ConfigLoader-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.34-1
- 更新到 0.34

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.30-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.30-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.30-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.30-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.30-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.30-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.30-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.30-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.30-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.30-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.30-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.30-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.30-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.30-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Iain Arnell <iarnell@gmail.com> 0.30-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-4
- Mass rebuild with perl-5.12.0

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.27-3
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Catalyst)
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)
- dropped old requires on perl(Catalyst)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.27-2
- rebuild against perl 5.10.1

* Tue Aug 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- auto-update to 0.27 (by cpan-spec-update 0.01)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-2
- add BR on parent (and open RT#48547)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-1
- auto-update to 0.25 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new req on perl(Catalyst::Runtime) (version 5.7008)
- added a new req on perl(Config::Any) (version 0.08)
- added a new req on perl(Data::Visitor) (version 0.24)
- added a new req on perl(MRO::Compat) (version 0.09)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- auto-update to 0.23 (by cpan-spec-update 0.01)
- added a new br on perl(Catalyst::Runtime) (version 5.7008)
- altered br on perl(Config::Any) (0.04 => 0.08)
- altered br on perl(Data::Visitor) (0.02 => 0.24)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- update to 0.22
- add br on MRO::Compat

* Wed Oct 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.21-2
- drop _with_network_tests bit

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- update to 0.21

* Sat May 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- update to 0.20

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-4
- rebuild for new perl

* Wed May 16 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.14-3
- bump

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.14-2
- conditionalize test which fails in mock (requires network access)

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- Specfile autogenerated by cpanspec 1.71.
