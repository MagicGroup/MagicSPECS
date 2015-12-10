# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-Package-Stash
Version:	0.37
Release:	4%{?dist}
Summary:	Routines for manipulating stashes
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Package-Stash/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Dist::CheckConflicts) >= 0.02
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(lib)
BuildRequires:	perl(Package::DeprecationManager)
BuildRequires:	perl(Package::Stash::XS) >= 0.24
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Requires)
# Optional tests:
%if ! (0%{?rhel} >= 7)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::LeakTrace)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
%endif
BuildRequires:	perl(Test::Script)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# For performance and consistency
Requires:	perl(Package::Stash::XS) >= 0.24
# Not found by rpm auto-provides
Provides:	perl(Package::Stash::Conflicts) = 0

%description
Manipulating stashes (Perl's symbol tables) is occasionally necessary, but
incredibly messy, and easy to get wrong. This module hides all of that behind
a simple API.

%prep
%setup -q -n Package-Stash-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%if ! (0%{?rhel} >= 7)
 AUTHOR_TESTING=1 RELEASE_TESTING=1
%else

%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{_bindir}/package-stash-conflicts
%{perl_vendorlib}/Package/
%{_mandir}/man3/Package::Stash.3pm*
%{_mandir}/man3/Package::Stash::PP.3pm*
%{_mandir}/man1/package-stash-conflicts.1*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.37-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.37-3
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.37-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.37-1
- 更新到 0.37

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.33-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.33-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.33-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.33-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.33-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.33-8
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Petr Pisar <ppisar@redhat.com> - 0.33-7
- Disable author tests on RHEL >= 7

* Fri Aug 24 2012 Paul Howarth <paul@city-fan.org> - 0.33-6
- Drop EPEL-4 support
  - Drop %%defattr, redundant since rpm 4.4
  - Test::LeakTrace, Test::Requires and Test::Script are now universally available
  - A suitably recent version of ExtUtils::MakeMaker is now universally available
- Don't need to remove empty directories from the buildroot

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.33-5
- Specify all dependendencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.33-3
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.33-2
- Fedora 17 mass rebuild

* Thu Sep 29 2011 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Add conflict on MooseX::Method::Signatures 0.36
- BR: perl(Carp)

* Tue Sep  6 2011 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Bring the behavior of has_symbol for nonexistant scalars into line with the
    XS version
  - Invalid package names (for instance, Foo:Bar) are not allowed
  - Invalid stash entry names (anything containing ::) are not allowed
- Update patches to apply cleanly
- Bump perl(Package::Stash::XS) version requirement to 0.24

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Fix ->add_symbol('$foo', qr/sdlfk/) on 5.12+
  - Fix ->add_symbol('$foo', \v1.2.3) on 5.10+
- Update patch for old Test::More versions
- Update patch for no Test::Requires

* Thu Jul 21 2011 Paul Howarth <paul@city-fan.org> - 0.30-2
- Perl mass rebuild

* Thu Jul 21 2011 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Fix compiler detection in Makefile.PL
- Update patch for old ExtUtils::MakeMaker versions
- Drop usage of macros for commands
- Drop redundant %%{?perl_default_filter}
- perl(Pod::Coverage::TrustPod) now available everywhere

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.29-2
- Perl mass rebuild

* Wed Apr  6 2011 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29
  - Really skip the package-stash-conflict script in the compile test

* Wed Mar 30 2011 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - META.json fixes
- Update patch for old ExtUtils::MakeMaker versions to apply cleanly

* Mon Mar 28 2011 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Skip the package-stash-conflicts script in the compile test

* Sat Mar  5 2011 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - Make the namespace cache lazy and weak, in case the stash is deleted
  - However, this doesn't work on 5.8, so disable the namespace caching
    entirely there
- Update patches to apply cleanly
- Bump perl(Package::Stash::XS) version requirement to 0.22
- Bump perl(Dist::CheckConflicts) version requirement to 0.02

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25 (make the leak tests author-only, since some smokers run
  release tests)
- Update patches to apply cleanly
- Bump perl(Package::Stash::XS) version requirement to 0.21
- Drop buildreq perl(Test::Exception), no longer needed

* Tue Jan 18 2011 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24 (reinstate Test::Requires dependency)

* Wed Jan 12 2011 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Lower perl prereq to 5.8.1
  - Make the leak tests release-only
- Update patches to apply cleanly
- Add patch to skip memory leak tests if we don't have Test::LeakTrace

* Thu Jan  6 2011 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22 (bump Package::Stash::XS version requirement since a bug was
  fixed there)
- Update patches for old ExtUtils::MakeMaker and Test::More versions
- BR/R perl(Package::Stash::XS) >= 0.19
- Content-free manpages for package-stash-conflicts and
  Package::Stash::Conflicts dropped upstream

* Tue Jan  4 2011 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Methods were renamed for brevity: s/_package//
  - Convert Package::Stash into a module which loads either the XS or pure perl
    implementation, depending on what's available
  - Use Test::Fatal instead of Test::Exception
  - Use Dist::CheckConflicts
  - Silence deprecation warnings for the method renaming for now
- New script and manpage: package-stash-conflicts
- New modules and manpages: Package::Stash::Conflicts and Package::Stash::PP
- New build requirements:
  - perl(Dist::CheckConflicts)
  - perl(Package::DeprecationManager)
  - perl(Package::Stash::XS)
  - perl(Test::LeakTrace)
  - perl(Test::Requires)
  - perl(Test::Script)
- Update patches for old ExtUtils::MakeMaker and Test::More versions
- Add new patch to work around absence of Test::Requires in EPEL-4
- Require perl(Package::Stash::XS) for performance and consistency
- Manually provide perl(Package::Stash::Conflicts), hidden from auto-provides

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon Sep 20 2010 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08 (re-enable the caching of the stash)
- Update patch for old ExtUtils::MakeMaker and Test::More versions

* Wed Jun 16 2010 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Bump Test::More requirement for done_testing
  - Update packaging stuff
- BR: perl(Test::EOL) and perl(Test::NoTabs)
- Unify spec for all active branches, adding patches for back-compatibility

* Mon Jun 14 2010 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04 (get_package_symbol now doesn't autovivify stash entries; a
  new method get_or_add_package_symbol can now be used for that behavior)

* Mon Jun 14 2010 Paul Howarth <paul@city-fan.org> - 0.03-2
- Incorporate package review suggestions (#602597)
  - Use %%{?perl_default_filter}
  - Use DESTDIR instead of PERL_INSTALL_ROOT

* Mon Jun  7 2010 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
