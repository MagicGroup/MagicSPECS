Name:           perl-Perl-PrereqScanner
Version:        1.019
Release:        2%{?dist}
Summary:        Tool to scan your Perl code for its prerequisites
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Perl-PrereqScanner/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Perl-PrereqScanner-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# run-time:
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120630
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
# Getopt::Long::Descriptive not used at tests
BuildRequires:  perl(lib)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Path)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(PPI) >= 1.215
# Scalar::Util not used at tests
BuildRequires:  perl(String::RewritePrefix) >= 0.005
# tests
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(PPI::Document)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Try::Tiny)
# optional tests
BuildRequires:  perl(Test::Pod) >= 1.41
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Module::Path)

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CPAN::Meta::Requirements\\)$ 

%description
The scanner will extract loosely your distribution prerequisites from
your files.

%prep
%setup -q -n Perl-PrereqScanner-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Petr Pisar <ppisar@redhat.com> - 1.019-1
- 1.019 bump

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.015-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Iain Arnell <iarnell@gmail.com> 1.015-1
- update to latest upstream version

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 1.014-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.011-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 1.011-2
- Perl 5.16 rebuild

* Sun Mar 25 2012 Iain Arnell <iarnell@gmail.com> 1.011-1
- update to latest upstream version

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 1.010-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.009-1
- update to the latest release

* Sun Nov 06 2011 Iain Arnell <iarnell@gmail.com> 1.008-1
- update to latest upstream version

* Thu Sep 22 2011 Iain Arnell <iarnell@gmail.com> 1.007-1
- update to latest upstream version

* Sun Aug 28 2011 Iain Arnell <iarnell@gmail.com> 1.006-1
- update to latest upstream version

* Thu Aug 18 2011 Iain Arnell <iarnell@gmail.com> 1.005-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.004-2
- Perl mass rebuild

* Sun Jun 05 2011 Iain Arnell <iarnell@gmail.com> 1.004-1
- update to latest upstream version

* Wed May 18 2011 Iain Arnell <iarnell@gmail.com> 1.003-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Iain Arnell <iarnell@gmail.com> 1.002-1
- update to latest upstream version

* Thu Jan 06 2011 Iain Arnell <iarnell@gmail.com> 1.001-1
- update to latest upstream version
- fixes scan_prereqs script

* Thu Dec 16 2010 Iain Arnell <iarnell@gmail.com> 1.000-1
- update to latest upstream version

* Mon Dec 06 2010 Iain Arnell <iarnell@gmail.com> 0.101892-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Nov 19 2010 Iain Arnell <iarnell@gmail.com> 0.101891-1
- update to latest upstream version

* Sun May 30 2010 Iain Arnell <iarnell@gmail.com> 0.101480-1
- update to latest upstream version

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 0.101250-2
- bump release for rebuild with perl-5.12.0

* Sun May 09 2010 Iain Arnell <iarnell@gmail.com> 0.101250-1
- update to latest upstream
- BR perl(Moose)
- BR perl(Moose::Role)
- BR perl(Params::Util)
- BR perl(String::RewritePrefix)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.100960-2
- Mass rebuild with perl-5.12.0

* Sun Apr 11 2010 Iain Arnell <iarnell@gmail.com> 0.100960-1
- update to latest upstream version

* Thu Apr 08 2010 Iain Arnell <iarnell@gmail.com> 0.100830-2
- drop perl BR

* Sun Apr 04 2010 Iain Arnell <iarnell@gmail.com> 0.100830-1
- Specfile autogenerated by cpanspec 1.78.
- use perl_default_filter and DESTDIR
