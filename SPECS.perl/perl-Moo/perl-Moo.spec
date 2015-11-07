Name:           perl-Moo
Version:	2.000002
Release:	3%{?dist}
Summary:        Minimalist Object Orientation (with Moose compatibility)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Moo/
Source0:        http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Moo-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Method::Modifiers) >= 1.10
BuildRequires:  perl(Devel::GlobalDestruction) >= 0.11
BuildRequires:  perl(Dist::CheckConflicts) >= 0.02
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Runtime) >= 0.012
BuildRequires:  perl(overload)
BuildRequires:  perl(Role::Tiny) >= 1.003002
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strictures) >= 1.004003
BuildRequires:  perl(Test::Fatal) >= 0.003
BuildRequires:  perl(Test::More) >= 0.96
Requires:       perl(Class::Method::Modifiers) >= 1.10
Requires:       perl(Role::Tiny) >= 1.003002
Requires:       perl(Class::MOP)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl(Moo::Conflicts)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}perl\\(Moo::_
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}perl\\(Moo::_

%description
This module is an extremely light-weight, high-performance Moose
replacement. It also avoids depending on any XS modules to allow simple
deployments. The name Moo is based on the idea that it provides almost -but
not quite- two thirds of Moose.

%prep
%setup -q -n Moo-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.000002-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 2.000002-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.000002-1
- 更新到 2.000002

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.003001-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.003001-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 1.003001-2
- Role::Tiny is now >= 1.003002

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 1.003001-1
- 1.003001 bump
- Source URL was changed in this release

* Fri Aug 16 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003000-2
- Added perl(Moo::Conflicts) to provides

* Fri Aug 09 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003000-1
- 1.003000 bump
- Update source link
- Specify all dependencies

* Thu Aug 08 2013 Petr Pisar <ppisar@redhat.com> - 1.002000-3
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 07 2013 Iain Arnell <iarnell@gmail.com> 1.002000-1
- update to latest upstream version

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.001000-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.000008-1
- update to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 05 2013 Iain Arnell <iarnell@gmail.com> 1.000007-1
- update to latest upstream version

* Sat Oct 27 2012 Iain Arnell <iarnell@gmail.com> 1.000005-1
- update to latest upstream version

* Fri Oct 19 2012 Iain Arnell <iarnell@gmail.com> 1.000004-1
- update to latest upstream version

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 1.000003-1
- update to latest upstream version

* Sun Jul 29 2012 Iain Arnell <iarnell@gmail.com> 1.000001-1
- update to latest upstream version

* Thu Jul 26 2012 Iain Arnell <iarnell@gmail.com> 1.000000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 20 2012 Iain Arnell <iarnell@gmail.com> 1.000000-1
- update to latest upstream version
- explicity require Role::Tiny >= 1.001003

* Tue Jul 17 2012 Iain Arnell <iarnell@gmail.com> 0.091014-1
- update to latest upstream version

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.091007-2
- Perl 5.16 rebuild

* Sat May 19 2012 Iain Arnell <iarnell@gmail.com> 0.091007-1
- update to latest upstream version

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 0.009014-1
- update to latest upstream version

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> 0.009013-1
- update to latest upstream version

* Sun Nov 20 2011 Iain Arnell <iarnell@gmail.com> 0.009012-1
- update to latest upstream version
- filter private requires/provides

* Mon Oct 10 2011 Iain Arnell <iarnell@gmail.com> 0.009011-1
- update to latest upstream version

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.009010-1
- Specfile autogenerated by cpanspec 1.79.
