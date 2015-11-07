# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION) < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-File-Slurp-Tiny
Version:	0.004
Release:	3%{?dist}
Summary:	A simple, sane and efficient file slurper
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/File-Slurp-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/File-Slurp-Tiny-%{version}.tar.gz
Patch0:		File-Slurp-Tiny-0.003-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides functions for fast and correct slurping and spewing
of files.

%prep
%setup -q -n File-Slurp-Tiny-%{version}

# Test suite needs patching if we have Test::More < 0.88
%if %{old_test_more}
%patch0
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/File/
%{_mandir}/man3/File::Slurp::Tiny.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.004-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.004-2
- 为 Magic 3.0 重建

* Thu Jul 16 2015 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004
  - Add discouragement notice (File::Slurper is a better choice)
  - Don't skip '.\n' and '..\n' in read_dir
  - Don't install benchmark.pl
- Use %%license where possible
- Release tests no longer part of main test suite

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-6
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.003-5
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Paul Howarth <paul@city-fan.org> - 0.003-3
- Make %%description explicit about the module operating on files
  (#1064995)

* Thu Feb 13 2014 Paul Howarth <paul@city-fan.org> - 0.003-2
- Sanitize for Fedora submission

* Thu Feb 13 2014 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
