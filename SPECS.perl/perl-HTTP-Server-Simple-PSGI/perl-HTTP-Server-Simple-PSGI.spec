Name:           perl-HTTP-Server-Simple-PSGI
Version:	0.16
Release:	3%{?dist}
Summary:        PSGI handler for HTTP::Server::Simple
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTTP-Server-Simple-PSGI/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/HTTP-Server-Simple-PSGI-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Server::Simple) >= 0.42
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
HTTP::Server::Simple::PSGI is a HTTP::Server::Simple based HTTP server that
can run PSGI applications. This module only depends on
HTTP::Server::Simple, which itself doesn't depend on any non-core modules
so it's best to be used as an embedded web server.

%prep
%setup -q -n HTTP-Server-Simple-PSGI-%{version}

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
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.16-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.16-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.16-1
- 更新到 0.16

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-3
- Perl mass rebuild

* Mon Mar 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.14-2
- Spec cleanup.

* Sun Jan 16 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.14-1
- Initial Fedora package.
