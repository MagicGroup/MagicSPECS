# Pick up the right dictionary for the spell check
%if %(perl -e 'print $] >= 5.010000 ? 1 : 0;')
%global speller hunspell
%else
%global speller aspell
%endif

# some arches don't have valgrind so we need to disable its support on them
%ifarch %{ix86} x86_64 ppc ppc64 s390x %{arm}
%global with_valgrind 1
%endif

Name:		perl-Test-LeakTrace
Summary:	Trace memory leaks
Version:	0.15
Release:	3%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-LeakTrace/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Test-LeakTrace-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl(Test::More) >= 0.62
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Spelling), %{speller}-en
BuildRequires:	perl(Test::Synopsis)
%if 0%{?with_valgrind}
BuildRequires:	perl(Test::Valgrind)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Obsolete/Provide old tests subpackage
# Can be removed during F19 development cycle
%if 0%{?perl_default_filter:1}
Obsoletes:	%{name}-tests < 0.14
Provides:	%{name}-tests = %{version}-%{release}
%endif

# Don't provide private perl libs
%{?perl_default_filter}

%description
Test::LeakTrace provides several functions that trace memory leaks. This module
scans arenas, the memory allocation system, so it can detect any leaked SVs in
given blocks.

Leaked SVs are SVs that are not released after the end of the scope they have
been created. These SVs include global variables and internal caches. For
example, if you call a method in a tracing block, perl might prepare a cache
for the method. Thus, to trace true leaks, no_leaks_ok() and leaks_cmp_ok()
executes a block more than once.

%prep
%setup -q -n Test-LeakTrace-%{version}

# Remove redundant exec bits
chmod -c -x lib/Test/LeakTrace/Script.pm t/lib/foo.pl

# Fix up shellbangs in doc scripts
sed -i -e 's|^#!perl|#!/usr/bin/perl|' benchmark/*.pl example/*.{pl,t} {t,xt}/*.t

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


# Run the release tests
# Don't spell-check JA.pod as it can generate false positives
mv lib/Test/LeakTrace/JA.pod ./
touch lib/Test/LeakTrace/JA.pod
%if 0%{?with_valgrind}
DICTIONARY=en_US  TEST_FILES="xt/*.t"
%else
DICTIONARY=en_US  TEST_FILES="$(echo xt/*.t | sed 's|xt/05_valgrind.t||')"
%endif
rm lib/Test/LeakTrace/JA.pod
mv ./JA.pod lib/Test/LeakTrace/

%clean
rm -rf %{buildroot}

%files
%doc Changes README benchmark/ example/ %{?perl_default_filter:t/ xt/}
%{perl_vendorarch}/auto/Test/
%{perl_vendorarch}/Test/
%{_mandir}/man3/Test::LeakTrace.3pm*
%{_mandir}/man3/Test::LeakTrace::JA.3pm*
%{_mandir}/man3/Test::LeakTrace::Script.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.15-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.15-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.15-1
- 更新到 0.15

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Wed Jul 18 2012 Dan Horák <dan[at]danny.cz> - 0.14-4
- valgrind is available only on selected arches and perl(Test::Valgrind) is noarch

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 0.14-3
- Perl 5.16 rebuild

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 0.14-2
- BR: perl(Test::Valgrind) for additional test coverage

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Fix Test::Valgrind failures
- Drop tests subpackage; move tests to main package documentation as long as
  we have %%{perl_default_filter} to avoid the resulting doc-file dependencies
- Run the release tests too, except for xt/05_valgrind.t since we don't have
  Test::Valgrind yet
- BR: perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::Spelling),
  aspell-en/hunspell-en and perl(Test::Synopsis) for the release tests
- Drop version requirement of perl(ExtUtils::MakeMaker) to 6.30, which works
  fine in EPEL-5
- Tidy %%description
- Make %%files list more explicit
- Package benchmark/ and example/ as documentation
- Drop explicit versioned requires of perl(Exporter) ≥ 5.57, satisfied by all
  supported distributions
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Use ">= 0", instead of "== 0" for no_leaks_ok()
  - Add count_sv() to count all the SVs in a perl interpreter
  - Fix tests broken for some perls in 0.12

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (#654301)
  - Fix false-positive related to XS code (CPAN RT #58133)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-2
- Mass rebuild with perl-5.12.0

* Sun Apr 04 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.10-1
- Specfile by Fedora::App::MaintainerTools 0.006

