# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

# With perl 5.8.9-5.12, we need Sub::Identify and Sub::Name
%global fixup_rename_sub %(perl -e 'print (($] > 5.008_008_9 && $] < 5.013_006_1) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-namespace-clean
Summary:	Keep your namespace tidy
Version:	0.23
Release:	4%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/namespace-clean/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/namespace-clean-%{version}.tar.gz
Patch1:		namespace-clean-0.22-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(B::Hooks::EndOfScope) >= 0.10
BuildRequires:	perl(constant)
BuildRequires:	perl(Devel::Hide)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(Package::Stash) >= 0.23
BuildRequires:	perl(Test::More)
BuildRequires:	perl(vars)
%if %{fixup_rename_sub}
BuildRequires:	perl(Sub::Identify) >= 0.04
BuildRequires:	perl(Sub::Name) >= 0.04
Requires:	perl(Sub::Identify) >= 0.04
Requires:	perl(Sub::Name) >= 0.04
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(B::Hooks::EndOfScope) >= 0.10

# Obsolete/Provide old tests subpackage
# Can be removed during F19 development cycle
%if 0%{?perl_default_filter:1}
Obsoletes:	%{name}-tests < 0.21-3
Provides:	%{name}-tests = %{version}-%{release}
# Avoid unwanted requires/provides that come with the test suite
%{perl_default_filter}
%endif

%description
When you define a function, or import one, into a Perl package, it will
naturally also be available as a method. This does not per se cause
problems, but it can complicate subclassing and, for example, plugin
classes that are included via multiple inheritance by loading them as
base classes.

The 'namespace::clean' pragma will remove all previously declared or
imported symbols at the end of the current package's compile cycle.
Functions called in the package itself will still be bound by their
name, but they won't show up as methods on your class or instances.

%prep
%setup -q -n namespace-clean-%{version}

# Patch test suite to work with Test::More < 0.88 if necessary
%if %{old_test_more}
%patch1 -p1
%endif

# The module doesn't try to use Hash::Util::FieldHash with 5.8.x
%if %(perl -e 'print (($] < 5.009_003_1) ? 1 : 0);')
%global perl_reqfilt /bin/sh -c "%{__perl_requires} | sed -e '/^perl(Hash::Util::FieldHash)/d'"
%define __perl_requires %{perl_reqfilt}
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes %{?perl_default_filter:t/}
%{perl_vendorlib}/namespace/
%{_mandir}/man3/namespace::clean.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.23-2
- Perl 5.16 rebuild

* Sun Mar 11 2012 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Rely on B::Hooks::EndOfScope version 0.10 to fix issues with new
    Module::Runtime versions (≥ 0.012) on perl 5.10 due to incorrect hook
    firing due to %^H localisation
  - Fix failures on 5.13.6 due to incorrect version number threshold
    (CPAN RT#74683)
- Don't need to remove empty directories from buildroot
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 27 2012 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Limit the debugger workarounds to perls between 5.8.8 and 5.14, extend
    debugger support to all perl versions (CPAN RT#69862)
  - If possible, automatically install (but not load) the debugger workaround
    libraries on perls between 5.8.8 and 5.14 (CPAN RT#72368)
  - Add back dropped NAME section (CPAN RT#70259)
  - Simplify the ≥ 5.10 PP variant even more - move the hook from DESTROY
    into DELETE
  - Force explicit callback invocation order on 5.8 PP
  - Replace the %^H tie approach with fieldhashes, which fixes all known
    corner cases and caveats on supported perls ≥ 5.8.1 (CPAN RT#73402)
  - Compile away the debugger fixup on perls ≥ 5.15.5
- Only BR:/R: Sub::Identify and Sub::Name for perl versions where they're
  actually needed
- Reinstate compatibility with old distributions like EL-5
  - Patch test suite to work with Test::More < 0.88 if necessary
  - Filter dependency on Hash::Util::FieldHash on perl 5.8.x
  - Add back buildroot definition, %%clean section, %%defattr etc.
- Only include tests if we have %%{perl_default_filter} to avoid the unwanted
  requires/provides that come with them
- Drop redundant buildreq perl(CPAN)
- Make %%files list more explicit
- Use tabs

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> - 0.21-3
- Drop tests subpackage; move tests to main package documentation

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 0.21-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.20-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> - 0.20-1
- Update to latest upstream version
- Update BR perl(Package::Stash) >= 0.22

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun Aug 01 2010 Iain Arnell <iarnell@gmail.com> - 0.18-1
- Update by Fedora::App::MaintainerTools 0.006
- Updating to latest GA CPAN version (0.18)
- Added a new br on perl(Exporter) (version 0)
- Altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- Added a new br on perl(Package::Stash) (version 0.03)
- Added a new br on perl(constant) (version 0)
- Added a new br on perl(vars) (version 0)
- Dropped old BR on perl(Symbol)
- Dropped old requires on perl(Symbol)
- Manually drop unnecessary requires

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-1
- Mass rebuild with perl-5.12.0 & update

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-2
- Update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-1
- Update filtering perl_default_filter
- Auto-update to 0.13 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Added a new br on perl(Sub::Identify) (version 0.04)
- Added a new br on perl(Sub::Name) (version 0.04)
- Altered br on perl(Test::More) (0.62 => 0.88)
- Added a new br on CPAN (inc::Module::AutoInstall found)
- Added a new req on perl(B::Hooks::EndOfScope) (version 0.07)
- Added a new req on perl(Sub::Identify) (version 0.04)
- Added a new req on perl(Sub::Name) (version 0.04)
- Added a new req on perl(Symbol) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11-1
- Update to 0.11

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.09-1
- Update to 0.09
- Note BR change from Scope::Guard to B::Hooks::EndOfScope

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-2
- Bump

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.08-1
- Initial Fedora packaging
- Generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
