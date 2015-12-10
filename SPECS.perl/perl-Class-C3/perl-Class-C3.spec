# MRO is part of the Perl core since 5.9.5
%global mro_in_core %(perl -e 'print $] > 5.009005 ? 1 : 0;')

Name:		perl-Class-C3
Version:	0.30
Release:	3%{?dist}
Summary:	Pragma to use the C3 method resolution order algorithm
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Class-C3/
Source0:        http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Class-C3-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Test suite
BuildRequires:	perl(Sub::Name)
BuildRequires:	perl(Test::Exception) >= 0.15
BuildRequires:	perl(Test::More) >= 0.47
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
# MRO::Compat itself requires Class::C3
# The test that uses the module is skipped unless MRO is part of the Perl core
%if 0%{!?perl_bootstrap:1} && %{mro_in_core}
BuildRequires:	perl(MRO::Compat)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Requirements for older distributions with Perl < 5.9.5
%if ! %{mro_in_core}
BuildRequires:	perl(Algorithm::C3) >= 0.06
BuildRequires:	perl(Class::C3::XS) >= 0.07
BuildRequires:	perl(Scalar::Util) >= 1.10
Requires:	perl(Algorithm::C3) >= 0.06
Requires:	perl(Class::C3::XS) >= 0.07
Requires:	perl(Scalar::Util) >= 1.10
%endif

# Let people "use c3;"
Provides:	perl(c3) = %{version}

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	%{name}-tests < %{version}-%{release}
Provides:	%{name}-tests = %{version}-%{release}

# Filter out bogus dependencies and provides (rpm 4.9 onwards)
%global __requires_exclude ^perl\\((c3|base)\\)
%global __provides_exclude ^perl\\(t::lib::

%description
This is a pragma to change Perl 5's standard method resolution order from
depth-first left-to-right (a.k.a - pre-order) to the more sophisticated C3
method resolution order.

%prep
%setup -q -n Class-C3-%{version}

# Filter out bogus dependencies and provides (prior to rpm 4.9)
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Evx 'perl[(](c3|base)[)]'"
%define __perl_requires %{reqfilt}
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(t::lib::'"
%define __perl_provides %{provfilt}

%build
%{?perl_ext_env_unset}
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
cp -p opt/c3.pm %{buildroot}%{perl_vendorlib}/
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/c3.pm
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::C3.3pm*
%{_mandir}/man3/Class::C3::next.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.30-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.30-2
- 更新到 0.30

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.28-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.28-1
- 更新到 0.28

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.23-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.23-6
- 为 Magic 3.0 重建

* Sat Jan 21 2012 Paul Howarth <paul@city-fan.org> - 0.23-5
- Obsolete/provide old -tests subpackage to support upgrades

* Wed Jan 18 2012 Paul Howarth <paul@city-fan.org> - 0.23-4
- Reinstate compatibility with older distributions like EL-5
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- BR: perl(MRO::Compat) for testing if we're not bootstrapping
- Don't use macros for commands
- Make %%files list more explicit
- Filter unwanted requires and provides
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> - 0.23-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- No more need to disable __perl_provides

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-4
- Bump

* Sat May 15 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-3
- Install c3.pm as well; drop opt/ from doc
- Conditionalise

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-2
- Mass rebuild with perl-5.12.0

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.22-1
- PERL_INSTALL_ROOT => DESTDIR
- Add perl_default_subpackage_tests, and drop t/ from doc
- Add perl_default_filter (and update filtering)
- Auto-update to 0.22 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Added a new br on perl(Scalar::Util) (version 1.10)
- Altered br on perl(Test::More) (0 => 0.47)
- Added a new req on perl(Scalar::Util) (version 1.10)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.21-3
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.21-1
- Update to 0.21

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.20-1
- Update to 0.20

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-2
- Rebuild for new perl

* Wed Oct 10 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.19-1
- Update to 0.19

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.18-1
- Update to 0.18

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.17-1
- Update to 0.17
- BR Class::C3::XS

* Mon Sep 25 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.14-1
- Update to 0.14

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-4
- Fix autoprovides (#205801)

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-3
- Bump

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-2
- Additional br's, minor spec tweaks

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.13-1
- Specfile autogenerated by cpanspec 1.69.1
