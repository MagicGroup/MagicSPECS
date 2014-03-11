Name:           perl-Test-Warn
Version:        0.24
Release:        4%{?dist}
Summary:        Perl extension to test methods for warnings
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Warn/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/Test-Warn-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp) >= 1.22
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Sub::Uplevel) >= 0.12
BuildRequires:  perl(Test::Builder) >= 0.13
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Tree::DAG_Node) >= 1.02
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Test::Builder::Tester) >= 1.02
Requires:       perl(Tree::DAG_Node) >= 1.02

%description
This module provides a few convenience methods for testing warning
based code.

%prep
%setup -q -n Test-Warn-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT

%check


%files
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Warn.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.24-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.24-2
- Perl 5.16 rebuild

* Sun Apr  1 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24 (compatibility with Carp 1.25) (#808856)
- BR: Perl core modules that might be dual-lived
- BR/R: at least version 1.02 of perl(Tree::DAG_Node)
- Drop redundant buildreq perl(Test::Exception)
- Don't need to remove empty directories from buildroot
- Drop explicit versioned runtime dependency on Test::Builder, satisfied in
  all distributions since the dawn of time (nearly)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Drop redundant %%{?perl_default_filter}
- Make %%files list more explicit
- Don't use macros for commands

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild
- remove unused BR Array::Compare

* Wed Mar  2 2011 Tom Callaway <spot@fedoraproject.org> - 0.23-1
- update to 0.23

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Tom Callaway <spot@fedoraproject.org> - 0.22-1
- update to 0.22

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.21-2
- rebuild against perl 5.10.1

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- add perl default filter (pro forma)
- use _fixperms incantation
- auto-update to 0.21 (by cpan-spec-update 0.01)
- altered br on perl(Test::Builder::Tester) (0 => 1.02)
- altered req on perl(Test::Builder::Tester) (0 => 1.02)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (#477298)
- Buildreq ExtUtils::MakeMaker, File::Spec, Test::Builder,
  Test::Builder::Tester, and Test::More (from upstream Makefile.PL)
- Add runtime dependencies on Test::Builder and Test::Builder::Tester

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-3
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-2
- rebuild for new perl

* Sat May  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.10-1
- Update to 0.10.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.09-1
- Update to 0.09.
- New upstream maintainer.
- New BR: perl(Test::Pod).

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-4
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Jul  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-2
- Dist tag.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.08-0.fdr.1
- First build.
