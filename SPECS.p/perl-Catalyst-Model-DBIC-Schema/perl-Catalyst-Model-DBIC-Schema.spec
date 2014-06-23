Name:           perl-Catalyst-Model-DBIC-Schema
Summary:        DBIx::Class::Schema Model Class
Version:        0.59
Release:        17%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RK/RKITOVER/Catalyst-Model-DBIC-Schema-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Model-DBIC-Schema/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

Provides:       perl(Catalyst::Model::DBIC::Schema::Types)

BuildRequires:  /usr/bin/catalyst.pl
BuildRequires:  perl(Carp::Clan)
BuildRequires:  perl(Catalyst::Component::InstancePerContext)
BuildRequires:  perl(Catalyst::Runtime) >= 5.80005
BuildRequires:  perl(Catalyst::Devel) >= 1.0
BuildRequires:  perl(CatalystX::Component::Traits) >= 0.14
BuildRequires:  perl(CPAN)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBIx::Class) >= 0.08114
BuildRequires:  perl(DBIx::Class::Cursor::Cached)
BuildRequires:  perl(DBIx::Class::Schema::Loader) >= 0.04005
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Hash::Merge)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Moose) >= 1.12
BuildRequires:  perl(MooseX::MarkAsMethods) >= 0.13
BuildRequires:  perl(MooseX::NonMoose) >= 0.16
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(namespace::autoclean) >= 0.09
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(Try::Tiny)

Requires:       perl(Catalyst::Runtime) >= 5.80005
Requires:       perl(CatalystX::Component::Traits) >= 0.14
Requires:       perl(DBIx::Class) >= 0.08114
Requires:       perl(DBIx::Class::Cursor::Cached)
Requires:       perl(DBIx::Class::Schema::Loader) >= 0.04005
Requires:       perl(Hash::Merge)
Requires:       perl(Moose) >= 1.12
Requires:       perl(MooseX::NonMoose) >= 0.16

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.59-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This is a Catalyst Model for DBIx::Class::Schema-based Models. See the
documentation for Catalyst::Helper::Model::DBIC::Schema for information on
generating these Models via Helper scripts.

%prep
%setup -q -n Catalyst-Model-DBIC-Schema-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
TEST_POD=1 C_M_DBIC_SCHEMA_TESTAPP=1 

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.59-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.59-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.59-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.59-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.59-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.59-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.59-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.59-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.59-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.59-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.59-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.59-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.59-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.59-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.59-3
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.59-2
- drop tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.59-1
- update to latest upstream version

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.50-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.40-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.40-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.40-3
- Mass rebuild with perl-5.12.0

* Mon Mar 22 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.40-2
- manually provide Catalyst::Model::DBIC::Schema::Types... le sigh

* Fri Mar 12 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.40-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.40)
- added a new br on perl(Carp::Clan) (version 0)
- altered br on perl(Catalyst::Runtime) (5.70 => 5.80005)
- added a new br on perl(CatalystX::Component::Traits) (version 0.14)
- altered br on perl(DBIx::Class) (0.07006 => 0.08114)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(List::MoreUtils) (version 0)
- added a new br on perl(Moose) (version 0.90)
- added a new br on perl(MooseX::Types) (version 0)
- added a new br on perl(Test::Exception) (version 0)
- added a new br on perl(Test::More) (version 0.94)
- added a new br on perl(Tie::IxHash) (version 0)
- added a new br on perl(namespace::autoclean) (version 0)
- dropped old BR on perl(Class::Accessor::Fast)
- dropped old BR on perl(Class::C3)
- dropped old BR on perl(Class::C3::XS)
- dropped old BR on perl(Class::Data::Accessor)
- dropped old BR on perl(MRO::Compat)
- dropped old BR on perl(Test::Pod::Coverage)
- dropped old BR on perl(UNIVERSAL::require)
- added manual BR on perl(Hash::Merge)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Carp::Clan) (version 0)
- altered req on perl(Catalyst::Runtime) (5.70 => 5.80005)
- added a new req on perl(CatalystX::Component::Traits) (version 0.14)
- added a new req on perl(DBIx::Class) (version 0.08114)
- added a new req on perl(List::MoreUtils) (version 0)
- added a new req on perl(Moose) (version 0.90)
- added a new req on perl(MooseX::Types) (version 0)
- added a new req on perl(Tie::IxHash) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)
- dropped old requires on perl(Class::Accessor::Fast)
- dropped old requires on perl(Class::Data::Accessor)
- added manual requires on perl(Hash::Merge)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.23-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 04 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- update to 0.23

* Sat Apr 04 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- update to 0.23

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.21-2
- bump

* Tue Sep 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- update to 0.21

* Tue Jul 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.20-2
- add DBIx::Class::Schema::Loader as a BR and R

* Sun Mar 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- Specfile autogenerated by cpanspec 1.74.
