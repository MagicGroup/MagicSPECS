Name:       perl-rpm-build-perl 
Version:    0.82
Release:    12%{?dist}
# README: GPLv2+
# perl.prov: LGPLv2+
License:    GPLv2+
Group:      Development/Libraries
Summary:    Perl compiler back-end to extract Perl dependencies 
Url:        http://search.cpan.org/dist/rpm-build-perl
Source:     http://search.cpan.org/CPAN/authors/id/A/AT/ATOURBIN/rpm-build-perl-%{version}.tar.gz 
# Perl 5.18 compatibility, CPAN RT#85411
Patch0:     rpm-build-perl-0.82-Fix-non-deterministic-failures-on-newer-perls.patch
# Perl 5.22 compatibility, bug #1231258, CPAN RT#104885
Patch1:     rpm-build-perl-0.82-Adjust-to-perl-5.22.patch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) 
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(version)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(encoding)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Try::Tiny)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Encode)
Requires:       perl(version)

%{?perl_default_filter}
# Do not export private modules
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(fake\\)

%description
B::PerlReq is a back-end module for the Perl compiler that extracts
dependencies from Perl source code, based on the internal compiled
structure that Perl itself creates after parsing a program. The output of
B::PerlReq is suitable for automatic dependency tracking (e.g. for RPM
packaging).

%package scripts
Summary:    Perl RPM prov/req scripts
Group:      Development/Libraries
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description scripts
The provides/requires scripts packaged along with perl-rpm-build-perl.

%prep
%setup -q -n rpm-build-perl-%{version}
%patch0 -p1
%patch1 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README* Changes perl5-alt-rpm-macros macros.env
%{perl_vendorarch}/*
%{_mandir}/man3/*.3*

%files scripts
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Wed Jun 17 2015 Petr Pisar <ppisar@redhat.com> - 0.82-12
- Other perl-5.22 fix for GV to IV optimization (bug #1231258)

* Wed Jun 17 2015 Petr Pisar <ppisar@redhat.com> - 0.82-11
- Make adjustments for perl-5.22 compatible with older perls (bug #1231258)

* Tue Jun 16 2015 Petr Pisar <ppisar@redhat.com> - 0.82-10
- Adjust to perl-5.22 (bug #1231258)

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.82-9
- Perl 5.22 rebuild

* Tue Nov 18 2014 Petr Pisar <ppisar@redhat.com> - 0.82-8
- Specify more dependencies (bug #1165197)

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.82-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.82-3
- Perl 5.18 rebuild
- Perl 5.18 compatibility (CPAN RT#85411)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 01 2012 Petr Pisar <ppisar@redhat.com> - 0.82-1
- 0.82 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.80-2
- Perl 5.16 rebuild
- Specify all dependencies
- Adapt tests to perl 5.16 (RT #77778)

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 0.80-1
- 0.80 bump

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.74-1
- update to 0.74, clean spec, fix tests for 5.14.1

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.72-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.72-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.72-1
- Mass rebuild with perl-5.12.0 & update

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.6.8-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.6.8-1
- update for submission
- split scripts off into their own package

* Tue Nov 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.6.8-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
