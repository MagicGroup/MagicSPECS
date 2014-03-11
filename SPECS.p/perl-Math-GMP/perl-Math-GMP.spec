Summary:	High speed arbitrary size integer math
Name:		perl-Math-GMP
Version:	2.06
Release:	11%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Math-GMP/
Source0:	http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/Math-GMP-%{version}.tar.gz
Source1:	14964AC8.asc
Source2:	161C06B1.asc
Patch0:		Math-GMP-2.06-stopwords.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	gmp-devel
BuildRequires:	perl(AutoLoader)
BuildRequires:	perl(Carp)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Comments)
BuildRequires:	perl(Module::Signature)
BuildRequires:	perl(Pod::Spell)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::YAML::Meta)
BuildRequires:	perl(Text::SpellChecker)
BuildRequires:	perl(YAML)
BuildRequires:	hunspell-en
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Critic and Pod Coverage tests fail, so make sure we don't try to run them for now
BuildConflicts:	perl(Perl::Critic)
BuildConflicts:	perl(Test::Pod::Coverage)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
Math::GMP was designed to be a drop-in replacement both for Math::BigInt and
for regular integer arithmetic. Unlike BigInt, though, Math::GMP uses the GNU
gmp library for all of its calculations, as opposed to straight Perl functions.
This can result in speed improvements.

%prep
# Do the build in a subdirectory so that the debug files list doesn't interfere
# with the signature test
%setup -q -c -n Math-GMP

# Additional words for spell checker to ignore
cd Math-GMP-%{version}
%patch0 -p2
cd -

# Link docs back to top level for %%doc
ln Math-GMP-%{version}/{README,Changes,LICENSE} .

# Create a GPG directory for testing, to avoid using ~/.gnupg
mkdir --mode=0700 gnupghome
export GNUPGHOME=$(pwd)/gnupghome
gpg --import %{SOURCE1} %{SOURCE2}

%build
cd Math-GMP-%{version}
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}
cd -

%install
rm -rf %{buildroot}
make -C Math-GMP-%{version} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
export GNUPGHOME=$(pwd)/gnupghome
cd Math-GMP-%{version}

# Signature test would fail on recent distros due to presence of MYMETA.yml
[ -f MYMETA.yml ] && mv MYMETA.yml ..

# Locale set to en_US for spell check tests
LANG=en_US  RELEASE_TESTING=1

# Restore MYMETA.yml if necessary
[ -f ../MYMETA.yml ] && mv ../MYMETA.yml .

cd -

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes LICENSE
%{perl_vendorarch}/Math/
%{perl_vendorarch}/auto/Math/
%{_mandir}/man3/Math::GMP.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.06-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.06-10
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> 2.06-9
- Use %%{_fixperms} macro rather than our own chmod incantation
- Add buildreqs for perl core modules, which might be dual-lived
- Don't run tests in VERBOSE mode anymore

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> 2.06-8.1
- Rebuild with new gmp

* Wed Jul 20 2011 Paul Howarth <paul@city-fan.org> 2.06-8
- Perl mass rebuild
- Work around MYMETA.yml causing signature test to fail
- Use LANG rather than LC_ALL to set locale for spell check test
- Nobody else likes macros for commands

* Wed Feb  9 2011 Paul Howarth <paul@city-fan.org> 2.06-7
- Fix spell check test to add words not in hunspell dictionary

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct  4 2010 Paul Howarth <paul@city-fan.org> 2.06-5
- Change BR: aspell-en to hunspell-en now that Text::SpellChecker uses a
  hunspell back-end

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> 2.06-4
- Don't clobber ~/.gnupg

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> 2.06-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 2.06-2
- Rebuild against perl 5.10.1

* Fri Sep 18 2009 Paul Howarth <paul@city-fan.org> 2.06-1
- Update to 2.06
  - Make Makefile.PL more forgiving of gmp library locations (CPAN RT#46323)
  - Update link to libgmp.org in INSTALL file (CPAN RT#46324)
- Use %%{?perl_default_filter}
- RELEASE_TESTING variable obsoletes TEST_{AUTHOR,CRITIC,SIGNATURE,SPELL}
- BuildConflict Test::Critic and Test::Pod::Coverage to avoid failing tests

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar  7 2009 Paul Howarth <paul@city-fan.org> 2.05-4
- Filter out unwanted provides for perl shared objects
- Do the build in a subdirectory so that the debug files list doesn't interfere
  with the signature test
- Enable the signature test
- Run the tests in the en_US locale - spell check tests now pass
- Add buildreq perl(YAML) to enable the YAML tests

* Thu Feb 26 2009 Paul Howarth <paul@city-fan.org> 2.05-3
- Add buildreq aspell-en as it's not pulled in by aspell after Fedora 10
- Add buildreq perl(File::Comments) to support spellchecking of comments
- Disable spellcheck tests as they fail anyway

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct  7 2008 Paul Howarth <paul@city-fan.org> 2.05-1
- New upstream maintainer, new upstream version 2.05
- 64-bit test suite compatibility issues fixed upstream, patch removed
- Run tests in verbose mode
- Add buildreq perl(Test::More) for basic test suite
- Add buildreqs perl(Module::Signature), perl(Perl::Critic), perl(Pod::Spell),
  perl(Test::Pod), perl(Test::YAML::Meta), and perl(Text::SpellChecker) for
  additional test suite functionality

* Fri Jun  6 2008 Paul Howarth <paul@city-fan.org> 2.04-10
- Apply 64-bit testsuite-fixing patch on sparc64 too

* Tue Mar 25 2008 Paul Howarth <paul@city-fan.org> 2.04-9
- Apply 64-bit testsuite-fixing patch on ia64 too (#436649)

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.04-8
- Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 2.04-7
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 2.04-6
- Clarify license as LGPL, version 2 or later

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.04-5
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 2.04-4
- FE6 mass rebuild

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 2.04-3
- Rebuild

* Tue Feb  7 2006 Paul Howarth <paul@city-fan.org> 2.04-2
- Apply patch to fix broken testsuite on 64-bit arches (CPAN RT#12751)

* Tue Nov 29 2005 Paul Howarth <paul@city-fan.org> 2.04-1
- Initial build
