Name:           perl-Test-TCP
Version:        2.02
Release:        2%{?dist}
Summary:        Testing TCP program
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-TCP/
Source0:        http://www.cpan.org/authors/id/T/TO/TOKUHIROM/Test-TCP-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::SharedFork) >= 0.19
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(File::Which)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::TCP is test utilities for TCP/IP program.

%prep
%setup -q -n Test-TCP-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes README*
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
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
