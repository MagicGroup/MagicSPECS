Name:		perl-Archive-Any-Lite
Version:	0.10
Release:	4%{?dist}
Summary:	Simple CPAN package extractor 
Summary(zh_CN.UTF-8): 简单的 CPAN 包解压器
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/Archive-Any-Lite
Source0:	http://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Archive-Any-Lite-%{version}.tar.gz
Patch0:		Archive-Any-Lite-0.08-EU:MM.patch
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Archive::Tar) >= 1.76
BuildRequires:	perl(Archive::Zip)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Uncompress::Bunzip2)
BuildRequires:	perl(IO::Zlib)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(FindBin)
BuildRequires:	perl(Test::More) >= 0.82
BuildRequires:	perl(Test::UseAllModules) >= 0.10
# Optional Tests
BuildRequires:	perl(Parallel::ForkManager) >= 0.7.6
BuildRequires:	perl(Test::Pod) >= 1.18
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(IO::Uncompress::Bunzip2)
Requires:	perl(IO::Zlib)

%description
This is a fork of Archive::Any by Michael Schwern and Clint Moore. The main
difference is that this works properly even when you fork(), and may require
less memory to extract a tarball. On the other hand, this isn't pluggable
(it only supports file formats used in the CPAN toolchains), and it doesn't
check MIME types.

%description -l zh_CN.UTF-8
简单的 CPAN 包解压器。

%prep
%setup -q -n Archive-Any-Lite-%{version}

# Build with ExtUtils::MakeMaker rather than ExtUtils::MakeMaker::CPANfile
%patch0

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}
magic_rpm_clean.sh

%check
make test TEST_POD=1

%files
%doc Changes README
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive::Any::Lite.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.10-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.10-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.10-1
- 更新到 0.10

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.09-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09
  - Updated version requirements

* Fri Apr 18 2014 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Support an optional hash reference for finer extraction control
- Add patch to build with ExtUtils::MakeMaker rather than
  ExtUtils::MakeMaker::CPANfile
- Since we now need Archive::Tar 1.76, the package can't build for EPEL < 7
  and so support for everything older can be dropped

* Sat Aug  3 2013 Paul Howarth <paul@city-fan.org> - 0.07-2
- Sanitize for Fedora submission

* Fri Aug  2 2013 Paul Howarth <paul@city-fan.org> - 0.07-1
- Initial RPM version
