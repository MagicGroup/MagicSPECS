Name:       perl-Test-Strict 
Version:	0.27
Release:	1%{?dist}
# see lib/Test/Strict.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Check syntax, presence of use strict/warnings, and test coverage
Source:     http://search.cpan.org/CPAN/authors/id/S/SZ/SZABGAB/Test-Strict-%{version}.tar.gz
Url:        http://search.cpan.org/dist/Test-Strict
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:  noarch
BuildRequires: perl(Devel::Cover)
BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Temp)
BuildRequires: perl(FindBin)
BuildRequires: perl(Test::Builder)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod)

%description
"Test::Strict" lets you check the syntax, presence of "use strict;" and
"use warnings;" in your perl code.  It reports its results in standard 
"Test::Simple" fashion. 

%prep
%setup -q -n Test-Strict-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README Changes 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.27-1
- 更新到 0.27

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-10
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-9
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.17-8
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.17-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-2
- 为 Magic 3.0 重建

* Thu Jan 03 2013 Petr Šabata <contyk@redhat.com> - 0.17-1
- 0.17 bump
- Modernize the spec a bit
- Remove unused build dependencies
- Update source URL

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.14-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.14-2
- Perl mass rebuild

* Thu Feb 24 2011 Iain Arnell <iarnell@gmail.com> 0.14-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13

* Tue Nov 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- bump

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update for submission

* Wed Nov 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

