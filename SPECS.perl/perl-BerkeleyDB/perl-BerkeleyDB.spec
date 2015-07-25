# We have db4 up to Fedora 13, then db5 (in the libdb package)
%if 0%{?fedora} > 13
%global db_pkg libdb
%else
%global db_pkg db4
%endif

# We need to know the exact DB version we're built against
%global db_ver %(sed '/DB_VERSION_STRING/!d;s/.*Berkeley DB[[:space:]]*\\([^:]*\\):.*/\\1/' /usr/include/db.h 2>/dev/null || echo 4.0.0)

Name:           perl-BerkeleyDB
Version:	0.55
Release:	1%{?dist}
Summary:        Interface to Berkeley DB
Summary(zh_CN.UTF-8): 伯克利 DB 的接口
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/BerkeleyDB/
Source0:        http://www.cpan.org/authors/id/P/PM/PMQS/BerkeleyDB-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{db_pkg}-devel
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
# For "".
BuildRequires:  perl(MLDBM)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Hard-code Berkeley DB requirement to avoid problems like #592209
Requires:       %{db_pkg} = %{db_ver}

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
BerkeleyDB is a module that allows Perl programs to make use of the
facilities provided by Berkeley DB. Berkeley DB is a C library that
provides a consistent interface to a number of database formats.
BerkeleyDB provides an interface to all four of the database types
(hash, btree, queue and recno) currently supported by Berkeley DB.

%description -l zh_CN.UTF-8
伯克利 DB 的接口。

%prep
%setup -q -n BerkeleyDB-%{version}
%{__perl} -pi -e 's,/local/,/, if ($. == 1)' dbinfo
chmod -x Changes README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

install -D -m755 dbinfo $RPM_BUILD_ROOT%{_bindir}/dbinfo

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

# Remove files we don't want packaged
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/{mkconsts,scan}.pl

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README Changes Todo
%{_bindir}/dbinfo
%{perl_vendorarch}/BerkeleyDB/
%{perl_vendorarch}/BerkeleyDB.pm
%doc %{perl_vendorarch}/BerkeleyDB.pod
%{perl_vendorarch}/auto/BerkeleyDB/
%{_mandir}/man3/BerkeleyDB.3pm*

%changelog
* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 0.55-1
- 更新到 0.55

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.49-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.49-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.49-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.49-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 21 2011 Paul Howarth <paul@city-fan.org> - 0.49-2
- Rebuild for libdb 5.2.36 in Rawhide

* Sun Sep 18 2011 Steven Pritchard <steve@kspei.com> 0.49-1
- Update to 0.49.
- BR Cwd (not in core now).

* Sun Jun 19 2011 Paul Howarth <paul@city-fan.org> - 0.48-2
- Perl mass rebuild

* Sun Jun 19 2011 Paul Howarth <paul@city-fan.org> - 0.48-1
- Update to 0.48
  - Added support for db_exists and lock_detect
  - Fixed bug with c_pget when the DB_GET_BOTH flag is used
  - Fixed bug with db_pget when the DB_GET_BOTH flag is used
  - Changes to build with BDB 5.2
  - Add support for new Heap database format
  - Fixed test harness issue with Heap.t (CPAN RT#68818)
- Don't package build tools mkconsts.pl and scan.pl

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.43-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Paul Howarth <paul@city-fan.org> - 0.43-4
- Rebuild for libdb 5.1.25 in Rawhide

* Wed Sep 29 2010 jkeating - 0.43-3
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Paul Howarth <paul@city-fan.org> - 0.43-2
- Rebuild for libdb 5.1.19 in Rawhide

* Tue Aug  3 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.43-1
- Update to 0.43
  - Changes to build with BDB 5.1
  - Dropped support for Server option when creating an environment
  - Documentation updates (CPAN RT#59202)
  - Fixed compilation error with MS Visual Studio 2005 (CPAN RT#59924)

* Wed Jul  7 2010 Paul Howarth <paul@city-fan.org> - 0.42-1
- Update to 0.42
  - added $db->Env method to retrieve environment object from a database object
  - get the tied interface to use truncate in the CLEAR method if available
- Build with libdb (Berkeley DB 5.x) from Fedora 14 onwards (#612139)
- Tag BerkeleyDB.pod as %%doc
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Tue May 25 2010 Paul Howarth <paul@city-fan.org> - 0.41-3
- Rebuild for Berkeley DB 4.8.30 in F-13 and Rawhide (#592209)
- Hard-code Berkeley DB requirement to avoid problems like #592209
- Add %%{?perl_default_filter}

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.41-2
- Mass rebuild with perl-5.12.0

* Sat Feb 13 2010 Steven Pritchard <steve@kspei.com> 0.41-1
- Update to 0.41.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.39-2
- rebuild against perl 5.10.1

* Sat Aug 29 2009 Steven Pritchard <steve@kspei.com> 0.39-1
- Update to 0.39.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Steven Pritchard <steve@kspei.com> 0.38-1
- Update to 0.38.

* Thu Jun 04 2009 Steven Pritchard <steve@kspei.com> 0.36-1
- Update to 0.36.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 15 2008 Steven Pritchard <steve@kspei.com> 0.34-1
- Update to 0.34.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.33-3
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.33-2
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 0.33-1
- Update to 0.33.
- Update License tag.
- BR Test::More.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.32-2
- Rebuild for selinux ppc32 issue.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 0.32-1
- Update to 0.32.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 0.31-3
- BR ExtUtils::MakeMaker.

* Mon Oct 16 2006 Steven Pritchard <steve@kspei.com> 0.31-2
- Rebuild.

* Mon Oct 16 2006 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.
- Use fixperms macro instead of our own chmod incantation.

* Wed Sep 13 2006 Steven Pritchard <steve@kspei.com> 0.30-1
- Update to 0.30.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 0.29-2
- Minor spec cleanup.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.29-1
- Update to 0.29.

* Fri Jun 30 2006 Steven Pritchard <steve@kspei.com> 0.28-1
- Update to 0.28

* Sat Feb 18 2006 Steven Pritchard <steve@kspei.com> 0.27-2
- Rebuild

* Tue Jan 10 2006 Steven Pritchard <steve@kspei.com> 0.27-1
- Update to 0.27

* Wed Oct 12 2005 Steven Pritchard <steve@kspei.com> 0.26-6
- Another rebuild

* Sat Sep 24 2005 Steven Pritchard <steve@kspei.com> 0.26-5
- Rebuild for new db4 in rawhide

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 0.26-4
- Spec cleanup
- Include COPYING and Artistic

* Wed Aug 03 2005 Steven Pritchard <steve@kspei.com> 0.26-3
- Move OPTIMIZE to Makefile.PL instead of make

* Mon Aug 01 2005 Steven Pritchard <steve@kspei.com> 0.26-2
- Various fixes from Paul Howarth:
  - Add description
  - Fix permissions on docs (also Paul Howarth)
  - Add OPTIMIZE to make
  - Don't own perl_vendorarch/auto/
  - BuildRequire Test::Pod and MLDBM

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> 0.26-1
- Specfile autogenerated.
- Add BuildRequires db4-devel.
- Install dbinfo script.
