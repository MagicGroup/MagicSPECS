Name:           perl-CatalystX-Component-Traits
Summary:        Automatic Trait Loading and Resolution for
Version:        0.16
Release:        23%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/CatalystX-Component-Traits-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CatalystX-Component-Traits
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Runtime) >= 5.80005
BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Module::Pluggable) >= 3.9
BuildRequires:  perl(MooseX::Traits::Pluggable) >= 0.08
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod)

Requires:       perl(Catalyst::Runtime) >= 5.80005
Requires:       perl(MooseX::Traits::Pluggable) >= 0.08


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
Adds a "COMPONENT" method to your Catalyst component base class that
reads the optional 'traits' parameter from app and component config
and instantiates the component subclass with those traits using
MooseX::Traits/new_with_traits from MooseX::Traits::Pluggable.


%prep
%setup -q -n CatalystX-Component-Traits-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.16-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.16-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.16-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-4
- Mass rebuild with perl-5.12.0

* Sun Mar 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.14-3
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Moose::Autobox)
- dropped old requires on perl(Moose::Autobox)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.14-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- auto-update to 0.14 (by cpan-spec-update 0.01)
- altered br on perl(Test::More) (0 => 0.88)
- added a new req on perl(List::MoreUtils) (version 0)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)

* Fri Sep 04 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- submission
- add standard req/prov filter
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered br on perl(MooseX::Traits::Pluggable) (0.06 => 0.08)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Catalyst::Runtime) (version 5.80005)
- added a new req on perl(Moose::Autobox) (version 0)
- added a new req on perl(MooseX::Traits::Pluggable) (version 0.08)


* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- submission

* Fri Aug 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
