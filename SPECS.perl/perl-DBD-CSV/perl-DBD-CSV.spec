Name:           perl-DBD-CSV
Version:	0.48
Release:	2%{?dist}
Summary:        DBI driver for CSV files
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-CSV/
Source0:        http://search.cpan.org/CPAN/authors/id/H/HM/HMBRAND/DBD-CSV-%{version}.tgz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(DBD::File) >= 0.40
BuildRequires:  perl(DBI) >= 1.614
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(SQL::Statement) >= 1.33
BuildRequires:  perl(Text::CSV_XS) >= 0.91
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.98
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(DBD::File) >= 0.40
Requires:       perl(DBI) >= 1.614
Requires:       perl(SQL::Statement) >= 1.31
Requires:       perl(Text::CSV_XS) >= 0.91

# RPM 4.8 style
%filter_from_requires /^perl(DBD::File)$/d
%filter_from_requires /^perl(Text::CSV_XS)$/d
%filter_setup
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(DBD::File\\)$
%global __requires_exclude %__requires_exclude|^perl\\(Text::CSV_XS\\)$

%description
The DBD::CSV module is yet another driver for the DBI (Database
independent interface for Perl). This one is based on the SQL
"engine" SQL::Statement and the abstract DBI driver DBD::File
and implements access to so-called CSV files (Comma separated
values). Such files are mostly used for exporting MS Access and
MS Excel data.

%prep
%setup -q -n DBD-CSV-%{version}
chmod -c a-x ChangeLog README lib/DBD/*.pm lib/Bundle/DBD/*.pm

%build
perl Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%doc ChangeLog README
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/DBD/
%exclude %{perl_vendorlib}/DBI/Test/
%{_mandir}/man3/*.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.48-2
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.48-1
- 更新到 0.48

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.36-13
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.36-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.36-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.36-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.36-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.36-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.36-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.36-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.36-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.36-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.36-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.36-2
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Petr Šabata <contyk@redhat.com> - 0.36-1
- 0.36 bump, debugging enhancements

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 0.35-2
- Perl 5.16 rebuild

* Tue Jun 05 2012 Petr Šabata <contyk@redhat.com> - 0.35-1
- 0.35 bump (documentation changes)

* Tue May 15 2012 Petr Šabata <contyk@redhat.com> - 0.34-1
- 0.34 bump (no code changes)
- Drop commands macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Petr Sabata <contyk@redhat.com> - 0.33-1
- 0.33 bump
- Remove now obsolete BuildRoot and defattr

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 0.31-5
- RPM 4.9 dependency filtering added

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.31-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 22 2010 Petr Pisar <ppisar@redhat.com> - 0.31-1
- 0.31 bump
- Remove unversioned Requires

* Mon Jul 12 2010 Petr Pisar <ppisar@redhat.com> - 0.30-1
- 0.30 bump (bug #613251)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 0.29-1
- 0.29 bump

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.27-2
- Mass rebuild with perl-5.12.0

* Thu Mar 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.27-1
- update
- replace DESTDIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.22-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-5
- Added perl(SQL::Statement) to requirements list (#208012).

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-4
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-3
- Rebuild for FC5 (perl 5.8.8).

* Sat Dec 17 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Missing build requirement: DBD::File >= 0.30.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- First build.
