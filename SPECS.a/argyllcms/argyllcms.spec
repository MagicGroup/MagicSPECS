Name:    argyllcms
Version: 1.8.2
Release: 1%{?dist}
Summary: ICC compatible color management system
Group:   User Interface/X
License: GPLv3 and MIT
URL:     http://gitorious.org/hargyllcms
Source0: http://people.freedesktop.org/~hughsient/releases/hargyllcms-%{version}.tar.xz

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: libtiff-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libusb1-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: automake
BuildRequires: zlib-devel

%description
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

Spectral sample data is supported, allowing a selection of illuminants observer
types, and paper fluorescent whitener additive compensation. Profiles can also
incorporate source specific gamut mappings for perceptual and saturation
intents. Gamut mapping and profile linking uses the CIECAM02 appearance model,
a unique gamut mapping algorithm, and a wide selection of rendering intents. It
also includes code for the fastest portable 8 bit raster color conversion
engine available anywhere, as well as support for fast, fully accurate 16 bit
conversion. Device color gamuts can also be viewed and compared using a VRML
viewer.

%package doc
Summary: Argyll CMS documentation
Group:   User Interface/X
# Does not really make sense without Argyll CMS itself
Requires: %{name} = %{version}-%{release}

%description doc
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

This package contains the Argyll color management system documentation.

%prep
%setup -q -n hargyllcms-%{version}
# we're not allowed to refer to acquisition devices as scanners
./legal.sh
autoreconf --force --install

%build
%configure --disable-static
make

%install
make install DESTDIR=%{buildroot}

# We don't want other programs to use these
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so

# rely on colord  to provide ENV{COLOR_MEASUREMENT_DEVICE}="1"
rm -f $RPM_BUILD_ROOT/lib/udev/rules.d/55-Argyll.rules

%files
%defattr(0644,root,root,0755)
%doc *.txt

%attr(0755,root,root) %{_bindir}/*
%{_datadir}/color/argyll
%{_datadir}/color/argyll/ref
%{_libdir}/lib*.so.*

%exclude %{_datadir}/doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files doc
%defattr(0644,root,root,0755)
%doc doc/*.html doc/*.jpg doc/*.txt

%changelog
* Mon Sep 07 2015 Richard Hughes <rhughes@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Richard Hughes <rhughes@redhat.com> - 1.7.0-1
- Update to 1.7.0
- Add better cross compatibility with non-Argyll ICC profiles
- Added a dispread & fakeread -Z option to set the number of bits to quantize
- Added a -P prune option to profcheck
- Added dispcal and collink -b black point hack
- Added histogram plot option -h to both profcheck and verify.
- Added IRIDAS .cube 3DLut format support to collink
- Added preset list of display techologies to select from in ccxxmake.
- Add support for DataColor Spyder 5.
- Add support for Klein K10-A colorimeter.
- Add X3D and X3DOM support as an alternative to VRML
- Fix various instrument communications problems for DTP20, DTP92 & DTP94
- Fix very major bug in illumread
- Ignore any patches that have zero values for creating Display profiles
- Improved gamut mapping to reduce unnecessary changes to less saturated colors

* Fri Oct 24 2014 Richard Hughes <rhughes@redhat.com> - 1.6.3-4
- Add experimental ColorHug2 driver, which has already been sent upstream.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 02 2014 Richard Hughes <rhughes@redhat.com> - 1.6.3-1
- Update to 1.6.3
- Added code to minimize ICC rounding error white point accuracy
- Changed colprof to deal with variable grid distribution in a more neuanced way
- Changed colprof to used a power_like function for the grid distribution shape
- Changed i1d3 driver to completely ignore any EEPROM checksum errors
- Fix bug in xicclu -py conversion.
- Fixed bug in dispcal to use the final measurement pass for the calibration
- Fixed bug in spotread, dispcal & dispread for CCSS capable instruments
- Renamed verify to colverify to avoid clash with MSWin program of the same name
- Switch dispread to use NoClamp readings
- Tweaked dispcal to try and improve accuracy of black point calibration

* Tue Nov 26 2013 Richard Hughes <rhughes@redhat.com> - 1.6.2-1
- Update to 1.6.2
- Added "dark region emphasis" -V parameter to targen and colprof
- Changed i1d3 driver to be more forgiving of EEProm checksum calculation
- Fixed "edges don't match" bug in printarg when -iCM -h -s/-S used.
- Fixed bug in -H flag in chartread, dispcal, dispread, illumread & spotread
- Fixed bug in dispcal black point optimization to err on the black side
- Fixed bug introduced into ColorMunki (spectro) reflective measurement
- Fixed major bug in illumread - result was being corrupted.
- Fixed problem with TV encoded output and dispread -E -k/-K

* Mon Aug 19 2013 Richard Hughes <rhughes@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Richard Hughes <rhughes@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.4.0-8
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.4.0-7
- rebuild against new libjpeg

* Wed Oct 24 2012 Richard Hughes <rhughes@redhat.com> - 1.4.0-6
- Drop 55-Argyll.rules, it's not required and we can rely on colord
  to provide the ENV{COLOR_MEASUREMENT_DEVICE}="1" without the
  plugdev group or invoking a usb-db instance for each USB device
  hotplug.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Jon Ciesla <limburgher@gmail.com> - 1.4.0-3
- Drop udev Requires.

* Mon May 07 2012 Jon Ciesla <limburgher@gmail.com> - 1.4.0-2
- Rebuild for new libtiff.

* Fri Apr 20 2012 Richard Hughes <rhughes@redhat.com> - 1.4.0-1
- Update to latest upstream release
- A colorimeter can now be used as a reference to make ccmx files
- Added dither/screening support for 8 bit output of render
- Added JPEG file support to cctiff, tiffgamut and extracticc
- Fixed double free in icc/icc.c for profiles that have duplicate tags
- Fix bugs in ColorMunki Transmissive measurement mode calibration.

* Mon Mar 19 2012 Richard Hughes <rhughes@redhat.com> - 1.3.7-1
- Update to 1.3.7
- Fix regression in Spyder support - ccmx files were not being handled

* Mon Mar 19 2012 Richard Hughes <rhughes@redhat.com> - 1.3.6-1
- Update to 1.3.6
- Add a -V option to spotread to allow tracking reading consistency.
- Add ColorHug support upstream (so distro patch removed).
- Add Spyder4 support.
- Add support for NEC SpectraSensor Pro version of the i1d3.
- Changed and expanded display selection to be instrument specific.

* Tue Feb 07 2012 Richard Hughes <rhughes@redhat.com> - 1.3.5-7
- Ship a shared library to reduce the installed package size from
  27.7Mb to 3.2Mb by removing 46 instances of static linking.

* Thu Jan 26 2012 Richard Hughes <rhughes@redhat.com> - 1.3.5-6
- Fix the ColorHug patch to not time out with firmware >= 1.1.1 and to
  correctly report negative numbers.
- Re-libtoolize to fix compile failure on rawhide.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
