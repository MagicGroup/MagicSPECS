# For initial import only; will be removed later
#global perl_bootstrap 1

Name:           perl-SOAP-Transport-TCP
Version:        0.715
Release:        8%{?dist}
Summary:        TCP Transport Support for SOAP::Lite
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/SOAP-Transport-TCP/
Source0:        http://www.cpan.org/authors/id/M/MK/MKUTTER/SOAP-Transport-TCP-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
# Avoid circular deps
%if !%{defined perl_bootstrap}
BuildRequires:  perl(File::Find)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::SessionData)
BuildRequires:  perl(IO::SessionSet)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(SOAP::Lite) >= 0.714
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::_server)
BuildRequires:  perl(Test::More)
%endif
Requires:       perl(SOAP::Lite) >= 0.714
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(SOAP::Lite\\)$

%description
The classes provided by this module implement direct TCP/IP communications
methods for both clients and servers.

%prep
%setup -q -n SOAP-Transport-TCP-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
# Avoid circular deps
%if !%{defined perl_bootstrap}
./Build test
%endif

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jan 15 2013 Liu Di <liudidi@gmail.com> - 0.715-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.715-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.715-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.715-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.715-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Petr Sabata <contyk@redhat.com> - 0.715-3
- Disable perl_bootstrap macro

* Wed Aug 24 2011 Petr Sabata <contyk@redhat.com> - 0.715-2
- Correcting various defects for the review

* Tue Aug 23 2011 Petr Sabata <contyk@redhat.com> 0.715-1
- Initial RPM
