Name:           perl-JSON-RPC
Version:        1.06
Release:        3%{?dist}
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
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Plack::Request)
BuildRequires:  perl(Plack::Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Router::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes:      perl-JSON-RPC-legacy < %{version}
Provides:       perl-JSON-RPC-legacy = %{version}

%{?perl_default_filter}

%description
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters.

%package Apache2
Summary:   JSON-RPC server for mod_perl2
Obsoletes: perl-JSON-RPC-legacy-server < %{version}
Provides:  perl-JSON-RPC-legacy-server = %{version}

%package CGI
Summary:   JSON-RPC server for CGI scripts
Obsoletes: perl-JSON-RPC-legacy-server < %{version}
Provides:  perl-JSON-RPC-legacy-server = %{version}

%package Daemon
Summary:   JSON-RPC standalone daemon
Obsoletes: perl-JSON-RPC-legacy-server < %{version}
Provides:  perl-JSON-RPC-legacy-server = %{version}

%description Apache2
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters. This is the mod_perl2 server
implementation.

%description CGI
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters. This is the CGI server
implementation.

%description Daemon
JSON-RPC is a stateless and light-weight remote procedure call (RPC)
protocol for inter-networking applications over HTTP. It uses JSON as the
data format for of all facets of a remote procedure call, including all
application data carried in parameters. This is the standalone daemon
to serve JSON-RPC requests.

%prep
%setup -q -n JSON-RPC-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes
%license LICENSE
%{perl_vendorlib}/JSON/RPC.pm
%{perl_vendorlib}/JSON/RPC/Constants.pm
%{perl_vendorlib}/JSON/RPC/Dispatch.pm
%{perl_vendorlib}/JSON/RPC/Legacy.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Client.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Procedure.pm
%{perl_vendorlib}/JSON/RPC/Parser.pm
%{perl_vendorlib}/JSON/RPC/Procedure.pm
%{perl_vendorlib}/JSON/RPC/Test.pm
%{_mandir}/man3/*

%files Apache2
%{perl_vendorlib}/JSON/RPC/Legacy/Server.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Server/Apache2.pm

%files CGI
%{perl_vendorlib}/JSON/RPC/Legacy/Server.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Server/CGI.pm

%files Daemon
%{perl_vendorlib}/JSON/RPC/Legacy/Server.pm
%{perl_vendorlib}/JSON/RPC/Legacy/Server/Daemon.pm

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-2
- Perl 5.22 rebuild

* Sun Oct 12 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.06-1
- Update to 1.06
- Use %%license macro

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.04-1
- Update to 1.04

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 1.03-7
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.03-3
- Use the version macro in Obsoletes

* Sat Jun 30 2012 Petr Pisar <ppisar@redhat.com> - 1.03-2
- Perl 5.16 rebuild

* Sat Jun 23 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.03-1
- Update to 1.03
- Merge back the legacy implementation in the main package
- Split the different server implementations in their own packages

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
