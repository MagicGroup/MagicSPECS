# This file is licensed under the terms of GNU GPLv2+.
Name:           perl-DynaLoader-Functions
Version:        0.002
Release:        6%{?dist}
Summary:        Deconstructed dynamic C library loading
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DynaLoader-Functions/
Source0:        http://www.cpan.org/authors/id/Z/ZE/ZEFRAM/DynaLoader-Functions-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
# Tests:
BuildRequires:  perl(Test::More)
# Optional tests:
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.280209
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(DynaLoader)

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(VMS::Filespec\\)

%description
This module provides a function-based interface to dynamic loading as used
by Perl. Some details of dynamic loading are very platform-dependent, so
correct use of these functions requires the programmer to be mindful of the
space of platform variations.

%prep
%setup -q -n DynaLoader-Functions-%{version}

%build
perl Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.002-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.002-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.002-4
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.002-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.002-1
- 0.002 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 0.001-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.001-4
- Perl 5.16 rebuild

* Thu Jun 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.001-3
- Update Requires
- Exclude requires VMS::Filespec.

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.001-2
- Perl 5.16 rebuild

* Thu Feb 09 2012 Petr Pisar <ppisar@redhat.com> - 0.001-1
- 0.001 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.000-2
- Perl mass rebuild

* Mon Jul 11 2011 Petr Pisar <ppisar@redhat.com> 0.000-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr
