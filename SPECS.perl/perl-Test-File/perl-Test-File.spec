Summary:	Test file attributes through Test::Builder
Name:		perl-Test-File
Version:	1.44
Release:	3%{?dist}
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-File/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Test-File-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Test::Builder) >= 0.33
BuildRequires:	perl(Test::Builder::Tester) >= 1.04
BuildRequires:	perl(Test::Manifest) >= 1.21
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides a collection of test utilities for file attributes.

Some file attributes depend on the owner of the process testing the file
in the same way the file test operators do.

%prep
%setup -q -n Test-File-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%files
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::File.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.44-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.44-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.44-1
- 更新到 1.44

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.34-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.34-2
- 为 Magic 3.0 重建

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - Added dir_exists_ok and dir_contains_ok
  - Added file_contains_like and file_contains_unlike
  - Fixed a few grammatical errors in POD
  - Added some SKIP blocks to avoid test failures when running as root
  - Fixed qr//mx patterns to work with older Perls (CPAN RT#74365)
  - Fixed incorrect spelling of "privileges" in SKIP blocks (CPAN RT#74483)
  - Skip testing of symlinks on Windows (CPAN RT#57682)
  - Fixed automatically generated test name for owner_isnt (CPAN RT#37676)
  - Fixed problem in MANIFEST file (CPAN RT#37676)
  - Fixed problem in links.t (CPAN RT#76853)
- This release by BAREFOOT -> update source URL
- BR: perl(base), perl(Exporter) and perl(File::Spec)
- Bump perl(Test::Manifest) version requirement to 1.21
- Bump perl(Test::More) version requirement to 0.88
- Drop perl(ExtUtils::MakeMaker) version requirement
- BR: at least version 1.00 of perl(Test::Pod)
- Drop buildreq perl(Test::Prereq) since t/prereq.t isn't in the test_manifest
- Package LICENSE file
- Expand %%summary and %%description
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't use macros for commands
- Make %%files list more explicit
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.29-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.29-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.29-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-1
- update to 1.29

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.25-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.25-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.25-1
- Upstream update.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-3
- helps if you upload new source

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-1
- bump to 1.22
- fix license tag

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Fri May 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Wed May 03 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- First build.
