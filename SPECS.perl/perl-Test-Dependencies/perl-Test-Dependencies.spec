Name:       perl-Test-Dependencies 
Version:    0.12
Release:    14%{?dist}
# see lib/Test/Dependencies.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Ensure that your Makefile.PL specifies all module dependencies 
Source:     http://search.cpan.org/CPAN/authors/id/Z/ZE/ZEV/Test-Dependencies-%{version}.tar.gz 
# Disable installing missing modules from CPAN
Patch0:     Test-Dependencies-0.12-Do-not-auto-install-modules-from-CPAN.patch
Url:        http://search.cpan.org/dist/Test-Dependencies
BuildArch:  noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Module::Install::Metadata)
BuildRequires:  perl(Module::Install::WriteAll)
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(B::PerlReq)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(PerlReq::Utils)
BuildRequires:  perl(Pod::Strip)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(warnings)
BuildRequires:  perl(YAML)
# Tests:
BuildRequires:  perl(Test::Builder::Tester) >= 0.64
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Makes sure that all of the modules that are 'use'd are listed in the
Makefile.PL as dependencies.

It has two styles: light, which is fast but confusable; and heavy, which takes
more time but is more accurate.

%prep
%setup -q -n Test-Dependencies-%{version}
%patch0 -p1
# Remove bundled modules
rm -r ./inc
sed -i -e '/^inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
# Hide ExtUtils::MakeMaker dependency declaration in META.yml from
# Test::Dependencies tests. System Module::Install::Makefile write it there
# but Test::Dependencies ignores ./inc. This is need for unbundling ./inc.
# CPAN RT#105285
sed -i -e '/ExtUtils::MakeMaker:/d' META.yml
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README Changes 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.12-14
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.12-13
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.12-12
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Petr Pisar <ppisar@redhat.com> - 0.12-11
- Perl 5.22 rebuild
- Specify all dependencies

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.12-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.12-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-2
- Perl mass rebuild

* Fri Feb 25 2011 Iain Arnell <iarnell@gmail.com> 0.12-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.11-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- update for submission

* Wed Nov 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.11-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

