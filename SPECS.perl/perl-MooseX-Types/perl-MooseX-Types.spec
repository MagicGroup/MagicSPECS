Name:       perl-MooseX-Types
Version:	0.46
Release:	2%{?dist}
# see Makefile.PL, lib/MooseX/Types.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Organize your Moose types in libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-%{version}.tar.gz
Url:        http://search.cpan.org/dist/MooseX-Types
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Carp)
BuildRequires: perl(Carp::Clan) >= 6.00
BuildRequires: perl(FindBin)
BuildRequires: perl(Moose) >= 1.06
BuildRequires: perl(namespace::clean) >= 0.19
BuildRequires: perl(Sub::Install) >= 0.924
# tests
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Test::Fatal)
BuildRequires: perl(Test::Requires)
BuildRequires: perl(Sub::Exporter)
# for M::I
BuildRequires: perl(CPAN)

BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Scalar::Util) >= 1.19
BuildRequires:  perl(Sub::Name)


%{?perl_default_filter}

%description
The types provided with the Moose man page are by design global. This
package helps you to organize and selectively import your own and the
built-in types in libraries. As a nice side effect, it catches typos at
compile-time too.

However, the main reason for this module is to provide an easy way to not
have conflicts with your type names, since the internal fully qualified
names of the types will be prefixed with the library's name.

This module will also provide you with some helper functions to make it
easier to use Moose types in your code.

%prep
%setup -q -n MooseX-Types-%{version}

# silence rpmlint
sed -i '1s,^#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.46-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.46-1
- 更新到 0.46

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.35-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.35-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.35-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Iain Arnell <iarnell@gmail.com> 0.35-1
- update to latest upstream version

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.31-1
- update to latest upstream version

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.30-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.27-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version
- remove explicit requires

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jul 04 2010 Iain Arnell <iarnell@gmail.com> 0.22-1
- update to latest upstream
- update BR perl(Moose) >= 1.06

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.21-3
- Mass rebuild with perl-5.12.0

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.21-2
- add perl_default_filter (and drop custom filtering scheme)
- PERL_INSTALL_ROOT => DESTDIR in install

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- auto-update to 0.21 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.61 => 0.93)
- altered req on perl(Moose) (0.61 => 0.93)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.20-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- auto-update to 0.20 (by cpan-spec-update 0.01)

* Mon Aug 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- auto-update to 0.18 (by cpan-spec-update 0.01)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- auto-update to 0.16 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- auto-update to 0.12 (by cpan-spec-update 0.01)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Carp::Clan) (version 6.00)
- added a new req on perl(Moose) (version 0.61)
- added a new req on perl(Scalar::Util) (version 1.19)
- added a new req on perl(Sub::Install) (version 0.924)
- added a new req on perl(Sub::Name) (version 0)
- added a new req on perl(namespace::clean) (version 0.08)

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-2
- add br on CPAN for bundled version of M::I

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Carp::Clan) (0 => 6.00)
- added a new br on perl(Scalar::Util) (version 1.19)
- added a new br on perl(Sub::Name) (version 0)
- altered br on perl(Test::More) (0.62 => 0.80)

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- update to 0.10

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08-2
- add br on Test::Exception

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08

* Mon Nov 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07, adjust BR accordingly.  Note especially dep on Moose >= 0.61

* Sun Oct 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- bump

* Tue Oct 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
