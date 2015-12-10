Name:           perl-Log-Report
Version:        1.07
Release:        4%{?dist}
Summary:        Report a problem with exceptions and translation support
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Log-Report/
Source0:        http://www.cpan.org/authors/id/M/MA/MARKOV/Log-Report-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Devel::GlobalDestruction) >= 0.09
# Dancer::Logger::Abstract not used at tests
# Dancer2::Core::Role::Logger not used at tests
# Dancer2::Core::Types not used at tests
# Dancer2::Plugin not used at tests
# Data::Dumper not used at tests
# DBIx::Class::Storage::Statistics not used at tests
BuildRequires:  perl(Encode) >= 2.00
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(locale)
BuildRequires:  perl(Log::Dispatch) >= 2.00
BuildRequires:  perl(Log::Log4perl)
# Makefile.PL states Log::Report::Optional 1.01 for contained
# Log::Report::{Minimal::Domain,Util}
BuildRequires:  perl(Log::Report::Minimal::Domain) >= 1.01
BuildRequires:  perl(Log::Report::Util) >= 1.01
# Mojo tests are optional
BuildRequires:  perl(Mojo::Base)
BuildRequires:  perl(Mojo::Log)
# Moo not used at tests
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# String::Print is not used
BuildRequires:  perl(strict)
BuildRequires:  perl(Sys::Syslog) >= 0.27
# Time::HiRes not used at tests
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.86
# Optional tests:
BuildRequires:  perl(Mojolicious) >= 2.16
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Devel::GlobalDestruction) >= 0.09
Requires:       perl(Encode) >= 2.00
# Makefile.PL states Log::Report::Optional 1.01 for contained
# Log::Report::{Minimal::Domain,Util}
Requires:       perl(Log::Report::Minimal::Domain) >= 1.01
Requires:       perl(Log::Report::Util) >= 1.01
Requires:       perl(overload)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Devel::GlobalDestruction|Encode|Log::Report::Minimal::Domain|Log::Report::Util|Sys::Syslog)\\)$

%description
Handling messages directed to users can be a hassle, certainly when the same
software is used for command-line and in a graphical interfaces (you may not
know how it is used), or has to cope with internationalization; these modules
try to simplify this.

%package Dancer
Summary:    Reroute Dancer logs into Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(Exporter)
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}

%description Dancer
When you use this logger in your Dancer application, it will nicely integrate
with non-Dancer modules which need logging.

%package Dancer2
Summary:    Reroute Dancer2 logs into Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(Dancer2::Core::Role::Logger)
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}

%description Dancer2
This logger allows the use of the many logging back-ends available in
Log::Report. It will process all of the Dancer2 log messages, and also allow
any other module to use the same logging facilities. The same log messages can
be sent to multiple destinations at the same time via flexible dispatchers.

%package DBIC
Summary:    Query profiler for DBIx::Class
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}

%description DBIC
Log DBIx::Class queries via Log::Report.

%package Dispatcher-Log4perl
Summary:    Log::Log4perl back-end for Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}
# Makefile.PL states Log::Report::Optional 1.01 for contained
# Log::Report::{Minimal::Domain,Util}
Requires:   perl(Log::Report::Util) >= 1.01

%description Dispatcher-Log4perl
This is an optional Log::Log4perl back-end for Log::Report logging framework.

%package Dispatcher-LogDispatch
Summary:    Log::Dispatch back-end for Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}
# Makefile.PL states Log::Report::Optional 1.01 for contained
# Log::Report::{Minimal::Domain,Util}
Requires:   perl(Log::Report::Util) >= 1.01

%description Dispatcher-LogDispatch
This is an optional Log::Dispatch back-end for Log::Report logging framework.

%package Dispatcher-Syslog
Summary:    Sys::Syslog back-end for Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}
Requires:   perl(Encode) >= 2.00
Requires:   perl(Sys::Syslog) >= 0.27
# Makefile.PL states Log::Report::Optional 1.01 for contained
# Log::Report::{Minimal::Domain,Util}
Requires:   perl(Log::Report::Util) >= 1.01

