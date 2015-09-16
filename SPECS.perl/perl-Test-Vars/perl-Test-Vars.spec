Name:		perl-Test-Vars
Version:	0.008
Release:	1%{?dist}
Summary:	Detects unused variables
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Vars/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Test-Vars-%{version}.tar.gz
BuildArch:	noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl(Module::Build) >= 0.38
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(utf8)
BuildRequires:	sed
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl >= 4:5.10.0
BuildRequires:	perl(B)
BuildRequires:	perl(constant)
BuildRequires:	perl(ExtUtils::Manifest)
BuildRequires:	perl(IO::Pipe)
BuildRequires:	perl(parent)
BuildRequires:	perl(Storable)
BuildRequires:	perl(strict)
BuildRequires:	perl(Symbol)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(warnings)
# ===================================================================
# Test suite requirements
# ===================================================================
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(Test::Tester)
# ===================================================================
# Optional test requirements
# ===================================================================
%if !0%{?rhel:1} && !0%{?perl_bootstrap:1}
BuildRequires:	perl(Moose::Role)
%endif
# ===================================================================
# Author/Release test requirements
# ===================================================================
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Synopsis)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Test::Vars finds unused variables in order to keep the source code tidy.

%prep
%setup -q -n Test-Vars-%{version}

# Placate rpmlint about script interpreters in examples
sed -i -e '1s|^#!perl|#!/usr/bin/perl|' example/*.t

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} %{buildroot}

%check
./Build test
./Build test --test_files="xt/*.t"

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README.md example/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Vars.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.008-1
- 更新到 0.008

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.002-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.002-2
- 为 Magic 3.0 重建

* Wed Oct 10 2012 Paul Howarth <paul@city-fan.org> - 0.002-1
- Update to 0.002
  - Fix compatibility with Perl 5.16 (CPAN RT#72133)
- Drop upstreamed patch for 5.16 compatibility

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Paul Howarth <paul@city-fan.org> - 0.001-5
- Fix compatibility with Perl 5.16 (CPAN RT#72133)
- Don't need to remove empty directories from buildroot

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.001-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug  8 2011 Paul Howarth <paul@city-fan.org> - 0.001-2
- Sanitize for Fedora submission
- Clean up for modern rpm

* Mon Aug  8 2011 Paul Howarth <paul@city-fan.org> - 0.001-1
- Initial RPM version
