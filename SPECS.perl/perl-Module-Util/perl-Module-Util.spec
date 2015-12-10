Name:       perl-Module-Util
Version:	1.09
Release:	3%{?dist}
# see lib/Module/Util.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Module name tools and transformations
Source:     http://search.cpan.org/CPAN/authors/id/M/MA/MATTLAW/Module-Util-%{version}.tar.gz
Url:        http://search.cpan.org/dist/Module-Util
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(Module::Build)
BuildRequires: perl(Test::More)

%{perl_default_filter}

%description
This module provides a few useful functions for manipulating module names.
Its main aim is to centralize some of the functions commonly used by
modules that manipulate other modules in some way, like converting module
names to relative paths.

%prep
%setup -q -n Module-Util-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man[13]/*.[13]*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.09-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.09-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.09-1
- 更新到 1.09

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.08-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.08-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.08-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.08-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.08-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.08-5
- 为 Magic 3.0 重建

* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 1.08-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.08-2
- Perl 5.16 rebuild

* Sun Jun 10 2012 Iain Arnell <iarnell@gmail.com> 1.08-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- use perl_default_filter
- use Module::Build, not EU::MM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-5
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- auto-update to 1.07 (by cpan-spec-update 0.01)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.05-1
- update to 1.05

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.04-1
- clean up for submission

* Wed Nov 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.04-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
