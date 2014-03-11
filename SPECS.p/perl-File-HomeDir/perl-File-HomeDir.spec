Name:           perl-File-HomeDir
Version:        0.99
Release:        5%{?dist}
Summary:        Find your home and other directories on any platform

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-HomeDir/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/File-HomeDir-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd) >= 3.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Path) >= 2.01
BuildRequires:  perl(File::Spec) >= 3.12
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(File::Which) >= 0.05
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::More) >= 0.47
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Cwd) >= 3.12
Requires:       perl(File::Path) >= 2.01
Requires:       perl(File::Spec) >= 3.12
Requires:       perl(File::Temp) >= 0.19
Requires:       perl(File::Which) >= 0.05

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude}|perl\\(Cwd\\)|perl\\(File::Path\\)|perl\\(File::Spec\\)|perl\\(File::Temp\\)|perl\\(File::Which\\)|perl\\(Mac::

%description
File::HomeDir is a module for locating the directories that are "owned"
by a user (typically your user) and to solve the various issues that
arise trying to find them consistently across a wide variety of
platforms.


%prep
%setup -q -n File-HomeDir-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# These tests don't do anything really useful. Also, they are broken.
# AUTOMATED_TESTING=1 



%files
%doc Changes LICENSE README
%{perl_vendorlib}/File/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.99-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.99-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.99-2
- Perl 5.16 rebuild

* Tue Jan 31 2012 Tom Callaway <spot@fedoraproject.org> - 0.99-1
- Update to 0.99

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.98-2
- Perl mass rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 0.98-1
- update to 0.98

* Fri Jun 24 2011 Marcela Maslanova <mmaslano@redhat.com> - 0.97-2
- fix filters for future rebuild
- add perl_bootstrap macro
- rebuild for perl 5.14.1

* Mon Feb 21 2011 Tom Callaway <spot@fedoraproject.org> - 0.97-1
- update to 0.97

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.93-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 22 2010 Petr Pisar <ppisar@redhat.com> - 0.93-1
- 0.93 bump
- Consolidate dependencies
- Remove unversioned Requires
- Update Summary and Description
- Remove unneded file permission fixes

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.86-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.86-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.86-1
- update for Padre

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.84-1
- update to 0.84

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-1
- update to the latest version for Padre editor

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.67-1
- 0.67

* Fri Nov 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-1
- 0.66

* Wed May 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.65-1
- Update to 0.65.

* Sat Feb 10 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.64-1
- Update to 0.64.

* Thu Jan 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-1
- Update to 0.63.

* Thu Jan  4 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.62-1
- Update to 0.62.

* Thu Aug 03 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.58-1
- First build.
