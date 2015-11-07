Name:		perl-Config-Tiny
Version:	2.23
Release:	2%{?dist}
Summary:	Perl module for reading and writing .ini style configuration files
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Config-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RS/RSAVAGE/Config-Tiny-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
# Test::MinimumVersion -> Perl::MinimumVersion -> Perl::Critic -> Config::Tiny
%if 0%{!?perl_bootstrap:1}
# Test::MinimumVersion not available for EPEL < 6
BuildRequires:	perl(Test::MinimumVersion)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Config::Tiny is a Perl module designed for reading and writing .ini
style configuration files. It is designed for simplicity and ease of
use, and thus only supports the most basic operations.

%prep
%setup -q -n Config-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t" AUTOMATED_TESTING=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Config/
%{_mandir}/man3/Config::Tiny.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.23-2
- 更新到 2.23

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 2.22-1
- 更新到 2.22

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.14-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.14-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.14-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.14-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.14-4
- Perl 5.16 rebuild

* Thu Jan 19 2012 Paul Howarth <paul@city-fan.org> - 2.14-3
- Reinstate compatibility with older distributions like EL-5
- Run release tests as well as the regular test suite
- BR: perl(Test::CPAN::Meta) and perl(Test::More)
- Only drop perl(Test::MinimumVersion) as a buildreq when bootstrapping, and
  add a comment about why that's needed
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Make %%files list more explicit
- No longer need to fix permissions of Tiny.pm
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 2.14-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.12-12
- Rebuild with Perl 5.14.1
- Use perl_bootstrap macro
- Add missing BR ExtUtils::MakeMaker

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.12-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.12-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.12-8
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-5
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-4
- Rebuild for perl 5.10 (again), first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-3
- Rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-2.1
- Rebuild with TMV, tests disabled for first pass

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.12-2
- Rebuild for new perl

* Thu Dec 13 2007 Ralf Corsépius <rc040203@freenet.de> - 2.12-1
- Update to 2.12

* Mon Oct  2 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.10-1
- Updated to 2.10

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.08-1
- Updated to 2.08

* Wed May 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.07-1
- Updated to 2.07

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.06-1
- Updated to 2.06

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.05-1
- Updated to 2.05

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-2
- Rebuild for FC5 (perl 5.8.8)

* Sat Jan 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-1
- Updated to 2.04

* Fri Dec 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.03-1
- Updated to 2.03

* Mon Jun 27 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.02-1
- Updated to 2.02

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.01-2
- Rebuilt

* Thu Mar 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.01-1
- Updated to 2.01

* Sun Jul 25 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:2.00-0.fdr.1
- Updated to 2.00

* Sat Jul 10 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.9-0.fdr.1
- Updated to 1.9

* Fri Jul  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.8-0.fdr.1
- Updated to 1.8

* Tue Jun 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.7-0.fdr.1
- Updated to 1.7

* Sat Jun  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.3
- Changed URL to canonical location (bug 1140)
- Added build req perl >= 1:5.6.1 and perl(Test::More) (bug 1140)
- Added missing req perl(:MODULE_COMPAT_...) (bug 1140)
- Updated to match most recent perl spec template (bug 1140)
- Removed unneeded optimization settings and find *.bs (bug 1140)

* Thu Mar 18 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.2
- Reduced directory ownership bloat

* Thu Mar 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.6-0.fdr.1
- Updated to 1.6

* Wed Jan  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:1.5-0.fdr.1
- Updated to 1.5

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:1.3-0.fdr.1
- Initial RPM release

