Name:           perl-Mouse
Summary:        Moose minus the antlers
Version:        1.11
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Mouse-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Mouse
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Class::Method::Modifiers)
BuildRequires:  perl(Declare::Constraints::Simple)
BuildRequires:  perl(Devel::PPPort) >= 3.19
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Fatal)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(Locale::US)
BuildRequires:  perl(Moose)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Regexp::Common)
BuildRequires:  perl(Scalar::Util) >= 1.14
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::LeakTrace) >= 0.10
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(XSLoader) >= 0.02

Requires:       perl(Scalar::Util) >= 1.14
Requires:       perl(XSLoader) >= 0.02

# virtual provides for perl-Any-Moose
Provides:       perl(Any-Moose) = %{version}

%{?perl_default_filter}
# filter unversioned Mouse::Util provide from Mouse/PurePerl.pm
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Mouse::Util\\)$

%description
Moose, a powerful metaobject-fueled extension of the Perl 5 object system,
is wonderful.  (For more information on Moose, please see 'perldoc Moose'
after installing the perl-Moose package.)

Unfortunately, it's a little slow. Though significant progress has been
made over the years, the compile time penalty is a non-starter for some
applications.  Mouse aims to alleviate this by providing a subset of Moose's
functionality, faster.

%package -n perl-Test-Mouse
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Test functions for Mouse specific features
Requires:   %{name} = %{version}-%{release}

%description -n perl-Test-Mouse
This module provides some useful test functions for Mouse based classes. It is
an experimental first release, so comments and suggestions are very welcome.

%prep
%setup -q -n Mouse-%{version}

find .           -type f -exec chmod -c -x {} +
find t/ xt/ benchmarks/ example/ tool/ -type f -print0 \
| xargs -0 sed -i '1s|^#!.*perl|#!%{__perl}|'

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes benchmarks/ example/ tool/ t/ xt/
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*
%exclude %{perl_vendorarch}/Test
%exclude %{_mandir}/man3/Test::Mouse*

%files -n perl-Test-Mouse
%{perl_vendorarch}/Test
%{_mandir}/man3/Test::Mouse*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Iain Arnell <iarnell@gmail.com> 1.11-1
- update to latest upstream version

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Perl 5.18 rebuild

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.06-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.05-1
- update to latest upstream version
- drop old tests sub-package obsoletes/provides

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Iain Arnell <iarnell@gmail.com> 1.04-1
- update to latest upstream version

* Fri Sep 07 2012 Iain Arnell <iarnell@gmail.com> 1.02-1
- update to latest upstream version

* Sun Aug 26 2012 Iain Arnell <iarnell@gmail.com> 1.01-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 0.99-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.97-4
- Perl 5.16 rebuild

* Wed Apr 18 2012 Iain Arnell <iarnell@gmail.com> 0.97-3
- sub-package Test::Mouse (rhbz#813698)
- drop tests sub-package; move tests to main package documentation
- filter unversioned Mouse::Util from provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Iain Arnell <iarnell@gmail.com> 0.97-1
- update to latest upstream version

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 0.95-1
- update to latest upstream version
- add virtual provides for perl-Any-Moose
- clean up some rpmlint warnings

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.93-3
- Perl mass rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.93-2
- Perl mass rebuild

* Sun Jun 26 2011 Iain Arnell <iarnell@gmail.com> 0.93-1
- update to latest upstream version

* Thu May 12 2011 Iain Arnell <iarnell@gmail.com> 0.92-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- additional BRs for improved test coverage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.58-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.58-2
- bump

* Mon May 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.58-1
- include .proverc in tests subpackage
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.58)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.53-2
- Mass rebuild with perl-5.12.0 & update

* Fri Apr 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.53-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.53)
- altered br on perl(Devel::PPPort) (0 => 3.19)
- altered br on perl(ExtUtils::ParseXS) (0 => 2.21)
- altered br on perl(Test::Exception) (0 => 0.29)
- added a new br on perl(Test::Requires) (version 0.03)
- added manual BR on perl(Class::Method::Modifiers) (or override to 0)
- added manual BR on perl(Test::Deep) (or override to 0)
- added manual BR on perl(Test::Output) (or override to 0)
- added manual BR on perl(Path::Class) (or override to 0)
- added manual BR on perl(IO::File) (or override to 0)
- added manual BR on perl(IO::String) (or override to 0)

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.50-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.47-1
- add perl_default_filter
- we're no longer noarch
- auto-update to 0.47 (by cpan-spec-update 0.01)
- added a new br on perl(Devel::PPPort) 
- added a new br on perl(ExtUtils::ParseXS)
- added a new br on perl(XSLoader) (version 0.1)
- added a new req on perl(Scalar::Util) (version 1.14)
- added a new req on perl(XSLoader) (version 0.1)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-1
- update filtering
- drop our soft-requires (except 1).  Anything using Mouse by this point
  should know to require them if their bits are needed.
- add benchmarks/ to doc
- auto-update to 0.35 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0.21 => 0.27)
- altered br on perl(Test::More) (0.8 => 0.88)

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.28-1
- auto-update to 0.28 (by cpan-spec-update 0.01)

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- auto-update to 0.27 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-1
- auto-update to 0.25 (by cpan-spec-update 0.01)
- altered req on perl(Scalar::Util) (1.19 => 1.14)

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- auto-update to 0.23 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0 => 0.21)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Test::More) (0 => 0.8)

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- update to 0.22

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- update to 0.19

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update to 0.14

* Tue Dec 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13

* Mon Oct 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- bump

* Wed Oct 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09
- add manual requires on the "soft" dependencies

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.06-2
- update description a touch.

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
