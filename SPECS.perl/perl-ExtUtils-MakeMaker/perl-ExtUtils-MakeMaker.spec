%global cpan_name ExtUtils-MakeMaker
%global cpan_version 7.10

Name:           perl-%{cpan_name}
Version:        %(echo '%{cpan_version}' | tr _ .)
Release:        2%{?dist}
Summary:        Create a module Makefile
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/%{cpan_name}/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/%{cpan_name}-%{cpan_version}.tar.gz
# Do not set RPATH to perl shared-library modules by default. Bug #773622.
# This is copy from `perl' package. This is distributor extension.
Patch0:         %{cpan_name}-7.08-USE_MM_LD_RUN_PATH.patch
# Link to libperl.so explicitly. Bug #960048.
Patch1:         %{cpan_name}-7.08-Link-to-libperl-explicitly-on-Linux.patch
# Unbundle version modules
Patch2:         %{cpan_name}-7.04-Unbundle-version.patch
# Unbundle Encode::Locale module
Patch3:         %{cpan_name}-7.00-Unbundle-Encode-Locale.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
# Makefile.Pl uses ExtUtils::MakeMaker from ./lib
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# If an XS module is compiled, xsubpp(1) is needed
BuildRequires:  perl-ExtUtils-ParseXS
BuildRequires:  sed
# Tests:
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(ExtUtils::Install) >= 1.52
# ExtUtils::Installed not used at tests
BuildRequires:  perl(ExtUtils::Manifest) >= 1.65
# ExtUtils::Packlist not used at tests
# ExtUtils::XSSymSet is not needed (VMS only)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(Getopt::Long)
# IO::File not used at tests
# IO::Handle not used
BuildRequires:  perl(less)
BuildRequires:  perl(overload)
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4400
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util) >= 1.13
BuildRequires:  perl(subs)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
# threads::shared not used
BuildRequires:  perl(utf8)
# XSLoader not used
# Optional tests
BuildRequires:  perl(B)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.130
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(PerlIO)
# Keep YAML optional
# Keep YAML::Tiny optional
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)
# CPAN::Meta 2.112150 is optional
# CPAN::Meta::Converter 2.141170 is optional
# CPAN::Meta::Requirements 2.130 is optional
Requires:       perl(Data::Dumper)
Requires:       perl(DynaLoader)
# Encode is needed for producing POD with =encoding statement correctly
Requires:       perl(Encode)
# Keep unbundled Encode::Locale optional, it's not in the core
Requires:       perl(ExtUtils::Command) >= 1.19
Requires:       perl(ExtUtils::Install) >= 1.52
Requires:       perl(ExtUtils::Manifest) >= 1.65
# ExtUtils::XSSymSet is not needed (VMS only)
Requires:       perl(File::Find)
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Getopt::Long)
# JSON::PP is optional
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       perl(Pod::Man)
Requires:       perl(POSIX)
Requires:       perl(Test::Harness)
# Time::HiRes is optional
# Text::ParseWords is not needed (Win32 only)
Requires:       perl(version)
# VMS::Filespec is not needed (VMS only)
# Win32 is not needed (Win32 only)
# If an XS module is compiled, xsubpp(1) is needed
Requires:       perl-ExtUtils-ParseXS

# Do not export underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)\s*$
# Do not export private redefinitions
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader|ExtUtils::MakeMaker::_version\\)

%description
This utility is designed to write a Makefile for an extension module from a
Makefile.PL. It is based on the Makefile.SH model provided by Andy
Dougherty and the perl5-porters.

%package -n perl-ExtUtils-Command
Summary:        Perl routines to replace common UNIX commands in Makefiles
License:        GPL+ or Artistic
Group:          Development/Libraries
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(File::Copy)
Requires:       perl(File::Find)
Requires:       perl(File::Path)
# File::Spec not used
# VMS::Feature not used

%description -n perl-ExtUtils-Command
This Perl module is used to replace common UNIX commands. In all cases the
functions work with @ARGV rather than taking arguments. This makes them
easier to deal with in Makefiles.

%prep
%setup -q -n ExtUtils-MakeMaker-%{cpan_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Remove bundled modules
rm -rf bundled
sed -i -e '/^bundled\// d' MANIFEST
rm -rf t/lib/Test
sed -i -e '/^t\/lib\/Test\// d' MANIFEST
rm -rf lib/ExtUtils/MakeMaker/version{,.pm}
sed -i -e '/^lib\/ExtUtils\/MakeMaker\/version[\/\.]/ d' MANIFEST
rm -rf lib/ExtUtils/MakeMaker/Locale.pm
sed -i -e '/^lib\/ExtUtils\/MakeMaker\/Locale\.pm/ d' MANIFEST

%build
BUILDING_AS_PACKAGE=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes CONTRIBUTING README
%{_bindir}/*
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/ExtUtils/Command.pm
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/ExtUtils::Command.*

%files -n perl-ExtUtils-Command
%dir %{perl_vendorlib}/ExtUtils
%{perl_vendorlib}/ExtUtils/Command.pm
%{_mandir}/man3/ExtUtils::Command.*

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 7.10-2
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Petr Pisar <ppisar@redhat.com> - 7.10-1
- 7.10 bump

* Wed Sep 09 2015 Petr Pisar <ppisar@redhat.com> - 7.08-1
- 7.08 bump

* Tue Sep 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.06-2
- Remove new line from INC (CPAN RT#106808)

* Tue Sep 01 2015 Petr Pisar <ppisar@redhat.com> - 7.06-1
- 7.06 bump
- ExtUtils::Command module is distributed by ExtUtils-MakeMaker

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.04-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.04-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.04-2
- Perl 5.22 rebuild

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 7.04-1
- 7.04 bump

* Tue Nov 11 2014 Petr Pisar <ppisar@redhat.com> - 7.02-1
- 7.02 bump
- Cope with missing Encode::Locale

* Wed Nov 05 2014 Petr Pisar <ppisar@redhat.com> - 7.00-2
- Fix building with older xsubpp

* Mon Oct 27 2014 Petr Pisar <ppisar@redhat.com> - 7.00-1
- 7.00 bump

* Fri Oct 24 2014 Petr Pisar <ppisar@redhat.com> - 6.98-311
- Require perl-ExtUtils-ParseXS because of xsubpp

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.98-310
- Increase release to favour standalone package

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 6.98-3
- Perl 5.20 rebuild

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
