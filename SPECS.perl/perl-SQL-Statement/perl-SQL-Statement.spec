Name:           perl-SQL-Statement
Version:	1.407
Release:	1%{?dist}
Summary:        SQL parsing and processing engine

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/SQL-Statement/
Source0:        http://www.cpan.org/authors/id/R/RE/REHSACK/SQL-Statement-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(DBI) >= 1.612
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Clone) >= 0.30
BuildRequires:  perl(Params::Util) >= 1.00
# for tests only:
# DBD::CSV buildrequires SQL::Statement
%if 0%{!?perl_bootstrap:1}
BuildRequires:  perl(DBD::CSV) >= 0.30
%endif
BuildRequires:  perl(DBD::DBM) >= 0.06
BuildRequires:  perl(DBD::File) >= 0.40
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBI::DBD::SqlEngine) >= 0.03
BuildRequires:  perl(DBD::XBase)
BuildRequires:  perl(MLDBM)
BuildRequires:  perl(Test::Simple) >= 0.90
# For maintainer tests only:
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
# Test::Pod::Spelling::CommonMistakes not packaged yet
# Bundle::Test::SQL::Statement not packaged or released yet
#BuildRequires:  perl(Test::Pod::Spelling::CommonMistakes)

%description
The SQL::Statement module implements a pure Perl SQL parsing and execution
engine.  While it by no means implements full ANSI standard, it does support
many features including column and table aliases, built-in and user-defined
functions, implicit and explicit joins, complexly nested search conditions, and
other features.


%prep
%setup -q -n SQL-Statement-%{version}
find  -type f -perm /111 | xargs chmod -c a-x
%{__perl} -pi -e 's/\r\n/\n/' README


%build
export SQL_STATEMENT_WARN_UPDATE=sure
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/SQL/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.407-1
- 更新到 1.407

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.33-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.33-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.33-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.33-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.33-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.33-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.33-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.33-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.33-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.33-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.33-8
- Perl 5.16 re-rebuild of bootstrapped packages

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 1.33-7
- Perl 5.16 rebuild

* Tue Apr 10 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-6
- remove DBD::AnyData which were removed by upstream for now 810377

* Fri Apr  6 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-5
- apply Paul's bootstrap macro 810377

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.33-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Petr Sabata <psabata@redhat.com> - 1.33-1
- 1.33 bump

* Mon Jan 24 2011 Petr Pisar <ppisar@redhat.com> - 1.32-1
- 1.32 bump
- Update build time dependencies

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.31-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Sep 07 2010 Petr Pisar <ppisar@redhat.com> - 1.31-1
- 1.31 bump (incompatible with perl(DBI) <= 1.611) (bug #631306)

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.27-1
- 1.27 bump (do not backport, 1.22 lower-cases unqouted identifiers)
- Make tests fatal again

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-2
- rebuild against perl 5.10.1

* Wed Sep 23 2009 Stepan Kasal <skasal@redhat.com> - 1.20-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-2
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-2
- Rebuild for FC5 (perl 5.8.8).

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- First build.
