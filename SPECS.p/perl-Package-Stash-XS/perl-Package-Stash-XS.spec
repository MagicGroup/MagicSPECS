Name:		perl-Package-Stash-XS
Version:	0.25
Release:	8%{?dist}
Summary:	Faster and more correct implementation of the Package::Stash API
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Package-Stash-XS/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Package-Stash-XS-%{version}.tar.gz
Patch1:		Package-Stash-XS-0.24-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl >= 3:5.8.1
BuildRequires:	perl(constant)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(lib)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Fatal)
%if ! (0%{?rhel} >= 7)
BuildRequires:	perl(Test::LeakTrace)
%endif
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(XSLoader)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This is a back-end for Package::Stash, which provides the functionality in a
way that's less buggy and much faster. It will be used by default if it's
installed, and should be preferred in all environments with a compiler.

%prep
%setup -q -n Package-Stash-XS-%{version}

# Patch test suite to work with old Test::More versions if necessary
%if "%{?rhel}" == "5"
%patch1 -p1
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
%if ! (0%{?rhel} >= 7)
 AUTHOR_TESTING=1 RELEASE_TESTING=1
%else
 RELEASE_TESTING=1
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorarch}/auto/Package/
%{perl_vendorarch}/Package/
%{_mandir}/man3/Package::Stash::XS.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.25-8
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Petr Pisar <ppisar@redhat.com> - 0.25-7
- Disable author tests on RHEL >= 7

* Sat Aug 25 2012 Paul Howarth <paul@city-fan.org> - 0.25-6
- Drop EPEL-4 support
  - Test::LeakTrace now universally available
  - Suitably recent version of ExtUtils::MakeMaker now universally available
  - Drop %%defattr, redundant since rpm 4.4
- BR: perl(File::Temp)
- Don't need to remove empty directories from the buildroot

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.25-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.25-3
- Perl 5.16 rebuild

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.25-2
- Use %%{_fixperms} macro instead of our own chmod incantation

* Tue Sep  6 2011 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Invalid package names (for instance, Foo:Bar) are not allowed
  - Invalid stash entry names (anything containing ::) are not allowed
- Update patches to apply cleanly

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Fix the test for scalar values, again
  - Disallow assigning globrefs to scalar glob slots (this doesn't actually
    make any sense)
- Update patches for old ExtUtils::MakeMaker and Test::More versions
- perl(Pod::Coverage::TrustPod) now available in EPEL-4 too
- Don't use macros for commands

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.22-2
- Perl mass rebuild

* Sat Mar  5 2011 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Make the namespace cache lazy and weak, in case the stash is deleted
  - However, this doesn't work on 5.8, so disable the namespace caching
    entirely there
- Update patches to apply cleanly

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Make the leak tests author-only, since some smokers run release tests
  - Fix some XS forward compat stuff
- Update patches to apply cleanly

* Wed Jan 12 2011 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Lower perl prereq to 5.8.1
  - Make the leak tests release-only
- Update patches to apply cleanly
- Drop no-Test::Requires patch, no longer needed
- Drop buildreq perl(Test::Requires), no longer needed
- Add patch to skip memory leak tests if we don't have Test::LeakTrace

* Thu Jan  6 2011 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19 (more correct validity test for scalars)
- Update patch for old Test::More versions

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.17-2
- Sanitize spec for Fedora submission

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.17-1
- Initial RPM build
