Name:           perl-Email-Sender
Version:        0.120002
Release:        5%{?dist}
Summary:        A library for sending email
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Email-Sender/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Email-Sender-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Capture::Tiny) >= 0.08
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Email::Abstract) >= 3
BuildRequires:  perl(Email::Address)
BuildRequires:  perl(Email::Simple) >= 1.998
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.11
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(JSON)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Moose) >= 0.70
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(Net::SMTP)
BuildRequires:  perl(Net::SMTP::SSL)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(Sub::Override)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::MockObject)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Throwable::Error) >= 0.100090
BuildRequires:  perl(Try::Tiny)
Requires:       perl(Email::Abstract) >= 3
Requires:       perl(Net::SMTP::SSL)
Requires:       perl(Throwable::Error) >= 0.100090
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Email::Sender replaces the old and sometimes problematic Email::Send library,
which did a decent job at handling very simple email sending tasks, but was not
suitable for serious use, for a variety of reasons.

%prep
%setup -q -n Email-Sender-%{version}

# pod coverage test fails
rm -f t/release-pod-coverage.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.120002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 0.120002-4
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.120002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.120002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Iain Arnell <iarnell@gmail.com> 0.120002-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 0.120001-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.110005-2
- Perl 5.16 rebuild

* Sun Mar 11 2012 Iain Arnell <iarnell@gmail.com> 0.110005-1
- update to latest upstream version

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 0.110004-1
- update to latest upstream version

* Fri Feb 03 2012 Iain Arnell <iarnell@gmail.com> 0.110003-1
- update to latest upstream version

* Wed Feb 01 2012 Iain Arnell <iarnell@gmail.com> 0.110002-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.110001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.110001-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.110001-1
- update to latest upstream version

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> 0.110000-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102370-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.102370-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Aug 30 2010 Iain Arnell <iarnell@gmail.com> 0.102370-1
- update to latest upstream
- drop Sys::Hostname::Long BR

* Tue Jun 29 2010 Iain Arnell <iarnell@gmail.com> 0.101760-2
- re-enable t/a-perl-minver.t

* Tue Jun 29 2010 Iain Arnell <iarnell@gmail.com> 0.101760-1
- update to latest upstream (fixes bz#608958)
- BR perl(Capture::Tiny) >= 0.08

* Sat May 08 2010 Iain Arnell <iarnell@gmail.com> 0.100460-4
- disable t/a-perl-minver.t (fails under perl 5.12.0)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.100460-3
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.100460-2
- Mass rebuild with perl-5.12.0

* Sat Mar 13 2010 Iain Arnell <iarnell@gmail.com> 0.100460-1
- update to latest upstream version
- use perl_default_filter and DESTDIR
- br perl(Pod::Coverage::TrustPod)
- remove failing pod coverage test

* Mon Feb 15 2010 Iain Arnell <iarnell@gmail.com> 0.100450-1
- update to latest upstream version

* Thu Jan 14 2010 Iain Arnell 0.100110-1
- Specfile autogenerated by cpanspec 1.78.
