Name:           perl-GD
Version:	2.56
Release:	3%{?dist}
Summary:        Perl interface to the GD graphics library

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/GD/
Source0:        http://www.cpan.org/authors/id/L/LD/LDS/GD-%{version}.tar.gz

Patch0:         GD-2.56-utf8.patch

BuildRequires:  gd-devel >= 2.0.28
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       gd >= 2.0.28
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This is a autoloadable interface module for GD, a popular library
for creating and manipulating PNG files.  With this library you can
create PNG images on the fly or modify existing files.

%prep
%setup -q -n GD-%{version}

# Re-code documentation as UTF8
%patch0

# Fix shellbangs in sample scripts
perl -pi -e 's|/usr/local/bin/perl\b|%{__perl}|' \
      demos/{*.{pl,cgi},truetype_test}

%build
perl Build.PL
./Build

%install
./Build install --destdir=%{buildroot} --installdirs=vendor --create_packlist=0
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

# These files should not have been installed
rm %{buildroot}%{_bindir}/bdf2gdfont.PLS \
   %{buildroot}%{_bindir}/README \
   %{buildroot}%{_mandir}/man1/bdf2gdfont.PLS.1*

# This binary is in gd-progs
rm %{buildroot}%{_bindir}/bdftogd

%check
./Build test

%files
%license LICENSE
%doc ChangeLog README README.QUICKDRAW demos/
%{_bindir}/bdf2gdfont.pl
# %%{_bindir}/bdftogd
%{_bindir}/cvtbdf.pl
%{perl_vendorarch}/auto/GD/
%{perl_vendorarch}/GD.pm
%{perl_vendorarch}/GD/
%{_mandir}/man1/bdf2gdfont.pl.1*
%{_mandir}/man3/GD.3*
%{_mandir}/man3/GD::Image.3*
%{_mandir}/man3/GD::Polygon.3*
%{_mandir}/man3/GD::Polyline.3*
%{_mandir}/man3/GD::Simple.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.56-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.56-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.56-1
- 更新到 2.56

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.44-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.44-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.44-13
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.44-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Iain Arnell <iarnell@gmail.com> 2.44-9
- Rebuild for libpng 1.5

* Sat Jun 18 2011 Iain Arnell <iarnell@gmail.com> 2.44-8
- patch to avoid issue with ExtUtils::MakeMaker and CCFLAGS
  see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=628522
- clean up spec for modern rpmbuild
- use perl_default_filter

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.44-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.44-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.44-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.44-3
- rebuild against perl 5.10.1

* Thu Oct 29 2009 Stepan Kasal <skasal@redhat.com> - 2.44-2
- give up tests on ppc

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.44-1
- new upstream version
- run tests always
- do not add bdf_scripts/ to docs
- switch off the test that fails in i686 koji

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.41-2
- fix Makefile.PL to install GD/Group.pm (bz 490429)

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.41-1
- update to 2.41

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.39-1
- update to 2.39

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-7
- tests work fine locally, one fails in mock, maybe needs a desktop? 
  conditionalized them, default off.

* Fri Apr  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-6
- license fix

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.35-4
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.35-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Sun Oct  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.35-2
- Removed a duplicate file (bdf_scripts/bdf2gdfont.PLS).

* Tue Sep  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.35-1
- Update to 2.35.

* Sat Jun  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.34-1
- Update to 2.34.

* Wed Mar  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.32-1
- Update to 2.32.

* Tue Feb 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.31-1
- Update to 2.31.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-3
- Missing BR: fontconfig-devel.

* Mon Feb 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-2
- Modular X (libX11-devel, libXpm-devel).

* Fri Oct 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.30-1
- Update to 2.30.

* Mon Aug  8 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.28-1
- Update to 2.28.

* Tue Jul 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.25-1
- Update to 2.25.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.23-2
- rebuilt

* Wed Mar  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.23-1
- Update to 2.23.

* Thu Dec 09 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.19-1
- Update to 2.19.
- GIF support has been restored in gd 2.0.28.
- Module autoconfigures itself with the gdlib-config program.

* Mon Jun 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.3
- Avoid RPATH problem in FC1 (bug 1756).
- Replaced hardcoded value by rpmmacro (%%{__perl}) (bug 1756).

* Mon Jun 14 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.12-0.fdr.2
- Bring up to date with current fedora.us perl spec template.

* Sat Feb  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.12-0.fdr.1
- Update to 2.12.
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.11-0.fdr.1
- Update to 2.11.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.41-0.fdr.1
- First build.
