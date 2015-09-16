Name:           perl-Image-Size
Version:	3.300
Release:	1%{?dist}
Summary:        Determine the size of images in several common formats in Perl

Group:          Development/Libraries
License:        LGPLv2 or Artistic 2.0
URL:            http://search.cpan.org/dist/Image-Size/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJRAY/Image-Size-%{version}.tar.gz
Source1:	Build.PL
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Image::Magick)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Compress::Zlib)
Requires:       perl(Image::Magick)

%description
Image::Size is a library based on the image-sizing code in the wwwimagesize
script, a tool that analyzes HTML files and adds HEIGHT and WIDTH tags to
IMG directives. Image::Size has generalized that code to return a raw (X, Y)
pair, and included wrappers to pre-format that output into either HTML or
a set of attribute pairs suitable for the CGI.pm library by Lincoln Stein.
Currently, Image::Size can size images in XPM, XBM, GIF, JPEG, PNG, MNG, TIFF,
the PPM family of formats (PPM/PGM/PBM) and if Image::Magick is installed,
the formats supported by it.


%prep
%setup -q -n Image-Size-%{version}
# Upstream forgot Build.PL
cp %{SOURCE1} .
pushd lib/Image/
iconv -f iso-8859-1 -t utf-8 -o Size.pm{.utf8,}
mv Size.pm{.utf8,}
popd


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*


%check
mv t/00_signature.t t/00_signature.t.skip
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{_bindir}/imgsize
%{perl_vendorlib}/Image/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.300-1
- 更新到 3.300

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.2-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 3.2-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.2-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.2-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.2-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.2-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.2-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.2-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.2-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.2-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.2-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.2-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2-1
- update to 3.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-3
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-2
- rebuild for new perl

* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1-1
- bump to 3.1
- license change (now LGPLv2 or Artistic 2.0)

* Sat Sep 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.01-1
- Update to 3.01.
- Makefile.PL -> Build.PL.

* Sat Jun 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.0-1
- Update to 3.0.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.992-5
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.992-4
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.992-3
- rebuilt

* Thu Jun  3 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.992-0.fdr.2
- Bring up to date with current fedora.us perl spec template.

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.992-0.fdr.1
- First build.
