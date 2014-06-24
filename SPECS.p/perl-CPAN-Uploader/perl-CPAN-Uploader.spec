Name:           perl-CPAN-Uploader
Version:        0.103007
Release:        4%{?dist}
Summary:        Upload things to the CPAN
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CPAN-Uploader/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/CPAN-Uploader-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::Spec)
# Getopt::Long::Descriptive 0.084 not used at tests
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(HTTP::Status)
# LWP::Protocol::https 1 not used at tests
BuildRequires:  perl(LWP::UserAgent)
# Term::ReadKey not used at tests
# optional run-time:
# Config::Identity
# tests
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(version)
# optional tests
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120900
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(LWP::Protocol::https) >= 1
Requires:       perl(Term::ReadKey)

# cpan-upload replaced by perl-CPAN-Uploader, bugs #1043581, #1095426
Provides:       cpan-upload = 2.2-17
Obsoletes:      cpan-upload < 2.2-18

%{?perl_default_filter}

%description
CPAN::Uploader is a module which automates the process of uploading a file to
CPAN using PAUSE, the Perl Authors Upload Server.

%prep
%setup -q -n CPAN-Uploader-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
RELEASE_TESTING=1 make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.103007-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Petr Pisar <ppisar@redhat.com> - 0.103007-2
- Obsolete cpan-upload properly (bug #1095426)
- Restore the utility name back to cpan-upload

* Mon May 05 2014 Petr Pisar <ppisar@redhat.com> - 0.103007-1
- 0.103007 bump

* Tue Dec 17 2013 Marcela Mašláňová <mmaslano@redhat.com> - 0.103002-5
- add Obsoletes/Provides to cpan-upload 1043581

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.103002-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Iain Arnell <iarnell@gmail.com> 0.103002-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.103001-2
- Perl 5.16 rebuild

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 0.103001-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.103000-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.103000-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.103000-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102150-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.102150-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Aug 05 2010 Iain Arnell <iarnell@gmail.com> 0.102150-1
- update to latest upstream

* Fri Jun 18 2010 Iain Arnell <iarnell@gmail.com> 0.101670-1
- update to latest upstream

* Sat Jun 05 2010 Iain Arnell <iarnell@gmail.com> 0.101550-1
- update to latest upstream

* Fri May 28 2010 Iain Arnell <iarnell@gmail.com> 0.101260-2
- bump release for rebuild with perl-5.12.0

* Sun May 09 2010 Iain Arnell <iarnell@gmail.com> 0.101260-1
- update to latest upstream

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.100760-2
- Mass rebuild with perl-5.12.0

* Thu Apr 08 2010 Iain Arnell <iarnell@gmail.com> 0.100760-1
- Specfile autogenerated by cpanspec 1.78.
- use perl_default_filter and DESTDIR
- tweak requires
