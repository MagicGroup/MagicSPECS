# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'printf "%d\\n", $Test::More::VERSION < 0.88 ? 1 : 0;' 2>/dev/null || echo 0)

Name:		perl-Test-CheckChanges
Summary:	Check that the Changes file matches the distribution
Version:	0.14
Release:	15%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-CheckChanges/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GA/GAM/Test-CheckChanges-%{version}.tar.gz 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:	noarch
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Test::Exception)
BuildRequires:	perl(Test::More)
# Perl::Critic not available in EPEL-4
%if "%{?rhel}" != "4"
BuildRequires:	perl(Test::Perl::Critic)
%endif
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)

%description
This module checks that your Changes file has an entry for the current version
of the Module being tested. The version information for the distribution being
tested is taken out of the Build data, or if that is not found, out of the
Makefile. It then attempts to open, in order, a file with the name Changes or
CHANGES. The Changes file is then parsed for version numbers. If one and only
one of the version numbers matches, the test passes; otherwise the test fails.
A message with the current version is printed if the test passes; otherwise
diagnostic messages are printed to help explain the failure.

%prep
%setup -q -n Test-CheckChanges-%{version}

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
%defattr(-,root,root,-)
%doc Changes README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CheckChanges.3pm*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.14-15
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.14-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.14-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.14-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.14-3
- Perl mass rebuild

* Fri May  6 2011 Paul Howarth <paul@city-fan.org> - 0.14-2
- Sanitize for Fedora submission

* Fri May  6 2011 Paul Howarth <paul@city-fan.org> - 0.14-1
- Initial RPM version
