Name:           perl-Starman
Version:        0.4009
Release:        2%{?dist}
Summary:        High-performance preforking PSGI/Plack web server
License:        GPL+ or Artistic

URL:            http://search.cpan.org/dist/Starman/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/Starman-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(HTTP::Parser::XS)
BuildRequires:  perl(HTTP::Status)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Module::Build::Tiny)
BuildRequires:  perl(Net::Server)
BuildRequires:  perl(Net::Server::SS::PreFork)
BuildRequires:  perl(parent)
BuildRequires:  perl(Plack)
BuildRequires:  perl(Plack::Test)
BuildRequires:  perl(Server::Starter)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::TCP)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Starman is a PSGI perl web server that has unique features such as high
performance, preforking, use of signals and a small memory footprint. It is PSGI
compatible and offers HTTP/1.1 support.

%prep
%setup -q -n Starman-%{version}

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir $RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/HTTP
%{perl_vendorlib}/Plack
%{perl_vendorlib}/Starman
%{perl_vendorlib}/Starman.pm
%{_bindir}/starman
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 06 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.4009-1
- Update to 0.4009

* Sun Sep 15 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.4008-1
- Update to 0.4008

* Sun Aug 18 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.4006-1
- Update to 0.4006

* Wed Aug 14 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.4004-1
- Update to 0.4004

* Sat Aug 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.4003-1
- Update to 0.4003

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 0.3014-3
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 16 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3014-1
- Update to 0.3014

* Sun Jun 02 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3011-2
- Remove ugly hack for the man page name

* Sun Apr 28 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3011-1
- Update to 0.3011
- Switch to Module::Build::Tiny as building mecanism

* Sun Mar 31 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3007-1
- Update to 0.3007
- Switch to Module::Build as building mecanism

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 23 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3006-1
- Update to 0.3006
- Remove the Group macro (no longer used)

* Sun Nov 18 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3005-1
- Update to 0.3005

* Sun Nov 11 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3004-1
- Update to 0.3004

* Sun Sep 30 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.3003-1
- Update to 0.3003

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Petr Pisar <ppisar@redhat.com> - 0.3001-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.3001-1
- Update to 0.3001

* Tue Feb 21 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.3000-1
- Update to 0.3000
- Add perl default filter

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.2014-1
- Update to 0.2014

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.2013-3
- Perl mass rebuild

* Thu Jul 07 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.2013-2
- Change the files stanza to be more explicit

* Fri Jun 17 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.2013-1
- Specfile autogenerated by cpanspec 1.78.