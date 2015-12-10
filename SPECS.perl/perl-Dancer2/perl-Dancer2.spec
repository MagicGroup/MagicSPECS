Name:           perl-Dancer2
Version:        0.161000
Release:        4%{?dist}
Summary:        Lightweight yet powerful web application framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Dancer2/
Source0:        http://www.cpan.org/modules/by-module/Dancer2/Dancer2-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::ShareDir::Install) >= 0.06
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(App::Cmd::Setup)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Load)
BuildRequires:  perl(Config::Any)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(Hash::Merge::Simple)
BuildRequires:  perl(HTTP::Body)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(HTTP::Headers::Fast)
BuildRequires:  perl(HTTP::Server::PSGI)
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(Import::Into)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(JSON)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moo) >= 1.003000
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(MooX::Types::MooseLike) >= 0.16
BuildRequires:  perl(MooX::Types::MooseLike::Base)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
# Plack::Builder version from Plack >= 1.0029 in Makefile.PL
BuildRequires:  perl(Plack::Builder) >= 1.0029
BuildRequires:  perl(Plack::Middleware::Conditional)
BuildRequires:  perl(Plack::Middleware::ContentLength)
BuildRequires:  perl(Plack::Middleware::FixMissingBodyInRedirect)
BuildRequires:  perl(Plack::Middleware::Head)
BuildRequires:  perl(Plack::Middleware::RemoveRedundantBody)
BuildRequires:  perl(Plack::Middleware::Static)
BuildRequires:  perl(Plack::MIME)
BuildRequires:  perl(Plack::Request)
BuildRequires:  perl(Pod::Simple::Search)
BuildRequires:  perl(Pod::Simple::SimpleTree)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Return::MultiLevel)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Safe::Isa)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sub::Quote)
BuildRequires:  perl(Template)
BuildRequires:  perl(Template::Tiny)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.92
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(YAML) >= 0.86
# Optional run-time:
BuildRequires:  perl(CGI::Deurl::XS)
BuildRequires:  perl(Crypt::URandom)
BuildRequires:  perl(Math::Random::ISAAC::XS)
BuildRequires:  perl(MIME::Types)
BuildRequires:  perl(URL::Encode::XS)
# Tests:
BuildRequires:  perl(Capture::Tiny) >= 0.12
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(Plack::Response)
BuildRequires:  perl(Plack::Test)
# Test::CPAN::Meta not used
BuildRequires:  perl(Test::Fatal)
# Test::NoTabs not used
# Test::Pod 1.41 not used
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional tests:
BuildRequires:  perl(Test::Memory::Cycle) >= 1.04
BuildRequires:  perl(Test::MockTime)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Exporter) >= 5.57
Requires:       perl(File::Copy)
Requires:       perl(File::Temp) >= 0.22
Requires:       perl(Moo) >= 1.003000
# Plack::Builder version from Plack >= 1.0029 in Makefile.PL
Requires:       perl(Plack::Builder) >= 1.0029
Requires:       perl(Pod::Simple::Search)
Requires:       perl(Pod::Simple::SimpleTree)
Requires:       perl(Template::Tiny)
Requires:       perl(Test::More) >= 0.92
Requires:       perl(YAML) >= 0.86

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Exporter\\)$
%global __requires_exclude %__requires_exclude|^perl\\(File::Temp\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Moo\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Plack::Builder\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Test::More\\)$
%global __requires_exclude %__requires_exclude|^perl\\(YAML\\)$

%description
Dancer2 is the new generation of Dancer, the lightweight web-framework for
Perl. Dancer2 is a complete rewrite based on Moo.

%prep
%setup -q -n Dancer2-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%license LICENSE
%doc AUTHORS Changes GitGuide.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%package -n dancer2
Summary:       Dancer2 command line interface

%description -n dancer2
Dancer2 is the new generation lightweight web-framework for Perl. This tool
provides nice, easily-extendable CLI interface for it.

%files -n dancer2
%doc LICENSE
%{_mandir}/man1/*
%{_bindir}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.161000-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.161000-3
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.161000-2
- 为 Magic 3.0 重建

* Thu Aug 06 2015 Petr Pisar <ppisar@redhat.com> - 0.161000-1
- 0.161000 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.160000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.160000-2
- Perl 5.22 rebuild

* Tue Apr 28 2015 David Dick <ddick@cpan.org> - 0.160000-1
- Upgrade to 0.160000.  Numerous bugfixes and enhancements

* Sat Mar 28 2015 David Dick <ddick@cpan.org> - 0.159003-1
- Upgrade to 0.159003.  Numerous bugfixes

* Wed Jan 14 2015 David Dick <ddick@cpan.org> - 0.158000-1
- Initial release
