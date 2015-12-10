%define rgbtxt  %{_datadir}/X11/rgb.txt

Name:           perl-Image-Info
Version:	1.38
Release:	4%{?dist}
Summary:        Image meta information extraction module for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Image-Info/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SR/SREZIC/Image-Info-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Image::Xbm), perl(Image::Xpm), perl(XML::Simple)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:       rgb
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This Perl extension allows you to extract meta information from
various types of image files.


%prep
%setup -q -n Image-Info-%{version}
chmod -c 644 exifdump imgdump
%{__perl} -pi -e 's|/usr/X11R6/lib/X11/rgb\.txt|%{rgbtxt}|' \
    lib/Image/Info/XPM.pm


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
%doc CHANGES README exifdump imgdump
%{perl_vendorlib}/Image/
%{perl_vendorlib}/Bundle/Image/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.38-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.38-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.38-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.38-1
- 更新到 1.38

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.28-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.28-14
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.28-13
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.28-11
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.28-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28-6
- rebuild against perl 5.10.1

* Mon Nov 09 2009 Adam Jackson <ajax@redhat.com> 1.28-5
- Requires: rgb, not Requires: /usr/share/X11/rgb.txt

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.28-1
- update to 1.28

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-3
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.27-1
- bump to 1.27

* Wed May 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.25-1
- Update to 1.25.

* Mon Feb 26 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Sat Sep 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.23-1
- Update to 1.23.

* Sun Jul 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Mon May  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.21-2
- Bumping release due to CVS problem.

* Mon May  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.21-1
- Update to 1.21.

* Mon Mar 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20.

* Wed Mar  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.19-1
- Update to 1.19 (broken: cpan tickets: #18020 and #18147).
- Module::Install 0.58 is broken (Image-Info-1.19-inc-Module-Install.pm.patch).
- BR: perl(Image::Xbm), perl(Image::Xpm), perl(XML::Simple).

* Fri Mar  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18 (broken: cpan ticket #6558).
- Dropped patches Image-Info-1.16-X[BP]M.pm.patch (accepted upstream).
- Dropped patch Image-Info-1.16-string.t.patch (test has been rewritten).

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-2
- BR: perl(Test::Pod), perl(Test::Pod::Coverage).

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17.
- New upstream maintainer.

* Wed Nov 23 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.16-6
- Add dependency on rgb.txt, adjust its location for FC5.
- Specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.16-4
- rebuilt

* Thu Jul  1 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.3
- Reverted Image::Xbm and Image::Xpm patches.
- Patched Image::Info::XBM.pm and Image::Info::XPM.pm instead.

* Tue Jun  8 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.2
- Patched Image::Xbm and Image::Xpm to avoid test failures in this module.

* Thu Jun  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.1
- Update to version 1.16.
- Bring up to date with current fedora.us perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.15-0.fdr.1
- First build.
