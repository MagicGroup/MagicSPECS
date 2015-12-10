Name:           perl-autodie
Version:	2.29
Release:	3%{?dist}
Summary:        Replace functions with ones that succeed or die
Summary(zh_CN.UTF-8): 把函数替换成执行成功或失败
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/autodie/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PJ/PJF/autodie-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(if)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(IPC::System::Simple) >= 0.12
%endif
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Sub::Identify is optional
BuildRequires:  perl(Tie::RefHash)
# Tests:
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(BSD::Resource)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)
Requires:       perl(Fcntl)
# Keep IPC::System::Simple 0.12 optional
Requires:       perl(overload)
Requires:       perl(POSIX)

# Remove falsely detected perl(lib)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(lib\\)$

%description
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".

%description -l zh_CN.UTF-8
把函数替换成执行成功或失败。

%prep
%setup -q -n autodie-%{version}
find -type f -exec chmod -x {} +

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
make test

%files
%doc AUTHORS Changes LICENSE README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.29-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.29-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.29-1
- 更新到 2.29

* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 2.26-1
- 更新到 2.26

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.25-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 2.25-1
- 2.25 bump

* Mon Mar 31 2014 Petr Pisar <ppisar@redhat.com> - 2.24-1
- 2.24 bump

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 2.23-1
- 2.23 bump

* Mon Sep 23 2013 Petr Pisar <ppisar@redhat.com> - 2.22-1
- 2.22 bump

* Thu Sep 12 2013 Petr Pisar <ppisar@redhat.com> - 2.21-1
- 2.21 bump

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.20-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.20-2
- Perl 5.18 rebuild

* Mon Jul 01 2013 Petr Pisar <ppisar@redhat.com> - 2.20-1
- 2.20 bump

* Wed Mar 06 2013 Petr Pisar <ppisar@redhat.com> - 2.16-1
- 2.16 bump

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> 2.13-1
- Specfile autogenerated by cpanspec 1.78.
