%global cpan_version 0.9152
Name:           perl-CPANPLUS
# Keep 2-digit major varion to compete with perl.spec for history
Version:	0.9156
Release:	3%{?dist}
Summary:        Ameliorated interface to the Comprehensive Perl Archive Network
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CPANPLUS/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/CPANPLUS-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
%if %{defined perl_bootstrap}
BuildRequires:  perl(ExtUtils::MakeMaker)
# ExtUtils::Manifest not used
BuildRequires:  perl(ExtUtils::MM_Unix)
# Module::Build not used
# YAML not used
%else
BuildRequires:  perl(inc::Module::Install)
%endif
BuildRequires:  perl(lib)
BuildRequires:  perl(Locale::Maketext::Simple)
BuildRequires:  perl(Module::Loaded)
# Run-time:
BuildRequires:  perl(Archive::Extract)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBIx::Simple)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Fetch)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Log::Message)
BuildRequires:  perl(Module::CoreList) >= 2.22
BuildRequires:  perl(Module::Load)
BuildRequires:  perl(Module::Load::Conditional)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(Object::Accessor)
BuildRequires:  perl(overload)
BuildRequires:  perl(Package::Constants)
BuildRequires:  perl(Params::Check)
BuildRequires:  perl(Parse::CPAN::Meta)
BuildRequires:  perl(strict)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Term::UI)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# lib/CPANPLUS/Internals.pm:465
Requires:       perl(File::Glob)
# lib/CPANPLUS/Internals/Utils.pm:68
Requires:       perl(File::Path)
# lib/CPANPLUS/Internals/Utils.pm:323
Requires:       perl(File::stat)
# bin/cpanp-boxed:10
Requires:       perl(FindBin)
# lib/CPANPLUS/Module.pm:477
Requires:       perl(Module::CoreList) >= 2.22
# lib/CPANPLUS/Configure.pm:181
Requires:       perl(Module::Pluggable)

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Your::Module::Here|Test)\\)

%description
The CPANPLUS library is an API to the CPAN mirrors and a collection of
interactive shells, command line programs, etc., that use this API.

%prep
%setup -q -n CPANPLUS-%{cpan_version}
# Remove bundled modules
%if !%{defined perl_bootstrap}
rm -rf inc
sed -i -e '/^inc\//d' MANIFEST
%else
rm -rf inc/bundle
sed -i -e '/^inc\/bundle\//d' MANIFEST
%endif
# Fix shebangs
sed -i -e '1i#!%{__perl}' bin/cpanp-run-perl

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test %{?_smp_mflags}

%files
%doc ChangeLog README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.9156-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.9156-2
- 更新到 0.9156

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.9154-1
- 更新到 0.9154

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.91.52-5
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.91.52-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.91.52-3
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Petr Pisar <ppisar@redhat.com> - 0.91.52-2
- 0.9152 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 04 2014 Petr Pisar <ppisar@redhat.com> - 0.91.48-1
- 0.9148 bump

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 0.91.46-1
- 0.9146 bump
- Run tests in parallel

* Wed Dec 11 2013 Petr Pisar <ppisar@redhat.com> - 0.91.44-1
- 0.9144 bump

* Mon Aug 26 2013 Petr Pisar <ppisar@redhat.com> - 0.91.42-1
- 0.9142 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.91.40-2
- Perl 5.18 re-rebuild of bootstrapped packages

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 0.91.40-1
- 0.9140 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.91.38-2
- Perl 5.18 rebuild
- Specify all dependencies

* Tue May 21 2013 Petr Pisar <ppisar@redhat.com> - 0.91.38-1
- 0.9138 bump

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 0.91.36-1
- 0.9136 bump

* Thu Apr 04 2013 Petr Pisar <ppisar@redhat.com> - 0.91.34-2
- Keep bundled inc::Module::Install modules at boot-strap (bug #947489)

* Thu Jan 24 2013 Petr Pisar <ppisar@redhat.com> 0.91.34-1
- Specfile autogenerated by cpanspec 1.78.
