Name:           perl-Test-Apocalypse
Version:	1.006
Release:	2%{?dist}
Summary:        Apocalypse's favorite tests bundled into a simple interface
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Apocalypse/
Source0:        http://www.cpan.org/authors/id/A/AP/APOCAL/Test-Apocalypse-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
# Run-time:
BuildRequires:  perl(Capture::Tiny) >= 0.10
BuildRequires:  perl(CPANPLUS) >= 0.90
BuildRequires:  perl(CPANPLUS::Backend)
BuildRequires:  perl(CPANPLUS::Configure)
BuildRequires:  perl(Devel::PPPort) >= 3.19
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find::Rule) >= 0.32
BuildRequires:  perl(File::Slurp) >= 9999.13
BuildRequires:  perl(File::Spec) >= 3.31
BuildRequires:  perl(File::Which) >= 1.09
BuildRequires:  perl(JSON::Any) >= 1.25
BuildRequires:  perl(Module::CoreList) >= 2.23
BuildRequires:  perl(Module::CPANTS::Analyse) >= 0.85
BuildRequires:  perl(Module::Pluggable) >= 3.9
BuildRequires:  perl(parent)
BuildRequires:  perl(Perl::Critic::Utils::Constants)
BuildRequires:  perl(Perl::Metrics::Simple) >= 0.13
BuildRequires:  perl(Perl::PrereqScanner) >= 1.000
BuildRequires:  perl(Pod::Coverage::TrustPod) >= 0.092830
BuildRequires:  perl(Task::Perl::Critic) >= 1.007
BuildRequires:  perl(Test::AutoLoader) >= 0.03
BuildRequires:  perl(Test::Block) >= 0.11
BuildRequires:  perl(Test::Builder) >= 0.96
BuildRequires:  perl(Test::CheckChanges)
BuildRequires:  perl(Test::Compile) >= 0.11
BuildRequires:  perl(Test::ConsistentVersion) >= 0.2.2
BuildRequires:  perl(Test::CPAN::Meta) >= 0.18
BuildRequires:  perl(Test::CPAN::Meta::JSON) >= 0.10
BuildRequires:  perl(Test::CPAN::Meta::YAML) >= 0.17
BuildRequires:  perl(Test::Deep) >= 0.108
BuildRequires:  perl(Test::Dir) >= 1.006
BuildRequires:  perl(Test::DistManifest) >= 1.005
BuildRequires:  perl(Test::EOL) >= 0.3
BuildRequires:  perl(Test::File) >= 1.29
BuildRequires:  perl(Test::Fixme) >= 0.04
BuildRequires:  perl(Test::HasVersion) >= 0.012
BuildRequires:  perl(Test::MinimumVersion) >= 0.101080
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::NoBreakpoints) >= 0.13
BuildRequires:  perl(Test::NoPlan) >= 0.0.6
# Test::NoWarnings is not needed (lib/Test/Apocalypse.pm:39)
BuildRequires:  perl(Test::Perl::Critic) >= 1.02
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::Pod::LinkCheck) >= 0.004
BuildRequires:  perl(Test::Pod::No404s) >= 0.01
BuildRequires:  perl(Test::Pod::Spelling::CommonMistakes) >= 1.000
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Script) >= 1.07
BuildRequires:  perl(Test::Signature) >= 1.10
BuildRequires:  perl(Test::Spelling) >= 0.11
BuildRequires:  perl(Test::Strict) >= 0.14
BuildRequires:  perl(Test::Synopsis) >= 0.06
BuildRequires:  perl(Test::Vars) >= 0.001
BuildRequires:  perl(version) >= 0.77
BuildRequires:  perl(YAML) >= 0.70
BuildRequires:  perl(YAML::Any) >= 0.72
# Tests:
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::NoWarnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Perl::Critic::Utils::Constants)
Requires:       perl(Test::CheckChanges)
Requires:       perl(Test::Portability::Files)
# Test::NoWarnings is not needed (lib/Test/Apocalypse.pm:39)

# Remove under-specified dependenices
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Test::More\\)$

%description
This module greatly simplifies common author tests for modules heading towards
CPAN. I was sick of copy/pasting the tons of t/foo.t scripts + managing them
in every distribution. I thought it would be nice to bundle all of it into one
module and toss it on CPAN :) That way, every time I update this module all of
my distributions would be magically updated!

%prep
%setup -q -n Test-Apocalypse-%{version}
# <https://rt.cpan.org/Public/Bug/Display.html?id=76848>
# Remove test interfering with Test::CheckChanges
rm t/000-report-versions-tiny.t
sed -i -e '/^t\/000-report-versions-tiny.t$/ d' MANIFEST

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes CommitLog examples LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.006-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.006-1
- 更新到 1.006

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.002-11
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.002-10
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.002-9
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.002-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 1.002-6
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Petr Pisar <ppisar@redhat.com> - 1.002-2
- Perl 5.16 rebuild

* Mon Jul 02 2012 Petr Pisar <ppisar@redhat.com> - 1.002-1
- 1.002 bump

* Fri Mar 25 2011 Petr Pisar <ppisar@redhat.com> - 1.001-1
- 1.001 bump
- Build-require Test::NoWarnings

* Mon Jan 24 2011 Petr Pisar <ppisar@redhat.com> 0.10-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff
