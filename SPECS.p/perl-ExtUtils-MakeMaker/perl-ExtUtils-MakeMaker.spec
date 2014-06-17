%global cpan_name ExtUtils-MakeMaker
%global cpan_version 6.98

Name:           perl-%{cpan_name}
Version:        %(echo '%{cpan_version}' | tr _ .)
Release:        3%{?dist}
Summary:        Create a module Makefile
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/%{cpan_name}/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/%{cpan_name}-%{cpan_version}.tar.gz
# Do not set RPATH to perl shared-library modules by default. Bug #773622.
# This is copy from `perl' package. This is distributor extension.
Patch0:         %{cpan_name}-6.96-USE_MM_LD_RUN_PATH.patch
# Link to libperl.so explicitly. Bug #960048.
Patch1:         %{cpan_name}-6.88-Link-to-libperl-explicitly-on-Linux.patch
BuildArch:      noarch
BuildRequires:  perl
# Makefile.Pl uses ExtUtils::MakeMaker from ./lib
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Unbundled
BuildRequires:  perl(File::Copy::Recursive)
# Tests:
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::Command)
BuildRequires:  perl(ExtUtils::Install)
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
# IO::Handle not used
BuildRequires:  perl(less)
BuildRequires:  perl(overload)
BuildRequires:  perl(Parse::CPAN::Meta)
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(subs)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
# threads::shared not used
BuildRequires:  perl(version)
# XSLoader not used
# Optional tests
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(PerlIO)
# Keep YAML optional
# Keep YAML::Tiny optional
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# CPAN::Meta is optional
Requires:       perl(Data::Dumper)
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Command)
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::Manifest)
# ExtUtils::XSSymSet is not needed (VMS only)
Requires:       perl(File::Find)
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Getopt::Long)
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       perl(Pod::Man)
Requires:       perl(POSIX)
Requires:       perl(Test::Harness)
# Time::HiRes is optional
# Text::ParseWords is not needed (Win32 only)
Requires:       perl(version)
# VMS::Filespec is not needed (VMS only)
# Win32 is not needed (Win32 only)

# Do not export underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)\s*$
# Do not export private redefinitions
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader|ExtUtils::MakeMaker::_version\\)

%description
This utility is designed to write a Makefile for an extension module from a
Makefile.PL. It is based on the Makefile.SH model provided by Andy
Dougherty and the perl5-porters.

%prep
%setup -q -n ExtUtils-MakeMaker-%{cpan_version}
%patch0 -p1
%patch1 -p1
# Remove bundled modules
rm -rf bundled/* ||:
sed -i -e '/^bundled\// d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes NOTES PATCHING README TODO
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 6.98-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Petr Pisar <ppisar@redhat.com> - 6.98-1
- 6.98 bump

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 6.96-1
- 6.96 bump

* Wed Mar 26 2014 Petr Pisar <ppisar@redhat.com> - 6.94-1
- 6.94 bump

* Fri Mar 14 2014 Petr Pisar <ppisar@redhat.com> - 6.92-1
- 6.92 bump

* Fri Feb 21 2014 Petr Pisar <ppisar@redhat.com> - 6.90-1
- 6.90 bump

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 6.88-1
- 6.88 bump

* Mon Jan 06 2014 Petr Pisar <ppisar@redhat.com> - 6.86-1
- 6.86 bump

* Mon Dec 02 2013 Petr Pisar <ppisar@redhat.com> - 6.84-1
- 6.84 bump

* Tue Nov 05 2013 Petr Pisar <ppisar@redhat.com> - 6.82-1
- 6.82 bump

* Wed Oct 16 2013 Petr Pisar <ppisar@redhat.com> - 6.80-1
- 6.80 bump

* Tue Sep 24 2013 Petr Pisar <ppisar@redhat.com> - 6.78-1
- 6.78 bump

* Mon Sep 16 2013 Petr Pisar <ppisar@redhat.com> - 6.76-2
- Specify all dependencies (bug #1007755)

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 6.76-1
- 6.76 bump

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 6.74-1
- 6.74 bump

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 6.72-1
- 6.72 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.68-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 6.68-4
- Perl 5.18 rebuild

* Tue Jul 02 2013 Petr Pisar <ppisar@redhat.com> - 6.68-3
- Link to libperl.so explicitly (bug #960048)

* Thu Jun 27 2013 Jitka Plesnikova <jplesnik@redhat.com> - 6.68-2
- Update BRs

* Mon Jun 17 2013 Petr Pisar <ppisar@redhat.com> - 6.68-1
- 6.68 bump

* Mon Apr 22 2013 Petr Pisar <ppisar@redhat.com> - 6.66-1
- 6.66 bump

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 6.64-2
- Run-require POD convertors to get manual pages when building other packages

* Mon Dec 17 2012 Petr Pisar <ppisar@redhat.com> - 6.64-1
- 6.64 bump

* Tue Aug 28 2012 Petr Pisar <ppisar@redhat.com> - 6.63.02-241
- Compute RPM version
- Do not build-require itself, the build script runs from ./lib

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.63.02-240
- update version to the same as in perl.srpm
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 6.62-3
- Perl 5.16 rebuild

* Thu Jan 12 2012 Petr Pisar <ppisar@redhat.com> - 6.62-2
- Do not set RPATH to perl shared-library modules by default (bug #773622)

* Fri Nov 25 2011 Petr Pisar <ppisar@redhat.com> 6.62-1
- Specfile autogenerated by cpanspec 1.78.
- Remove defattr and BuildRoot from spec.
