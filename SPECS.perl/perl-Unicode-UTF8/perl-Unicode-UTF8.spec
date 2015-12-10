Summary:	Encoding and decoding of UTF-8 encoding form
Name:		perl-Unicode-UTF8
Version:	0.60
Release:	7%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Unicode-UTF8/
Source0:	http://search.cpan.org/CPAN/authors/id/C/CH/CHANSEN/Unicode-UTF8-%{version}.tar.gz
# Module Build
BuildRequires:	perl(ExtUtils::MakeMaker)
%if "%{?rhel}" != "6"
BuildRequires:	perl(inc::Module::Install)
BuildRequires:	perl(Module::Install::ReadmeFromPod)
%else
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(Pod::Text)
BuildRequires:	perl(vars)
%endif
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(Encode) >= 1.9801
BuildRequires:	perl(IO::File)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Fatal) >= 0.006
BuildRequires:	perl(Test::More) >= 0.47
# Optional Tests
BuildRequires:	perl(Taint::Runtime) >= 0.03
BuildRequires:	perl(Test::LeakTrace) >= 0.10
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Variable::Magic)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Exporter)
Requires:	perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides functions to encode and decode UTF-8 encoding form as
specified by Unicode and ISO/IEC 10646:2011.

%prep
%setup -q -n Unicode-UTF8-%{version}

# Unbundle inc::Module::Install, we'll use system version instead
# unless we're on EL-6, where there's no Module::Install::ReadmeFromPod
%if "%{?rhel}" != "6"
rm -rf inc/
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/Unicode/
%{perl_vendorarch}/auto/Unicode/
%{_mandir}/man3/Unicode::UTF8.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.60-7
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.60-6
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.60-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.60-4
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.60-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Paul Howarth <paul@city-fan.org> - 0.60-1
- Update to 0.60
  - Added valid_utf8()
  - Skip copy-on-write tests on Perl 5.19

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-3
- BR: perl(Scalar::Util) for the test suite (#1003650)
- Add buildreqs for deps of bundled inc::Module::Install for EL-6 build

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-2
- Sanitize for Fedora submission

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-1
- Initial RPM build
