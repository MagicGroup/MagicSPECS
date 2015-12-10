# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'printf "%d\\n", $Test::More::VERSION < 0.88 ? 1 : 0;' 2>/dev/null || echo 0)

# We don't really need ExtUtils::MakeMaker > 6.31
%global old_eumm %(perl -MExtUtils::MakeMaker -e 'printf "%d\\n", $ExtUtils::MakeMaker::VERSION < 6.31 ? 1 : 0;' 2>/dev/null || echo 0)

Name:		perl-Dist-CheckConflicts
Version:	0.11
Release:	4%{?dist}
Summary:	Declare version conflicts for your dist
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Dist-CheckConflicts/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Dist-CheckConflicts-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(List::MoreUtils) >= 0.12
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Sub::Exporter)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
One shortcoming of the CPAN clients that currently exist is that they have no
way of specifying conflicting downstream dependencies of modules. This module
attempts to work around this issue by allowing you to specify conflicting
versions of modules separately, and deal with them after the module is done
installing.

For instance, say you have a module Foo, and some other module Bar uses Foo. If
Foo were to change its API in a non-backwards-compatible way, this would cause
Bar to break until it is updated to use the new API. Foo can't just depend on
the fixed version of Bar, because this will cause a circular dependency
(because Bar is already depending on Foo), and this doesn't express intent
properly anyway - Foo doesn't use Bar at all. The ideal solution would be for
there to be a way to specify conflicting versions of modules in a way that would
let CPAN clients update conflicting modules automatically after an existing
module is upgraded, but until that happens, this module will allow users to do
this manually.

%prep
%setup -q -n Dist-CheckConflicts-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
 RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Dist/
%{_mandir}/man3/Dist::CheckConflicts.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.11-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.11-3
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.11-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.02-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.02-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.02-6
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.02-5
- Pod::Coverage::TrustPod now available in all supported releases
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.02-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Paul Howarth <paul@city-fan.org> - 0.02-2
- Sanitize for Fedora submission

* Tue Jan  4 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Initial RPM version
