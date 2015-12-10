Name:           perl-DBD-XBase
Version:	1.05
Release:	3%{?dist}
Summary:        Perl module for reading and writing the dbf files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://www.adelton.com/perl/DBD-XBase/
Source0:        http://www.adelton.com/perl/DBD-XBase/DBD-XBase-%{version}.tar.gz
Patch0:         DBD-XBase-0.241-indexdump.PL.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(DBI)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module can read and write XBase database files, known as dbf in
dBase and FoxPro world. It also transparently reads memo fields from
the dbt, fpt and smt files and works with index files (ndx, ntx, mdx, idx,
cdx and SDBM). This module XBase.pm provides simple native interface
to XBase files. For DBI compliant database access, see DBD::XBase and
DBI modules and their man pages.


%prep
%setup -q -n DBD-XBase-%{version}
%patch0 -p1
chmod a-x eg/*table

# We want to distribute dbfdump.pl, not dbfdump
find . -type f | xargs %{__perl} -i.theorig -pe 's/(?<!\$)\bdbfdump/dbfdump.pl/g'
find . -type f -name '*.theorig' | %{__perl} -pe 's/\.theorig$//' | while read i ; do touch -r $i.theorig $i ; done
find . -type f -name '*.theorig' -exec rm -f {} ';'
mv bin/dbfdump.PL bin/dbfdump.pl.PL

%build
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
%doc Changes README ToDo driver_characteristics new-XBase
%doc eg/
%{_bindir}/*
%{perl_vendorlib}/DBD/
%{perl_vendorlib}/XBase*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.05-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.05-2
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.05-1
- 更新到 1.05

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.03-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.03-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.03-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.03-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.03-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.03-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.03-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Jan Pazdziora <jpazdziora@redhat.com> - 1.03-1
- Rebase to 1.03.

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.241-14
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.241-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.241-12
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.241-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.241-10
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.241-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.241-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.241-7
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.241-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.241-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-5
- Rebuild due to repodata corruption (#195611).

* Thu Mar 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-4
- dbfdump renamed to dbfdump.pl to avoid file conflict with shapelib (#181999).

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec 16 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-2
- Patch to remove the duplicate shebang line in bin/indexdump (#175895).

* Sat Nov 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-1
- First build.
