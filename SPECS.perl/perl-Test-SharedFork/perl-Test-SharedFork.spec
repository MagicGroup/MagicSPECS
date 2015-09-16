Name:           perl-Test-SharedFork
Summary:        Fork test
Version:	0.33
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/EX/EXODIST/Test-SharedFork-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Test-SharedFork

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)

%{?perl_default_filter}

Obsoletes: perl-Test-SharedFork-tests <= %{version}-%{release}
Provides: perl-Test-SharedFork-tests = %{version}-%{release}

%description
Test::SharedFork is utility module for Test::Builder. It manages testing
by keeping the test count consistent between parent and child processes.

%prep
%setup -q -n Test-SharedFork-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.33-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.33-1
- 更新到 0.33

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.20-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.20-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.20-2
- Perl 5.16 rebuild

* Tue Feb 14 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.20-1
- Upstream update.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.19-1
- Upstream update.

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.18-1
- Upstream update.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-3
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-2
- Perl 5.14 mass rebuild

* Fri Feb 18 2011 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.16-1
- Update to 0.16.
- Abandon perl-Test-SharedFork-tests.
- Spec file overhaul.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.15-3
- re-add macros. -tests sub-package was missing during update

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.15-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Dec 22 2010 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.15-1
- Update to 0.15.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-2
- Mass rebuild with perl-5.12.0

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- specfile by Fedora::App::MaintainerTools 0.006


