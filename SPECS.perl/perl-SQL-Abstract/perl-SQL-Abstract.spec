Name:           perl-SQL-Abstract
Version:	1.81
Release:	4%{?dist}
Summary:        Generate SQL from Perl data structures
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/SQL-Abstract
Source0:        http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/SQL-Abstract-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Test::More) >= 0.92
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Class::Accessor::Grouped) >= 0.10005
BuildRequires:  perl(Clone) >= 0.31
BuildRequires:  perl(Getopt::Long::Descriptive) >= 0.091
BuildRequires:  perl(Hash::Merge) >= 0.12
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::Builder)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Class::Accessor::Grouped) >= 0.10005
Requires:       perl(Getopt::Long::Descriptive) >= 0.091
Requires:       perl(Hash::Merge) >= 0.12

%{?perl_default_filter}

%description
%{summary}.

%package -n perl-DBIx-Class-Storage-Debug-PrettyPrint
Summary:        Pretty Printing DebugObj
Group:          Development/Libraries
License:        GPL+ or Artistic

%description -n perl-DBIx-Class-Storage-Debug-PrettyPrint
%{summary}.

%prep
%setup -q -n SQL-Abstract-%{version}

%build
PERL5_CPANPLUS_IS_RUNNING=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check
SQLATEST_TESTER=1 make test

%files
%{perl_vendorlib}/SQL/
%{_mandir}/man3/SQL::Abstract.3pm*
%{_mandir}/man3/SQL::Abstract::Test.3pm*
%{_mandir}/man3/SQL::Abstract::Tree.3pm*
 
%files -n perl-DBIx-Class-Storage-Debug-PrettyPrint
%{perl_vendorlib}/DBIx/
%{_mandir}/man3/DBIx::Class::Storage::Debug::PrettyPrint.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.81-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.81-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.81-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.81-1
- 更新到 1.81

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.73-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.73-2
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 1.73-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.72-6
- Perl 5.16 rebuild

* Sun Apr  8 2012 Paul Howarth <paul@city-fan.org> - 1.72-5
- Split DBIx::Class::Storage::Debug::PrettyPrint off into its own sub-package
  to avoid a dependency cycle, since perl-SQL-Abstract and perl-DBIx-Class
  would otherwise require each other and make perl-DBIx-Class unbootable

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.72-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 1.72-1
- update to latest upstream version
- update BR perl(Test::Deep) >= 0.106
- update BR perl(Test::More) >= 0.92
- new R/BR perl(Class::Accessor::Grouped) >= 0.10002
- new R/BR perl(Getopt::Long::Descriptive) >= 0.086
- new R/BR perl(Hash::Merge) >= 0.12
- add format-sql script and PrettyPrint.pm to files

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.67-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.67-1
- update to 1.67

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.61-2
- Mass rebuild with perl-5.12.0

* Mon Feb 22 2010 Chris Weyl <cweyl@alumni.drew.edu> - 1.61-1
- update to 1.61 (for latest DBIx::Class)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.60-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.60-1
- auto-update to 1.60 (by cpan-spec-update 0.01)

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.58-1
- add default filtering (pro forma)
- auto-update to 1.58 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.56-1
- auto-update to 1.56 (by cpan-spec-update 0.01)

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.55-1
- added SQLATEST_TESTER=1 to force tests
- auto-update to 1.55 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- added a new br on perl(Clone) (version 0.31)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(Test::Builder) (version 0)

* Mon Mar 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.50-2
- add missing BR: perl(Test::Exception)

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.50-1
- update to 1.50

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.24-1
- update to 1.24 (for DBIx::Class 0.8012)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.22-4
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.22-3
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.22-2
- license tag fix

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.22-1
- bump to 1.22

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.21-2
- fc6 bump

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.21-1
- bump to 1.21

* Thu Jan  5 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.20-1
- bump to 1.20

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.19-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.19-1
- Initial package for Fedora Extras
