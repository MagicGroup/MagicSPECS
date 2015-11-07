Name:           perl-DBIx-Class-Schema-Loader
Summary:        Dynamic definition of a DBIx::Class::Schema
Version:	0.07043
Release:	3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/DBIx-Class-Schema-Loader-%{version}.tar.gz
URL:            http://search.cpan.org/dist/DBIx-Class-Schema-Loader/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp::Clan)
BuildRequires:  perl(Class::Accessor::Grouped) >= 0.10002
BuildRequires:  perl(Class::C3) >= 0.18
BuildRequires:  perl(Class::C3::Componentised) >= 1.0008
BuildRequires:  perl(Class::Inspector) >= 1.27
BuildRequires:  perl(Class::Unload)
BuildRequires:  perl(Config::Any)
BuildRequires:  perl(Config::General)
BuildRequires:  perl(Data::Dump) >= 1.06
BuildRequires:  perl(DBD::SQLite) >= 1.29
BuildRequires:  perl(DBI) >= 1.56
BuildRequires:  perl(DBIx::Class) >= 0.08127
BuildRequires:  perl(DBIx::Class::IntrospectableM2M)
BuildRequires:  perl(Digest::MD5) >= 2.36
BuildRequires:  perl(Exporter) >= 5.63
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path) >= 2.07
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.16
BuildRequires:  perl(Hash::Merge)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Lingua::EN::Inflect::Number) >= 1.1
BuildRequires:  perl(Lingua::EN::Inflect::Phrase) >= 0.02
BuildRequires:  perl(Lingua::EN::Tagger) >= 0.2
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Moose) >= 1.12
BuildRequires:  perl(MooseX::MarkAsMethods) >= 0.13
BuildRequires:  perl(MooseX::NonMoose) >= 0.16
BuildRequires:  perl(namespace::autoclean) >= 0.09
BuildRequires:  perl(namespace::clean) >= 0.20
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Scope::Guard)
BuildRequires:  perl(String::CamelCase) >= 0.02
BuildRequires:  perl(String::ToIdentifier::EN) >= 0.05
BuildRequires:  perl(Sub::Name)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Warn) >= 0.21
BuildRequires:  perl(Text::Balanced)
BuildRequires:  perl(Try::Tiny)

Requires:       perl(Class::Accessor::Grouped) >= 0.10002
Requires:       perl(Class::C3) >= 0.18
Requires:       perl(Class::C3::Componentised) >= 1.0008
Requires:       perl(Data::Dump) >= 1.06
Requires:       perl(DBIx::Class) >= 0.08127
Requires:       perl(Digest::MD5) >= 2.36
Requires:       perl(Exporter) >= 5.63
Requires:       perl(Lingua::EN::Inflect::Number) >= 1.1
Requires:       perl(Lingua::EN::Inflect::Phrase) >= 0.02
Requires:       perl(Scope::Guard)
Requires:       perl(Text::Balanced)

# hidden from PAUSE
Provides:       perl(DBIx::Class::Schema::Loader::Utils)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.07010-5
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
DBIx::Class::Schema::Loader automates the definition of a
DBIx::Class::Schema by scanning database table definitions
and setting up the columns, primary keys, and relationships.

%prep
%setup -q -n DBIx-Class-Schema-Loader-%{version}

mv README README.iconv
iconv -f iso-8859-1 -t utf-8 README.iconv >README
touch -r README.iconv README
rm -f README.iconv

find t -type f -print0 | xargs -0 sed -i '1s,#!.*perl,#!%{__perl},'

%build
%{__perl} Makefile.PL --skipdeps INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +

