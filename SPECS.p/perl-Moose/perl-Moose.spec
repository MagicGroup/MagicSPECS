Name:           perl-Moose
Summary:        Complete modern object system for Perl 5
Version:        2.0604
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Moose-%{version}.tar.gz
URL:            http://search.cpan.org/dist/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Class::MOP is now included in Moose itself
Obsoletes:      perl-Class-MOP <= 1.12-2.fc15
Obsoletes:      perl-Class-MOP-tests <= 1.12-2.fc15

# configure
BuildRequires:  perl(Dist::CheckConflicts) >= 0.02
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30

# develop
BuildRequires:  perl(Algorithm::C3)
BuildRequires:  perl(DBM::Deep) >= 1.0003
%if !0%{?perl_bootstrap}
BuildRequires:  perl(Data::Visitor)
%endif
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Calendar::Mayan)
BuildRequires:  perl(DateTime::Format::MySQL)
BuildRequires:  perl(Declare::Constraints::Simple)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(Locale::US)
BuildRequires:  perl(Module::Info)
BuildRequires:  perl(Module::Refresh)
BuildRequires:  perl(PadWalker)
BuildRequires:  perl(Params::Coerce)
BuildRequires:  perl(Regexp::Common)
BuildRequires:  perl(Test::Deep)
# author test - we almost certainly don't want this in mock!
#BuildRequires:  perl(Test::DependentModules) >= 0.12
BuildRequires:  perl(Test::Inline)
BuildRequires:  perl(Test::LeakTrace)
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(Test::Spelling)
BuildRequires:  perl(URI)
# not decalared in META.json
BuildRequires:  perl(Carp) >= 1.22
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(SUPER) >= 1.10

# test
BuildRequires:  perl(Test::Fatal) >= 0.001
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires) >= 0.05

# runtime
BuildRequires:  perl(Class::Load) >= 0.09
BuildRequires:  perl(Class::Load::XS) >= 0.01
BuildRequires:  perl(Data::OptList) >= 0.107
BuildRequires:  perl(Devel::GlobalDestruction)
BuildRequires:  perl(Eval::Closure) >= 0.04
BuildRequires:  perl(List::MoreUtils) >= 0.28
BuildRequires:  perl(MRO::Compat) >= 0.05
BuildRequires:  perl(Package::DeprecationManager) >= 0.11
BuildRequires:  perl(Package::Stash) >= 0.32
BuildRequires:  perl(Package::Stash::XS) >= 0.24
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(Scalar::Util) >= 1.19
BuildRequires:  perl(Sub::Exporter) >= 0.980
BuildRequires:  perl(Sub::Name) >= 0.05
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Try::Tiny) >= 0.02


Requires:       perl(Data::OptList) >= 0.107
Requires:       perl(Dist::CheckConflicts) >= 0.02

# recommended (note: this uses Moose itself)
Requires:       perl(Devel::PartialDump) >= 0.14

# hidden from PAUSE
Provides:       perl(Moose::Conflicts)
Provides:       perl(Moose::Error::Util)

# virtual provides for perl-Any-Moose
Provides:       perl(Any-Moose) = %{version}

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 2.0401-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Moose is an extension of the Perl 5 object system.

The main goal of Moose is to make Perl 5 Object Oriented programming easier,
more consistent and less tedious. With Moose you can to think more about what
you want to do and less about the mechanics of OOP.

Additionally, Moose is built on top of Class::MOP, which is a metaclass system
for Perl 5. This means that Moose not only makes building normal Perl 5
objects better, but it provides the power of metaclass programming as well.
Moose is different from other Perl 5 object systems because it is not a new
system, but instead an extension of the existing one.

%package -n perl-Test-Moose
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Test functions for Moose specific features
Requires:   %{name} = %{version}-%{release}

%description -n perl-Test-Moose
This module provides some useful test functions for Moose based classes.
It is an experimental first release, so comments and suggestions are
very welcome.

%prep
%setup -q -n Moose-%{version}

# silence rpmlint warnings
find benchmarks/ -type f -name '*.pl' -print0 \
  | xargs -0 sed -i '1s,#!.*perl,#!%{__perl},'
find t/ -type f -name '*.t' -print0 \
  | xargs -0 sed -i '1s,#!.*perl,#!%{__perl},'

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check



%files
%doc Changes Changes.Class-MOP LICENSE README TODO doap.rdf
%doc t/ benchmarks/
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*
%{_bindir}/moose-outdated
%exclude %{perl_vendorarch}/Test
%exclude %{_mandir}/man3/Test::Moose*

