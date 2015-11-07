Name:           perl-Socket
Epoch:          1
Version:	2.020
Release:	4%{?dist}
Summary:        Networking constants and support functions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Socket/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Socket-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::Constant) >= 0.23
# ExtUtils::Constant::ProxySubs not used
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Scalar::Util is needed only if getaddrinfo(3) does not exist. Not our case.
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(XSLoader)
# Tests only:
BuildRequires:  perl(Errno)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides a variety of constants, structure manipulators and other
functions related to socket-based networking. The values and functions
provided are useful when used in conjunction with Perl core functions such as
socket(), setsockopt() and bind(). It also provides several other support
functions, mostly for dealing with conversions of network addresses between
human-readable and native binary forms, and for hostname resolver operations.

%prep
%setup -q -n Socket-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Artistic Changes Copying LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Socket*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1:2.020-4
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1:2.020-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1:2.020-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:2.020-1
- 更新到 2.020

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:2.014-5
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:2.014-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:2.014-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1:2.014-1
- 2.014 bump

* Tue Oct 29 2013 Petr Pisar <ppisar@redhat.com> - 1:2.013-1
- 2.013 bump

* Tue Sep 10 2013 Petr Pisar <ppisar@redhat.com> - 1:2.012-1
- 2.012 bump

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 1:2.011-1
- 2.011 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-3
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.010-1
- Increase epoch to compete with perl.spec

* Tue Jun 25 2013 Petr Pisar <ppisar@redhat.com> - 2.010-1
- 2.010 bump

* Fri May 24 2013 Petr Pisar <ppisar@redhat.com> - 2.009-3
- Specify all dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Pisar <ppisar@redhat.com> - 2.009-1
- 2.009 bump

* Thu Jan 03 2013 Petr Pisar <ppisar@redhat.com> - 2.008-1
- 2.008 bump

* Mon Dec 17 2012 Petr Pisar <ppisar@redhat.com> - 2.007-1
- 2.007 bump

* Thu Nov 08 2012 Petr Pisar <ppisar@redhat.com> - 2.006-2
- Update description

* Mon Aug 20 2012 Petr Pisar <ppisar@redhat.com> - 2.006-1
- 2.006 bump

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 2.005-1
- 2.005 bump

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 2.004-1
- 2.004 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2.002-2
- Perl 5.16 rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.002-1
- 2.002 bump

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.001-2
- Perl 5.16 rebuild

* Wed Mar 28 2012 Petr Pisar <ppisar@redhat.com> - 2.001-1
- 2.001 bump (bug-fixing release)

* Tue Mar 27 2012 Petr Pisar <ppisar@redhat.com> - 2.000-3
- Fix invalid write while unpacking AF_UNIX sockaddr (bug #806543)

* Mon Mar 19 2012 Petr Pisar <ppisar@redhat.com> - 2.000-2
- Increase release number due to F17 build

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 2.000-1
- 2.000 bump
- Fix a buffer overflow (RT#75623)

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> - 1.99-1
- 1.99 bump

* Thu Feb 16 2012 Petr Pisar <ppisar@redhat.com> - 1.98-1
- 1.98 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 1.97-1
- 1.97 bump
- License texts added

* Mon Dec 12 2011 Petr Pisar <ppisar@redhat.com> - 1.96-1
- 1.96 bump

* Fri Dec 02 2011 Petr Pisar <ppisar@redhat.com> - 1.95-1
- 1.95 bump

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> 1.94.07-1
- 1.94_07 packaged.
