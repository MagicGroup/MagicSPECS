Name:           perl-Class-Method-Modifiers
Summary:        Provides Moose-like method modifiers
Version:	2.11
Release:	2%{?dist}
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-Method-Modifiers
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Method-Modifiers-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(if)
BuildRequires:  perl(version)
# Optional Test Requirements
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120900
BuildRequires:  perl(Moose)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(B)
Requires:       perl(Carp)
Requires:       perl(Exporter)

# Avoid doc-file dependencies
%{?perl_default_filter}

%description
Method modifiers are a powerful feature from the CLOS (Common Lisp Object
System) world.

In its most basic form, a method modifier is just a method that calls
'$self->SUPER::foo(@_)'. I for one have trouble remembering that exact
invocation, so my classes seldom re-dispatch to their base classes. Very
bad!

'Class::Method::Modifiers' provides three modifiers: 'before', 'around',
and 'after'. 'before' and 'after' are run just before and after the method
they modify, but can not really affect that original method. 'around' is
run in place of the original method, with a hook to easily call that
original method. See the 'MODIFIERS' section for more details on how the
particular modifiers work.

%prep
%setup -q -n Class-Method-Modifiers-%{version}

# Drop unnecessary exec permissions from test files
chmod -c -x t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::Method::Modifiers.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.11-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.11-1
- 更新到 2.11

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 2.10-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Paul Howarth <paul@city-fan.org> <paul@city-fan.org> - 2.10-1
- Update to 2.10
  - Remove erroneous perl 5.8 requirement
  - Support for handling lvalue methods
  - Convert to building with Dist::Zilla
  - Repository migrated to the github moose organization
  - Refresh configure_requires checking in generated Makefile.PL
  - New CONTRIBUTING file
  - Updated tests:
    - Compile test now only runs for authors
    - Check-deps test replaced by information-only report-prereqs test
- Drop obsoletes/provides for old tests sub-package
- Drop redundant Group tag
- Classify buildreqs by usage
- Make %%files list more explicit

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 2.03-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 2.03-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 05 2013 Iain Arnell <iarnell@gmail.com> 2.00-1
- update to latest upstream version

* Sun Oct 28 2012 Iain Arnell <iarnell@gmail.com> 1.12-1
- update to latest upstream version

* Sat Oct 27 2012 Iain Arnell <iarnell@gmail.com> 1.10-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.09-2
- Perl 5.16 rebuild

* Tue Apr 03 2012 Iain Arnell <iarnell@gmail.com> 1.09-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1.08-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 1.08-2
- rebuilt again for F17 mass rebuild

* Fri Jan 13 2012 Iain Arnell <iarnell@gmail.com> 1.08-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 1.07-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.05-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.04-2
- rebuild against perl 5.10.1

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.04-1
- auto-update to 1.04 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.02-1
- auto-update to 1.02 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.01-3
- remove MM version qualifier (F-8's is older)

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.01-2
- bump

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.01-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
