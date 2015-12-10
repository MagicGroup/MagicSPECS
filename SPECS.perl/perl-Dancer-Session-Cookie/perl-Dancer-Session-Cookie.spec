Name:           perl-Dancer-Session-Cookie
Version:	0.27
Release:	3%{?dist}
Summary:        Encrypted cookie-based session back-end for Dancer
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Dancer-Session-Cookie/
Source0:        http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Dancer-Session-Cookie-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Crypt::CBC)
BuildRequires:  perl(Crypt::Rijndael)
BuildRequires:  perl(Dancer) >= 1.13
BuildRequires:  perl(Dancer::Config)
BuildRequires:  perl(Dancer::Session::Abstract)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Storable)
BuildRequires:  perl(String::CRC32)
# Tests only:
BuildRequires:  perl(Dancer::ModuleLoader)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
# Optional tests:
BuildRequires:  perl(Dancer::Config)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(LWP)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Test::TCP)
BuildRequires:  perl(Test::Pod) >= 1.22
BuildRequires:  perl(YAML)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Dancer) >= 1.13
Requires:       perl(String::CRC32)

# Do not export unde-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Dancer\\)\\s*$

%description
This module implements a session engine for sessions stored entirely in
cookies. Usually only session ID is stored in cookies and the session data
itself are saved in some external storage, e.g. database. This module allows to
avoid using external storage at all.

%prep
%setup -q -n Dancer-Session-Cookie-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.27-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.27-2
- 更新到 0.27

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.26-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.26-1
- 更新到 0.26

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.15-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.15-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> 0.15-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot and defattr from spec code.
