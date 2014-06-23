Name:		perl-Test-Perl-Critic
Summary:	Use Perl::Critic in test programs
Version:	1.02
Release:	14%{?dist}
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-Perl-Critic/
Source0:	http://search.cpan.org/CPAN/authors/id/T/TH/THALJEF/Test-Perl-Critic-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(English)
BuildRequires:	perl(Module::Build) >= 0.35
BuildRequires:	perl(Perl::Critic) >= 1.105
BuildRequires:	perl(Perl::Critic::Utils) >= 1.105
BuildRequires:	perl(Perl::Critic::Violation) >= 1.105
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Perl::Critic) >= 1.105
Requires:	perl(Perl::Critic::Utils) >= 1.105
Requires:	perl(Perl::Critic::Violation) >= 1.105

# Avoid doc-file dependencies from tests
%{?perl_default_filter}

# Obsolete/provide old -tests subpackage (can be removed in F19 development cycle)
Obsoletes:	%{name}-tests < %{version}-%{release}
Provides:	%{name}-tests = %{version}-%{release}

%description
Test::Perl::Critic wraps the Perl::Critic engine in a convenient
subroutine suitable for test programs written using the Test::More
framework. This makes it easy to integrate coding-standards enforcement
into the build process. For ultimate convenience (at the expense of some
flexibility), see the criticism pragma.

%prep
%setup -q -n Test-Perl-Critic-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
TEST_AUTHOR=1 ./Build test

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README %{?perl_default_filter:t/ xt/}
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Perl::Critic.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.02-14
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Pisar <ppisar@redhat.com> - 1.02-11
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.02-8
- Perl 5.16 rebuild

* Wed Mar 21 2012 Paul Howarth <paul@city-fan.org> - 1.02-7
- Drop -tests subpackage (general lack of interest in this), but include
  them as documentation for the main package
- Drop redundant BR: perl(ExtUtils::MakeMaker)
- Drop redundant unversioned explicit requires
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands
- Run the author tests in %%check
- BR: perl(Test::Pod) and perl(Test::Pod::Coverage)
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.02-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.02-1
- Update by Fedora::App::MaintainerTools 0.006
- Updating to latest GA CPAN version (1.02)
- Added a new br on perl(Carp) (version 0)
- Added a new br on perl(English) (version 0)
- Altered br on perl(Module::Build) (0 => 0.35)
- Altered br on perl(Perl::Critic) (0.21 => 1.105)
- Added a new br on perl(Perl::Critic::Utils) (version 1.105)
- Added a new br on perl(Perl::Critic::Violation) (version 1.105)
- Added a new br on perl(Test::Builder) (version 0)
- Added a new br on perl(Test::More) (version 0)
- Force-adding ExtUtils::MakeMaker as a BR
- Dropped old BR on perl(Test::Pod)
- Dropped old BR on perl(Test::Pod::Coverage)
- Added a new req on perl(Carp) (version 0)
- Added a new req on perl(English) (version 0)
- Added a new req on perl(Perl::Critic) (version 1.105)
- Added a new req on perl(Perl::Critic::Utils) (version 1.105)
- Added a new req on perl(Perl::Critic::Violation) (version 1.105)
- Added a new req on perl(Test::Builder) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.01-8
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-5
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-4
- Disable tests, take out patch, doesn't fix test failures

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-3
- Patch for test failure

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.01-2
- Rebuild for new perl

* Sat Jan 27 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01

* Sun Nov 12 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.08-1
- Update to 0.08

* Sat Sep 23 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.07-1
- First build
