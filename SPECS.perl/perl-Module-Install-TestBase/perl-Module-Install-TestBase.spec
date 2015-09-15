Name:           perl-Module-Install-TestBase
Version:        0.86
Release:        5%{?dist}
Summary:        Module::Install support for Test::Base
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Install-TestBase/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/Module-Install-TestBase-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
# Filter::Util::Call not used at tests
# The Module::Install::Base version contrain is phony, bug #1134351,
# <https://github.com/ingydotnet/module-install-testbase-pm/issues/2>
BuildRequires:  perl(Module::Install::Base)
# Spiffy not used at tests
# Test::Base 0.86 not used at tests
# Test::Base::Filter not used at tests
# Test::Builder not used at tests
# Test::Builder::Module not used at tests
# Test::More not used at tests
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Test::More)
# Test::Pod not used
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(Filter::Util::Call)
Requires:   perl(Spiffy)
Requires:   perl(Test::Base) >= 0.86
Requires:   perl(Test::Base::Filter)
Requires:   perl(Test::Builder)
Requires:   perl(Test::Builder::Module)
Requires:   perl(Test::More)
# Module::Install::TestBase splitted from Test-Base in 0.85
Conflicts:  perl-Test-Base < 0.85

%description
This Perl module adds the use_test_base directive to Module::Install. Now you
can get full Test-Base support for you module with no external dependency on
Test::Base.

%prep
%setup -q -n Module-Install-TestBase-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-4
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.86-3
- Perl 5.20 rebuild

* Thu Aug 28 2014 Petr Pisar <ppisar@redhat.com> - 0.86-2
- Do not require exact version of Module::Install::Base (bug #1134351)

* Wed Aug 27 2014 Petr Pisar <ppisar@redhat.com> 0.86-1
- Specfile autogenerated by cpanspec 1.78.