%files -n perl-Test-Moose
%{perl_vendorarch}/Test
%{_mandir}/man3/Test::Moose*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.0604-3
- 为 Magic 3.0 重建

* Tue Oct 23 2012 Liu Di <liudidi@gmail.com> - 2.0604-2
- 为 Magic 3.0 重建

* Fri Oct 19 2012 Iain Arnell <iarnell@gmail.com> 2.0604-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 2.0603-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0602-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0602-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 2.0602-2
- Perl 5.16 rebuild

* Mon May 07 2012 Iain Arnell <iarnell@gmail.com> 2.0602-1
- update to latest upstream version

* Fri Apr 06 2012 Iain Arnell <iarnell@gmail.com> 2.0402-2
- avoid circular build-dependencies with Data::Visitor and Devel::Partialdump
  (patch from Paul Howarth rhbz#810394)

* Sun Feb 05 2012 Iain Arnell <iarnell@gmail.com> 2.0402-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.0401-2
- drop tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 2.0401-1
- update to latest upstream version

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 2.0205-2
- add virtual provides for perl-Any-Moose

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 2.0205-1
- update to latest upstream version

* Tue Sep 13 2011 Petr Pisar <ppisar@redhat.com> - 2.0204-2
- Build-require Carp because Carp dual-lives now (bug #736768)

* Sun Aug 28 2011 Iain Arnell <iarnell@gmail.com> 2.0204-1
- update to latest upstream version
- additional build/test dependencies for more testing

* Sat Jul 30 2011 Iain Arnell <iarnell@gmail.com> 2.0202-1
- update to latest upstream version

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.0010-2
- Perl mass rebuild

* Sat Jun 25 2011 Iain Arnell <iarnell@gmail.com> 2.0010-1
- update to latest upstream version

* Fri May 20 2011 Iain Arnell <iarnell@gmail.com> 2.0007-1
- update to latest upstream version

* Tue May 03 2011 Iain Arnell <iarnell@gmail.com> 2.0002-2
- drop unnecessary BR perl(Devel::PartialDump)

* Tue May 03 2011 Iain Arnell <iarnell@gmail.com> 2.0002-1
- update to latest upstream version

* Tue Apr 26 2011 Iain Arnell <iarnell@gmail.com> 2.0001-3
- add explicit perl(Dist::CheckConflicts) requirement

* Sat Apr 23 2011 Iain Arnell <iarnell@gmail.com> 2.0001-2
- obsolete perl-Class-MOP-tests too

* Sat Apr 23 2011 Iain Arnell <iarnell@gmail.com> 2.0001-1
- update to latest upstream version

* Fri Apr 22 2011 Iain Arnell <iarnell@gmail.com> 2.00-1
- update to latest upstream version
- regenerate BuildRequires from META.json
- obsoletes perl-Class-MOP (now incluced in Moose itself)
- clean up spec for modern rpmbuild

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 1.25-1
- update to latest upstream version

* Sat Mar 05 2011 Iain Arnell <iarnell@gmail.com> 1.24-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 1.23-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Iain Arnell <iarnell@gmail.com> 1.21-1
- update to latest upstream version
- update R/BR perl(Class::MOP) >= 1.11
- update R/BR perl(Params::Util) >= 1.00
- update R/BR perl(Package::DeprecationManager) >= 0.10
- new BR perl(Test::Fatal) >= 0.001
- drop old BR perl(Test::Exception)

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 1.15-1
- update to latest upstream version
- update BR perl(Class::MOP) >= 1.09
- new BR perl(Params:Util)

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> 1.14-1
- update to latest upstream version
- update BR perl(Class:MOP) >= 1.05
- new BR perl(Test::Requires) >= 0.05
- new R/BR perl(Package::DeprecationManager) >= 0.04

* Sat Jul 03 2010 Iain Arnell <iarnell@gmail.com> 1.08-1
- update to latest upstream
- update BR perl(Class:MOP) >= 1.02

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-1
- update

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02-1
- Mass rebuild with perl-5.12.0
- switch off tests for meantime, needs Class::ISA

* Fri Apr 30 2010 Marclea Mašláňová <mmaslano@redhat.com> 1.01-1
- update

* Fri Mar 12 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.99-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.99)

* Sat Feb 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.98-1
- update by Fedora::App::MaintainerTools 0.003

* Sat Feb 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.96-1
- auto-update by cpan-spec-update 0.002
- dropped old BR on perl(UNIVERSAL::require)
- dropped old BR on perl(Sub::Install)
- dropped old BR on perl(Test::LongString)
- dropped old BR on perl(Filter::Simple)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.94-3
- PERL_INSTALL_ROOT => DESTDIR
- add perl_default_subpackage_tests
- properly exclude vendorarch/auto/ directory
- add br on DateTime::Calendar::Mayan

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.94-2
- we're not noarch anymore :)

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.94-1
- auto-update to 0.94 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.94 => 0.98)
- altered req on perl(Class::MOP) (0.94 => 0.98)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.92-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.92-1
- auto-update to 0.92 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.93 => 0.94)
- altered req on perl(Class::MOP) (0.93 => 0.94)

