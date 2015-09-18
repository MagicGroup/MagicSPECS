Name:           perl-CGI-Fast
Version:        2.10
Release:        2%{?dist}
Summary:        CGI Interface for Fast CGI
# lib/CGI/Fast.pm probably qotes piece of Artistic license before declaring
# "as Perl itself" <https://github.com/leejo/cgi-fast/issues/13>
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Fast/
Source0:        http://www.cpan.org/authors/id/L/LE/LEEJO/CGI-Fast-%{version}.tar.gz
# Make Test::Deep tests optional as it's not in the core in contrast to the
# CGI-Fast
Patch0:         CGI-Fast-2.04-Make-Test-Deep-tests-optional.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(CGI) >= 4.00
%if 0%(perl -e 'print $] >= 5.019')
BuildRequires:  perl(deprecate)
%endif
BuildRequires:  perl(FCGI) >= 0.67
BuildRequires:  perl(if)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(warnings)
# Optional tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Temp)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Deep) >= 0.11
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if 0%(perl -e 'print $] >= 5.019')
Requires:       perl(deprecate)
%endif
Requires:       perl(CGI) >= 4.00
Requires:       perl(FCGI) >= 0.67
# perl-CGI-Fast was split from perl-CGI
Conflicts:      perl-CGI < 4.00

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((CGI|FCGI)\\)$

%description
CGI::Fast is a subclass of the CGI object created by CGI.pm. It is
specialized to work well FCGI module, which greatly speeds up CGI scripts
by turning them into persistently running server processes. Scripts that
perform time-consuming initialization processes, such as loading large
modules or opening persistent database connections, will see large
performance improvements.

%prep
%setup -q -n CGI-Fast-%{version}
%patch0 -p1

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
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.10-2
- 为 Magic 3.0 重建

* Tue Jun 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.10-1
- 2.10 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-2
- Perl 5.22 rebuild

* Thu Mar 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.09-1
- 2.09 bump

* Mon Feb 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.07-1
- 2.07 bump

* Wed Jan 14 2015 Petr Pisar <ppisar@redhat.com> - 2.05-2
- Specify run-time dependency versions

* Mon Dec 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.05-1
- 2.05 bump

* Wed Dec 10 2014 Petr Pisar <ppisar@redhat.com> - 2.04-2
- Do not load Test::Deep where not needed
- Make Test::Deep tests optional as it's not in the core in contrast to the
  CGI-Fast

* Mon Oct 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.04-1
- 2.04 bump

* Wed Sep 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.03-1
- 2.03 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-2
- Perl 5.20 rebuild

* Mon Jun 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.02-1
- 2.02 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.01-1
- 2.01 bump

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.00-1
- Specfile autogenerated by cpanspec 1.78.
