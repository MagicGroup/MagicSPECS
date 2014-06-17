Name:		perl-ExtUtils-InstallPaths
Version:	0.010
Release:	3%{?dist}
Summary:	Build.PL install path logic made easy
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/ExtUtils-InstallPaths
Source0:	http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::Config) >= 0.002
BuildRequires:	perl(File::Spec)
# Test Suite
BuildRequires:	perl(Config)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::More)
# Release Tests
# perl-Pod-Coverage-TrustPod -> perl-Pod-Eventual -> perl-Mixin-Linewise ->
#   perl-YAML-Tiny -> perl-Module-Build-Tiny -> perl-ExtUtils-InstallPaths
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module tries to make install path resolution as easy as possible.

When you want to install a module, it needs to figure out where to install
things. The nutshell version of how this works is that default installation
locations are determined from ExtUtils::Config, and they may be individually
overridden by using the install_path attribute. An install_base attribute lets
you specify an alternative installation root like /home/foo and prefix does
something similar in a rather different (and more complicated) way. destdir
lets you specify a temporary installation directory like /tmp/install in case
you want to create bundled-up installable packages.

%prep
%setup -q -n ExtUtils-InstallPaths-%{version}

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
%{_mandir}/man3/ExtUtils::InstallPaths.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.010-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Deprecated usage of legacy configuration variables
  - Generate default paths more dynamically

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.009-6
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.009-4
- Perl 5.18 rebuild

* Tue Apr 16 2013 Paul Howarth <paul@city-fan.org> - 0.009-3
- Drop non-dual-lived buildreqs (#947454)

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.009-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.009-1
- Initial RPM version
