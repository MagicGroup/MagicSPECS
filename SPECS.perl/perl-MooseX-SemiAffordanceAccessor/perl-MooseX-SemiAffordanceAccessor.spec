Name:           perl-MooseX-SemiAffordanceAccessor
Summary:        Name your accessors foo() and set_foo()
Version:	0.10
Release:	3%{?dist}
License:        Artistic 2.0
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/MooseX-SemiAffordanceAccessor-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/MooseX-SemiAffordanceAccessor
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.31
BuildRequires:  perl(Moose) >= 1.16
BuildRequires:  perl(Test::More) >= 0.88

Requires:       perl(Moose) >= 1.16

%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
This module does not provide any methods. Simply loading it changes the
default naming policy for the loading class so that accessors are
separated into get and set methods. The get methods have the same name
as the accessor, while set methods are prefixed with "set_".If you
define an attribute with a leading underscore, then the set method will
start with "_set_".If you explicitly set a "reader" or "writer" name
when creating an attribute, then that attribute's naming scheme is left
unchanged.


%prep
%setup -q -n MooseX-SemiAffordanceAccessor-%{version}

# sigh
find lib/ -type f -exec perl -pi -e 's/0\.5504/0.55/' {} ';'

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
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.10-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10-1
- 更新到 0.10

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.09-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.09-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.09-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.09-2
- Perl mass rebuild

* Mon Mar 07 2011 Iain Arnell <iarnell@gmail.com> 0.09-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Aug 26 2010 Iain Arnell <iarnell@gmail.com> 0.08-2
- add new LICENSE to docs

* Thu Aug 26 2010 Iain Arnell <iarnell@gmail.com> 0.08-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.08)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- altered br on perl(Moose) (0.84 => 0.94)
- altered br on perl(Test::More) (0 => 0.88)
- dropped old BR on perl(Module::Build::Compat)
- altered req on perl(Moose) (0.84 => 0.94)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-2
- rebuild against perl 5.10.1

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- auto-update to 0.05 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.56 => 0.84)
- added a new req on perl(Moose) (version 0.84)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- submission

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
