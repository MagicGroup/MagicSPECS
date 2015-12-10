Name:           perl-GDGraph
Version:	1.49
Release:	3%{?dist}
Epoch:          1
Summary:        Graph generation package for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/GDGraph/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RU/RUZ/GDGraph-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(GD) >= 1.18
BuildRequires:  perl(GD::Text) >= 0.80
BuildRequires:  perl(GD::Text::Align)
# Tests
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(GD) >= 1.18
Requires:       perl(GD::Text) >= 0.80

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(GD\\)

%description
%{summary}.


%prep
%setup -q -n GDGraph-%{version}
%{__perl} -pi -e 's{^#!/usr/local/bin/perl\b}{#!%{__perl}}' samples/sample1A.pl
%{__perl} -pi -e 's/\r\n/\n/' samples/sample64.pl


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES README samples/
%{perl_vendorlib}/GD/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:1.49-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:1.49-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:1.49-1
- 更新到 1.49

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.44-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.44-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:1.44-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1:1.44-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:1.44-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.44-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1:1.44-13
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.44-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.44-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.44-9
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.44-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.44-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.44-4
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.44-3
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.44-2.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.44-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Jun  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:1.44-2
- Bumping release (due to dist tag mismatches).

* Sat May  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1:1.44-1
- Update to 1.44.

* Thu May 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4308-1
- Update to 1.4308.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4307-1
- Update to 1.4307.

* Mon Feb  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4306-1
- Update to 1.4306.

* Thu Dec 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.4305-1
- Update to 1.4305.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.43-4
- rebuilt

* Sun Jul 11 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.43-0.fdr.3
- Unowned directory: %%{perl_vendorlib}/GD (see bug 1800 comment #1).

* Wed Jun 30 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.43-0.fdr.2
- Bring up to date with current fedora.us perl spec template.
- Added the samples directory to the documentation files.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.43-0.fdr.1
- First build.
