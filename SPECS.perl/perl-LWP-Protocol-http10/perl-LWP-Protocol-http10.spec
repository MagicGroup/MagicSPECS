Name:           perl-LWP-Protocol-http10
Version:	6.03
Release:	3%{?dist}
Summary:        Legacy HTTP/1.0 support for LWP
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/LWP-Protocol-http10/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/LWP-Protocol-http10-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Response) >= 6
BuildRequires:  perl(HTTP::Status) >= 6
BuildRequires:  perl(LWP::Protocol) >= 6

Requires:       perl(HTTP::Response) >= 6
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(HTTP::Response\\)
Requires:       perl(HTTP::Status) >= 6
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(HTTP::Status\\)
Requires:       perl(LWP::Protocol) >= 6
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(LWP::Protocol\\)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Make optional dependency mandatory
Requires:       perl(URI::Escape)

%description
The LWP::Protocol::http10 module provides support for using HTTP/1.0
protocol with LWP. To use it you need to call LWP::Protocol::implementor()
to override the standard handler for http URLs.

%prep
%setup -q -n LWP-Protocol-http10-%{version}

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
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 6.03-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 6.03-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 6.03-1
- 更新到 6.03

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.02-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 6.02-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 6.02-4
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 6.02-3
- Rework filters.

* Fri Jun 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 6.02-2
- Reflect feedback from package review.

* Mon Apr 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 6.02-1
- Specfile autogenerated by cpanspec 1.78.
