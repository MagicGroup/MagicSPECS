Name:           perl-Test-TCP
Version:	2.14
Release:	3%{?dist}
Summary:        Testing TCP program
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-TCP/
Source0:        http://www.cpan.org/authors/id/T/TO/TOKUHIROM/Test-TCP-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl >= 0:5.008001
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(IO::Socket::IP)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::SharedFork) >= 0.29
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(warnings)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::TCP is test utilities for TCP/IP program.

%prep
%setup -q -n Test-TCP-%{version}

# FIXME: Work around to inconsistency in Test-TCP-2.07
sed -i -e 's,use Test::SharedFork 0.12;,use Test::SharedFork 0.29;,' lib/Test/TCP.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README*
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.14-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.14-2
- 更新到 2.14

* Sat Jul 25 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.13-1
- Upstream update.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.12-2
- Perl 5.22 rebuild

* Tue May 19 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.12-1
- Upstream update.
- Reflect upstream Source0: having changed.

* Tue Apr 07 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.11-1
- Upstream update.

* Tue Apr 07 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.10-1
- Upstream update.

* Fri Apr 03 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.09-1
- Upstream update.

* Thu Apr 02 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.08-1
- Upstream update.
- Reflect Source0: having changed.

* Mon Jan 26 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.07-1
- Upstream update.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.06-2
- Perl 5.20 rebuild

* Thu Jul 03 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.06-1
- Upstream update.
- Remove Test-TCP-2.02-Wait-infinitely-if-max_wait-is-negative.patch
  (Patch was incorporated by upstream).

* Mon Jun 30 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.05-1
- Upstream update.
- Reflect upstream having switched to ExtUtils::MakeMaker.
- Rework deps.

* Fri Jun 27 2014 Petr Pisar <ppisar@redhat.com> - 2.02-3
- Fix a race in a test (bug #1113962)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 07 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.02-1
- Upstream update.

* Tue Sep 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.01-1
- Upstream update.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.00-2
- Perl 5.18 rebuild

* Thu Jun 13 2013 Ralf Corsépius <corsepiu@fedoraproject.org> 2.00-1
- Upstream update.

* Tue May 21 2013 Ralf Corsépius <corsepiu@fedoraproject.org> 1.27-1
- Upstream update.

* Wed Apr 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> 1.26-1
- Upstream update.
- Reflect upstream having switched to perl(Module::Build).

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> 1.21-1
- Upstream update.
- Drop Obs/Prov perl-Test-TCP-tests.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.18-1
- Upstream update.

* Tue Jul 31 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.17-1
- Upstream update.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Petr Pisar <ppisar@redhat.com> - 1.16-2
- Perl 5.16 rebuild

* Tue Jul 10 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.16-1
- Upstream update.

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.15-2
- Perl 5.16 rebuild

* Sun Feb 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 1.15-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.14-1
- Upstream update.
- BR: perl(Test::Shared::Fork) >= 0.19.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-2
- Perl mass rebuild

* Fri Jun 03 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.13-1
- Upstream update.
- Spec file cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 09 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 1.11-1
- Update to 1.11.
- Rework spec.
- Abandon *-tests.

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-2
- Mass rebuild with perl-5.12.0

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- specfile by Fedora::App::MaintainerTools 0.006
