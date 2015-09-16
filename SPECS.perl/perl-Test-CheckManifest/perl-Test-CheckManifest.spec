Name:           perl-Test-CheckManifest
Version:	1.29
Release:	1%{?dist}
Summary:        Check if your Manifest matches your distro
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-CheckManifest/
Source0:        http://www.cpan.org/authors/id/R/RE/RENEEB/Test-CheckManifest-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This package checks whether the Manifest file matches the distro or not. To
match a distro the Manifest has to name all files that come along with the
distribution.

%prep
# Unpackage tarball in a subdirectory, otherwise the testsuite will fail.
%setup -q -c -n %{name}-%{version}
%setup -q -T -D -n %{name}-%{version} -a0

%build
cd Test-CheckManifest-%{version}
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
cd ..

%install
cd Test-CheckManifest-%{version}
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
cd ..

%check
cd Test-CheckManifest-%{version}

cd ..

%files
%defattr(-,root,root,-)
%doc Test-CheckManifest-%{version}/Changes Test-CheckManifest-%{version}/README Test-CheckManifest-%{version}/LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.29-1
- 更新到 1.29

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.26-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.26-2
- 为 Magic 3.0 重建

* Sun Aug 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.26-1
- Upstream update.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Perl 5.16 rebuild

* Sun Feb 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.25-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.24-2
- Perl mass rebuild

* Sun Apr 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.24-1
- Upstream update.

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.23-1
- Upstream update.
- Add LICENSE file.
- Spec cleanup.

* Tue Mar 01 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.22-2
- Extend %%description upon reviewer's request.

* Sat Feb 05 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.22-1
- Initial Fedora package.
