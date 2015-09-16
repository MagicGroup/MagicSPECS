Name:           perl-DBIx-DBSchema
Version:	0.45
Release:	1%{?dist}
Summary:        Database-independent schema objects

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBIx-DBSchema/
Source0:	http://www.cpan.org/authors/id/I/IV/IVAN/DBIx-DBSchema-%{version}.tar.gz

BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(DBI)
BuildRequires:	perl(FreezeThaw)

# Required by the tests
BuildRequires:	perl(DBD::Pg) >= 1.32

%description
DBIx::DBSchema objects are collections of DBIx::DBSchema::Table objects and 
represent a database schema.

This module implements an OO-interface to database schemas. Using this module, 
you can create a database schema with an OO Perl interface. You can read the
schema from an existing database. You can save the schema to disk and restore
it a different process. Most importantly, DBIx::DBSchema can write SQL CREATE
statements statements for different databases from a single source.

Currently supported databases are MySQL and PostgreSQL. 

%prep
%setup -q -n DBIx-DBSchema-%{version}
chmod -x README Changes
find -name '*.pm' -exec chmod -x {} \;

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.45-1
- 更新到 0.45

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.40-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.40-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.40-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.40-2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.40-1
- Upstream update.
- Modernize specfile.

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.39-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.39-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.39-1
- Upstream update.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.38-2
- Mass rebuild with perl-5.12.0

* Mon Mar 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.38-1
- Upstream update.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.36-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.36-2
- rebuild for new perl

* Sat Dec 22 2007 Ralf Corsépius <rc040203@freenet.de> - 0.36-1
- Upstream update.
- Remove DBIx-DBSchema-0.28-version.diff.

* Wed Oct 31 2007 Ralf Corsépius <rc040203@freenet.de> - 0.35-1
- Upstream update.

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.34-1
- Upstream update.
- Update license tag.

* Mon Jul 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.33-1
- Upstream update.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.32-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.31-2
- Mass rebuild.

* Sat Apr 22 2006  Ralf Corsépius <rc040203@freenet.de> - 0.31-1
- Upstream update.

* Sun Feb 19 2006  Ralf Corsépius <rc040203@freenet.de> - 0.30-1
- Upstream update.

* Wed Dec 21 2005  Ralf Corsépius <rc040203@freenet.de> - 0.28-2
- Apply work around to CPAN incompatibility (PR #175468, J.V. Dias).

* Mon Dec 05 2005  Ralf Corsépius <rc040203@freenet.de> - 0.28-1
- Upstream update.

* Sun Nov 06 2005  Ralf Corsépius <rc040203@freenet.de> - 0.27-2
- Change URL (PR #170384, Paul Howard).

* Tue Oct 10 2005  Ralf Corsépius <rc040203@freenet.de> - 0.27-1
- Initial package.
- FE submission.
 
