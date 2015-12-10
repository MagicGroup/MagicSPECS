Name:		perl-Readonly
Version:	2.00
Release:	3%{?dist}
Summary:	Facility for creating read-only scalars, arrays, hashes
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Readonly/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SA/SANKO/Readonly-%{version}.tar.gz
Patch0:		Readonly-1.61-interpreter.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(vars)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)
# Speed it up since we can
Requires:	perl(Readonly::XS)

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	perl-Readonly-tests < %{version}-%{release}
Provides:	perl-Readonly-tests = %{version}-%{release}

%description
Readonly provides a facility for creating non-modifiable scalars,
arrays, and hashes. Any attempt to modify a Readonly variable throws
an exception.

Readonly:
* Creates scalars, arrays (not lists), and hashes
* Creates variables that look and work like native perl variables
* Creates global or lexical variables
* Works at run-time or compile-time
* Works with deep or shallow data structures
* Prevents reassignment of Readonly variables

%prep
%setup -q -n Readonly-%{version}

# Fix script interpreter for test suite since we're packaging it
%patch0

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%doc Changes LICENSE README.md eg/benchmark.pl t/
%{perl_vendorlib}/Readonly.pm
%{_mandir}/man3/Readonly.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.00-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.00-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.00-1
- 更新到 2.00

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-23
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-22
- 为 Magic 3.0 重建

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.03-21
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.03-19
- Perl 5.16 rebuild

* Thu Mar  1 2012 Paul Howarth <paul@city-fan.org> - 1.03-18
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- No need to remove empty directories from buildroot
- Add buildreqs for Perl core modules that might be dual-lived
- Fix script interpreter for test suite since we're packaging it
- Drop redundant %%{?perl_default_filter}
- Don't use macros for commands
- Make %%files list more explicit
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.03-16
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-14
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-13
- Mass rebuild with perl-5.12.0

* Sun Feb 21 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-12
- Add perl_default_filter, etc
- Minor spec updates

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.03-11
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-8
- Rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-7
- Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-6.2
- Add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.03-6.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Wed Oct 04 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-6
- Add explict requires on perl(Readonly::XS); perl(Readonly::XS) is available
  for all architectures Fedora supports, so there's no good reason to not
  require it
- Spec file rework

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.03-5
- Bump for mass rebuild

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-4
- Remove requires on perl-Readonly-XS

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-3
- Fix license and BuildRequires, use %%{?_smp_mflags} with make

* Sat Nov 12 2005 Michael A. Peters <mpeters@mac.com> - 1.03-2
- Separate out perl-Readonly-XS into its own package
- Package benchmark.pl as a doc

* Mon Nov 7 2005 Michael A. Peters <mpeters@mac.com> - 1.03-1
- Initial spec file
