Summary:	A Module::Build class for building XS modules
Name:		perl-Module-Build-XSUtil
Version:	0.16
Release:	1%{?dist}
License:	GPL+ or Artistic
URL:		https://github.com/hideo55/Module-Build-XSUtil
Source0:	https://cpan.metacpan.org/authors/id/H/HI/HIDEAKIO/Module-Build-XSUtil-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# Module Build
BuildRequires:	perl
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(utf8)
# Module
BuildRequires:	perl(Config)
BuildRequires:	perl(Devel::CheckCompiler)
BuildRequires:	perl(Devel::PPPort)
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test
BuildRequires:	perl(Capture::Tiny)
BuildRequires:	perl(Cwd::Guard)
BuildRequires:	perl(File::Copy::Recursive)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More) >= 0.88
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Devel::CheckCompiler)
Requires:	perl(Devel::PPPort)
Requires:	perl(ExtUtils::CBuilder)

%description
Module::Build::XSUtil is a subclass of Module::Build to support building XS
modules. It adds a number of compiler-related optional parameters to
Module::Build's "new" method.

%prep
%setup -q -n Module-Build-XSUtil-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Build::XSUtil.3*

%changelog
* Tue Jun 30 2015 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Fix regexp of _gcc_version for Ubuntu and Debian
  - Set -std=c99 explicitly for older GCC

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.15-2
- Perl 5.22 rebuild

* Fri Apr 24 2015 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Update XSHelper to fix STATIC_INLINE for gcc -std=c89

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 0.14-2
- Sanitize for Fedora submission

* Sat Oct  4 2014 Paul Howarth <paul@city-fan.org> - 0.14-1
- Initial RPM version
