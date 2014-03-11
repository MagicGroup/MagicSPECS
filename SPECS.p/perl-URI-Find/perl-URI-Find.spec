Name:           perl-URI-Find
Summary:        Find URIs in plain text
Version:        20111103
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSCHWERN/URI-Find-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/URI-Find
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Module::Build) >= 0.30
BuildRequires:  perl(Test::More) >= 0.82
# needed for tests
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(URI) >= 1.00
BuildRequires:  perl(URI::URL) >= 5.00

Requires:       perl(URI) >= 1.00
Requires:       perl(URI::URL) >= 5.00


%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
This module does one thing: Finds URIs and URLs in plain text. It finds
them quickly and it finds them *all* (or what URI::URL considers a URI to
be.) It only finds URIs which include a scheme (http:// or the like), for
something a bit less strict have a look at URI::Find::Schemeless.

For a command-line interface, see Darren Chamberlain's 'urifind' script.
It's available from his CPAN directory:

    http://www.cpan.org/authors/id/D/DA/DARREN/

%prep
%setup -q -n URI-Find-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README TODO
%{perl_vendorlib}/*
%{_bindir}/urifind
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 20111103-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 20111103-2
- Perl 5.16 rebuild

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 20111103-1
- Update to 20111103
- Remove the defattr macro (no longer used)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20100505-2
- Perl mass rebuild

* Sun Mar 27 2011 Iain Arnell <iarnell@gmail.com> 20100505-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100211-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 20100211-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 20100211-2
- Mass rebuild with perl-5.12.0

* Tue Mar 02 2010 Chris Weyl <cweyl@alumni.drew.edu> 20100211-1
- update by Fedora::App::MaintainerTools 0.004
- updating to latest GA CPAN version (20100211)
- added a new req on perl(URI) (version 1.00)
- added a new req on perl(URI::URL) (version 5.00)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 20090319-4
- rebuild against perl 5.10.1

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 20090319-3
- Use Build.PL (Fix mass rebuild breakdown).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090319-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 20090319-1
- auto-update to 20090319 (by cpan-spec-update 0.01)
- added a new br on perl(Test::More) (version 0.82)
- added a new br on perl(Module::Build) (version 0.30)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 14 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.16-2
- bump

* Fri Dec 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update for submission

* Thu Dec 11 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.16-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.6)