%description Dispatcher-Syslog
This is an optional Sys::Syslog back-end for Log::Report logging framework.

%package Mojo
Summary:    Divert log messages into Log::Report
Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl-Log-Report = %{?epoch:%epoch:}%{version}-%{release}
Requires:   perl(Mojo::Log)

%description Mojo
Mojo likes to log messages directly into a file, by default. This is a Mojo
extension that can route Mojo messages into Log::Report logging framework.


%prep
%setup -q -n Log-Report-%{version}

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
%doc ChangeLog README
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/Dancer
%exclude %{perl_vendorlib}/Dancer2
%exclude %{perl_vendorlib}/Log/Report/DBIC
%exclude %{perl_vendorlib}/Log/Report/Dispatcher/Log4perl.*
%exclude %{perl_vendorlib}/Log/Report/Dispatcher/LogDispatch.*
%exclude %{perl_vendorlib}/Log/Report/Dispatcher/Syslog.*
%exclude %{perl_vendorlib}/MojoX
%{_mandir}/man3/*
%exclude %{_mandir}/man3/Dancer::*
%exclude %{_mandir}/man3/Dancer2::*
%exclude %{_mandir}/man3/Log::Report::DBIC::Profiler.*
%exclude %{_mandir}/man3/Log::Report::Dispatcher::Log4perl.*
%exclude %{_mandir}/man3/Log::Report::Dispatcher::LogDispatch.*
%exclude %{_mandir}/man3/Log::Report::Dispatcher::Syslog.*
%exclude %{_mandir}/man3/MojoX::Log::Report.*

%files Dancer
%{perl_vendorlib}/Dancer
%{_mandir}/man3/Dancer::*

%files Dancer2
%{perl_vendorlib}/Dancer2
%{_mandir}/man3/Dancer2::*

%files DBIC
%{perl_vendorlib}/Log/Report/DBIC
%{_mandir}/man3/Log::Report::DBIC::Profiler.*

%files Dispatcher-Log4perl
%{perl_vendorlib}/Log/Report/Dispatcher/Log4perl.*
%{_mandir}/man3/Log::Report::Dispatcher::Log4perl.*

%files Dispatcher-LogDispatch
%{perl_vendorlib}/Log/Report/Dispatcher/LogDispatch.*
%{_mandir}/man3/Log::Report::Dispatcher::LogDispatch.*

%files Dispatcher-Syslog
%{perl_vendorlib}/Log/Report/Dispatcher/Syslog.*
%{_mandir}/man3/Log::Report::Dispatcher::Syslog.*

%files Mojo
%{perl_vendorlib}/MojoX
%{_mandir}/man3/MojoX::Log::Report.*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.07-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.07-3
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 1.07-2
- 为 Magic 3.0 重建

* Wed Jul 22 2015 Petr Pisar <ppisar@redhat.com> - 1.07-1
- 1.07 bump

* Tue Jun 16 2015 Petr Pisar <ppisar@redhat.com> - 1.06-1
- 1.06 bump

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-3
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-2
- Perl 5.20 rebuild

* Mon Jun 30 2014 Petr Pisar <ppisar@redhat.com> - 1.05-1
- 1.05 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Petr Pisar <ppisar@redhat.com> - 1.04-1
- 1.04 bump

* Mon May 26 2014 Petr Pisar <ppisar@redhat.com> - 1.03-1
- 1.03 bump

* Tue Mar 11 2014 Petr Pisar <ppisar@redhat.com> - 1.02-1
- 1.02 bump

* Mon Jan 27 2014 Petr Pisar <ppisar@redhat.com> - 1.01-1
- 1.01 bump

* Wed Nov 20 2013 Petr Pisar <ppisar@redhat.com> 0.998-1
- Specfile autogenerated by cpanspec 1.78.
