# We need to patch the test suite if we have an old version of Test::More or Test::Spelling
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.94) ? 1 : 0);' 2>/dev/null || echo 0)
%global older_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)
%global even_older_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.82) ? 1 : 0);' 2>/dev/null || echo 0)
%global old_test_spelling %(perl -MTest::Spelling -e 'print (($Test::Spelling::VERSION < 0.12) ? 1 : 0);' 2>/dev/null || echo 0)

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Pod-Wordlist-hanekomu
Version:	1.122840
Release:	9%{?dist}
Summary:	Add words for spell checking POD
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		https://metacpan.org/module/Pod::Wordlist::hanekomu/
Source0:	http://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Pod-Wordlist-hanekomu-%{version}.tar.gz
Patch1:		Pod-Wordlist-hanekomu-1.110090-Test::More-version.patch
Patch2:		Pod-Wordlist-hanekomu-1.121370-Test::More-done_testing.patch
Patch3:		Pod-Wordlist-hanekomu-1.113620-Test::More-note.patch
Patch4:		Pod-Wordlist-hanekomu-1.122840-old-Test::Spelling.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Carp)
BuildRequires:	perl(English)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Spelling), aspell-en
BuildRequires:	perl(utf8)
# ===================================================================
# Author/Release test requirements
#
# Don't run these tests or include their requirements if we're
# bootstrapping, as many of these modules require each other for
# their author/release tests.
# ===================================================================
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::HasVersion)
BuildRequires:	perl(Test::CheckChanges)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
# Test::Vars requires Perl 5.10 and so is not available in EPEL-5
%if "%{?rhel}" != "5"
BuildRequires:	perl(Test::Vars)
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
When loaded, this module automatically adds Test::Spelling stopwords for
POD spell checking, that is, words that should be ignored by the spell
check.

The stopword list includes some CPAN author names, technical terms (e.g.
JSON, URI) and other commonly-used words not included in the default
word list (e.g. mixin, munging).

%prep
%setup -q -n Pod-Wordlist-hanekomu-%{version}

# We have to patch the test suite if we have an old Test::More
#
# Don't really need Test::More ≥ 0.94
%if %{old_test_more}
%patch1 -p1
%endif
# done_testing requires Test::More ≥ 0.88
%if %{older_test_more}
%patch2 -p1
%endif
# note() requires Test::More ≥ 0.82
%if %{even_older_test_more}
%patch3 -p1
%endif

# Don't really need Test::Spelling ≥ 0.12
%if %{old_test_spelling}
%patch4
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
 %{!?perl_bootstrap:AUTHOR_TESTING=1 RELEASE_TESTING=1}

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Pod/
%{_mandir}/man3/Pod::Wordlist::hanekomu.3pm*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.122840-9
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.122840-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.122840-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.122840-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.122840-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.122840-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.122840-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.122840-2
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Paul Howarth <paul@city-fan.org> - 1.122840-1
- Update to 1.122840
  - Added "MongoDB", "RDBMS", "SQLite" and "iteratively"
- Update patch for building with Test::Spelling < 0.12

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.121370-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.121370-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.121370-2
- Perl 5.16 rebuild

* Thu May 17 2012 Paul Howarth <paul@city-fan.org> - 1.121370-1
- Update to 1.121370
  - Added: "GUIDs", "UUID", "UUIDs", "searchable"
- Update patch for building with Test::More < 0.88

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 1.121231-1
- Update to 1.121231
  - Added "deserialized" and "parameterizable"
- Drop now-redundant BR: perl(Test::Requires)
- Update patch for building with Test::More < 0.88
- Add new patch for building with Test::Spelling < 0.12 if necessary

* Sun Apr  1 2012 Paul Howarth <paul@city-fan.org> - 1.120920-1
- Update to 1.120920
  - Added "pre", "precompute", "prereq", "prereqs", "symlinked"
- Drop %%defattr, redundant since rpm 4.4
- perl(Test::Kwalitee) and perl(Test::MinimumVersion) now available in EPEL-5

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 1.120740-1
- Update to 1.120740
  - Documentation and metadata update
  - Added "CamelCase", "CPANPLUS", "EINTR", "GUID", "HTTPS", "IETF", "IRC",
    "ISP", "ISP's", "JSON", "modulino", "SMTP", "SSL", "URI's", "UTC", "wiki"
    "analyses", "chunked", "locator", "redirections", "reusability", and
    "timestamp"
- BR: perl(Test::Requires)
- Update %%description
- Use metacpan.org URLs
- Don't need to remove empty directories from buildroot
- Drop support for EOL EL-4:
  - No longer need to support building with ExtUtils::MakeMaker < 6.30
  - Unconditionally BR: perl(Test::Perl::Critic) and perl(Test::Synopsis)
- Update patch for building with Test::More < 0.88

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.113620-2
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Wed Dec 28 2011 Paul Howarth <paul@city-fan.org> - 1.113620-1
- Update to 1.113620
  - Added "Lapworth", "UTF", "aggregator", "aggregators", "probe's",
    "runtime", "seekable" and "sigils"
- Re-diff patches where necessary to avoid .orig file pollution

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 1.110090-3
- Sanitize for Fedora/EPEL submission

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 1.110090-2
- BR: perl(Test::HasVersion) and perl(Test::Vars) for full release test
  coverage

* Sun Aug  7 2011 Paul Howarth <paul@city-fan.org> - 1.110090-1
- Initial RPM version