%{_fixperms} %{buildroot}/*

%check
export SCHEMA_LOADER_TESTS_BACKCOMPAT=1
make test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man[13]/*
%{_bindir}/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.07043-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.07043-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.07043-1
- 更新到 0.07043

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.07033-12
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.07033-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.07033-10
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.07033-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07033-8
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07033-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07033-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07033-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07033-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07033-3
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.07033-2
- 为 Magic 3.0 重建

* Sun Sep 09 2012 Iain Arnell <iarnell@gmail.com> 0.07033-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07025-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Petr Pisar <ppisar@redhat.com> - 0.07025-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Iain Arnell <iarnell@gmail.com> 0.07025-1
- update to latest upstream version
- BR inc::Module::Install instead of EU::MM

* Sat May 12 2012 Iain Arnell <iarnell@gmail.com> 0.07024-1
- update to latest upstream version

* Mon May 07 2012 Iain Arnell <iarnell@gmail.com> 0.07023-1
- update to latest upstream version

* Mon Apr 09 2012 Iain Arnell <iarnell@gmail.com> 0.07022-1
- update to latest upstream version

* Sun Apr 01 2012 Iain Arnell <iarnell@gmail.com> 0.07020-1
- update to latest upstream version

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 0.07019-1
- update to latest upstream version

* Wed Feb 08 2012 Iain Arnell <iarnell@gmail.com> 0.07017-1
- update to latest upstream version

* Fri Feb 03 2012 Iain Arnell <iarnell@gmail.com> 0.07015-1
- update to latest upstream version
- silence rpmlint wrong-script-interpreter warning

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.07010-5
- drop tests subpackage; move tests to main package documentation
- clean up spec for modern rpmbuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07010-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.07010-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.07010-2
- Perl mass rebuild

* Sat Apr 23 2011 Iain Arnell <iarnell@gmail.com> 0.07010-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 05 2010 Iain Arnell <iarnell@gmail.com> 0.07002-2
- provides perl(DBIx::Class::Schema::Loader::Utils)

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> 0.07002-1
- update to 0.07002
- disable auto_install
- remove unnecessary explicit requires

* Mon Aug 16 2010 Iain Arnell <iarnell@gmail.com> 0.07001-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.07001)
- altered br on perl(DBD::SQLite) (1.12 => 1.29)
- added a new br on perl(Exporter) (version 5.63)
- added a new br on perl(Lingua::EN::Inflect::Phrase) (version 0.02)
- added a new br on perl(Moose) (version 0)
- added a new br on perl(MooseX::NonMoose) (version 0)
- added a new br on perl(Scope::Guard) (version 0)
- altered br on perl(Test::More) (0.92 => 0.94)
- added a new br on perl(Try::Tiny) (version 0)
- added a new br on perl(namespace::clean) (version 0)
- added a new req on perl(Exporter) (version 5.63)
- added a new req on perl(Lingua::EN::Inflect::Phrase) (version 0.02)
- added a new req on perl(Scope::Guard) (version 0)
- added a new req on perl(Try::Tiny) (version 0)
- added a new req on perl(namespace::clean) (version 0)
- dropped old requires on perl(namespace::autoclean)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05003-2
- Mass rebuild with perl-5.12.0

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05003-1
- switch filtering systems
- add files in bin && man1
- enable back-compat testing
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(Class::Accessor::Grouped) (version 0.09002)
- added a new br on perl(Class::C3::Componentised) (version 1.0005)
- added a new br on perl(Class::Unload) (version 0)
- altered br on perl(DBIx::Class) (0.07006 => 0.08114)
- added a new br on perl(File::Copy) (version 0)
- altered br on perl(File::Path) (0 => 2.07)
- added a new br on perl(File::Slurp) (version 9999.13)
- added a new br on perl(File::Temp) (version 0.16)
- added a new br on perl(IPC::Open3) (version 0)
- added a new br on perl(List::MoreUtils) (version 0)
- added a new br on perl(Test::Exception) (version 0)
- altered br on perl(Test::More) (0.47 => 0.92)
- added a new br on perl(namespace::autoclean) (version 0)
- dropped old BR on perl(Class::Accessor::Fast)
- dropped old BR on perl(Class::Data::Accessor)
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)
- dropped old BR on perl(UNIVERSAL::require)
- dropped old BR on perl(YAML::Tiny)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Carp::Clan) (version 0)
- added a new req on perl(Class::Accessor::Grouped) (version 0.09002)
- added a new req on perl(Class::C3) (version 0.18)
- added a new req on perl(Class::C3::Componentised) (version 1.0005)
- added a new req on perl(Class::Inspector) (version 0)
- added a new req on perl(Class::Unload) (version 0)
- added a new req on perl(DBIx::Class) (version 0.08114)
- added a new req on perl(Data::Dump) (version 1.06)
- added a new req on perl(Digest::MD5) (version 2.36)
- added a new req on perl(File::Slurp) (version 9999.13)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(Lingua::EN::Inflect::Number) (version 1.1)
- added a new req on perl(List::MoreUtils) (version 0)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(Text::Balanced) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)
- dropped old requires on perl(Class::Accessor::Fast)
- dropped old requires on perl(Class::Data::Accessor)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04006-6
- rebuild against perl 5.10.1

* Wed Aug 05 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.04006-5
- Remove R: DBIX::Class.

* Wed Aug 05 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.04006-4
- Fix mass rebuild breakdown:
  Replace bundled Module-Install with Module-Install-0.91.
  Add --skipdeps.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> 0.04006-2
- fix duplicate directory ownership (perl-DBIx-Class owns %{perl_vendorlib}/DBIx/Class/)

* Wed Jun 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04006-1
- auto-update to 0.04006 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Test::More) (0 => 0.47)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04005-2
- bump

* Mon Jun 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04005-1
- update to 0.4005
- filter _docdir requires/provides

* Mon Mar 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04004-1
- brush-up for review submission

* Wed Oct 17 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.04003-1
- Specfile autogenerated by cpanspec 1.71.
