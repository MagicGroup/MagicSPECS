Name:           perl-Throwable
Version:	0.200013
Release:	3%{?dist}
Summary:        Role for classes that can be thrown
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Throwable/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/Throwable-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Devel::StackTrace) >= 1.21
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.11
BuildRequires:  perl(Moose) >= 0.87
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage::TrustPod)

Requires:       perl(Devel::StackTrace) >= 1.21
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Throwable is a role for classes that are meant to be thrown as exceptions
to standard program flow. It is very simple and does only two things: saves
any previous value for $@ and calls die $self.

%prep
%setup -q -n Throwable-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 make test

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.200013-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.200013-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.200013-1
- 更新到 0.200013

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.102080-13
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 29 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.102080-11
- Remove bogus R: perl(ExtUtils::MakeMaker) (RHBZ #1052853).
- Remove redundant R: perl(Moose).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.102080-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.102080-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.102080-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102080-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.102080-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jul 30 2010 Iain Arnell <iarnell@gmail.com> 0.102080-1
- update to latest upstream
- update spec for modern rpmbuild

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.101110-2
- Mass rebuild with perl-5.12.0

* Sat Apr 24 2010 Iain Arnell <iarnell@gmail.com> 0.101110-1
- update to latest upstream version
- use perl_default_filter and DESTDIR

* Sat Feb 27 2010 Iain Arnell <iarnell@gmail.com> 0.100090-2
- BR perl(Pod::Coverage::TrustPod)

* Thu Jan 14 2010 Iain Arnell 0.100090-1
- Specfile autogenerated by cpanspec 1.78.
