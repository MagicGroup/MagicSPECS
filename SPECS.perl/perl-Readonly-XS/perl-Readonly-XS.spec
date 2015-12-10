Name:		perl-Readonly-XS
Version:	1.05
Release:	18%{?dist}
Summary:	Companion module for Readonly
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Readonly-XS/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RO/ROODE/Readonly-XS-%{version}.tar.gz
Patch0:		Readonly-XS-1.05-prereq.patch
Patch1:		Readonly-XS-1.05-interpreter.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test suite
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
Requires:	perl(Readonly) >= 1.02

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	perl-Readonly-XS-tests < %{version}-%{release}
Provides:	perl-Readonly-XS-tests = %{version}-%{release}

# Don't provide the private XS.so() lib
%{?perl_default_filter}

%description
Readonly::XS is a companion module for Readonly, to speed up read-only
scalar variables.

%prep
%setup -q -n Readonly-XS-%{version}

# Build process does not actually need perl(Readonly)
%patch0

# Fix script interpreter for test suite since we're packaging it
%patch1

# Avoid doc-file dependencies from tests if we don't have %%perl_default_filter
%global perl_reqfilt /bin/sh -c "%{__perl_requires} | grep -Fvx 'perl(Test::More)'"
%define __perl_requires %{perl_reqfilt}

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


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes t/
%{perl_vendorarch}/auto/Readonly/
%{perl_vendorarch}/Readonly/
%{_mandir}/man3/Readonly::XS.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.05-18
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.05-17
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.05-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.05-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.05-14
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.05-13
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.05-11
- Perl 5.16 rebuild

* Thu Mar  1 2012 Paul Howarth <paul@city-fan.org> - 1.05-10
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Don't use macros for commands
- No need to remove empty directories from buildroot
- Add buildreqs for Perl core modules that might be dual-lived
- Rename makefile patch to include module name and version
- Fix script interpreter for test suite since we're packaging it
- Add filter for doc-file dependencies if we don't have %%perl_default_filter
- Make %%files list more explicit
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.05-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-5
- Mass rebuild with perl-5.12.0

* Sun Feb 21 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.05-4
- Add perl_default_filter, etc
- PERL_INSTALL_ROOT => DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.05-1
- Update to 1.05
- Filter our provides to prevent private lib from showing up
- Drop patch1; incorporated upstream as of 1.05

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-11
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.04-10.2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-9.2
- Patch Carp::croak call for new perl

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-9
- Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-8.2
- Add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-8.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-8
- Bump

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-7
- Bump for missing patch...

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-6
- Drop br on perl(Readonly), patch Makefile.PL as well
- Rework spec to use macros

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.04-5
- Rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.04-4
- Bump for mass rebuild

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-3
- Proper version on perl(Readonly) BuildRequires & Requires

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-1
- New Version
- BuildRequires perl(Readonly), remove explicit requires on
  perl-Readonly version

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-2
- Fix license and BuildRequires

* Sat Nov 12 2005 Michael A. Peters <mpeters@mac.com> - 1.03-1
- Created spec file
