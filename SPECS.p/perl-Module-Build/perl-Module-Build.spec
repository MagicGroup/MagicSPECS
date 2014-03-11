%global cpan_version_major 0.40
%global cpan_version_minor 03
%global cpan_version %{cpan_version_major}%{?cpan_version_minor}

Name:           perl-Module-Build
Epoch:          2
Version:        %{cpan_version_major}%{?cpan_version_minor:.%cpan_version_minor}
Release:        5%{?dist}
Summary:        Build and install Perl modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Build/
Source0:        http://www.cpan.org/authors/id/L/LE/LEONT/Module-Build-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-devel
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta) >= 2.110420
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.003
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:  perl(ExtUtils::Install) >= 0.3
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(ExtUtils::Mkbootstrap)
BuildRequires:  perl(ExtUtils::Packlist)
BuildRequires:  perl(ExtUtils::ParseXS) >= 2.21
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.15
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(lib)
# perl(Module::Build) is loaded from ./lib
BuildRequires:  perl(Module::Metadata) >= 1.000002
BuildRequires:  perl(Parse::CPAN::Meta)
BuildRequires:  perl(Perl::OSType) >= 1
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(PAR::Dist)
%if 0%{?fedora}  || 0%{?rhel} < 7
BuildRequires:  perl(Pod::Readme)
%endif
%endif
BuildRequires:  perl(Test::Harness) >= 3.16
BuildRequires:  perl(Test::More) >= 0.49
BuildRequires:  perl(version) >= 0.87
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(CPAN::Meta) >= 2.110420
Requires:       perl(CPAN::Meta::YAML) >= 0.003
Requires:       perl(ExtUtils::CBuilder) >= 0.27
Requires:       perl(ExtUtils::Install) >= 0.3
Requires:       perl(ExtUtils::Manifest) >= 1.54
Requires:       perl(ExtUtils::Mkbootstrap)
Requires:       perl(ExtUtils::ParseXS) >= 2.21
Requires:       perl(Module::Metadata) >= 1.000002
# Keep PAR support optional (PAR::Dist)
Requires:       perl(Perl::OSType) >= 1
Requires:       perl(Test::Harness)

%{?perl_default_filter}
# Remove under-sspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.
Developers may alter the behavior of the module through sub-classing in a
much more straightforward way than with MakeMaker. It also does not require
a make on your system - most of the Module::Build code is pure-perl and
written in a very cross-platform way. In fact, you don't even need a shell,
so even platforms like MacOS (traditional) can use it fairly easily. Its
only prerequisites are modules that are included with perl 5.6.0, and it
works fine on perl 5.005 if you can install a few additional modules.

%prep
%setup -q -n Module-Build-%{cpan_version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test

%files
%doc Changes contrib LICENSE README
%{_bindir}/config_data
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Jan 17 2013 Liu Di <liudidi@gmail.com> - 2:0.40.03-5
- 为 Magic 3.0 重建

* Mon Dec 10 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-4
- YAML::Tiny is not needed at build time (bug #885146)

* Wed Nov 21 2012 Petr Šabata <contyk@redhat.com> - 2:0.40.03-3
- Add a few missing deps
- Drop command macros

* Mon Sep 03 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-2
- Do not build-require Module::Build (bug #849328)

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.03-1
- 0.4003 bump

* Mon Jul 30 2012 Jitka Plesnikova <jplesnik@redhat.com>  2:0.40.02-1
- 0.4002 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.40.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-2
- Perl 5.16 rebuild

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40.01-1
- 0.4001 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-3
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-2
- Do not run PAR tests on bootstrap

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 2:0.40-1
- 0.40 bump
- All reverse dependecies must require use 2-digit Module::Build version now

* Wed May 30 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-5
- conditionalize some test

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3800-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-3
- BR on perl-devel because this package contains macros used by rpmbuild
  for Perl packages

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-2
- rebuild with Perl 5.14.1, remove defatter

* Wed Mar 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.3800-1
- update to 0.3800

* Wed Mar 02 2011 Petr Pisar <ppisar@redhat.com> - 1:0.3624-2
- Raise epoch to  Core level
- Remove BuildRoot stuff

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.3624-1
- update to new version
- fix BR, R

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3607-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-3
- switch off experimental test

* Tue Jun  8 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-2
- copy check part&upload key from Paul Howarth
- fix macro

* Mon May 31 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3607-1
- add BR, update, switch on some other tests

* Tue Mar 09 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.3603-1
- Specfile autogenerated by cpanspec 1.78.
