%global pkgname Test-TrailingSpace

Name:           perl-Test-TrailingSpace
Version:        0.0205
Release:        1%{?dist}
Summary:        Test for trailing space in source files
License:        MIT
URL:            http://search.cpan.org/dist/Test-TrailingSpace/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Module::Build) >= 0.28
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(autodie)
BuildRequires:  perl(File::Find::Object::Rule) >= 0.0301
BuildRequires:  perl(Test::More)
# Tests:
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
# Pod::Coverage::TrustPod 1.08 not used
BuildRequires:  perl(Test::Builder::Tester)
# Test::CPAN::Changes not used
# Test::Pod 1.41 not used
# Test::Pod::Coverage 1.08 not used
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is used to test for lack of trailing space.

%prep
%setup -qn %{pkgname}-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Sep 09 2015 Petr Pisar <ppisar@redhat.com> - 0.0205-1
- 0.0205 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0204-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.0204-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.0204-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Christopher Meng <rpm@cicku.me> - 0.0204-1
- Update to 0.0204

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Christopher Meng <rpm@cicku.me> - 0.0203-1
- Initial Package.
