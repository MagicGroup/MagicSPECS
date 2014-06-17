Name:           perl-DBIx-Class
Summary:        Extensible and flexible object <-> relational mapper
Version:        0.08203
Release:        12%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/F/FR/FREW/DBIx-Class-%{version}.tar.gz
URL:            http://search.cpan.org/dist/DBIx-Class/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Class::Accessor::Grouped) >= 0.10002
BuildRequires:  perl(Class::C3::Componentised) >= 1.0009
BuildRequires:  perl(Class::Inspector) >= 1.24
BuildRequires:  perl(Class::Method::Modifiers) >= 1.06
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Config::Any) >= 0.20
BuildRequires:  perl(Context::Preserve) >= 0.01
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Data::Compare) >= 1.22
BuildRequires:  perl(Data::Dumper::Concise) >= 2.020
BuildRequires:  perl(Data::Page) >= 2.00
BuildRequires:  perl(DBD::SQLite) >= 1.29
BuildRequires:  perl(DBI) >= 1.609
%if !0%{?perl_bootstrap}
BuildRequires:  perl(DBIx::Class::Storage::Debug::PrettyPrint)
%endif
BuildRequires:  perl(Devel::GlobalDestruction)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Path) >= 2.07
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(Math::Base36) >= 0.07
BuildRequires:  perl(Math::BigInt) >= 1.89
BuildRequires:  perl(Module::Find) >= 0.06
BuildRequires:  perl(Moo) >= 0.009100
BuildRequires:  perl(MRO::Compat) >= 0.09
BuildRequires:  perl(Package::Stash) >= 0.28
BuildRequires:  perl(Path::Class) >= 0.18
BuildRequires:  perl(Scope::Guard) >= 0.03
BuildRequires:  perl(SQL::Abstract) >= 1.73
BuildRequires:  perl(strictures) >= 1.003001
BuildRequires:  perl(Sub::Name) >= 0.04
BuildRequires:  perl(Test::Builder) >= 0.94
BuildRequires:  perl(Test::Exception) >= 0.31
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Warn) >= 0.21
BuildRequires:  perl(Text::CSV_XS)
BuildRequires:  perl(Try::Tiny) >= 0.04

Requires:       perl(Class::Accessor::Grouped) >= 0.10002
Requires:       perl(Class::C3::Componentised) >= 1.0009
Requires:       perl(Class::Inspector) >= 1.24
Requires:       perl(Config::Any) >= 0.20
Requires:       perl(Context::Preserve) >= 0.01
Requires:       perl(Data::Compare) >= 1.22
Requires:       perl(Data::Dumper::Concise) >= 2.020
Requires:       perl(Data::Page) >= 2.00
Requires:       perl(DBI) >= 1.609
Requires:       perl(Module::Find) >= 0.06
Requires:       perl(MRO::Compat) >= 0.09
Requires:       perl(Path::Class) >= 0.18
Requires:       perl(Scope::Guard) >= 0.03
Requires:       perl(SQL::Abstract) >= 1.72
Requires:       perl(Sub::Name) >= 0.04

### Additional generated deps. These deps are regenerated from scratch every
### time this spec file is updated.
# from DBIx::Class::Optional::Dependencies
BuildRequires: perl(Class::DBI::Plugin::DeepAbstractSearch)
BuildRequires: perl(Class::Trigger)
BuildRequires: perl(Clone)
BuildRequires: perl(DBIx::ContextualFetch)
BuildRequires: perl(Date::Simple) >= 3.03
BuildRequires: perl(DateTime::Format::MySQL)
BuildRequires: perl(DateTime::Format::Pg)
BuildRequires: perl(DateTime::Format::SQLite)
BuildRequires: perl(DateTime::Format::Strptime)
BuildRequires: perl(Devel::Cycle) >= 1.10
BuildRequires: perl(Getopt::Long::Descriptive) >= 0.081
BuildRequires: perl(Hash::Merge) >= 0.12
BuildRequires: perl(JSON::Any) >= 1.22
BuildRequires: perl(Moose) >= 0.98
BuildRequires: perl(MooseX::Types) >= 0.21
BuildRequires: perl(MooseX::Types::JSON) >= 0.02
BuildRequires: perl(MooseX::Types::Path::Class) >= 0.05
BuildRequires: perl(Pod::Coverage) >= 0.20
BuildRequires: perl(SQL::Translator) >= 0.11005
BuildRequires: perl(Test::Memory::Cycle)
BuildRequires: perl(Text::CSV) >= 1.16
BuildRequires: perl(Time::Piece::MySQL)
BuildRequires: perl(namespace::autoclean) >= 0.09
BuildRequires: perl(namespace::clean) >= 0.20

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.08196-2
Provides:       %{name}-tests = %{version}-%{release}

