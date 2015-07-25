Name:           perl-DBIx-Class-DateTime-Epoch
Summary:        Automatic inflation/deflation of epoch-based DateTime objects for DBIx::Class
Version:        0.08
Release:        15%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BR/BRICAS/DBIx-Class-DateTime-Epoch-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/DBIx-Class-DateTime-Epoch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::SQLite)
BuildRequires:  perl(DBICx::TestDatabase)
BuildRequires:  perl(DBIx::Class) >= 0.08103
BuildRequires:  perl(DBIx::Class::TimeStamp) >= 0.07
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.62
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)

Requires:       perl(DBIx::Class) >= 0.08103
Requires:       perl(DBIx::Class::TimeStamp) >= 0.07

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.08-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This module automatically inflates/deflates DateTime objects
corresponding to applicable columns. Columns may also be defined to
specify their nature, such as columns representing a creation time
(set at time of insertion) or a modification time (set at time of
every update).


%prep
%setup -q -n DBIx-Class-DateTime-Epoch-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.08-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.08-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.08-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.08-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.08-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.08-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.08-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.08-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.08-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.08-3
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.08-2
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream version

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.07-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.07-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.07-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-2
- Mass rebuild with perl-5.12.0

* Sat Mar 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.06)
- dropped old BR on perl(Module::Build::Compat)
- dropped old BR on perl(Test::Pod::Coverage)
- altered req on perl(DBIx::Class) (0 => 0.08103)
- added a new req on perl(DBIx::Class::TimeStamp) (version 0.07)
- added a new req on perl(DateTime) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05-5
- rebuild against perl 5.10.1

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-4
- adjust file ownership

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> 0.05-2
- fix duplicate directory ownership (perl-DBIx-Class owns %{perl_vendorlib}/DBIx/Class/)

* Wed Jun 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- auto-update to 0.05 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(DBIx::Class) (0 => 0.08103)
- added a new br on perl(DBIx::Class::TimeStamp) (version 0.07)
- added a new br on perl(DBICx::TestDatabase) (version 0)

* Fri Apr 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- update for submission

* Fri Apr 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
