Name:           perl-Module-CPANTS-Analyse
Version:        0.86
Release:        5%{?dist}
Summary:        Generate Kwalitee ratings for a distribution
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-CPANTS-Analyse/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAXIM/Module-CPANTS-Analyse-%{version}.tar.gz
Source1:        66B25843.asc
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Archive::Any) >= 0.06
BuildRequires:  perl(Archive::Tar) >= 1.48
BuildRequires:  perl(Array::Diff) >= 0.04
BuildRequires:  perl(Class::Accessor) >= 0.19
BuildRequires:  perl(CPAN::DistnameInfo) >= 0.06
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::chdir)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(File::Slurp)
BuildRequires:  perl(IO::Capture) >= 0.05
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(LWP::Simple)
BuildRequires:  perl(Module::ExtractUse) >= 0.18
BuildRequires:  perl(Module::Pluggable) >= 2.96
BuildRequires:  perl(Module::Signature)
BuildRequires:  perl(Pod::Simple::Checker) >= 2.02
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Set::Scalar)
BuildRequires:  perl(Software::License) >= 0.003
BuildRequires:  perl(Test::CPAN::Meta::YAML::Version)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
# We need to avoid Perl::Critic when bootstrapping because some of its dependencies
# such as PPIx::Regexp and Exception::Class may want to use Test::Kwalitee, which of
# course requires Module::CPANTS::Analyse
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(Test::Perl::Critic)
%endif
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Warn) >= 0.11
BuildRequires:  perl(Text::CSV_XS) >= 0.45
BuildRequires:  perl(version) >= 0.73
BuildRequires:  perl(YAML::Any)
Requires:       perl(Archive::Any) >= 0.06
Requires:       perl(Archive::Tar) >= 1.48
Requires:       perl(Array::Diff) >= 0.04
Requires:       perl(Class::Accessor) >= 0.19
Requires:       perl(CPAN::DistnameInfo) >= 0.06
Requires:       perl(IO::Capture) >= 0.05
Requires:       perl(Module::ExtractUse) >= 0.18
Requires:       perl(Module::Pluggable) >= 2.96
Requires:       perl(Pod::Simple::Checker) >= 2.02
Requires:       perl(version) >= 0.73
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
CPANTS is an acronym for CPAN Testing Service. The goals of the CPANTS project
are to provide some sort of quality measure (called "Kwalitee") and lots of
metadata for all distributions on CPAN.

%prep
%setup -q -n Module-CPANTS-Analyse-%{version}

# Fix line endings
sed -i -e 's/\r$//' bin/cpants_lint.pl Changes README TODO

# Don't want to clobber home directory when using gpg
mkdir --mode=0700 gpghome
export GNUPGHOME=$(pwd)/gpghome
gpg --import %{SOURCE1} || :

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT

%check
export GNUPGHOME=$(pwd)/gpghome

 AUTHOR_TEST=1 TEST_FILES="xt/*.t"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes README TODO
%{_bindir}/cpants_lint.pl
%dir %{perl_vendorlib}/Module/
%dir %{perl_vendorlib}/Module/CPANTS/
%{perl_vendorlib}/Module/CPANTS/Analyse.pm
%{perl_vendorlib}/Module/CPANTS/Kwalitee.pm
%dir %{perl_vendorlib}/Module/CPANTS/Kwalitee/
%{perl_vendorlib}/Module/CPANTS/Kwalitee/*.pm
%{_mandir}/man1/cpants_lint.pl.1*
%{_mandir}/man3/Module::CPANTS::Analyse.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::BrokenInstaller.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::CpantsErrors.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Distname.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Distros.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Files.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::FindModules.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::License.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Manifest.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::MetaYML.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::NeedsCompiler.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Pod.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Prereq.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Repackageable.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Signature.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Uses.3pm*
%{_mandir}/man3/Module::CPANTS::Kwalitee::Version.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.86-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.86-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.86-2
- Perl 5.16 rebuild

* Mon May 28 2012 Paul Howarth <paul@city-fan.org> - 0.86-1
- Update to 0.86 release
  - Add several strict and warnings equivalents and make it easy to add more
  - Fix when Moose is used and strict is not used
  - Add info about MIN_PERL_VERSION
  - Better remedy for metayml_declares_perl_version
  - metayml_declares_perl_version moved from experimental to extra
  - Some pod improvements
  - Fix CPAN RT#65903 - no more Test::YAML::Meta::Version on CPAN
  - Replace YAML::Syck with YAML::Any
  - no_symlinks checks only files in MANIFEST, use "maniread" in
    ExtUtils::Manifest
  - Add more equivalents for use_strict and use_warnings tests
  - Implement valid_signature metric
- This release by DAXIM -> update source URL
- Drop patch for Test::CPAN::Meta::YAML::Version, no longer needed
- Bump module version requirements:
  - perl(Archive::Tar) => 1.48
  - perl(Software::License) => 0.003
  - perl(Test::Warn) => 0.11
  - perl(Text::CSV_XS) => 0.45
- Switch to ExtUtils::MakeMaker flow so we don't need Module::Build ≥ 0.40
- BR: perl(Cwd), perl(ExtUtils::Manifest), perl(File::chdir),
  perl(Module::Signature), perl(Set::Scalar) and perl(Test::Pod::Coverage)
- BR: perl(YAML::Any) rather than perl(YAML::Syck)
- Drop perl(Test::CPAN::Meta::YAML::Version) version requirement

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.85-11
- Fix line endings of cpants_lint.pl script and documentation
- Run the author tests too
- BR: perl(Perl::Critic) except when bootstrapping
- BR: perl(Test::CPAN::Meta::YAML::Version) rather than
  perl(Test::CPAN::Meta::YAML)
- Don't BR: perl(Test::Pod::Coverage) due to presence of naked subroutines
- Sort buildreqs for readability
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.85-9
- Patch to use Test::CPAN::Meta::YAML instead of Test::YAML::Meta

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.85-9
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.85-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.85-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.85-5
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.85-4
- Fix source URL

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.85-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.85-1
- Update to 0.85 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-2
- Added more new & missing BRs

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.82-1
- Update to 0.82 release

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.75-3
- rebuild for new perl

* Wed Dec 26 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-2.fc9
- Added Test::Deep, Test::Pod, Test::Pod::Coverage build requires

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.75-1.fc9
- Specfile autogenerated by cpanspec 1.73.
