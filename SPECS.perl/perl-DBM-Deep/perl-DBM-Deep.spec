Name:           perl-DBM-Deep
Version:	2.0012
Release:	2%{?dist}
Summary:        A pure perl multi-level hash/array DBM
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/DBM-Deep/
Source0:        http://www.cpan.org/modules/by-module/DBM/DBM-Deep-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 3:5.8.4
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Exporter)
# Package in RHEL cannot BR: package in EPEL
%if ! (0%{?rhel} >= 7)
BuildRequires:  perl(FileHandle::Fmode)
%endif
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Pod::Usage) >= 1.3
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# not automatically detected
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Digest::MD5)

%description
A unique flat-file database module, written in pure perl. True multi-level
hash/array support (unlike MLDBM, which is faked), hybrid OO / tie()
interface, cross-platform FTPable files, and quite fast. Can handle
millions of keys and unlimited hash levels without significant slow-down.
Written from the ground-up in pure perl -- this is NOT a wrapper around a
C-based DBM. Out-of-the-box compatibility with Unix, Mac OS X and Windows.

%prep
%setup -q -n DBM-Deep-%{version}

%build
export PERL_MM_USE_DEFAULT=1
perl Build.PL installdirs=vendor 
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
LONG_TESTS=1 TEST_SQLITE=1 ./Build test

%files
%doc Changes README
%{perl_vendorlib}/DBM/
%{_mandir}/man3/DBM::Deep*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.0012-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.0012-1
- 更新到 2.0012

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.0008-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.0008-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.0008-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.0008-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.0008-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.0008-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.0008-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.0008-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.0008-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Paul Howarth <paul@city-fan.org> - 2.0008-1
- Update to 2.0008 (#832921)
  - Arrays and hashes retrieved from a database no longer create circular
    references (CPAN RT#77746)
- Don't use macros for commands

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 2.0007-2
- Perl 5.16 rebuild

* Mon May 28 2012 Paul Howarth <paul@city-fan.org> - 2.0007-1
- Update to 2.0007
  - Include one-line descriptions of each POD page after the name
    (CPAN RT#76378)
  - t/98_pod.t: skip tests if Pod::Simple 3.21 is installed (CPAN RT#77419)
- BR: perl(Pod::Simple)

* Fri May 18 2012 Petr Pisar <ppisar@redhat.com> - 2.0006-2
- Do not build-require FileHandle::Fmode on RHEL ≥ 7 (#822885)

* Mon Apr  2 2012 Paul Howarth <paul@city-fan.org> - 2.0006-1
- Update to 2.0006
  - Try harder to get t/27_filehandle.t to work under TB2; the extra
    'TAP version 13' line was causing a TAP parse error

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 2.0005-1
- Update to 2.0005 (t/27_filehandle.t has been fixed again; it no longer
  violates Test::Builder's encapsulation)
- BR/R: perl(Carp) and perl(Data::Dumper)
- Add buildreqs for module and support utilities: perl ≥ 5.8.4, perl(base),
  perl(constant), perl(DBI), perl(FileHandle::Fmode) and perl(Pod::Usage) ≥ 1.3
- Add buildreqs for additional test coverage: perl(DBD::SQLite),
  perl(Exporter), perl(Test::Pod) and perl(Test::Pod::Coverage)
- Run LONG_TESTS and SQLite tests too
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Use %%{_fixperms} macro rather than our own chmod incantation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 2.0004-2
- R/BR perl(Digest::MD5)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0004-1
- update to 2.004
- clean spec, add BR Test::Deep, Test::Warn

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.983-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-9
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.983-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.983-3
- rebuild for new perl

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.983-2
- FE6 Rebuild

* Thu Apr 27 2006 Andreas Thienemann <andreas@bawue.net> 0.983-1
- Specfile autogenerated by cpanspec 1.64.
- Cleaned up for FE
