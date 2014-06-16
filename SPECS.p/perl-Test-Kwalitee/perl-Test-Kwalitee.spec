Name:		perl-Test-Kwalitee
Version:	1.18
Release:	2%{?dist}
Summary:	Test the Kwalitee of a distribution before you release it
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://metacpan.org/module/Test::Kwalitee
Source0:	http://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Kwalitee-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	perl(Module::Build::Tiny) >= 0.034
# Module
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Dist::CheckConflicts) >= 0.02
BuildRequires:	perl(Module::CPANTS::Analyse) >= 0.92
BuildRequires:	perl(namespace::clean)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder) >= 0.88
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(lib)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More) >= 0.94
BuildRequires:	perl(Test::Tester) >= 0.108
BuildRequires:	perl(Test::Warnings) >= 0.005
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Dist::CheckConflicts) >= 0.02

%description
Kwalitee is an automatically-measurable gauge of how good your software
is. That's very different from quality, which a computer really can't
measure in a general sense (if you can, you've solved a hard problem in
computer science).

%prep
%setup -q -n Test-Kwalitee-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
chmod -c 755 %{buildroot}%{_bindir}/kwalitee-metrics

%check
./Build test

%files
%doc Changes CONTRIBUTING LICENSE README README.md
%{_bindir}/kwalitee-metrics
%{perl_vendorlib}/Test/
%{_mandir}/man1/kwalitee-metrics.1*
%{_mandir}/man3/Test::Kwalitee.3pm*
%{_mandir}/man3/Test::Kwalitee::Conflicts.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - Updated list of available metrics
- Bump perl(Module::Build::Tiny) version requirement to 0.034
- Package README.md

* Mon Oct 21 2013 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - Now printing even more diagnostics on error (as much as we have available)
- Package new CONTRIBUTING file
- Update buildreqs as needed

* Wed Sep 25 2013 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Re-release with fixed compile test
- Bump perl(Module::Build::Tiny) version requirement to 0.027
- Update buildreqs for tests
  - Drop perl(CPAN::Meta::Check)
  - Add perl(ExtUtils::MakeMaker), perl(File::Spec::Functions) and
    perl(List::Util)
  - Bump perl(Test::CheckDeps) version requirement to 0.007

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Updated inaccurate test prereq
- Update buildreqs for tests
  - Drop perl(Capture::Tiny) and perl(Test::Script)
  - Require at least version 0.005 of perl(Test::Warnings)
  - BR: perl(File::Spec), perl(IO::Handle) and perl(IPC::Open3)

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Added missing abstract for kwalitee-metrics script
  - No longer issuing a warning if the test is running from xt/ (see v1.10)
- BR:/R: perl(Dist::CheckConflicts) ≥ 0.02
- Bump perl(Module::Build::Tiny) version requirement to 0.026
- BR: perl(CPAN::Meta::Check) ≥ 0.007 for the test suite

* Fri Aug  2 2013 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Adjusted tests to compensate for changes made in Module::CPANTS::Analyse
    0.88/0.90_01
- BR: perl(blib) for the test suite

* Tue Jul 30 2013 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Install the kwalitee-metrics script

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.10-2
- Perl 5.18 rebuild

* Mon Jul 29 2013 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10
  - We now issue a warning if running when neither AUTHOR_TESTING or
    RELEASE_TESTING environment variables are set
  - Test level adjusted, so location of failing test is correct
  - Include a script to dump all metrics ("kwalitee-metrics")
- BR: perl(Test::Script) ≥ 1.05 and perl(Test::Warnings) for the test suite

* Thu Jul 18 2013 Paul Howarth <paul@city-fan.org> - 1.09-1
- Update to 1.09
  - The has_test_pod, has_test_pod_coverage tests have been removed - they are
    classified as 'extra', and have been largely considered to be a bad idea
    anyway (these are often shipped as, and ought to be, in xt/)
  - The extractable test has been removed, as it does nothing in dists before
    there is a tarball present
  - New tests have been added: all standard kwalitee tests that can be run on a
    bare distribution without a tarball
- BR: perl(Capture::Tiny) for test suite

* Tue Jul 16 2013 Paul Howarth <paul@city-fan.org> - 1.08-1
- Update to 1.08
  - Documentation fixed to reflect which indicators are actually available
  - Metric names are no longer hardcoded, so Module::CPANTS::Analyse has more
    freedom to add and remove metrics
- Bump perl(Module::Build::Tiny) version requirement to 0.025
- Bump perl(Test::Builder) version requirement to 0.88

* Sat Jun 29 2013 Paul Howarth <paul@city-fan.org> - 1.07-1
- Update to 1.07
  - Now the indicators are run in the exact order they are returned from
    Module::CPANTS::Kwalitee::*, as some tests depend on the results of
    earlier tests
  - Synopsis updated to recommend a better way to run this module, ensuring
    that it is not run by cpantesters or at installation time
  - We no longer create a function in our namespace for every metric we are
    going to test; this should not break anyone, as these subs were never
    documented as part of the public API
  - Switch to Module::Build::Tiny flow
- BR: perl(namespace::clean) for module
- Bump version requirement for perl(Test::CheckDeps) to 0.006
- Don't bother with the extra tests (and their requirements) since
  Module::Build::Tiny doesn't provide any convenient method to run them

* Tue May 14 2013 Paul Howarth <paul@city-fan.org> - 1.06-1
- Update to 1.06
  - Restore previous behaviour of plan()ing in import, to unbreak some dists
    that didn't follow the docs (which in this case is ok since it's a horrible
    idea for a Test module to plan itself anyway) (v1.05)
  - More diagnostic data is printed when a test fails (CPAN RT#85107)
- Drop perl(Test::Builder) version requirement again

* Mon May 13 2013 Paul Howarth <paul@city-fan.org> - 1.05-1
- Update to 1.05
  - More rigorous testing of output; in order to make this possible, now we do
    END { done_testing } instead of planning a test count
- Bump perl(Test::Builder) version requirement to 0.88
- BR: perl(Test::Deep) and perl(Test::Tester) for the test suite
- Drop buildroot definition and cleaning since this release cannot work on EL-5
  due to the use of done_testing

* Wed May  1 2013 Paul Howarth <paul@city-fan.org> - 1.04-1
- Update to 1.04
  - Fixed documentation to refer to the proper names of Kwalitee tests
    (CPAN RT#24506)
  - Cleaned up partially-botched distribution metadata and README
- Classify buildreqs by usage
- Add buildreqs for new tests
- Explicitly run extra tests unless bootstrapping

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 1.02-1
- Update to 1.02
  - No operational changes - re-releasing under new management via github and
    Dist::Zilla
- This release by ETHER -> update source URL
- Update upstream URLs to MetaCPAN
- Switch to ExtUtils::MakeMaker flow
- Package upstream's new LICENSE file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.01-13
- Perl 5.16 rebuild

* Thu Mar  8 2012 Paul Howarth <paul@city-fan.org> - 1.01-12
- BR: perl(Cwd), perl(strict), perl(Test::Builder), perl(vars), perl(warnings)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Make %%files list more explicit
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.01-10
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.01-9
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.01-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.01-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.01-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Allisson Azevedo <allisson@gmail.com> - 1.01-1
- Initial rpm release
