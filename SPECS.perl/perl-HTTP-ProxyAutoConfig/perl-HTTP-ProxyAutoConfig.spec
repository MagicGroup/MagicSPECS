Name:           perl-HTTP-ProxyAutoConfig
Version:        0.3
Release:        7%{?dist}
Summary:        Use a .pac or wpad.dat file to get proxy information
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTTP-ProxyAutoConfig/
Source0:        http://www.cpan.org/authors/id/M/MA/MACKENNA/HTTP-ProxyAutoConfig-%{version}.tar.gz
Source1:        LICENSE.correspondence
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.56
%{?_with_network_tests:
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::UserAgent) >= 5.834
BuildRequires:  perl(Test::More)
}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
HTTP::ProxyAutoConfig allows perl scripts that need to access the Internet
to determine whether to do so via a proxy server. To do this, it uses proxy
settings provided by an IT department, either on the Web or in a browser's
.pac file on disk.

%prep
%setup -q -n HTTP-ProxyAutoConfig-%{version}
cp %{SOURCE1} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
# tests require network access, disabled by default
%{?_with_network_tests: }

%files
%doc Changes examples README LICENSE.correspondence
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.3-7
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.3-6
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.3-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.3-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.3-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.3-2
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Petr Šabata <contyk@redhat.com> 0.3-1
- Specfile autogenerated by cpanspec 1.78.
