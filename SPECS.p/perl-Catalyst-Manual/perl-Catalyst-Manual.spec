Name:           perl-Catalyst-Manual
Summary:        Catalyst web framework manual
Epoch:          1
Version:        5.9002
Release:        5%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/H/HK/HKCLARK/Catalyst-Manual-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Manual/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 1:5.9002-3
Provides:       %{name}-tests = %{epoch}:%{version}-%{release}

%{?perl_default_filter}

%description
This is the manual to the Catalyst web framework.

%prep
%setup -q -n Catalyst-Manual-%{version}

#remove extraneous .gitignore
find -name .gitignore -print0 | xargs -0 rm -f

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:5.9002-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1:5.9002-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1:5.9002-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.9002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 1:5.9002-1
- update to latest upstream version

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:5.8005-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.8005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Iain Arnell <iarnell@gmail.com> 1:5.8005-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:5.8004-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:5.8004-3
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:5.8004-2
- rebuild so -tests correctly uses epoch in versioned dep

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:5.8004-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)

* Thu Jan 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 1:5.8003-1
- auto-update to 5.8003 (by cpan-spec-update 0.01)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:5.8002-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 1:5.8002-1
- auto-update to 5.8002 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.8000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.8000-2
- add br on CPAN until bundled M::I is installed

* Sun May 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.8000-1
- auto-update to 5.8000 (by cpan-spec-update 0.01)

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.7021-1
- auto-update to 5.7021 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Sat Apr 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.7020-2
- reclaim Catalyst::Manual

* Wed Apr 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.7020-1
- update to 5.7020

* Mon Mar 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.7017-1
- update to 5.7017

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.7016-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.7016-1
- update to 5.7016

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7014-1
- update to 5.7014

* Fri Jul 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7013-1
- update to 5.7013
- don't just exclude Catalyst::Manual's man page, but the .pm as well.
  (RH BZ#455151)

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7012-2
- re-exclude Catalyst::Manual.3pm

* Sun Jun 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7012-1
- update to 7.012...
- ...and add an epoch.  sigh.

* Sun Jun 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.701003-1
- update to 5.701003
- un-exclude Catalyst::Manual pod as it's been moved over from
  Catalyst::Runtime to this dist
- License tag update: GPL -> GPL+

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.700701-3
- rebuild for new perl

* Tue Jun 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.700701-2
- bump

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.700701-1
- Specfile autogenerated by cpanspec 1.71.
