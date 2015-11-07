Name:           perl-Date-Manip
Version:	6.51
Release:	2%{?dist}
Summary:        Date manipulation routines
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Date-Manip/
Source0:        http://www.cpan.org/authors/id/S/SB/SBECK/Date-Manip-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
# Tests only
BuildRequires:  perl(Test::Inter)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# This package was formerly known as perl-DateManip
Provides: perl-DateManip = %{version}-%{release}
Obsoletes: perl-DateManip < 5.48-1

%{?perl_default_filter}

%description
Date::Manip is a series of modules designed to make any common date/time
operation easy to do. Operations such as comparing two times, determining a
data a given amount of time from another, or parsing international times
are all easily done. It deals with time as it is used in the Gregorian
calendar (the one currently in use) with full support for time changes due
to daylight saving time.

%prep
%setup -q -n Date-Manip-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%{perl_vendorlib}/Date/
%{_mandir}/man[13]/*.[13]*
%{_bindir}/dm_*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 6.51-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 6.51-1
- 更新到 6.51

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 6.36-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 6.36-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 6.36-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.36-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.36-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.36-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.36-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 6.36-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 6.36-2
- 为 Magic 3.0 重建

* Thu Nov 01 2012 Petr Šabata <contyk@redhat.com> - 6.36-1
- 6.36 bump

* Wed Sep 12 2012 Jitka Plesnikova <jplesnik@redhat.com> - 6.34-1
- 6.34 bump
- examples are included in man pages and bin directory. Remove them from doc.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 6.32-2
- Perl 5.16 rebuild

* Mon Jun 04 2012 Petr Šabata <contyk@redhat.com> - 6.32-1
- 6.32 bump
- Remove command macros
- Don't require a specific version of Module::Build

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 6.31-2
- Round Module::Build version to 2 digits

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.31-1
- bump to 6.31

* Fri Jan 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 6.30-1
- bump to 6.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 01 2011 Petr Pisar <ppisar@redhat.com> - 6.25-1
- 6.25 bump
- Package examples

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.24-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 6.24-2
- Perl mass rebuild

* Tue Jun 14 2011 Petr Sabata <contyk@redhat.com> - 6.24-1
- 6.24 bump
- defattr removed

* Mon Apr 18 2011 Petr Sabata <psabata@redhat.com> - 6.23-1
- 6.23 bump
- IO::File added to BR
- Buildroot stuff removed

* Tue Mar  8 2011 Petr Sabata <psabata@redhat.com> - 6.22-1
- 6.22 bump, new timezone data

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Marcela Mašláňová <mmaslano@redhat.com> - 6.21-1
- update to 6.21

* Fri Dec  3 2010 Petr Sabata <psabata@redhat.com> - 6.20-1
- 6.20 bump, internal resources might be incompatible with previous versions

* Wed Oct 27 2010 Petr Pisar <ppisar@redhat.com> - 6.14-1
- 6.14 bump
- Remove double-required perl(YAML::Syck)

* Mon Oct 18 2010 Petr Sabata <psabata@redhat.com> - 6.13-1
- 6.13 bump

* Mon Oct  4 2010 Petr Sabata <psabata@redhat.com> - 6.12-1
- 6.12 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 6.11-1
- 6.11 bump

* Tue Apr 27 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.07-3
- Mass rebuild with perl-5.12.0

* Fri Apr 16 2010 Marcela Mašláňová <mmaslano@redhat.com> - 6.07-1
- update

* Mon Feb  1 2010 Marcela Mašláňová <mmaslano@redhat.com> - 6.05-1
- update, remove patch (tested functionality without it)

* Wed Jan 13 2010 Marcela Mašláňová <mmaslano@redhat.com> - 5.54-5
- add license into doc and fix rpmlint warnings

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 5.54-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Stepan Kasal <skasal@redhat.com> - 5.54-1
- new upstream version
- add BuildRequires so that testsuite can be fully executed

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.48-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.48-2
- rebuild for new perl

* Thu Jan  3 2008 Ed Avis <eda@waniasset.com> - 5.48-1
- Update to 5.48.
- rhbz#214709 Krasnoyarsk patch now upstream.
- Changed name to Date-Manip as now used on CPAN.

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 5.44-4
- Apply patch to use date +%%z as possible source for timezone data
- Fix license tag

* Tue Mar 20 2007 Robin Norwood <rnorwood@redhat.com> - 5.44-3
- Fix minor issues in spec file for package review
- Bump release
- Resolves: rhbz#226250

* Fri Nov 10 2006 Robin Norwood <rnorwood@redhat.com> - 5.44-2
- Add support for KRAT and KRAST timezones
- Include magic dist tag in release
- Resolves: rhbz#214709
- Related: rhbz#100786

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.44-1.3
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.44-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.44-1
- Update to 5.44.

* Mon Apr 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.42a-4
- Bring up to date with current Fedora.Extras perl spec template. (#155913)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 5.42a-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.42a-1
- update to 5.42a

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated.
