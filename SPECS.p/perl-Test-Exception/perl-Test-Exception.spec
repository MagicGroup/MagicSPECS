Name:           perl-Test-Exception
Version:        0.31
Release:        9%{?dist}
Summary:        Library of test functions for exception based Perl code
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Exception/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AD/ADIE/Test-Exception-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build) >= 0.35
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Sub::Uplevel) >= 0.18
BuildRequires:  perl(Test::Builder) >= 0.7
BuildRequires:  perl(Test::Builder::Tester) >= 1.07
BuildRequires:  perl(Test::Harness) >= 2.03
BuildRequires:  perl(Test::More) >= 0.7
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Simple) >= 0.7
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides a few convenience methods for testing exception
based code. It is built with Test::Builder and plays happily with
Test::More and friends.

%prep
%setup -q -n Test-Exception-%{version}

find . -type f -perm +100 -exec chmod a-x {} \;

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.31-9
- 为 Magic 3.0 重建

* Thu Oct 18 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-8
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.31-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.31-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 10 2010 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-2
- Mass rebuild with perl-5.12.0

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- auto-update to 0.29 (by cpan-spec-update 0.01)
- altered br on perl(Module::Build) (0 => 0.35)
- altered br on perl(Test::Builder) (0 => 0.7)
- altered br on perl(Test::Builder::Tester) (0 => 1.07)
- added a new br on perl(Test::Harness) (version 2.03)
- added a new br on perl(Test::More) (version 0.7)
- added a new br on perl(Test::Simple) (version 0.7)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.27-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.27-2
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 0.27-1
- Update to 0.27.

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.26-2
- rebuild for new perl

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.26-1
- Update to 0.26.
- Update License tag.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.
- Drop executable bits.

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-3
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-2
- Rebuild for FC5 (perl 5.8.8).

* Tue Jun  7 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-4
- Add dist tag.

* Sat Apr 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.20-3
- Avoid .packlist creation with Module::Build >= 0.2609.
- Trust that %%{perl_vendorlib} is defined.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.20-2
- rebuilt

* Fri Nov  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- Update to 0.20.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.15-0.fdr.1
- First build.
