Name:           perl-JSON-Any
Summary:        A meta-module to make working with JSON easier
Version:	1.39
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/JSON-Any-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/JSON-Any/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Cpanel::JSON::XS)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(JSON)
# Not in Fedora
# BuildRequires:  perl(JSON::DWIW)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(JSON::Syck)
BuildRequires:  perl(JSON::XS) >= 1.52
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.42
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(Test::Without::Module)

Requires:       perl(Carp)
Requires:       perl(JSON::XS) >= 1.52

%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
JSON::Any provides a coherent API to bring together the various JSON modules
currently on CPAN.

%prep
%setup -q -n JSON-Any-%{version}

find .  -type f -exec chmod -c -x {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor --default
make

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.39-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.39-1
- 更新到 1.39

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-8
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-7
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-6
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.34-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.34-1
- Update to 1.34

* Sun Apr 20 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1.33-1
- Update to 1.33

* Sun Nov 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1.32-1
- Update to 1.32

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.30-2
- Perl 5.18 rebuild

* Sun Jun 16 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1.30-1
- Update to 1.30

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.29-2
- Perl 5.16 rebuild
- Specify all dependencies

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 1.29-1
- Update to 1.29
- Remove the defattr macro (no longer used)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.25-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Iain Arnell <iarnell@gmail.com> 1.25-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- restore JSON and JSON::Syck BRs for tests

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.22-2
- Mass rebuild with perl-5.12.0

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.22-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(JSON)
- dropped old BR on perl(JSON::Syck)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.21-2
- rebuild against perl 5.10.1

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.21-1
- auto-update to 1.21 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Test::More) (0.62 => 0.42)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Carp) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.19-1
- update to 1.19

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.16-4
- Fix Patch:/%%patch0 mismatch.

* Sat Mar 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.16-3
- patch to allow utf8 to work properly with JSON::XS earlier than version 2
- patch to skip JSON when JSON is earlier than version 2

* Wed Mar 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.16-2
- bump

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.16-1
- Specfile autogenerated by cpanspec 1.74.