* Fri Sep 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.90-1
- switch filtering systems...
- auto-update to 0.90 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.92 => 0.93)
- altered br on perl(Test::More) (0.77 => 0.88)
- added a new br on perl(Try::Tiny) (version 0.02)
- altered req on perl(Class::MOP) (0.92 => 0.93)
- added a new req on perl(Try::Tiny) (version 0.02)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.89-1
- auto-update to 0.89 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.89 => 0.92)
- altered req on perl(Class::MOP) (0.89 => 0.92)

* Mon Jul 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.88-1
- auto-update to 0.88 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.85 => 0.89)
- altered br on perl(Sub::Exporter) (0.972 => 0.980)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Class::MOP) (version 0.89)
- added a new req on perl(Data::OptList) (version 0)
- added a new req on perl(List::MoreUtils) (version 0.12)
- added a new req on perl(Scalar::Util) (version 1.19)
- added a new req on perl(Sub::Exporter) (version 0.980)
- added a new req on perl(Sub::Name) (version 0)
- added a new req on perl(Task::Weaken) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.81-2
- split off Test::Moose

* Tue Jun 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.81-1
- auto-update to 0.81 (by cpan-spec-update 0.01)
- altered br on perl(Class::MOP) (0.83 => 0.85)

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.80-1
- auto-update to 0.80 (by cpan-spec-update 0.01)

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.79-1
- auto-update to 0.79 (by cpan-spec-update 0.01)

* Wed May 13 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.78-1
- auto-update to 0.78 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0.21 => 0.27)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Sub::Name) (version 0)
- altered br on perl(Class::MOP) (0.81 => 0.83)
- altered br on perl(Sub::Exporter) (0.954 => 0.972)
- added a new br on perl(Carp) (version 0)

* Mon May 04 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.74-2
- switch filtering to a cleaner system

* Sat Apr 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.74-1
- update to 0.74

* Wed Apr 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.73-1
- update to 0.73

* Sun Mar 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.72-1
- update to 0.72

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.71-1
- update to 0.71

* Sun Jan 04 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.64-1
- update to 0.64

* Sun Dec 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.63-1
- update to 0.63
- bump br versions on Moose, List::MoreUtils

* Sat Dec 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.62-1
- update to 0.62
- new Task::Weaken and Class::MOP requirements

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.61-4
- aaaand drop them again, as it was really perl-Class-MOP's issue.

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.61-3
- same with Devel::GlobalDestruction (same RT as below)

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.61-2
- add Sub::Name as a build dep (RT#40772)

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.61-1
- update to 0.61
- update BR's

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.57-2
- add additional test BR's

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.57-1
- update to 0.57

* Fri Jul 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.54-1
- update to 0.54

* Sat Jun 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.51-1
- update to 0.51

* Tue Jun 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.50-1
- update to 0.50
- drop obviated test patch

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.44-2
- bump

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.44-1
- update to 0.44

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.33-3
- rebuild for new perl

* Mon Jan 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.33-2
- remove *.orig files from t/ (BZ#427754)

* Sat Dec 15 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.33-1
- update to 0.33

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.32-1
- update to 0.32

* Sun Nov 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.30-1
- update to 0.30

* Sat Nov 17 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- update to 0.29
- refactor to Module::Install

* Sun Oct 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.26-1
- udpate to 0.26

* Sat Aug 11 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.24-1
- update to 0.24
- license tag: GPL -> GPL+
- patch t/202_...t to write to a tmpdir rather than .

* Thu May 31 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- update to 0.22

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- update to 0.21

* Tue May 01 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.20-2
- add t/ to %%doc
- add br for optional test #7

* Sat Apr 07 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- update to 0.20
- add additional BR's for new optional tests

* Fri Mar 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- Sub::Name only needed as a br for Moose < 0.18
- update to 0.18

* Thu Nov 16 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.17-2
- add IO::File and IO::String to br's for testing

* Thu Nov 16 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17

* Mon Nov 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- update to 0.15

* Tue Oct 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update to 0.14
- drop some cruft from the specfile
- make %%description a touch more verbose :)

* Tue Oct 03 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13

* Fri Sep 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.12-2
- bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- Specfile autogenerated by cpanspec 1.69.1.
