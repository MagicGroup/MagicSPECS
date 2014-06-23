Name:           perl-Test-TCP
Version:        1.17
Release:        8%{?dist}
Summary:        Testing TCP program
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-TCP/
Source0:        http://www.cpan.org/authors/id/T/TO/TOKUHIROM/Test-TCP-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test::SharedFork) >= 0.19
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Get rid of perl-Test-TCP-tests
Obsoletes: perl-Test-TCP-tests < %{version}-%{release}
Provides: perl-Test-TCP-tests = %{version}-%{release}

%description
Test::TCP is test utilities for TCP/IP program.

%prep
%setup -q -n Test-TCP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.17-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.17-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.17-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.17-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.17-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.17-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.17-2
- 为 Magic 3.0 重建

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
