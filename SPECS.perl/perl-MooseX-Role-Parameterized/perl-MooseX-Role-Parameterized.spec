Name:           perl-MooseX-Role-Parameterized
Summary:        Make your roles flexible through parameterization
Version:	1.08
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Role-Parameterized-%{version}.tar.gz
URL:            http://search.cpan.org/dist/MooseX-Role-Parameterized
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Moose) >= 2.0300
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.96

Requires:       perl(Moose) >= 2.0300

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 1.00-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Roles are composable units of behavior. They are useful for factoring out
functionality common to many classes from any part of your class hierarchy.
(See Moose::Cookbook::Roles::Recipe1 for an introduction to Moose::Role.)

While combining roles affords you a great deal of flexibility, individual
roles have very little in the way of configurability. Core Moose provides
alias for renaming methods to avoid conflicts, and excludes for ignoring
methods you don't want or need (see Moose::Cookbook::Roles::Recipe2 for more
about alias and excludes).

Because roles serve many different masters, they usually provide only the
least common denominator of functionality. To empower roles further, more
configurability than alias and excludes is required. Perhaps your role needs
to know which method to call when it is done. Or what default value to use for
its url attribute.

Parameterized roles offer exactly this solution.

%prep
%setup -q -n MooseX-Role-Parameterized-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.08-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.08-1
- 更新到 1.08

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.00-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.00-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.00-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.00-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.00-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.00-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.00-4
- Perl 5.16 rebuild

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1.00-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 1.00-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 1.00-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.26-2
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 13 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.18-2
- perl-5.12.0 mass rebuild.

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.18)

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- auto-update to 0.15 (by cpan-spec-update 0.01)
- altered br on perl(Test::More) (0 => 0.88)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Wed Aug 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- drop README, LICENSE from doc

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- auto-update to 0.09 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new req on perl(Moose) (version 0.78)

* Wed May 20 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- auto-update to 0.06 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0 => 0.27)
- altered br on perl(Moose) (0.63 => 0.78)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update to 0.04

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update to 0.03

* Mon Jan 12 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- update for submission

* Sun Jan 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.7)
