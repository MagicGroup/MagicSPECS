Name:           perl-Log-Any-Adapter
Version:        0.06
Release:        3%{?dist}
Summary:        Tell Log::Any where to send its logs
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Log-Any-Adapter/
Source0:        http://www.cpan.org/authors/id/J/JS/JSWARTZ/Log-Any-Adapter-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Devel::GlobalDestruction)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(Guard)
BuildRequires:  perl(Log::Any) >= 0.10
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Requires:       perl(Log::Any) >= 0.10
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Log::Any\\)

%description
The Log-Any-Adapter distribution implements Log::Any class methods to
specify where logs should be sent. It is a separate distribution so as to
keep Log::Any itself as simple and unchanging as possible.

%prep
%setup -q -n Log-Any-Adapter-%{version}

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
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-2
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.06-1
- Upstream update.
- Reflect upstream having abandoned using ExtUtils::AutoInstall.
- Spec cleanup.
- Add rpm-4.9 filter.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.03-2
- Perl mass rebuild

* Sun Feb 06 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.03-1
- Initial Fedora package.
