Name:           perl-MooseX-Traits-Pluggable 
Summary:        A pluggable extension to MooseX::Traits 
Version:        0.10
Release:        9%{?dist}
License:        GPL+ or Artistic 
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RK/RKITOVER/MooseX-Traits-Pluggable-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/MooseX-Traits-Pluggable
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Class::MOP) >= 0.84
BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)

Requires:       perl(Class::MOP) >= 0.84
Requires:       perl(List::MoreUtils)
Requires:       perl(Moose)
Requires:       perl(Moose::Role)
Requires:       perl(namespace::autoclean)
Requires:       perl(Scalar::Util)


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
This module adds support for class precedence search for traits and some
extra attributes, described below.

See the MooseX::Traits manpage for more information.

%prep
%setup -q -n MooseX-Traits-Pluggable-%{version}

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
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.10-9
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.10-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.10-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.10-2
- Perl mass rebuild

* Mon Mar 07 2011 Iain Arnell <iarnell@gmail.com> 0.10-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.09)
- added a new req on perl(Class::MOP) (version 0.84)
- added a new req on perl(List::MoreUtils) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(Moose::Role) (version 0)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- submission
- br CPAN for inc::Module::Install::AutoInstall

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
