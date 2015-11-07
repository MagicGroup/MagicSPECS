Name:		perl-Test-Assert
Version:	0.0504
Release:	13%{?dist}
Summary:	Assertion methods for those who like JUnit
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Assert/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DE/DEXTER/Test-Assert-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl(Class::Inspector)
BuildRequires:	perl(constant)
BuildRequires:	perl(constant::boolean) >= 0.02
BuildRequires:	perl(Exception::Base) >= 0.21
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(Symbol::Util) >= 0.0202
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Unit::Lite) >= 0.11
BuildRequires:	perl(warnings)
# Release test requirements
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(Test::CheckChanges)
BuildRequires:	perl(Test::Distribution)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Signature)
BuildRequires:	perl(Test::Spelling), hunspell-en
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Avoid doc-file dependencies
%{?perl_default_filter}

%description
This class provides a set of assertion methods useful for writing tests.
The API is based on JUnit4 and Test::Unit and the methods die on failure.

%prep
%setup -q -c -n Test-Assert

# Copy up documentation for convenience with %%doc
cp -a Test-Assert-%{version}/{Changes,eg,LICENSE,README} .

%build
cd Test-Assert-%{version}
perl Build.PL installdirs=vendor
./Build
cd -

%install
cd Test-Assert-%{version}
./Build install destdir=%{buildroot} create_packlist=0
cd -
%{_fixperms} %{buildroot}

%check
cd Test-Assert-%{version}

# === MAIN TEST SUITE === #

./Build test

# ===  RELEASE TESTS  === #
RELEASE_TESTS="$(echo xt/*.t)"

# Don't run the copyright test as it will fail after the year of module release
RELEASE_TESTS="$(echo $RELEASE_TESTS | sed 's|xt/copyright.t||')"

# Don't run the spelling test yet as we need to add extra stopwords
RELEASE_TESTS="$(echo $RELEASE_TESTS | sed 's|xt/pod_spell.t||')"

# Signature test would fail on recent distros due to presence of MYMETA.*
[ -f MYMETA.yml ] && mv MYMETA.yml ..
[ -f MYMETA.json ] && mv MYMETA.json ..

./Build test --test_files "$RELEASE_TESTS"

# Put any MYMETA.* files back where they were
[ -f ../MYMETA.yml ] && mv ../MYMETA.yml .
[ -f ../MYMETA.json ] && mv ../MYMETA.json .

# Fix the POD Spell test and run it
mv xt/pod_spellrc xt/pod_spellrc.orig
(
	cat xt/pod_spellrc.orig
	echo "'fail'"
	echo "JUnit4"
	echo "value1"
	echo "value2"
) > xt/pod_spellrc
./Build test --test_files xt/pod_spell.t
mv xt/pod_spellrc.orig xt/pod_spellrc

cd -

%files
%doc Changes LICENSE README eg/
%{perl_vendorlib}/Exception/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Exception::Assertion.3pm*
%{_mandir}/man3/Test::Assert.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0504-13
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.0504-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.0504-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.0504-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0504-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0504-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0504-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0504-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0504-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0504-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.0504-3
- Perl 5.16 rebuild

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.0504-2
- Run the release tests too
  - Extract upstream tarball in a subdir to avoid interference with signature/
    manifest tests
  - BR: perl(File::Slurp)
  - BR: perl(Test::CheckChanges)
  - BR: perl(Test::Distribution)
  - BR: perl(Test::Kwalitee)
  - BR: perl(Test::MinimumVersion)
  - BR: perl(Test::Perl::Critic)
  - BR: perl(Test::Pod)
  - BR: perl(Test::Pod::Coverage)
  - BR: perl(Test::Signature)
  - BR: perl(Test::Spelling), hunspell-en

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.0504-1
- Update to 0.0504:
  - Fixed error message for assert_deep_equals
  - Uses Symbol::Util as exported; all exported symbols can be removed with
    "no Test::Assert" statement
  - Minor refactoring of "assert_deep_equals" method and its private methods
  - Require Symbol::Util ≥ 0.0202 and constant::boolean ≥ 0.02
  - Build requires Class::Inspector
  - The ":assert" tag also imports the "ASSERT" constant
- Spec clean-up:
  - Include LICENSE file
  - Include eg/ directory as %%doc
  - Add %%{?perl_default_filter} to avoid doc-file dependencies from examples
  - BR: Perl core modules that might be dual-lived
  - Don't need to remove empty directories from buildroot
  - Make %%files list more explicit
  - Drop %%defattr, redundant since rpm 4.4
  - Drop buildroot definition and cleaning, redundant since rpm 4.6
  - Don't use macros for commands
  - Drop unnecessary dependency filtering
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.0501-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0501-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0501-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.0501-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0501-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> - 0.0501-1
- Initial rpm release
