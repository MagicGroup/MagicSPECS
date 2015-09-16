Name:           perl-perlmenu
Version:        4.0
Release:        26%{?dist}
Summary:        Perl library module for curses-based menus & data-entry templates

Group:          Development/Libraries
License:        LGPLv2 or Artistic clarified
URL:            http://www.public.iastate.edu/~skunz/PerlMenu/homepage.html
Source0:        ftp://ftp.iastate.edu/pub/perl/perlmenu.v%{version}.tar.Z
Patch0:         getcapforperl5.patch
BuildArch:      noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
PerlMenu - Perl library module for curses-based menus & data-entry templates.


%prep
%setup -q -n perlmenu.v%{version}
%patch0 -p0
mkdir examples
mv demo* ez* template_* menuutil.pl examples/
find examples -type f -exec chmod 644 {} \;
sed -i -e 's|/usr/local/bin/perl5|%{__perl}|' examples/*

%build
%{__perl} create_menu.pl 

%install
install -d $RPM_BUILD_ROOT%{perl_vendorlib}
install -p -m 644 perlmenu.pm $RPM_BUILD_ROOT%{perl_vendorlib}

%files
%doc FAQ MENUUTIL_DOC MENU_DOC README RELEASE_NOTES TO_DO COPYING examples
%{perl_vendorlib}/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.0-25
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.0-24
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 04 2013 Parag <paragn AT fedoraproject DOT org> - 4.0-22
- Fix Source url for reported source audit

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.0-20
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 4.0-17
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.0-15
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.0-14
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.0-12
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.0-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.0-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Parag Nemade <panemade@gmail.com>- 4.0-7
- Fix Patch tag

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.0-6
- Rebuild for new perl

* Tue Aug 21 2007 Parag Nemade <panemade@gmail.com>- 4.0-5
- update License tag 

* Fri Jan 26 2007 Parag Nemade <panemade@gmail.com>- 4.0-4
- Added pactch to enable getcap for perl5 for bug rh#233541

* Fri Sep 01 2006 Parag Nemade <panemade@gmail.com>- 4.0-4
- Corrected License tag

* Mon Jul 31 2006 Parag Nemade <panemade@gmail.com>- 4.0-3
- Removed parameters passed to create_menu.pl
- Changed installation path of menuutil.pl to examples directory

* Thu Jul 20 2006 Parag Nemade <panemade@gmail.com>- 4.0-2
- Added examples directory

* Tue Jul 18 2006 Parag Nemade <panemade@gmail.com>- 4.0-1
- Initial Release

