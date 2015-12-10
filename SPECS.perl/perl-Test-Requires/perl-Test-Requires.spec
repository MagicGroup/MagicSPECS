# Only need manual requires for "use base XXX;" prior to rpm 4.9
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e')

Name:		perl-Test-Requires
Summary:	Checks to see if a given module can be loaded
Version:	0.10
Release:	3%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Requires
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-Requires-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(Test::More) >= 0.61
%if ! ( 0%{?rhel} )
# Test::Perl::Critic -> Perl::Critic -> PPIx::Regexp -> Test::Kwalitee ->
#   Module::CPANTS::Analyse -> Test::Warn -> Sub::Uplevel -> Pod::Wordlist::hanekomu -> Test::Requires
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::Perl::Critic)
%endif
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Spelling)
%if %(perl -e 'print $] >= 5.010 ? 1 : 0;')
BuildRequires:	hunspell-en
%else
BuildRequires:	aspell-en
%endif
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if ! %{rpm49}
Requires:	perl(Test::Builder::Module)
%endif

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	%{name}-tests < %{version}-%{release}
Provides:	%{name}-tests = %{version}-%{release}

%description
Test::Requires checks to see if the module can be loaded.

If this fails, rather than failing tests this skips all tests.

%prep
%setup -q -n Test-Requires-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
# note the "skipped" warnings indicate success :)

 TEST_FILES="xt/*.t"

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Requires.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.10-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10-1
- 更新到 0.10

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-10
- 为 Magic 3.0 重建

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.06-9
- BR: perl(base), perl(Cwd), perl(Data::Dumper)
- RHEL builds don't use Test::Spelling so they don't need dictionaries either

* Wed Aug 15 2012 Marcela Maslanova <mmaslano@redhat.com> - 0.06-8
- Conditionalize test packages

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.06-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.06-5
- Perl 5.16 rebuild

* Thu Mar 22 2012 Paul Howarth <paul@city-fan.org> - 0.06-4
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't need explicit runtime dependency on perl(Test::Builder::Module) if we
  have rpm ≥ 4.9 as it can auto-detect it
- BR: at least version 0.61 of perl(Test::More) as per upstream
- Drop unnecessary version requirement for perl(ExtUtils::MakeMaker)
- Drop redundant %%{?perl_default_filter}
- BR: aspell-en rather than hunspell-en on old distributions where
  Test::Spelling uses aspell instead of hunspell
- Don't BR: perl(Test::Perl::Critic) when bootstrapping
- Don't use macros for commands
- Don't need to remove empty directories from buildroot
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 0.06-3
- BR: hunspell-en rather than aspell-en (#731272)

* Thu Nov 18 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Run release tests as well as standard test suite in %%check
- Drop no-longer-needed buildreq perl(Filter::Util::Call)
- New buildreqs perl(Test::Perl::Critic), perl(Test::Pod), perl(Test::Spelling)

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> - 0.06-1
- Update to latest upstream version

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.03-2
- Mass rebuild with perl-5.12.0

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Specfile by Fedora::App::MaintainerTools 0.006


