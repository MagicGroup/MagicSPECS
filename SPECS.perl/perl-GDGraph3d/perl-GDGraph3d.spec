Name:           perl-GDGraph3d
Version:        0.63
Release:        24%{?dist}
Summary:        3D graph generation package for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/GD-Graph3d/
Source0:        http://www.cpan.org/authors/id/W/WA/WADG/GD-Graph3d-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(GD), perl(GD::Text), perl(GD::Graph)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-GD-Graph3d = %{version}-%{release}

%description
This is the GD::Graph3d extensions module. It provides 3D graphs for
the GD::Graph module by Martien Verbruggen, which in turn generates
graph using Lincoln Stein's GD.pm.


%prep
%setup -q -n GD-Graph3d-%{version}
%{__perl} -pi -e 's/\r//g' Changes


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
%doc Changes
%{perl_vendorlib}/GD/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-23
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.63-21
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.63-20
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.63-18
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.63-16
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-14
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-13
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.63-12
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-9
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-8
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-7.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-7
- Correction of CPAN URL (#242941).

* Sat Sep  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-6
- Rebuild for FC6.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-5
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.63-4
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.63-3
- rebuilt

* Sat Jan 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.63-2
- Added versioning to the Provides statement (bug 2371).

* Sun Jan  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.63-0.fdr.1
- Update to 0.63.

* Sun Jul 11 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.56-0.fdr.3
- Unowned directory: %%{perl_vendorlib}/GD (see bug 1800 comment #1).

* Wed Jun 30 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.56-0.fdr.2
- Bring up to date with current fedora.us perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.56-0.fdr.1
- First build.
