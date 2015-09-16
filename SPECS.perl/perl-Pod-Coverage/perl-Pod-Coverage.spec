Name:           perl-Pod-Coverage
Version:	0.23
Release:	1%{?dist}
Summary:        Checks if the documentation of a module is comprehensive
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Pod-Coverage/
Source0:        http://www.cpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(Devel::Symdump) >= 2.01
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Find) >= 0.21
BuildRequires:  perl(Pod::Parser) >= 1.13
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(Devel::Symdump) >= 2.01
Requires:       perl(Pod::Find) >= 0.21
Requires:       perl(Pod::Parser) >= 1.13
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Devel::Symdump\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Find\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Pod::Parser\\)$

%description
Developers hate writing documentation.  They'd hate it even more if their
computer tattled on them, but maybe they'll be even more thankful in the
long run.  Even if not, perlmodstyle tells you to, so you must obey.

This module provides a mechanism for determining if the pod for a given
module is comprehensive.

%prep
%setup -q -n Pod-Coverage-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes examples
%{_bindir}/pod_cover
%{perl_vendorlib}/Pod/
%{_mandir}/man3/Pod::Coverage.3pm*
%{_mandir}/man3/Pod::Coverage::CountParents.3pm*
%{_mandir}/man3/Pod::Coverage::ExportOnly.3pm*
%{_mandir}/man3/Pod::Coverage::Overloader.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.23-1
- 更新到 0.23

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.22-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.22-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.22-2
- Perl 5.16 rebuild

* Wed Feb 08 2012 Petr Šabata <contyk@redhat.com> - 0.22-1
- 0.22 bump
- Switch to EE::MM
- Modernize spec

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.21-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 14 2010 Petr Sabata <psabata@redhat.com> - 0.21-1
- New release, v0.21

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.20-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20 (test updates)
- No README in upstream distribution
- BR: perl(Test::More)
- More specific files list

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-3
- Rebuild for perl 5.10 (again), second pass with tests enabled

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-2
- Rebuild for perl 5.10 (again), first pass without Test::Pod, tests

* Sat Jan 12 2008 Steven Pritchard <steve@kspei.com> 0.19-1
- Update to 0.19.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to match cpanspec output.

* Thu Jan 10 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-3
- rebuild 2, enable Test::Pod, tests

* Thu Jan 10 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.18-2.1
- rebuild (first pass, no tests, no Test::Pod)

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-2
- Version 0.18 is now a noarch package.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-5
- Rebuild for FC5 (perl 5.8.8).

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-4
- Add dist tag.

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-3
- Avoid .packlist creation with Module::Build >= 0.2609.
- Trust that %%{perl_vendorlib} is defined.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Nov 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.17-1
- Update to 0.17.

* Wed Oct 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.16-0.fdr.1
- Update to 0.16.

* Thu May 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.14-0.fdr.1
- First build.
