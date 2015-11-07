Name:           perl-DBD-SQLite
Version:	1.49_02
Release:	2%{?dist}
Summary:        SQLite DBI Driver
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
patch0:         perl-DBD-SQLite-bz543982.patch
# if sqlite >= 3.1.3 then
#   perl-DBD-SQLite uses the external library
# else
#   perl-DBD-SQLite is self-contained (uses the sqlite local copy)
BuildRequires:  sqlite-devel
BuildRequires:  perl(constant)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Prevent bug #443495
BuildRequires:  perl(DBI) >= 1.607
# Tests only
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More) >= 0.42
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite 
libraries.

%prep
%setup -q -n DBD-SQLite-%{version}
%patch0 -p1 -b .bz543982

%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
     -name '*.bs' -size 0 \) -exec rm -f {} ';'
find %{buildroot} -depth -type d -empty -exec rmdir {} ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.49_02-2
- 更新到 1.49_02

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.49_01-1
- 更新到 1.49_01

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.37-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.37-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.37-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.37-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.37-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.37-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.37-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.37-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.37-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.37-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.37-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.37-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.37-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.37-2
- Perl 5.16 rebuild

* Tue Jun 12 2012 Petr Šabata <contyk@redhat.com> - 1.37-1
- 1.37 bump (sqlite3.7.11 and various bugfixes)
- Drop command macros
- Fix dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 1.35-1
- 1.35 bump

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-2
- Perl mass rebuild

* Mon May 30 2011 Petr Sabata <contyk@redhat.com> - 1.33-1
- 1.33 bump
- BuildRoot and defattr cleanup
- Dropping the FTS3 tests patch; included upstream

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.31-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Petr Sabata <psabata@redhat.com> - 1.31-1
- New release, v1.31
- Significant FTS3 changes -- might break compatibility with pre-1.30 applications using FTS3
- New FTS3 tests patch by Paul Howarth

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-4
- fix testsuite to run with the latest sqlite (bugs.debian.org/591111)

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-3
- rebuild

* Mon Jun 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-2
- fix description/summary

* Thu Jun 10 2010 Petr Sabata <psabata@redhat.com> - 1.29-1
- Update to the latest release

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-4
- Mass rebuild with perl-5.12.0

* Mon Jan 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-3
- 543982 change Makefile.PL to compile with system sqlite

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.27-2
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> 1.27-1
- new upstream version

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.25-4
- Filtering errant private provides

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> 1.25-2
- rebuild against DBI 1.609

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.25-1
- 1.25 needed for DBIx::Class 0.08103
- auto-update to 1.25 (by cpan-spec-update 0.01)
- added a new br on perl(File::Spec) (version 0.82)
- altered br on perl(Test::More) (0 => 0.42)
- added a new br on perl(DBI) (version 1.57)

* Mon Apr 20 2009 Marcela Maslanova <mmaslano@redhat.com> 1.23-1
- update to the latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun  2 2008 Marcela Maslanova <mmaslano@redhat.com> 1.14-8

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-7
- reenable tests

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-6
- apply sanity patches derived from RT#32100

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-5.1
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.14-4.1
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3.1
- tests disabled, due to x86_64 failures

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3
- rebuild for new perl

* Wed Dec 19 2007 Steven Pritchard <steve@kspei.com> 1.14-2
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.

* Mon Dec 10 2007 Robin Norwood <rnorwood@redhat.com> - 1.14-1
- Update to latest upstream version: 1.14
- Remove patch - no longer needed.

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-2
- Rebuild for FC6.

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Wed Apr  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-4
- Patch to build with system sqlite 3.3.x (#183530).
- Patch to avoid type information segv (#187873).

* Thu Mar  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-3
- DBD::SQLite fails to build with the current FC-5 sqlite version (3.3.3);
  see bugzilla entry #183530.
  Forcing package rebuild with the included version of sqlite (3.2.7).

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-2
- Build requirement added: sqlite-devel.
- Doc file added: Changes.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.
- This new version can use an external SQLite library (>= 3.1.3).

* Sun Jun 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-2
- temporary maintainership.

* Sat Jun 11 2005 Michael A. Peters <mpeters@mac.com> 1.08-1.1
- minor changes for initial cvs checkin (removed tabs, better url in
- url tag and description tag)

* Tue Apr 12 2005 Michael A. Peters <mpeters@mac.com> 1.08-1
- created initial spec file from Fedora spectemplate-perl.spec
