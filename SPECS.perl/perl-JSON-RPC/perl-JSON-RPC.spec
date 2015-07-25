Name:           perl-JSON-RPC
Version:        1.01
Release:        13%{?dist}
Summary:        Perl implementation of JSON-RPC 1.1 protocol
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JSON-RPC/
Source0:        http://www.cpan.org/authors/id/D/DM/DMAKI/JSON-RPC-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(CGI)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Class::Accessor::Lite)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(JSON) >= 2
BuildRequires:  perl(LWP::UserAgent) >= 2.001
BuildRequires:  perl(Plack::Request)
BuildRequires:  perl(Plack::Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Router::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters.

%package legacy-server
Summary: The legacy server part of JSON::RPC

%package legacy
Summary: The legacy client part of JSON::RPC

%description legacy-server
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters. This is the legacy server-side
implementation, which exposes the 0.xx version of the API.

%description legacy
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters. This is the legacy client-side
implementation, which allows the use of the 0.xx version of the API.

%prep
%setup -q -n JSON-RPC-%{version}

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
%doc Changes README
%{perl_vendorlib}/JSON/RPC.pm
%{perl_vendorlib}/JSON/RPC/Constants.pm
%{perl_vendorlib}/JSON/RPC/Dispatch.pm
%{perl_vendorlib}/JSON/RPC/Parser.pm
%{perl_vendorlib}/JSON/RPC/Procedure.pm
%{_mandir}/man3/*

%files legacy
%{perl_vendorlib}/JSON/RPC/Legacy.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Client.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Procedure.pm

%files legacy-server
%{perl_vendorlib}/JSON/RPC/Legacy/Server
%{perl_vendorlib}/JSON/RPC/Legacy/Server.pm

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.01-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.01-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.01-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.01-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.01-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.01-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.01-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.01-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.01-1
- Update to 1.01
- Split the lagacy implementation into its own sub-packages

* Thu Oct 27 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.96-10
- Split out the server part in its own sub-package
- Tidy up the spec file

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.96-9
- Perl mass rebuild

* Sun Feb 13 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.96-8
- Add the perl default filter to filter the examples.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.96-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.96-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.96-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.96-2
- Remove unneeded Requires

* Tue Apr 14 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.96-1
- Specfile autogenerated by cpanspec 1.77.
