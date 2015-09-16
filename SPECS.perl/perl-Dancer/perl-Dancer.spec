Name:           perl-Dancer
Version:	1.3140
Release:	0%{?dist}
Summary:        Lightweight yet powerful web application framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Dancer/
Source0:        http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Dancer-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Clone)
BuildRequires:  perl(CGI)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(HTTP::Body) >= 1.07
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Server::Simple::PSGI) >= 0.11
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(JSON)
BuildRequires:  perl(lib)
BuildRequires:  perl(LWP)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(MIME::Types)
BuildRequires:  perl(Plack::Builder)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(strict)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test::CheckManifest)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Try::Tiny) >= 0.09
BuildRequires:  perl(URI) >= 1.59
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(YAML)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Run-time for tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::stat)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Plack::Handler::FCGI)
BuildRequires:  perl(Plack::Runner)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(URI::Escape)
# Optional tests:
BuildRequires:  perl(HTTP::Parser::XS)
BuildRequires:  perl(Dancer::Session::Cookie) >= 0.14
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(HTTP::Body) >= 1.07
Requires:       perl(HTTP::Server::Simple::PSGI) >= 0.11
Requires:       perl(LWP)
Requires:       perl(Try::Tiny) >= 0.09
Requires:       perl(URI) >= 1.59

# Do not export under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(HTTP::Body|HTTP::Server::Simple::PSGI|Try::Tiny|URI\\)\\s*$

%description
Dancer is a web application framework designed to be as effortless as
possible for the developer, taking care of the boring bits as easily as
possible, yet staying out of your way and letting you get on with writing
your code.

%prep
%setup -q -n Dancer-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check


%files
%{_bindir}/dancer
%{perl_vendorlib}/*
%{_mandir}/man1/dancer.1*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.3091-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.3091-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.3091-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.3091-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.3091-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.3091-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3091-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3091-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3091-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.3091-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.3091-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.3091-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.3091-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3091-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Petr Pisar <ppisar@redhat.com> - 1.3091-2
- Enable optional tests requiring perl(Dancer::Session::Cookie).

* Mon Dec 19 2011 Petr Pisar <ppisar@redhat.com> - 1.3091-1
- 1.3091 bump

* Wed Dec 14 2011 Petr Šabata <contyk@redhat.com> - 1.3090-1
- 1.3090 bump

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.3080-1
- 1.3080 bump

* Wed Aug 24 2011 Petr Sabata <contyk@redhat.com> - 1.3072-1
- 1.3072 bump

* Wed Aug 10 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.3071-1
- update
- add filter for RPM 4.8

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.3040-3
- Perl mass rebuild

* Mon May 16 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.3040-2
- add tests BR: CGI, YAML, Template, Clone

* Fri May 13 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.3040-1
- Specfile autogenerated by cpanspec 1.79.
