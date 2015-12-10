Name:           perl-Log-Log4perl
Version:	1.46
Release:	3%{?dist}
Summary:        Log4j implementation for Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Log-Log4perl/
Source0:        http://www.cpan.org/authors/id/M/MS/MSCHILLI/Log-Log4perl-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(IPC::Semaphore)
BuildRequires:  perl(IPC::SysV)
BuildRequires:  perl(Log::Dispatch::File)
BuildRequires:  perl(Log::Dispatch::FileRotate) >= 1.10
BuildRequires:  perl(Log::Dispatch::Screen)
BuildRequires:  perl(Log::Dispatch::Syslog)
BuildRequires:  perl(RRDs)
BuildRequires:  perl(Storable)
# Term::ANSIColor is not needed for runing tests
BuildRequires:  perl(XML::DOM)
# Tests
BuildRequires:  perl(fields)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.45
# Optional tests
%if ! (0%{?rhel} >= 7)
BuildRequires:  perl(DBD::CSV)
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(SQL::Statement)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Log::Log4perl lets you remote-control and fine-tune the logging
behavior of your system from the outside. It implements the widely
popular (Java-based) Log4j logging package in pure Perl.

%prep
%setup -q -n Log-Log4perl-%{version}
find lib -name "*.pm" -exec chmod -c a-x {} +
perl -pi -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' eg/newsyslog-test eg/benchmarks/simple

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check
 L4P_ALL_TESTS=1

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.46-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.46-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.46-1
- 更新到 1.46

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.39-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.39-10
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.39-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.39-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.39-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.39-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.39-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.39-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.39-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.39-2
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Petr Šabata <contyk@redhat.com> - 1.39-1
- 1.39 bump

* Wed Sep 26 2012 Petr Pisar <ppisar@redhat.com> - 1.38-2
- Disable optional tests on RHEL >= 7

* Wed Sep 26 2012 Petr Pisar <ppisar@redhat.com> - 1.38-1
- 1.38 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 1.37-2
- Perl 5.16 rebuild

* Fri Jun 08 2012 Petr Šabata <contyk@redhat.com> - 1.37-1
- 1.37 bump
- Drop command macros

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> - 1.36-1
- 1.36 bump

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.35-1
- bump to 1.35

* Mon Nov 07 2011 Petr Sabata <contyk@redhat.com> - 1.34-1
- 1.34 bump
- Removing the BuildRoot tag

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.33-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.33-2
- Perl mass rebuild

* Wed Jun  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-1
- 1.33 bump
- clean spec from defattr, clean section & rm -rf

* Mon Feb 28 2011 Petr Sabata <psabata@redhat.com> - 1.32-1
- 1.32 bump, bugfix release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.30-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 08 2010 Petr Pisar <ppisar@redhat.com> - 1.30-1
- 1.30 bump
- l4p-tmpl executable added
- Add BuildRequires for tests
- Spelling in package description corrected

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.24-2
- rebuild against perl 5.10.1

* Thu Aug 06 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.24-1
- Fix mass rebuild breakdown: Upgrade to upstream 1.24.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.20-1
- Upstream update.
- Reactivate testsuite.
- Remove examples (eg, ldap) from %%doc.
- Don't chmod -x eg/*.
- Remove BR: perl(IPC::Shareable).

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1.1
- disable tests

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1
- bump to 1.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Sat Oct 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sun Jun 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-2
- Log::Dispatch::FileRotate is no longer excluded due to licensing
  problems (the package now includes copyright information).

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Added a couple of comments as suggested by Paul Howarth (#176137).

* Tue Feb  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Disabled the Log::Dispatch::FileRotate requirement (see #171640).

* Mon Dec 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Sat Oct 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- First build.