# hidden from PAUSE
Provides:       perl(DBIx::Class::ResultSource::RowParser) = %{version}

%?perl_default_filter
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(DBD::Pg\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(DBD::Pg\\)$
%global __requires_exclude %__requires_exclude|perl\\(DBIx::Class::(Admin|CDBICompat|ClassResolver|Storage|Componentised|ResultSourceProxy)
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{perl_vendorlib}/DBIx/Class/Admin
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}%{perl_vendorlib}/DBIx/Class/Admin
%global __provides_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/CDBICompat
%global __requires_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/CDBICompat
%global __provides_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/PK/Auto
%global __requires_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/PK/Auto
%global __provides_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/SQLAHacks
%global __requires_exclude_from %__provides_exclude_from|%{perl_vendorlib}/DBIx/Class/SQLAHacks
%global __provides_exclude %__provides_exclude|perl\\(DBIx::Class::SQLAHacks\\)
%global __requires_exclude %__requires_exclude|perl\\(DBIx::Class::SQLAHacks\\)
%global __provides_exclude %__provides_exclude|perl\\(DBIx::Class::Storage::DBIHacks\\)
%global __requires_exclude %__requires_exclude|perl\\(DBIx::Class::Storage::DBIHacks\\)
%global __provides_exclude %__provides_exclude|perl\\(DBIx::Class::SQLMaker::
%global __requires_exclude %__requires_exclude|perl\\(DBIx::Class::SQLMaker::

%description
This is an SQL to OO mapper with an object API inspired by Class::DBI
(and a compatibility layer as a springboard for porting) and a
resultset API that allows abstract encapsulation of database
operations. It aims to make representing queries in your code as perl-
ish as possible while still providing access to as many of the
capabilities of the database as possible, including retrieving related
records from multiple tables in a single query, JOIN, LEFT JOIN, COUNT,
DISTINCT, GROUP BY and HAVING support.

%prep
%setup -q -n DBIx-Class-%{version}

find t/ -type f -exec perl -pi -e 's|\r||; s|^#!perl|#!%{__perl}|' {} +
find .  -type f -exec chmod -c -x {} +
find t/ -type f -name '*.orig' -exec rm -v {} +

# utf8 issues
for i in `find . -type f` ; do
    iconv -f iso8859-1 -t UTF-8 $i > foo
    mv foo $i
done

chmod -c +x script/*

# skip dbic_pretty.t when bootstrapping
%if 0%{?perl_bootstrap}
rm t/storage/dbic_pretty.t
%endif

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
# note this test suite is noisy!
export DBICTEST_THREAD_STRESS=1
export DBICTEST_FORK_STRESS=1
export DBICTEST_STORAGE_STRESS=1
export DATA_DUMPER_TEST=1
make test

%files
%doc Changes README examples/ t/
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man[13]/*


%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.08203-12
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.08203-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.08203-10
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.08203-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.08203-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.08203-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08203-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08203-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08203-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08203-3
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.08203-2
- 为 Magic 3.0 重建

* Sat Oct 20 2012 Iain Arnell <iarnell@gmail.com> 0.08203-1
- update to latest upstream version

* Sun Aug 26 2012 Iain Arnell <iarnell@gmail.com> 0.08200-1
- update to latest upstream version

* Sat Aug 04 2012 Iain Arnell <iarnell@gmail.com> 0.08198-3
- rebuild without bootstrap again

* Sat Aug 04 2012 Iain Arnell <iarnell@gmail.com> 0.08198-2
- explicitly provide DBIx::Class::ResultSource::RowParser
- build with bootstrap enabled to fix broken dependencies

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 0.08198-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08196-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.08196-5
- Perl 5.16 re-rebuild of bootstrapped packages

* Sat Jun 30 2012 Petr Pisar <ppisar@redhat.com> - 0.08196-4
- Perl 5.16 rebuild

* Thu Apr 12 2012 Iain Arnell <iarnell@gmail.com> 0.08196-3
- BR DBIx::Class::Storage::Debug::PrettyPrint (rhbz#812143)

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.08196-2
- drop tests subpackage; move tests to main package documentation
- drop old-style filtering

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.08196-1
- update to latest upstream version

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.08195-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- minor filtering tweak

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.08127-5.1
- Fix the filters for perl(DBIx::Class::SQLMaker*)

* Fri Jul 22 2011 Petr Sabata <contyk@redhat.com> - 0.08127-5
- RPM 4.9 dependency filtering added

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.08127-4
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.08127-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08127-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Iain Arnell <iarnell@gmail.com> 0.08127-1
- update to latest upstream version
- additional filters from requires

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.08126-1
- update to latest upstream version

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08123-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Sep 09 2010 Iain Arnell <iarnell@gmail.com> 0.08123-1.1
- don't buildrequire Test::Pod

* Thu Sep 02 2010 Iain Arnell <iarnell@gmail.com> 0.08123-1
- update to latest upstream version
- dbicadmin script needs to be executable for tests
- manually tweak real buildrequires

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08120-4
- Mass rebuild with perl-5.12.0

* Fri Mar 19 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08120-3
- quiet our repo/dep-checking scripts as we figure out how to handle no_index
  from a "requires" perspective

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08120-2
- update F::A::MT so bits marked as "no_index" are filtered both for provides
  _and_ requires
- update by Fedora::App::MaintainerTools 0.006
- additional deps script run; 27 deps found

* Sat Mar 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08120-1
- update by Fedora::App::MaintainerTools 0.004
- updating to latest GA CPAN version (0.08120)
- added a new br on perl(Context::Preserve) (version 0.01)
- added manual BR on perl(Test::Moose)
- added a new req on perl(Context::Preserve) (version 0.01)
- dropped old requires on perl(List::Util)
- dropped old requires on perl(Scalar::Util)
- dropped old requires on perl(Storable)
- additional deps script run; 27 deps found

* Fri Mar  5 2010 Stepan Kasal <skasal@redhat.com> 0.08119-3
- filter also requires for "hidden" package declarations

* Thu Mar 04 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08119-2
- add ok to BR (unlisted optional testing dep)

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08119-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(Path::Class) (0.16 => 0.18)
- dropped old BR on perl(Class::C3)
- dropped old BR on perl(JSON::Any)
- altered req on perl(Path::Class) (0.16 => 0.18)
- dropped old requires on perl(DBD::SQLite)
- dropped old requires on perl(JSON::Any)
- additional deps script run; 26 deps found

* Sun Feb 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08117-1
- auto-update to 0.08117 (by cpan-spec-update 0.01)
- altered br on perl(Class::Accessor::Grouped) (0.09000 => 0.09002)
- altered br on perl(DBI) (1.605 => 1.609)
- altered br on perl(SQL::Abstract) (1.60 => 1.61)
- altered req on perl(Class::Accessor::Grouped) (0.09000 => 0.09002)
- altered req on perl(DBI) (1.605 => 1.609)
- altered req on perl(SQL::Abstract) (1.60 => 1.61)

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08115-1
- auto-update to 0.08115 (by cpan-spec-update 0.01)
- added a new br on perl(Data::Dumper::Concise) (version 1.000)
- altered br on perl(SQL::Abstract) (1.58 => 1.60)
- added a new req on perl(Data::Dumper::Concise) (version 1.000)
- altered req on perl(SQL::Abstract) (1.58 => 1.60)

* Tue Jan 19 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.08112-2
- bump

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08112-1
- auto-update to 0.08112 (by cpan-spec-update 0.01)

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08111-1
- update filtering
- auto-update to 0.08111 (by cpan-spec-update 0.01)
- altered br on perl(Carp::Clan) (6 => 6.0)
- altered br on perl(Class::Accessor::Grouped) (0.08003 => 0.09000)
- altered br on perl(Data::Page) (2 => 2.00)
- altered br on perl(File::Temp) (0 => 0.22)
- altered br on perl(SQL::Abstract) (1.56 => 1.58)
- altered br on perl(Test::More) (0 => 0.92)
- altered br on perl(Test::Warn) (0.11 => 0.21)
- altered req on perl(Carp::Clan) (6 => 6.0)
- altered req on perl(Class::Accessor::Grouped) (0.08003 => 0.09000)
- altered req on perl(Data::Page) (2 => 2.00)
- altered req on perl(SQL::Abstract) (1.56 => 1.58)

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08109-1
- auto-update to 0.08109 (by cpan-spec-update 0.01)
- added a new br on perl(File::Temp) (version 0.22)
- altered br on perl(Test::More) (0.82 => 0.92)

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08108-1
- auto-update to 0.08108 (by cpan-spec-update 0.01)

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.08107-3
- Add BR: perl(CPAN) to fix rebuild-breakdown.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08107-1
- auto-update to 0.08107 (by cpan-spec-update 0.01)
- altered br on perl(DBD::SQLite) (1.13 => 1.25)
- altered br on perl(SQL::Abstract) (1.55 => 1.56)
- added a new req on perl(Carp::Clan) (version 6)
- altered req on perl(Class::Accessor::Grouped) (0.05002 => 0.08003)
- altered req on perl(Class::C3::Componentised) (0 => 1.0005)
- added a new req on perl(Class::Inspector) (version 1.24)
- added a new req on perl(DBD::SQLite) (version 1.25)
- added a new req on perl(DBI) (version 1.605)
- added a new req on perl(Data::Page) (version 2)
- added a new req on perl(JSON::Any) (version 1.18)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(MRO::Compat) (version 0.09)
- added a new req on perl(Module::Find) (version 0.06)
- added a new req on perl(Path::Class) (version 0.16)
- altered req on perl(SQL::Abstract) (1.2 => 1.56)
- added a new req on perl(SQL::Abstract::Limit) (version 0.13)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(Scope::Guard) (version 0.03)
- added a new req on perl(Storable) (version 0)
- added a new req on perl(Sub::Name) (version 0.04)
- ** manual updates follow
- force a provides on perl(DBIx::Class::Storage::DBI::Replicated::Types)
- rejigger filtering to a cleaner variant
- drop remaining patch artifacts

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08103-1
- auto-update to 0.08103 (by cpan-spec-update 0.01)
- altered br on perl(Class::Inspector) (0 => 1.24)
- altered br on perl(Carp::Clan) (0 => 6)
- altered br on perl(JSON::Any) (1.17 => 1.18)
- altered br on perl(Module::Find) (0 => 0.06)
- altered br on perl(DBI) (1.4 => 1.605)
- altered br on perl(SQL::Abstract) (1.51 => 1.55)
- added a new br on perl(Test::More) (version 0.82)
- altered br on perl(Path::Class) (0 => 0.16)

* Sun May 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08102-3
- we should also provide perl(DBIx::Class::CDBICompat::Relationship) (and do
  now so provide)

* Sun May 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08102-2
- additional BR's for optional tests

* Sun May 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08102-1
- drop verbose.patch: largely supersceded
- auto-update to 0.08102 (by cpan-spec-update 0.01)
- added a new br on perl(MRO::Compat) (version 0.09)
- added a new br on perl(Test::Warn) (version 0.11)
- altered br on perl(SQL::Abstract) (1.24 => 1.51)
- added a new br on perl(Sub::Name) (version 0.04)
- altered br on perl(Test::Builder) (0.32 => 0.33)
- altered br on perl(Class::C3::Componentised) (0 => 1.0005)
- altered br on perl(Class::Accessor::Grouped) (0.08002 => 0.08003)
- added a new br on perl(Path::Class) (version 0)

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> 0.08012-3
- Added missing build requirement perl(Test::Deep) for make tests
- Re-diffed make tests patch for more verbosity when skipping tests

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08012-1
- update to 0.08012

* Thu Oct 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-9
- stop filtering perl(DBD::Multi)

* Sun Oct 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-8
- filter all prov/req from anything under _docdir
- note we still filter perl(DBD::Multi), at least until review bug bz#465690
  is completed...
- ...and perl(DBD::Pg) will always be filtered

* Wed Oct 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-7
- fix patch fuzz

* Mon Jun 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-6
- bump

* Wed Apr 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-5
- pod coverage testing NOT enabled; test currently "fails"
- make tests skip a little more verbosely...
- add a br of Class::Data::Inheritable for the CDBI-compat testing

* Tue Apr 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-4
- drop unneeded patch1
- set explicit provides version to 0 :)

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-3
- add perl(Test::Exception) as a br
- revert patches to skip on DBD::SQLite < 1.13

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-2
- BR JSON -> JSON::Any
- rework sqlite/tests patch to skip on DBD::SQLite < 1.15...  1.14 is in
  rawhide/f9, and frankly, doesn't quite pass muster *sigh*

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08010-1
- update to 0.08010

* Wed Jan 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08008-3
- add additional BR's for optional tests

* Fri Jan 11 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08008-2
- patch to work around certain tests as DBD::SQLite isn't going to 1.13
  anytime soon (see RH#245699)

* Tue Dec 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08008-1
- update to 0.08008
- correct provides filtering...

* Tue Sep 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08007-1
- Specfile autogenerated by cpanspec 1.71.
