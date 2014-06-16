Name:           perl-Perl-Critic-Pulp
Version:        85
Release:        2%{?dist}
Summary:        Some add-on perlcritic policies
License:        GPLv3+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Perl-Critic-Pulp/
Source0:        http://www.cpan.org/authors/id/K/KR/KRYDE/Perl-Critic-Pulp-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::String) >= 1.02
BuildRequires:  perl(List::MoreUtils) >= 0.24
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Perl::Critic) >= 1.084
BuildRequires:  perl(Perl::Critic::Policy) >= 1.084
BuildRequires:  perl(Perl::Critic::Utils) >= 1.100
BuildRequires:  perl(Perl::Critic::Utils::PPI)
BuildRequires:  perl(Perl::Critic::Violation)
BuildRequires:  perl(Pod::Escapes)
BuildRequires:  perl(Pod::MinimumVersion) >= 50
BuildRequires:  perl(Pod::ParseLink)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(PPI) >= 1.212
BuildRequires:  perl(PPI::Document)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(version)
# Tests only:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(PPI::Dumper)
BuildRequires:  perl(Test::More)
# Optional tests only:
BuildRequires:  perl(Perl::MinimumVersion)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(IO::String) >= 1.02
Requires:       perl(List::MoreUtils) >= 0.24
Requires:       perl(Perl::Critic) >= 1.084
Requires:       perl(Pod::MinimumVersion) >= 50
Requires:       perl(PPI) >= 1.212
Requires:       perl(PPI::Document)
# This is plug-in into Test::More. Depend on it even if not mentioned in the
# code.
Requires:       perl(Test::More)

# Filter underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(List::MoreUtils\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Policy\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Utils\\)\\s*$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::Utils\\) >= 0\\.21$
%global __requires_exclude %__requires_exclude|perl\\(Perl::Critic::PodParser::ProhibitVerbatimMarkup\\)\\s*$
# Filter private redefinitions
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Perl::MinimumVersion\\)\\s*$
# Filter private parsers 
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::PodParser::ProhibitVerbatimMarkup\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Policy::Documentation::ProhibitAdjacentLinks::Parser\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodMinimumVersionViolation\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitBadAproposMarkup\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitLinkToSelf\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitParagraphTwoDots\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::ProhibitUnbalancedParens\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::PodParser::RequireLinkedURLs\\)\\s*$
%global __provides_exclude %__provides_exclude|perl\\(Perl::Critic::Pulp::ProhibitDuplicateHashKeys::Qword\\)\\s*$

%description
This is a collection of add-on policies for Perl::Critic.  They're under
a "pulp" theme plus other themes according to their purpose (see "POLICY
THEMES" in Perl::Critic).

%prep
%setup -q -n Perl-Critic-Pulp-%{version}

%build
perl Makefile.PL INSTALLDIRS=perl OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes COPYING README
%{perl_privlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Petr Pisar <ppisar@redhat.com> - 85-1
- 85 version bump

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 84-1
- 84 version bump

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 83-1
- 83 version bump

* Mon Apr 28 2014 Petr Pisar <ppisar@redhat.com> - 82-1
- 82 version bump

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 81-1
- 81 version bump

* Thu Apr 03 2014 Petr Pisar <ppisar@redhat.com> - 80-2
- Restore compatibility with version-0.9907 (#1083991)

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 80-1
- 80 version bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 79-2
- Perl 5.18 rebuild

* Wed Mar 20 2013 Petr Pisar <ppisar@redhat.com> - 79-1
- 79 bump

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> - 78-1
- 78 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 77-1
- 77 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Pisar <ppisar@redhat.com> - 76-1
- 76 bump

* Mon Nov 26 2012 Petr Pisar <ppisar@redhat.com> - 75-1
- 75 bump

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 74-1
- 74 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Petr Pisar <ppisar@redhat.com> - 73-2
- Perl 5.16 rebuild

* Mon Jul 02 2012 Petr Pisar <ppisar@redhat.com> - 73-1
- 73 bump

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 72-2
- Perl 5.16 rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 72-1
- 72 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 71-1
- 71 bump

* Fri May 18 2012 Petr Pisar <ppisar@redhat.com> - 70-1
- 70 bump

* Mon Jan 30 2012 Petr Pisar <ppisar@redhat.com> - 69-1
- 69 bump

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 68-1
- 68 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 67-1
- 67 bump

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 66-1
- 66 bump

* Mon Sep 19 2011 Petr Pisar <ppisar@redhat.com> - 65-1
- 65 bump

* Mon Aug 22 2011 Petr Pisar <ppisar@redhat.com> - 64-1
- 64 bump

* Tue Jul 26 2011 Petr Pisar <ppisar@redhat.com> - 62-1
- 62 bump
- Remove RPM 4.8 filters

* Tue Jul 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 61-3
- add RPM4.9 macro filter

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 61-2
- Perl mass rebuild

* Mon Jun 06 2011 Petr Pisar <ppisar@redhat.com> - 61-1
- Version 61 bump

* Mon May 23 2011 Petr Pisar <ppisar@redhat.com> - 60-2
- Remove explicit defattr

* Mon May 23 2011 Petr Pisar <ppisar@redhat.com> - 60-1
- Version 60 bump

* Tue May 10 2011 Petr Pisar <ppisar@redhat.com> - 59-1
- Version 59 bump

* Tue May 10 2011 Petr Pisar <ppisar@redhat.com> - 58-1
- Version 58 bump

* Fri May 06 2011 Petr Pisar <ppisar@redhat.com> - 57-1
- Version 57 bump

* Thu Apr 28 2011 Petr Pisar <ppisar@redhat.com> - 56-1
- Version 56 bump
- Do not provide private parsers

* Tue Apr 26 2011 Petr Pisar <ppisar@redhat.com> - 55-1
- Version 55 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 54-1
- 54 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 51-1
- Version 51 bump

* Thu Apr 21 2011 Petr Pisar <ppisar@redhat.com> - 46-2
- Do not provide Perl::MinimumVersion

* Tue Jan 25 2011 Petr Pisar <ppisar@redhat.com> 46-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuidRoot stuff
- Install into perl core direcotory
- Make the package no-architecture depndend (the XS compilation is test-time)
