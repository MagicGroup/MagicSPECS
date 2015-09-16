Name:		perl-Perl-Critic
Version:	1.126
Release:	3%{?dist}
Summary:	Critique Perl source code for best-practices
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Perl-Critic/
Source0:	http://search.cpan.org/CPAN/authors/id/T/TH/THALJEF/Perl-Critic-%{version}.tar.gz
BuildArch:	noarch

# Build process
BuildRequires:	perl(lib)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Task::Weaken)

# Module requirements
%if ! (0%{?rhel} >= 7)
BuildRequires:	aspell-en
%endif
BuildRequires:	perl(B::Keywords) >= 1.05
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config::Tiny) >= 2
BuildRequires:	perl(Email::Address) >= 1.889
BuildRequires:	perl(English)
BuildRequires:	perl(Exception::Class) >= 1.23
BuildRequires:	perl(Exporter) >= 5.58
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Unix)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(IO::String)
BuildRequires:	perl(List::MoreUtils) >= 0.19
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Module::Pluggable) >= 3.1
BuildRequires:	perl(Perl::Tidy)
BuildRequires:	perl(Pod::Parser)
BuildRequires:	perl(Pod::PlainText)
BuildRequires:	perl(Pod::Select)
BuildRequires:	perl(Pod::Spell) >= 1
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(PPI) >= 1.215
BuildRequires:	perl(PPIx::Regexp) >= 0.010
BuildRequires:	perl(PPIx::Utilities::Node)
BuildRequires:	perl(PPIx::Utilities::Statement) >= 1.001
BuildRequires:	perl(Readonly) >= 1.03
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(String::Format) >= 1.13
BuildRequires:	perl(Test::Builder) >= 0.92
BuildRequires:	perl(Text::ParseWords) >= 3
BuildRequires:	perl(version) >= 0.77

# Optional module requirements
BuildRequires:	perl(File::HomeDir)
BuildRequires:	perl(File::Which)
BuildRequires:	perl(Readonly::XS)
BuildRequires:	perl(Term::ANSIColor) >= 2.02

# Main test suite
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::Memory::Cycle)
BuildRequires:	perl(Test::More)

# We don't run the author tests when bootstrapping due to circular dependencies
# Test::Perl::Critic obviously pulls in Perl::Critic too
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Devel::EnforceEncapsulation)
BuildRequires:	perl(Perl::Critic::Policy::Editor::RequireEmacsFileVariables)
BuildRequires:	perl(Perl::Critic::Policy::ErrorHandling::RequireUseOfExceptions)
%if ! (0%{?rhel} >= 7)
BuildRequires:	perl(Test::Kwalitee)
%endif
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Without::Module)
%endif

# Optional/not automatically detected runtime dependencies
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if ! (0%{?rhel} >= 7)
Requires:	aspell
%endif
Requires:	perl(File::HomeDir)
Requires:	perl(File::Which)
Requires:	perl(Module::Pluggable) >= 3.1
Requires:	perl(Pod::Parser)
Requires:	perl(PPI) >= 1.215
Requires:	perl(Readonly::XS)
Requires:	perl(Term::ANSIColor) >= 2.02

%description
Perl::Critic is an extensible framework for creating and applying coding
standards to Perl source code. Essentially, it is a static source code
analysis engine. Perl::Critic is distributed with a number of
Perl::Critic::Policy modules that attempt to enforce various coding
guidelines. Most Policy modules are based on Damian Conway's book Perl
Best Practices. However, Perl::Critic is not limited to PBP and will
even support Policies that contradict Conway. You can enable, disable,
and customize those Polices through the Perl::Critic interface. You can
also create new Policy modules that suit your own tastes.

%package -n perl-Test-Perl-Critic-Policy
Summary:	A framework for testing your custom Policies
Group:		Development/Libraries
License:	GPL+ or Artistic

%description -n perl-Test-Perl-Critic-Policy
This module provides a framework for function-testing your custom
Perl::Critic::Policy modules. Policy testing usually involves feeding it a
string of Perl code and checking its behavior. In the old days, those strings
of Perl code were mixed directly in the test script. That sucked.

%prep
%setup -q -n Perl-Critic-%{version}

