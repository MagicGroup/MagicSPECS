Name:           perl-Parse-RecDescent
Version:        1.967009
Release:        10%{?dist}
Summary:        Generate Recursive-Descent Parsers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Parse-RecDescent/
Source0:        http://search.cpan.org/CPAN/authors/id/J/JT/JTBRAUN/Parse-RecDescent-%{version}.tar.gz
Patch0:         Parse-RecDescent-1.967002-utf8.patch
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Text::Balanced) >= 1.95
# Tests:
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Warn)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Text::Balanced) >= 1.95

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Text::Balanced\\)$

%description
Parse::RecDescent incrementally generates top-down recursive-descent
text parsers from simple yacc-like grammar specifications. It
provides:

 * Regular expressions or literal strings as terminals (tokens)
 * Multiple (non-contiguous) productions for any rule
 * Repeated and optional subrules within productions
 * Full access to Perl within actions specified as part of the grammar
 * Simple automated error reporting during parser generation and parsing
 * The ability to commit to, uncommit to, or reject particular
   productions during a parse
 * The ability to pass data up and down the parse tree ("down" via
   subrule argument lists, "up" via subrule return values)
 * Incremental extension of the parsing grammar (even during a parse)
 * Precompilation of parser objects
 * User-definable reduce-reduce conflict resolution via "scoring" of
   matching productions

%prep
%setup -q -n Parse-RecDescent-%{version}

# Recode as UTF8
%patch0 -p1

# Fix permissions and script interpreters
chmod -c a-x demo/* tutorial/*
perl -pi -e 's|^#!\s?/usr/local/bin/perl\b|#!/usr/bin/perl|' demo/*

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
./Build test

%files
%doc Changes README ToDo demo/ tutorial/
%{perl_vendorlib}/Parse/
%{_mandir}/man3/Parse::RecDescent.3pm*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.967009-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.967009-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.967009-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.967009-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.967009-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.967009-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.967009-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.967009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.967009-2
- Perl 5.16 rebuild

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 1.967009-1
- 1.967009 bump

* Sat Feb 11 2012 Paul Howarth <paul@city-fan.org> - 1.967006-1
- Update to 1.967006 (#789560)
  - Localize the OUT filehandle during Precompile
  - Document the <autotree:Base::Class> form of the <autotree> directive
  - Provide a simple test for the <autotree> directive, t/autotree.t; renamed
    basics.t to ensure it runs before autotree.t
  - Allow a global <skip:> directive that functions the same as modifying
    $Parse::RecDescent::skip prior to compiling a grammar
  - Require that the $file returned by caller() be eq '-', rather than merely
    starting with '-'
  - Warn on empty productions followed by other productions: the empty
    production always matches, so following productions will never be reached
  - NON-BACKWARDS COMPATIBLE CHANGE: a repetition directive such as 'id(s /,/)'
    correctly creates a temporary @item variable to hold the 'id's that are
    matched. That @item variable is then used to set the real $item[] entry for
    that repetition. The same treatment is now given to %%item. Formerly, in a
    production like:
      id ',' id(s /,/)
    matched against:
      xxx, yyy, zzz
    The $item{id} entry that should be 'xxx' is overwritten by 'yyy' and then
    'zzz' prior to the action being executed. Now 'yyy' and 'zzz' set
    $item{id}, but in the private %%item, which goes out of scope once the
    repetition match completes.
  - EXPERIMENTAL: when precompiling, optionally create a standalone parser by
    including most of the contents of Parse::RecDescent in the resulting
    Precompiled output
  - Accept an optional $options hashref to Precompile, which can be used to
    specify $options->{-standalone}, which currently defaults to false
  - The subroutines import, Precompile and Save are not included in the
    Precompile'd parser
  - The included Parse::RecDescent module is renamed to
    Parse::RecDescent::_Runtime to avoid namespace conflicts with an installed
    and use'd Parse::RecDescent
  - Add a new t/precompile.t to test precompilation
  - Add a new $_FILENAME global to Parse::RecDescent to make it easy for the
    Precompile method to find the module
  - Remove the prototype from _generate; it is not required, and it caused
    t/precompile.t (which ends up re-defining a lot of Parse::RecDescent
    subroutines) to fail needlessly, as the calls to _generate in Replace and
    Extend normally do not see the prototype, but do when re-defined
  - POD documentation for standalone parsers added
  - Added ExtUtils::MakeMaker build/configure version requirements
    (CPAN RT#74787)
- BR: perl(Test::Pod) and perl(Test::Warn) for additional test coverage
- Use a patch rather than scripted iconv to fix character encoding
- Improve %%summary
- Tidy %%description
- Make %%files list more explicit
- Don't use macros for commands
- Don't need to specify compiler flags for pure-perl package
- Drop redundant 'find' commands from %%install

* Tue Jan 31 2012 Petr Šabata <contyk@redhat.com> - 1.967003-1
- 1.967003 bump (backwards-incompatible changes)
- Spec cleanup and modernization
- New Source URL
- Install to vendor

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.965001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.965001-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.965001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.965001-2
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Sep 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.965001-1
- update
- use Module::Build

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.964-2
- Mass rebuild with perl-5.12.0

* Fri Feb 19 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.964-1
- update, fix previous issue and https://rt.cpan.org/Public/Bug/Display.html?id=53948

* Tue Feb 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 1.963-2
- apply upstream patch https://rt.cpan.org/Public/Bug/Display.html?id=54457
  which should fix problems with rebuilds of other modules

* Tue Feb  9 2010 Paul Howarth <paul@city-fan.org> 1.963-1
- update to 1.963 (fix subtle bug in leftop and rightop due to removal of $&)
- recode Changes as utf-8
- more script interpreter fixes

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.962.2-1
- updated for latest GA SQL::Translator
- add default filtering
- auto-update to 1.962.2 (by cpan-spec-update 0.01)
- added a new br on perl(Text::Balanced) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Stepan Kasal <skasal@redhat.com> - 1.96-1
- new upstream version

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-5
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-4
- rebuild for new perl

* Wed Nov 14 2007 Robin Norwood <rnorwood@redhat.com> - 1.95.1-3
- Apply fixes from package review:
  - Remove BR: perl
  - Use iconv to convert file to utf-8
  - Include BR: perl(Test::Pod)
  - Fix old changelog entry
- Resolves: bz#226274

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-2
- add BR: perl(version), perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.95.1-1
- bump to 1.95.1
- correct license tag (now under perl license)
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jul 20 2007 Robin Norwood <rnorwood@redhat.com> - 1.94-6.fc8
- Bring fixes from EPEL build into F8
- Fix minor specfile issues
- Package the docs as well

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.94-5.2.1
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.94-5.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.94-5
- #155620
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.94-4
- rebuild

* Tue Feb 17 2004 Chip Turner <cturner@redhat.com> 1.94-2
- fix rm to not be interactive (bz115997)

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.94-1
- update to 1.94

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Sat Jul 20 2002 Chip Turner <cturner@localhost.localdomain>
- remove Text::Balanced modules since they are now in core perl

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Fri Jun 07 2002 cturner@redhat.com
- Specfile autogenerated
