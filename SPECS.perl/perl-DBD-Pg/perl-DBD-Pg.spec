Name:           perl-DBD-Pg
Summary:        A PostgreSQL interface for perl
Version:	3.5.3
Release:	2%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/DBD-Pg/

BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  postgresql-devel >= 7.4
# Run-time:
# Prevent bug #443495
BuildRequires:  perl(DBI) >= 1.607
BuildRequires:  perl(Exporter)
BuildRequires:  perl(version)
# Tests:
%tests_req perl(Cwd)
%tests_req perl(Data::Dumper)
%tests_req perl(Test::More) >= 0.61
%tests_req perl(Test::Simple)
%tests_req perl(Time::HiRes)
%tests_req postgresql-server
# Optional tests:
%tests_req perl(Encode)
%tests_req perl(File::Temp)
# test sub-package requirements
%tests_subpackage_requires perl(Carp)
%tests_subpackage_requires perl(Data::Peek)
%tests_subpackage_requires perl(DBD::Pg)
%tests_subpackage_requires perl(DBI)
%tests_subpackage_requires perl(File::Spec)
%tests_subpackage_requires perl(lib)
%tests_subpackage_requires perl(YAML)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(DBI) >= 1.52

# Missed by the find provides script:
Provides:       perl(DBD::Pg) = %{version}

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DBD::Pg\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(DBI\\)$
#{?perl_default_subpackage_tests}

%description
DBD::Pg is a Perl module that works with the DBI module to provide access
to PostgreSQL databases.

%prep
%setup -q -n DBD-Pg-%{version}
# Move testme.tmp.pl into tests sub-package
mv testme.tmp.pl t/
sed -i -e '/^testme.tmp.pl$/ s/^/t\//' MANIFEST
sed -i -e '1 s/#!.*//' t/testme.tmp.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
# If variables undefined, package test will create it's own database.


%files
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/Pg.pm
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.5.3-2
- 更新到 3.5.3

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.5.1-1
- 更新到 3.5.1

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.19.3-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.19.3-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.19.3-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.19.3-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.19.3-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.19.3-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.19.3-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.19.3-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.19.3-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.19.3-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.19.3-3
- 为 Magic 3.0 重建

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-2
- Specify all dependencies
- Move testme.tmp.pl to tests sub-package

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-1
- 2.19.3 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 2.19.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.19.2-1
- bump to 2.19.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-3
- Perl mass rebuild

* Mon Apr  4 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-2
- add requirement for test file

* Tue Mar 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-1
- update to 2.18.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.17.2-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.17.2)

* Thu Sep 30 2010 Petr Sabata <psabata@redhat.com> - 2.17.1-3
- Fixing BuildRequires (perl-version, Test::More)
- Re-enabling tests
- Resolves: rhbz#633108

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.17.1-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Petr Pisar <ppisar@redhat.com> - 2.17.1-1
- upstream released 2.17.1
- GPL+ license corrected to GPLv2+
- enable and run %%check in C locale

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.15.1-3
- drop patch that was upstreamed long ago (<=2.8.7)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-2
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-1
- new upstream version
- add versioned provide (#525502)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-2
- rebuild against perl-DBI-1.609

* Mon May  4 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-1
- new upstream release, also fixes #498899

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Stepan Kasal <skasal@redhat.com> - 2.11.6-2
- fix the source URL

* Fri Dec  5 2008 Marcela Mašláňová <mmaslano@redhat.com> - 2.11.6-1
- update

* Fri Oct 31 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.11.2-1
- update to 2.11.2

* Mon Aug 29 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.10.0-1
- update to 2.10.0

* Mon Aug 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.9.2-1
- update to 2.9.2

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.8.7-1
- new version has Pg.pm twice in two locations
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-9
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.49-8
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-7
- rebuild for new perl

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-6
- Apply changes from package review.
- Resolves: bz#226252

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-5.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-5
- Fix license tag
- Add %%doc
- Remove explicit Provides: perl(DBD::Pg) = %%{version}
- Other cleanups

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-4
- Fix summary

* Tue Dec 06 2006 Robin Norwood <rnorwood@redhat.com> - 1.49-3
- rebuild for new version of postgres.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.49-2
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 1.49-1
- Upgrade to upstream version 1.49

* Wed Apr 12 2006 Jason Vas Dias <jvdias@redhat.com> - 1.48-1
- Upgrade to upstream version 1.48

* Wed Mar 22 2006 Jason Vas Dias <jvdias@redhat.com> - 1.47-1
- Upgrade to upstream version 1.47

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 1.45-1
- Upgrade to upstream version 1.45

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.43-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 03 2005 Florian La Roche <laroche@redhat.com>
- make sure correct Provides: are generated for this module

* Tue Jun 28 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.43-1
- Update to 1.43 (corrects #156840).

* Thu May 19 2005 Warren Togami <wtogami@redhat.com> - 1.41-2
- Disable gcc optimization to workaround broken placeholders (#156840)

* Wed  Apr 13 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.41-1
- Update to 1.41.
- Updated the requirements versions.
- Specfile cleanup. (#154203)

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 1.40-2
- rebuild for new libpq soname

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.40-1
- 1.40

* Tue Oct 12 2004 Chip Turner <cturner@redhat.com> 1.32-1
- bugzilla: 127755, update to 1.32

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.31-2
- rebuild

* Thu Dec 11 2003 Chip Turner <cturner@redhat.com> 1.31-1
- update to 1.31

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.22-1
- move to upstream 1.22

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Mon Jan 13 2003 Chip Turner <cturner@redhat.com>
- update to 1.21

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use internal rpm dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-5
- Rebuild

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-4
- Rebuild, to fix #66304

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-3
- Integrate with newer perl

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-1
- 1.13

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-8
- Rebuild

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-7
- Rebuild

* Thu Jan 31 2002 Tim Powers <timp@redhat.com>
- rebuild to solve more deps

* Tue Jan 29 2002 Bill Nottingham <notting@redhat.com> 1.01-5
- rebuild (dependencies)

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-2
- Rebuild

* Sun Jul  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.01 bugfix release ("bytea" coredumped with values outside 0...127)
- Add perl-DBI and perl to BuildRequires (they were just in Requires: previously)

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.00
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.98, for postgresql-7.1
- add doc files
- cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- First cut