# Drop Test::Kwalitee tests in RHEL ≥ 7
%if 0%{?rhel} >= 7
rm xt/author/95_kwalitee.t
sed -i -e '/^xt\/author\/95_kwalitee.t$/ d' MANIFEST
%endif

# Drop exec bits from samples/docs to avoid dependency bloat
find tools examples -type f -exec chmod -c -x {} ';'

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
LC_ALL=en_US ./Build %{!?perl_bootstrap:author}test

%files
%doc Changes LICENSE README TODO.pod examples/ extras/ tools/
%{_bindir}/perlcritic
%{perl_vendorlib}/Perl/
%{_mandir}/man1/perlcritic.1*
%{_mandir}/man3/Perl::Critic*.3pm*

%files -n perl-Test-Perl-Critic-Policy
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Perl::Critic::Policy.3pm*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.126-3
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.126-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.126-1
- 更新到 1.126

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.118-12
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.118-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.118-10
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.118-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.118-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.118-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.118-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.118-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.118-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.118-3
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.118-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Paul Howarth <paul@city-fan.org> - 1.118-1
- update to 1.118
  Policy Changes:
  - CodeLayout::RequireTidyCode: revise to work with incompatible changes in
    Perl::Tidy 20120619 (CPAN RT#77977)
  - TestingAndDebugging::ProhibitNoWarnings: correct the parse of the
    'no warnings' statement, so that 'no warnings "qw"' is recognized as
    suppressing just 'qw' warnings (CPAN RT#74647)
  - Miscellanea::RequireRcsKeywords has been moved to the Perl-Critic-More
    distribution (CPAN RT#69546)
  Other Changes:
  - make all unescaped literal "{" characters in regexps into character
    classes; these are deprecated, and became noisy with Perl 5.17.0
    (CPAN RT#77510)
- drop now-redundant patch for Perl::Tidy compatibility
- BR: perl(lib) for the build process
- BR: perl(base), perl(PPIx::Utilities::Node) and perl(Test::Builder) ≥ 0.92
  for the module (Test::Builder required by Test::Perl::Critic::Policy)
- BR: perl(Exporter) ≥ 5.58; with older versions we get:
  ":color_severity" is not exported by the Perl::Critic::Utils::Constants module
- BR: perl(File::Spec::Functions) for the test suite
- drop buildreqs for perl(charnames), perl(File::Basename), perl(File::Find),
  perl(overload), perl(strict) and perl(warnings) - not dual lived

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.117-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jul 10 2012 Paul Howarth <paul@city-fan.org> - 1.117-8
- fix breakage with Perl::Tidy ≥ 20120619 (CPAN RT#77977)

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.117-7
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.117-6
- Perl 5.16 rebuild

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.117-5
- conditionalize aspell

* Tue Apr 24 2012 Petr Pisar <ppisar@redhat.com> - 1.117-4
- do not use Test::Kwalitee on RHEL ≥ 7

* Tue Feb 28 2012 Paul Howarth <paul@city-fan.org> - 1.117-3
- spec clean-up
  - separate build requirements and runtime requirements
  - drop redundant %%{?perl_default_filter}
  - fix permissions verbosely
  - use tabs

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.117-2
- drop %%defattr, no longer needed

* Thu Dec 22 2011 Paul Howarth <paul@city-fan.org> - 1.117-1
- update to 1.117
  New Policies:
  - Variables::ProhibitAugmentedAssignmentInDeclaration reports constructs like
    'my $x += 1'
  Policy Changes:
  - BuiltinFunctions::ProhibitLvalueSubstr: add explicit 'use version'
    (CPAN RT#68498)
  - CodeLayout::ProhibitHardTabs: add 'pbp' to the default_themes list
    (CPAN RT#71093)
  - ControlStructures::ProhibitMutatingListFunctions now understands that
    tr///r (introduced in 5.13.7) does not change its operand
  - ControlStructures::ProhibitMutatingListFunctions now understands that
    '//=', '<<=', and '>>=' are assignment operators (CPAN RT#70901)
  - ErrorHandling::RequireCheckingReturnValueOfEval now allows things
    like grep { eval $_ } (CPAN RT#69489)
  - Modules::RequireExplicitPackage now has configuraion option
    allow_import_of, to allow the import of specified modules before the
    package statement (CPAN RT#72660)
  - RegularExpressions::ProhibitEnumeratedClasses no longer thinks
    that [A-Za-z_] matches \w. RT #69322.
  - RegularExpressions::ProhibitUnusedCaptures now skips the first block of
    an 'if' or 'elsif' if the regular expression is bound to its operand with
    the '!~' operator (CPAN RT#69867)
  - RegularExpressions::ProhibitUnusedCaptures now looks into lists and blocks
    in the replacement portion of the regular expression if /e is asserted
    (CPAN RT#72086)
  - RegularExpressions::RequireDotMatchAnything,
    RegularExpressions::RequireExtendedFormatting and
    RegularExpressions::RequireLineBoundaryMatching now honor defaults set with
    'use re "/modifiers"' (CPAN RT#72151)
  - Subroutines::ProhibitManyArgs now recognizes '+' as a prototype character
  - Variables::ProhibitPunctuationVars now recognizes bracketed variables
    embedded in interpolated strings (e.g. "${$}"); for the purpose of the
    'allow' configuration, these are considered equivalent to the unbracketed
    form (CPAN RT#72910)
  Other Changes:
  - corrected POD in Perl::Critic::PPI::Utils (CPAN RT#68898)
  - Perl::Critic::Violation source() method now returns the line containing
    the violation (not the first line) when the statement containing the
    violation spans multiple lines
- this release by THALJEF -> update source URL
- drop stopwords patch, now included upstream

* Fri Jul 22 2011 Paul Howarth <paul@city-fan.org> - 1.116-6
- reinstate author tests: META.yml creation issue fixed in perl-5.14.1-182

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 1.116-5
- completely disable author tests to avoid Kwalitee META complaints

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.116-4
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.116-3
- Perl mass rebuild

* Wed Jun 29 2011 Paul Howarth <paul@city-fan.org> - 1.116-2
- move BR: perl(Test::Perl::Critic) to author test section where it belongs
- run the author tests if we're not bootstrapping

* Mon May 16 2011 Paul Howarth <paul@city-fan.org> - 1.116-1
- update to 1.116
  - BuiltInFunctions::ProhibitLvalueSubstr does not report violations if the
    document contains an explicit 'use n.nnn;' where the version is before
    5.005 (CPAN RT#59112)
  - Documentation::RequirePodSections no longer blows up on code having POD but
    no =head1 (CPAN RT#67231)
  - RegularExpressions::ProhibitUnusedCapture should more reliably find things
    like s/(a)/${1}2/ (CPAN RT#67273)
  - ValuesAndExpressions::ProhibitMagicNumbers and Module::RequireVersionVar
    now treat versions passed as the second argument of a 'package' statement
    the same as versions declared as 'our $VERSION ...' (CPAN RT#67159)
  - Variables::RequireLexicalLoopIterators does not report violations if the
    document contains an explicit 'use n.nnn;' where the version is before
    5.004 (CPAN RT#67760)

* Fri Apr  1 2011 Paul Howarth <paul@city-fan.org> - 1.115-1
- update to 1.115
  - fatal error in RegularExpressions::ProhibitUnusedCapture here document
    check (CPAN RT#67116)
  - internal POD error in Documentation::RequirePodLinksIncludeText
    (CPAN RT#67012)

* Tue Mar 29 2011 Paul Howarth <paul@city-fan.org> 1.114-1
- update to 1.114
  - Documentation::RequirePodLinksIncludeText now handles nested POD formatting
    (CPAN RT#65569)
  - clarified relation of severity numbers to names in Perl::Critic POD
    (CPAN RT#66017)
  - removed caveats from Variables::RequireLocalizedPunctuationVars, no longer
    necessary with PPI 1.208 (CPAN RT#65514)
  - have InputOutput::RequireBriefOpen attempt to expand scope as necessary to
    deal with the case where the open() and the corresponding close() are not
    in the same scope (CPAN RT#64437)
  - RegularExpressions::ProhibitUnusedCapture now looks inside double-quotish
    things (CPAN RT#38942)
  - RegularExpressions::ProhibitUnusedCapture now takes logical alternation
    into account, so that (e.g.)
	if ( /(a)/ || /(b)/ ) {
		say $1;
	}
    is not a violation (CPAN RT#38942)
  - ValuesAndExpressions::ProhibitCommaSeparatedStatements now recognizes
    'return { foo => 1, bar => 2 }' as containing a hash constructor, not a
    block; this was fixed by PPI 1.215 (CPAN RT#61301)
  - ValuesAndExpressions::ProhibitCommaSeparatedStatements now recognizes
    'bless { foo => 1, bar => 2 }' as containing a hash constructor, not a
    block; this was fixed by PPI 1.215 (CPAN RT#64132)
- bump PPI version requirement to 1.215
- BR/R: perl(Pod::Parser)
- BR/R: optional modules perl(Readonly::XS), perl(Term::ANSIColor) >= 2.02
- BR: perl(Pod::Spell) >= 1
- BR: perl(Text::ParseWords) >= 3
- add runtime deps for optional modules perl(File::HomeDir), perl(File::Which)
- drop redundant (for modern rpm) BuildRoot tag and buildroot cleaning
- split Test::Perl::Critic::Policy off into its own package
- add dependency on aspell for Perl::Critic::Policy::Documentation::PodSpelling
- add version 1.889 requirement for perl(Email::Address)
- add version 0.19 requirement for perl(List::MoreUtils)
- add version 0.010 requirement for perl(PPIx::Regexp)
- add version 1.001 requirement for perl(PPIx::Utilities::Statement)
- add version 0.77 requirement for perl(version)
- drop unused buildreq perl(Test::Spelling)
- drop bogus buildreqs perl(lib) and perl(base)
- add option for building with author tests enabled (--with authortests)
- add patch with words not in Fedora dictionaries for spell check tests
- split buildreqs into separate sections for build process, the module, the
  main test suite and the author tests

* Mon Mar  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.113-1
- update to 1.113

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.111-1
- update

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.108-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Aug  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.108-1
- update

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.105-4
- mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.105-3
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> - 1.105-2
- use the new filtering macros (verified that the resulting provides
  and requires are the same)
- add version to perl(PPI) require (#541020)

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.105-1
- new upstream version
- update build requires

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.098-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.098-1
- "neaten" filtering
- auto-update to 1.098 (by cpan-spec-update 0.01)
- added a new br on perl(strict) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new br on perl(Pod::Usage) (version 0)
- added a new br on perl(File::Find) (version 0)
- added a new br on perl(PPI::Token::Whitespace) (version 1.203)
- added a new br on perl(charnames) (version 0)
- added a new br on perl(PPI::Document::File) (version 1.203)
- added a new br on perl(File::Spec::Unix) (version 0)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(lib) (version 0)
- added a new br on perl(Getopt::Long) (version 0)
- added a new br on perl(Exporter) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(overload) (version 0)
- added a new br on perl(base) (version 0)
- added a new br on perl(version) (version 0)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(warnings) (version 0)
- added a new br on perl(PPI::Document) (version 1.203)
- added a new br on perl(File::Basename) (version 0)
- added a new br on perl(PPI::Token::Quote::Single) (version 1.203)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Path) (version 0)
- added a new br on perl(Pod::PlainText) (version 0)
- added a new br on perl(Pod::Select) (version 0)
- added a new br on perl(PPI::Node) (version 1.203)
- added a new br on perl(English) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.092-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.092-1
- update to 1.092

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.082-1
- update to 1.082
- resolve BZ#431577
- add t/ examples/ extras/ tools/, and filter

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-3
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-2
- add missing BR: perl-Exception-Class

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-1
- bump to 1.080

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.053-2
- rebuild for new perl

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.053-1
- Update to 1.053.

* Tue Mar 20 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Thu Feb 15 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.

* Fri Jan 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-2
- Bumping release (forgot to commit sources and .cvsignore changes).

* Fri Jan 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.
- New build requirement: perl(Test::Memory::Cycle).

* Thu Jan 25 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- perl(Set::Scalar) is no longer required.

* Wed Jan 24 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.
- New requirement: perl(B::Keywords).
- Author tests coverage improved.

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Enabled author tests.
- BR perl(HomeDir).

* Sun Dec 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22.

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.
- New BR: perl(Set::Scalar).

* Sat Sep 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.2-1
- First build.
