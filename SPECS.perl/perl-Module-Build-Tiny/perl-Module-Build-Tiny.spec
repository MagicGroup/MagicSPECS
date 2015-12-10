Summary:	A tiny replacement for Module::Build
Summary(zh_CN.UTF-8): Module::Build 的一个小的替代
Name:		perl-Module-Build-Tiny
Version:	0.039
Release:	5%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Module-Build-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/Module-Build-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
# Module
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(ExtUtils::Config) >= 0.003
BuildRequires:	perl(ExtUtils::Helpers) >= 0.020
BuildRequires:	perl(ExtUtils::Install)
BuildRequires:	perl(ExtUtils::InstallPaths) >= 0.002
BuildRequires:	perl(ExtUtils::ParseXS)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Getopt::Long) >= 2.36
BuildRequires:	perl(JSON::PP) >= 2
BuildRequires:	perl(Pod::Man)
BuildRequires:	perl(TAP::Harness::Env)
# Test
BuildRequires:	perl(blib)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::ShareDir)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(XSLoader)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(DynaLoader)
Requires:	perl(ExtUtils::CBuilder)
Requires:	perl(ExtUtils::ParseXS)
Requires:	perl(Pod::Man)
Requires:	perl(TAP::Harness::Env)

%description
Many Perl distributions use a Build.PL file instead of a Makefile.PL file to
drive distribution configuration, build, test and installation. Traditionally,
Build.PL uses Module::Build as the underlying build system. This module
provides a simple, lightweight, drop-in replacement.

Whereas Module::Build has over 6,700 lines of code; this module has less than
70, yet supports the features needed by most pure-Perl distributions.

%description -l zh_CN.UTF-8
Module::Build 的一个小的替代。

%prep
%setup -q -n Module-Build-Tiny-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
magic_rpm_clean.sh

%check
AUTHOR_TESTING=1 RELEASE_TESTING=1 ./Build test

%files
%doc Changes LICENSE README Todo
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Build::Tiny.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.039-5
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.039-4
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.039-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.039-2
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Liu Di <liudidi@gmail.com> - 0.039-1
- 更新到 0.039

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.036-7
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.036-6
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.036-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.036-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.036-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 Paul Howarth <paul@city-fan.org> - 0.036-1
- Update to 0.036
  - Add --jobs argument to MBT
  - Add xs directory to include list

* Tue Feb 18 2014 Paul Howarth <paul@city-fan.org> - 0.035-1
- Update to 0.035
  - Fix install test in absence of a compiler

* Wed Jan 22 2014 Paul Howarth <paul@city-fan.org> - 0.034-1
- Update to 0.034
  - Make install tests more platform independent

* Tue Jan 21 2014 Paul Howarth <paul@city-fan.org> - 0.033-1
- Update to 0.033
  - Require Getopt::Long 2.36
  - Add install tests

* Mon Jan 20 2014 Paul Howarth <paul@city-fan.org> - 0.032-1
- Update to 0.032
  - Process argument sources separately
  - Use mod2fname appropriately
- BR:/R: perl(DynaLoader)
- BR: perl(GetOpt::Long) ≥ 2.36 for GetOptionsFromArray
- Drop dependencies on TAP::Harness as we only use TAP::Harness::Env

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 0.030-1
- Update to 0.030
  - Respect harness environmental variables
  - Add main dir to include path
  - 'include_dirs' must be a list ref, not just a string (CPAN RT#54606)
- BR:/R: perl(TAP::Harness) ≥ 3.29

* Mon Sep 30 2013 Paul Howarth <paul@city-fan.org> - 0.028-1
- Update to 0.028
  - Revert "Removed clean and realclean actions"
  - Build .c and .o in temp/ instead of lib
  - Got rid of IO layers
  - Separate libdoc and bindoc checks

* Mon Sep  9 2013 Paul Howarth <paul@city-fan.org> - 0.027-1
- Update to 0.027
  - Various documentation updates

* Tue Aug 20 2013 Paul Howarth <paul@city-fan.org> - 0.026-1
- Update to 0.026
  - Safe PERL_MB_OPT during configuration stage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.025-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.025-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Paul Howarth <paul@city-fan.org> - 0.025-1
- Update to 0.025
  - Use local tempdir

* Sun Jun 30 2013 Paul Howarth <paul@city-fan.org> - 0.024-1
- Update to 0.024
  - Generate man pages in the correct section

* Wed Jun 12 2013 Paul Howarth <paul@city-fan.org> - 0.023-1
- Update to 0.023
  - Implement --pureperl-only
  - Skip compilation test when not having a compiler

* Sat Jun  1 2013 Paul Howarth <paul@city-fan.org> - 0.022-1
- Update to 0.022
  - Fix dirname code for toplevel XS modules

* Mon May 27 2013 Paul Howarth <paul@city-fan.org> - 0.021-1
- Update to 0.021
  - Add XS support
  - Only manify if really installable
- BR:/R: perl(ExtUtils::CBuilder) and perl(ExtUtils::ParseXS)
- BR: perl(XSLoader) for the test suite

* Mon May 20 2013 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.020
  - Accept a --create_packlist argument

* Tue Apr 30 2013 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.019
  - Accept --pureperl-only
- Bump perl(ExtUtils::Helpers) version requirement to 0.020

* Thu Apr 25 2013 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Lazily load Pod::Man and TAP::Harness
  - Don't manify unless necessary
- Bump perl(ExtUtils::Helpers) version requirement to 0.019
- Explicitly require perl(Pod::Man) and perl(TAP::Harness) ≥ 3.0

* Tue Apr 23 2013 Paul Howarth <paul@city-fan.org> - 0.017-2
- Updates following package review (#947455)
  - BR: perl(ExtUtils::Config) for module
  - BR: perl(File::ShareDir) for test suite
  - Drop BR: perl(File::Basename) and perl(File::Find), not dual-lived

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Switched back from JSON to JSON::PP
  - Remove dependency on File::Find::Rule
  - Switched back to ExtUtils::Helpers for detildefy
  - Drop .modulebuildrc support per Lancaster consensus
  - Fix loading of File::Find
  - Fix redefined warning for find
- Drop BR: perl(ExtUtils::BuildRC), perl(File::Find::Rule), perl(File::HomeDir),
  perl(File::pushd)
- BR: perl(JSON::PP) rather than perl(JSON), and perl(Pod::Man)
- Bump perl(ExtUtils::Helpers) version requirement to 0.017 to avoid the need
  for a workaround for misplaced manpage

* Thu Apr  4 2013 Paul Howarth <paul@city-fan.org> - 0.014-1
- Update to 0.014
  - Added sharedir support
  - Fixed Synopsis
  - Make blib/arch, to satisfy blib.pm
  - Removed dependencies on Test::Exception, Capture::Tiny and File::Slurp

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.013-2
- Sanitize for Fedora submission

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.013-1
- Initial RPM version
