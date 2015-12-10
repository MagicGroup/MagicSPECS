Name:           perl-Test-Pod-LinkCheck
Version:        0.008
Release:        6%{?dist}
Summary:        Tests POD for invalid links
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Pod-LinkCheck/
Source0:        http://www.cpan.org/authors/id/A/AP/APOCAL/Test-Pod-LinkCheck-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
# ExtUtils::MakeMaker not used
BuildRequires:  perl(Module::Build::Tiny) >= 0.039
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(App::PodLinkCheck::ParseLinks) >= 4
BuildRequires:  perl(App::PodLinkCheck::ParseSections)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Moose) >= 1.01
BuildRequires:  perl(Moose::Util::TypeConstraints) >= 1.01
BuildRequires:  perl(parent)
BuildRequires:  perl(Pod::Find)
BuildRequires:  perl(Test::Builder) >= 0.94
BuildRequires:  perl(Test::Pod) >= 1.44
# Tests:
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Tester)
# Optional tests:
%if %{undefined perl_bootstrap}
# Break build-time cycle with perl-Test-Apocalypse

# Disable using of Test::Apocalypse, because it cannot be built with Perl 5.22
# due to failing perl-Test-Vars
%if ! 0%(perl -e 'print $] >= 5.022')
BuildRequires:  perl(Test::Apocalypse) >= 1.000
%endif
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(App::PodLinkCheck::ParseSections)
Requires:       perl(Capture::Tiny)
Requires:       perl(Config)
Requires:       perl(File::Spec)
Requires:       perl(Pod::Find)

%description
This module looks for any links in your POD and verifies that they point to
a valid resource. It uses the Pod::Simple parser to analyze the pod files
and look at their links. In a nutshell, it looks for L<Foo> links and makes
sure that Foo exists. It also recognizes section links, L</SYNOPSIS> for
example. Also, manual pages are resolved and checked.

%prep
%setup -q -n Test-Pod-LinkCheck-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install "--destdir=$RPM_BUILD_ROOT" --create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc AUTHOR_PLEDGE Changes CommitLog examples LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.008-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.008-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-3
- Perl 5.22 re-rebuild of bootstrapped packages
- Disable using of Test::Apocalypse with Perl 5.22

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-2
- Perl 5.22 rebuild

* Tue Nov 04 2014 Petr Pisar <ppisar@redhat.com> - 0.008-1
- 0.008 bump

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-11
- Perl 5.20 re-rebuild of bootstrapped packages

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-10
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.007-8
- Perl 5.18 re-rebuild of bootstrapped packages
- Specify all dependencies
- Remove perl_bootstrap definition

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.007-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.007-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.007-2
- Perl 5.16 rebuild

* Wed Apr 25 2012 Petr Pisar <ppisar@redhat.com> 0.007-1
- Specfile autogenerated by cpanspec 1.78.
