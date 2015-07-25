# PPI::XSAccessor is experimental
%if 0%{?rhel} >= 7
%bcond_with XSAccessor
%else
%bcond_without XSAccessor
%endif

Name:           perl-PPI
Version:        1.215
Release:        16%{?dist}
Summary:        Parse, Analyze and Manipulate Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/PPI/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/PPI-%{version}.tar.gz
Patch0:         PPI-1.215-utf8.patch
BuildArch:      noarch
# =============== Module Build ======================
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Task::Weaken)
# =============== Module Runtime ====================
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone) >= 0.30
BuildRequires:  perl(constant)
BuildRequires:  perl(Digest::MD5) >= 2.35
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.84
BuildRequires:  perl(IO::String) >= 1.07
BuildRequires:  perl(List::MoreUtils) >= 0.16
BuildRequires:  perl(List::Util) >= 1.20
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable) >= 2.17
# =============== Test Suite ========================
BuildRequires:  perl(Class::Inspector) >= 1.22
BuildRequires:  perl(File::Remove) >= 0.39
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(Test::More) >= 0.86
BuildRequires:  perl(Test::NoWarnings) >= 0.084
BuildRequires:  perl(Test::Object) >= 0.07
BuildRequires:  perl(Test::SubCalls) >= 1.07
BuildRequires:  perl(Time::HiRes)
# =============== Release Tests =====================
# Circular dependencies in release tests, so don't do them when bootstrapping:
# Perl::MinimumVersion -> PPI
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(File::Find::Rule) >= 0.32
BuildRequires:  perl(File::Find::Rule::Perl) >= 1.09
BuildRequires:  perl(Perl::MinimumVersion) >= 1.20
BuildRequires:  perl(Pod::Simple) >= 3.14
BuildRequires:  perl(Test::ClassAPI) >= 1.03
BuildRequires:  perl(Test::CPAN::Meta) >= 0.17
BuildRequires:  perl(Test::MinimumVersion) >= 0.101080
BuildRequires:  perl(Test::Pod) >= 1.44
%endif
# =============== Module Runtime ====================
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if %{with XSAccessor}
Requires:       perl(Class::XSAccessor)
%endif
# Run-require Task::Weaken, see Changes for more details.
Requires:       perl(Task::Weaken)

# Filter out redundant unversioned provides
%global __provides_exclude ^perl\\(PPI::.+\\)$

%description
Parse, analyze and manipulate Perl (without perl).

%prep
%setup -q -n PPI-%{version}

# Recode documentation as UTF-8
%patch0

%if %{without XSAccessor}
rm lib/PPI/XSAccessor.pm
sed -i '/^lib\/PPI\/XSAccessor\.pm$/d' MANIFEST
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check

%if 0%{!?perl_bootstrap:1}
 TEST_FILES="xt/*.t" RELEASE_TESTING=1
%endif

%files
%doc Changes LICENSE README inline2test.conf inline2test.tpl
%{perl_vendorlib}/PPI/
%{perl_vendorlib}/PPI.pm
%{_mandir}/man3/PPI*.3pm*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.215-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.215-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.215-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.215-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.215-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.215-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.215-10
- 为 Magic 3.0 重建

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 1.215-9
- classify buildreqs by usage
- BR: perl(Time::HiRes) for the test suite
- BR: perl(Pod::Simple) ≥ 3.14 for the release tests
- BR: at least version 0.17 of perl(Test::CPAN::Meta)
- bump perl(Test::Pod) version requirement to 1.44
- don't need to remove empty directories from the buildroot

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.215-8
- specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-7
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.215-6
- perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.215-5
- perl 5.16 rebuild
- build-require Class::Inspector for tests

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.215-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Paul Howarth <paul@city-fan.org> - 1.215-3
- always run test suite but don't run release tests when bootstrapping
- nobody else likes macros for commands
- clean up for modern rpm:
  - drop explicit buildroot tag
  - drop buildroot cleaning
  - drop %%defattr
  - use native provides filtering
- use a patch rather than scripting iconv to fix character encoding
- upstream file permissions no longer need fixing

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.215-2
- rebuild with Perl 5.14.1
- use perl_bootstrap macro

