Name:           perl-Test-TempDir
Version:        0.10
Release:        6%{?dist}
Summary:        Temporary files support for testing
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-TempDir/
Source0:        http://www.cpan.org/authors/id/E/ET/ETHER/Test-TempDir-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Directory::Scratch)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::NFSLock)
BuildRequires:  perl(Module::Build::Tiny)
BuildRequires:  perl(Moose) >= 0.87
BuildRequires:  perl(MooseX::Types::Path::Class)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(namespace::clean) >= 0.08
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test::CheckDeps)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::use::ok)
Requires:       perl(File::NFSLock)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Test::TempDir provides temporary directory creation with testing in mind.

%prep
%setup -q -n Test-TempDir-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist | xargs rm -f
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Test
%{_mandir}/man3/Test::TempDir*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.10-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.10-5
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.10-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.10-2
- Perl 5.22 rebuild

* Sun May 17 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 0.10-1
- Update to 0.10

* Sun Nov 09 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.09-1
- Update to 0.09

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 29 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.08-1
- Update to 0.08
- Switch to make as a build system

* Sun Sep 15 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 0.07-1
- Update to 0.07
- Switch to Module::Build::Tiny as a build system
- Add new BRs to run more tests

* Sun Aug 04 2013 Petr Pisar <ppisar@redhat.com> - 0.05-15
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 0.05-12
- Add perl default filter
- Remove no-longer-used macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.05-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.05-8
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.05-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jul 03 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.05-4
- Add perl(File::NFSLock) to the Requires (#611056)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.05-2
- rebuild against perl 5.10.1

* Tue Aug 25 2009 Stepan Kasal <skasal@redhat.com> - 0.05-1
- new upstream version
- spec file cleanup

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 01 2009 Allisson Azevedo <allisson@gmail.com> 0.04-2
- Fix requires.

* Sun Feb 01 2009 Allisson Azevedo <allisson@gmail.com> 0.04-1
- Initial rpm release.
