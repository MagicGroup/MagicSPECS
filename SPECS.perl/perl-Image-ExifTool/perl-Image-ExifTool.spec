Name:		perl-Image-ExifTool
Version:	8.75
Release:	4%{?dist}
License:	GPL+ or Artistic
Group:		Applications/Multimedia
Summary:	Utility for reading and writing image meta info
URL:		http://www.sno.phy.queensu.ca/%7Ephil/exiftool/
Source0:	http://www.sno.phy.queensu.ca/%7Ephil/exiftool/Image-ExifTool-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	perl >= 1:5.6.1, perl(ExtUtils::Command::MM)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
ExifTool is a Perl module with an included command-line application for 
reading and writing meta information in image, audio, and video files. 
It reads EXIF, GPS, IPTC, XMP, JFIF, MakerNotes, GeoTIFF, ICC Profile, 
Photoshop IRB, FlashPix, AFCP, and ID3 meta information from JPG, JP2, 
TIFF, GIF, PNG, MNG, JNG, MIFF, EPS, PS, AI, PDF, PSD, BMP, THM, CRW, 
CR2, MRW, NEF, PEF, ORF, DNG, and many other types of images. ExifTool 
also extracts information from the maker notes of many digital cameras 
by various manufacturers including Canon, Casio, FujiFilm, GE, HP, 
JVC/Victor, Kodak, Leaf, Minolta/Konica-Minolta, Nikon, Olympus/Epson, 
Panasonic/Leica, Pentax/Asahi, Reconyx, Ricoh, Samsung, Sanyo, 
Sigma/Foveon, and Sony.

%prep
%setup -q -n Image-ExifTool-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

# Somehow, these empty directories are getting created.
# Delete them.
rm -rf %{buildroot}%{perl_vendorlib}/*-linux-thread-multi

%check


%files
%doc README Changes
%{_bindir}/exiftool
%{perl_vendorlib}/File/
%{perl_vendorlib}/Image/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 8.75-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 8.75-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 8.75-2
- 为 Magic 3.0 重建

* Mon Jan  9 2012 Tom Callaway <spot@fedoraproject.org> - 8.75-1
- update to 8.75

* Mon Sep 26 2011 Tom Callaway <spot@fedoraproject.org> - 8.65-1
- update to 8.65

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 8.60-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 8.60-2
- Perl mass rebuild

* Tue Jun 28 2011 Tom Callaway <spot@fedoraproject.org> - 8.60-1
- update to 8.60

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 8.50-2
- Perl mass rebuild

* Thu Mar  3 2011 Tom Callaway <spot@fedoraproject.org> - 8.50-1
- update to 8.50

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 8.40-1
- update to 8.40

* Tue Jul 13 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 8.25-1
- update to 8.25

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 8.15-2
- Mass rebuild with perl-5.12.0

* Tue Mar 23 2010 Tom "spot" Callaway <tcallawa@redhat.com> 8.15-1
- update to 8.15

* Mon Feb 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> 8.10-1
- update to 8.10

* Mon Dec  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 8.00-1
- update to 8.00 (Production)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 7.67-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> 7.67-1
- update to 7.67

* Tue Jan  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> 7.60-1
- update to 7.60

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.51-1
- update to 7.51

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.25-2
- get rid of empty arch-specific directories (bz 448744)

* Fri Apr 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.25-1
- update to 7.25

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.15-1
- 7.15
- rebuild for new perl

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 7.00-1
- 7.00

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 6.95-1
- 6.95
- license tag fix

* Wed Aug  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> 6.94-1
- bump to 6.94

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 6.77-1
- bump to 6.77

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 6.69-1

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.40-1
- bump to 6.40

* Wed Aug  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.30-1
- bump to 6.30
 
* Tue Jul 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.26-2
- clean up the places where "use the" shows up in the code as a workaround

* Fri Jul  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.26-1
- bump to 6.26

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.15-1
- bump to 6.15

* Fri Mar 31 2006 Tom "spot" Callaway <tcallawa@redhat.com> 6.09-1
- bump to 6.09

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 5.89-1
- bump to 5.89

* Thu Aug  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 5.53-1
- initial package for Fedora Extras