* Sun Mar 27 2011 Paul Howarth <paul@city-fan.org> - 1.215-1
- update to 1.215 (general fix release):
  - index_locations on an empty document no longer warns
  - Corrected a bug in line-spanning attribute support
  - Regression test for line-spanning attribute support
  - return { foo => 1 } should parse curlys as hash constructor, not block
    (CPAN RT#61305)
  - Fixed bug with map and regexp confusing PPI (CPAN RT#63943)
  - Updated copyright year to 2011
  - Fix bless {} probably contains a hash constructor (CPAN RT#64247)
  - Backed out glob fix
  - Fix cast can trump braces in PPI::Token::Symbol->symbol (CPAN RT#65199)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.213-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.213-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.213-1
- update to 1.213 (targeted bug fix, no changes to parsing or normal usage)
  - Updated to Module::Install 1.00
  - Updated module dependencies in xt author tests
  - Fixed extremely broken PPI::Token::Pod::merge and added test case
- bump perl(Perl::MinimumVersion) requirement to 1.25
- bump perl(Test::CPAN::Meta) requirement to 0.17
- bump perl(Test::Pod) requirement to 1.44

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.212-1
- update to 1.212 (experimental/development support and bugfixes)
  - Fixed bug in ForLoop back-compatibility warning (CPAN RT#48819)
  - Added support for $ENV{X_TOKENIZER} --> $PPI::Lexer::X_TOKENIZER
  - Upgraded to Module::Install 0.93
  - Added support for $PPI::Lexer::X_TOKENIZER, for alternate tokenizers
  - Added an extra test case to validate we handle byte order marks properly
  - Moved author tests from t to xt
  - Fixed CPAN RT#26082: scalar { %%x } is misparsed
  - Fixed CPAN RT#26591: VMS patch for PPI 1.118
  - Fixed CPAN RT#44862: PPI cannot parse "package Foo::100;" correctly
  - Fixed CPAN RT#54208: PPI::Token::Quote::Literal::literal missing
- run release tests as well as regular test suite
- BR: perl(File::Find::Rule) >= 0.32, perl(File::Find::Rule::Perl) >= 1.09, 
  perl(Perl::MinimumVersion) >= 1.24 and perl(Test::MinimumVersion) >= 0.101080 
  for release tests

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.210-1
- update to 1.210 (packaging fixes)
- use RELEASE_TESTING rather than AUTOMATED_TESTING for better test coverage

* Sat Jul 31 2010 Paul Howarth <paul@city-fan.org> - 1.209-1
- update to 1.209 (small optimisation release, no functional changes)

* Fri Jul 30 2010 Paul Howarth <paul@city-fan.org> - 1.208-1
- update to 1.208
  - don't assign '' to $^W, it generates a warning on Gentoo
  - added missing PPI::Token::Regexp fix to Changes file
  - updating Copyright to the new year
  - fixed #50309: literal() wrong result on "qw (a b c)"
  - PPI::Dumper no longer causes Elements to flush location data
  - PPI::Dumper no longer disables location information for non-Documents
  - +{ package => 1 } doesn't create a PPI::Statement::Package
  - extra methods in PPI::Token::Regexp and PPI::Token::QuoteLike::Regexp
- use %%{_fixperms} macro instead of our own chmod incantation

* Fri Jul 30 2010 Paul Howarth <paul@city-fan.org> - 1.206-6
- BR: perl(Task::Weaken) and perl(Test::CPAN::Meta) for improved test coverage
- enable AUTOMATED_TESTING
- use DESTDIR rather than PERL_INSTALL_ROOT

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.206-5
- Mass rebuild with perl-5.12.0

* Thu Feb 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.206-4
- fix filtering, provide versioned provides

* Wed Feb 10 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.206-3
- make rpmlint happy

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.206-2
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.206-1
- new upstream version
- update build requires

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.203-1
- update to 1.203

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-3
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.201-1
- bump to 1.201

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.118-1
- Update to 1.118.

* Wed Sep  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.117-1
- Update to 1.117.

* Sun Jun  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.115-2
- Removed the perl(IO::Scalar) build requirement.

* Sun Jun  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.115-1
- Update to 1.115.

* Wed May 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.113-1
- Update to 1.113.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.112-1
- Update to 1.112.

* Sat Apr 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.111-1
- First build.
