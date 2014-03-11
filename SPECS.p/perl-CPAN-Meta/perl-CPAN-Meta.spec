Name:           perl-CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Version:        2.120921
Release:        5%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CPAN-Meta/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.008
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.20
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(JSON::PP) >= 2.27200
BuildRequires:  perl(overload)
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4403
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(version) >= 0.88

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 2.113640-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.

%prep
%setup -q -n CPAN-Meta-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes history LICENSE README Todo t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.120921-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 2.120921-2
- Build-require Data::Dumper for tests

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.120921-1
- update to latest upstream version

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 2.120900-1
- update to latest upstream version

* Sun Mar 04 2012 Iain Arnell <iarnell@gmail.com> 2.120630-1
- update to latest upstream version

* Wed Feb 22 2012 Iain Arnell <iarnell@gmail.com> 2.120530-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 2.120351-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 2.113640-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.113640-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.113640-1
- update to latest version, which deprecated Version::Requirements

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 2.112621-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 2.112150-1
- update to latest upstream version

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.110930-2
- Perl mass rebuild

* Sun Apr 03 2011 Iain Arnell <iarnell@gmail.com> 2.110930-1
- update to latest upstream version

* Sat Apr 02 2011 Iain Arnell <iarnell@gmail.com> 2.110910-1
- update to latest upstream version

* Sun Mar 06 2011 Iain Arnell <iarnell@gmail.com> 2.110580-1
- update to latest upstream version
- drop BR perl(Storable)

* Sat Feb 26 2011 Iain Arnell <iarnell@gmail.com> 2.110550-1
- update to latest upstream version

* Thu Feb 17 2011 Iain Arnell <iarnell@gmail.com> 2.110440-1
- update to latest upstream
- drop BR perl(autodie)
- drop BR perl(Data::Dumper)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110350-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 2.110350-1
- update to latest upstream version

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.102400-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Aug 29 2010 Iain Arnell <iarnell@gmail.com> 2.102400-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.102400)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0.20)
- added a new br on perl(IO::Dir) (version 0)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Storable) (version 0)
- added a new br on perl(autodie) (version 0)
- added a new br on perl(version) (version 0.82)

* Thu Aug 05 2010 Iain Arnell <iarnell@gmail.com> 2.102160-1
- update to latest upstream

* Wed Jun 16 2010 Iain Arnell <iarnell@gmail.com> 2.101670-1
- update to latest upstream

* Mon Jun 14 2010 Iain Arnell <iarnell@gmail.com> 2.101610-1
- update to latest upstream

* Tue Jun 01 2010 Iain Arnell <iarnell@gmail.com> 2.101461-2
- rebuild for perl-5.12

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 2.101461-1
- Specfile autogenerated by cpanspec 1.78.
- drop explicit requirements
