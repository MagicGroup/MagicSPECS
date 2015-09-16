# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:           perl-Scalar-Properties
Version:        1.100860
Release:        9%{?dist}
Summary:        Run-time properties on scalar variables
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Scalar-Properties/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARCEL/Scalar-Properties-%{version}.tar.gz
Patch3:         Scalar-Properties-1.100860-skip-MYMETA.yml.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.11
# ===================================================================
# Module requirements
# ===================================================================
# (no non-core/dual-lived requirements)
# ===================================================================
# Test requirements
# ===================================================================
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
# ===================================================================
# Author test requirements
# (skipped as the Critic test fails in version 1.100860)
# ===================================================================
BuildRequires:  perl(English)
BuildConflicts: perl(Test::Perl::Critic)
# ===================================================================
# Release test requirements
# (Spelling check can't find "versa" in version 1.100860)
# ===================================================================
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildConflicts: perl(Pod::Wordlist::hanekomu)
BuildRequires:  perl(Test::CheckChanges)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::DistManifest)
BuildRequires:  perl(Test::HasVersion)
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Spelling), aspell-en
BuildRequires:  perl(Test::Synopsis)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Scalar::Properties attempts to make Perl more object-oriented by taking an idea
from Ruby: Everything you manipulate is an object, and the results of those
manipulations are objects themselves.

%prep
%setup -q -n Scalar-Properties-%{version}

# MANIFEST.SKIP should include MYMETA.yml; otherwise, t/release-dist-manifest.t
# may fail due to it appearing unexpectedly
%patch3 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test AUTHOR_TESTING=1 RELEASE_TESTING=1

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Scalar/
%{_mandir}/man3/Scalar::Properties.3pm*

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.100860-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-7
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.100860-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 1.100860-4
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100860-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 1.100860-1
- Update to 1.100860
  - Converted the distribution to Dist::Zilla-style
- Run the author/release tests too, adding buildreqs as necessary
- Package LICENSE file
- Clean up for modern rpmbuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.13-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-10
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-8
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-3
- fix source url

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1.1
- BR: Test::More

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1
- 0.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Apr 09 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.12-1
- First build.
