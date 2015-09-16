Name:		perl-SUPER
Version:	1.20141117
Release:	1%{?dist}
Summary:	Sane superclass method dispatcher
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/SUPER/
Source0:	http://search.cpan.org/CPAN/authors/id/C/CH/CHROMATIC/SUPER-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# =============== Module Build =================
BuildRequires:	perl(Module::Build)
# =============== Module Runtime ===============
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Scalar::Util) >= 1.20
BuildRequires:	perl(Sub::Identify) >= 0.03
# =============== Test Suite ===================
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(Test::More)
# =============== Module Runtime ===============
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Scalar::Util) >= 1.20
Requires:	perl(Sub::Identify) >= 0.03

%description
When subclassing a class, you occasionally want to dispatch control to the
superclass - at least conditionally and temporarily. This module provides
an easier, cleaner way for class methods to access their ancestor's
implementation.

%prep
%setup -q -n SUPER-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/SUPER.pm
%{_mandir}/man3/SUPER.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.20141117-1
- 更新到 1.20141117

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.20120705-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.20120705-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.20120705-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20120705-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20120705-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20120705-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.20120705-3
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Paul Howarth <paul@city-fan.org> - 1.20120705-1
- Update to 1.20120705
  - Resolved PAUSE packaging nit (CPAN RT#77110)
  - Converted to dzil
- Drop provides filter, not needed due to fix for CPAN RT#77110
- Classify buildreqs by what they are required for
- BR: perl(Test::Builder::Module) rather than perl(Test::Simple) ≥ 0.61
- BR: perl(base), perl(lib) and perl(Test::More)

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.17-8
- Perl 5.16 rebuild

* Tue Mar  6 2012 Paul Howarth <paul@city-fan.org> - 1.17-7
- Add provides filters that work with all supported distributions
- BR: perl(Carp) and perl(Exporter)
- Make %%files list more explicit
- Drop explicit requires of perl(Exporter) since it's auto-detected by rpm
  4.9 onwards, and is bundled with perl on all older distributions
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- %%defattr redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.17-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.17-2
- Mass rebuild with perl-5.12.0

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.17-1
- Update filtering
- Auto-update to 1.17 (by cpan-spec-update 0.01)
- Added a new br on perl(Scalar::Util) (version 1.20)
- Altered br on perl(Sub::Identify) (0 => 0.03)
- Altered br on perl(Test::Simple) (0 => 0.61)
- Added a new req on perl(Scalar::Util) (version 1.20)
- Added a new req on perl(Sub::Identify) (version 0.03)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-3
- Rebuild for new perl

* Wed Jan 02 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-2
- Adjust License-tag
- BR: perl(Test::Simple) (BZ 419631)

* Wed Apr 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 1.16-1
- Update to 1.16

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.15-1
- Update to 1.15
- Add explict requires on perl(Exporter); missed due to a use base construct

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-4
- Bump

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-3
- Update %%description and %%summary

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-2
- Filter errant perl(DB) provide

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 1.14-1
- Specfile autogenerated by cpanspec 1.69.1
