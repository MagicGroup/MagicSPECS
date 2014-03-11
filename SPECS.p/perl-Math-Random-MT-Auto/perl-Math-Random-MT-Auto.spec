Name:           perl-Math-Random-MT-Auto
Version:        6.22
Release:        1%{?dist}
Summary:        Auto-seeded Mersenne Twister PRNGs
License:        BSD 
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Math-Random-MT-Auto/
Source0:        http://www.cpan.org/authors/id/J/JD/JDHEDDEN/Math-Random-MT-Auto-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exception::Class) >= 1.32
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Object::InsideOut) >= 3.88
BuildRequires:  perl(Object::InsideOut::Util)
BuildRequires:  perl(Scalar::Util) >= 1.23
BuildRequires:  perl(strict)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
# Optional tests
BuildRequires:  perl(LWP::UserAgent)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Exception::Class) >= 1.32
Requires:       perl(Fcntl)
Requires:       perl(Object::InsideOut) >= 3.88
Requires:       perl(Scalar::Util) >= 1.23

%{?perl_default_filter}

# Removed underpsecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Exception::Class\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Object::InsideOut\\)
%global __requires_exclude %__requires_exclude|^perl\\(Scalar::Util\\)

%description
The Mersenne Twister is a fast pseudo-random number generator (PRNG) that is
capable of providing large volumes (> 10^6004) of "high quality"
pseudo-random data to applications that may exhaust available "truly" random
data sources or system-provided PRNGs such as rand.

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Object::InsideOut\\)$

%prep
%setup -q -n Math-Random-MT-Auto-%{version}
chmod -x examples/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README examples
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Math*
%{_mandir}/man3/*

%changelog
* Wed Sep 05 2012 Petr Pisar <ppisar@redhat.com> - 6.22-1
- 6.22 bump

* Wed Aug 08 2012 Petr Pisar <ppisar@redhat.com> - 6.21-1
- 6.21 bump

* Tue Aug 07 2012 Petr Pisar <ppisar@redhat.com> - 6.19-2
- 6.19 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 6.18-2
- Perl 5.16 rebuild

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 6.18-1
- 6.18 bump

* Thu Jan 19 2012 Petr Pisar <ppisar@redhat.com> - 6.17-1
- 6.17 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 6.16-4
- update filtering for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 6.16-3
- Perl mass rebuild

* Mon Mar 07 2011 Iain Arnell <iarnell@gmail.com> 6.16-2
- only filter unversion Object::InsideOut requires

* Thu Feb 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 6.16-1
- update to 6.16
- fix filtering of requires
- clean specfile according to current guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.14-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.14-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.14-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 6.14-1
- update to 6.14
- switch to inline req filtering

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.12-1
- 6.12

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.02-4
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.02-3
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 6.02-2
- bump

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> 6.02-1
- update to 6.02
- add t/ to doc
- minor spec tweaks to deal with the once and future perl split

* Fri Feb 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.04-3
- bump

* Thu Feb 22 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.04-2
- drop execute bit on filter-requires.sh to appease rpmlint

* Mon Feb 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.04-1
- Specfile autogenerated by cpanspec 1.70.
