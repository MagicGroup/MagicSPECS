# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION) < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-ExtUtils-Config
Version:	0.007
Release:	14%{?dist}
Summary:	A wrapper for perl's configuration
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/ExtUtils-Config
Source0:	http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Config)
BuildRequires:	perl(Data::Dumper)
# Test Suite
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Release Tests
# perl-Pod-Coverage-TrustPod -> perl-Pod-Eventual -> perl-Mixin-Linewise ->
#   perl-YAML-Tiny -> perl-Module-Build-Tiny -> perl-ExtUtils-Config
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
%endif
# Avoid Test::Kwalitee as it tries to verify the module's signature, which will fail
# if we have to patch Makefile.PL, tests etc. for old distribution support
BuildConflicts:	perl(Test::Kwalitee)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
ExtUtils::Config is an abstraction around the %%Config hash.

%prep
%setup -q -n ExtUtils-Config-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::Config.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.007-14
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.007-13
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.007-12
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.007-11
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.007-10
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.007-9
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.007-7
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.007-5
- Perl 5.18 rebuild

* Mon Jul 22 2013 Paul Howarth <paul@city-fan.org> - 0.007-4
- Avoid Test::Kwalitee as it tries to verify the module's signature, which will fail
  if we have to patch Makefile.PL, tests etc. for old distribution support

* Fri Jul  5 2013 Paul Howarth <paul@city-fan.org> - 0.007-3
- Don't BR: perl(Test::Kwalitee) when bootstrapping

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.007-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Initial RPM version
