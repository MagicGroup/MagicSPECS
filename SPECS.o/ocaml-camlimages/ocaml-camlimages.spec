Name:           ocaml-camlimages
Version:        4.1.0
Release:        5%{?dist}
Summary:        OCaml image processing library

Group:          Development/Libraries
License:        LGPLv2 with exceptions
URL:            http://cristal.inria.fr/camlimages/eng.html

Source0:        https://bitbucket.org/camlspotter/camlimages/get/%{version}.tar.gz

# This file isn't published any more (that I could find).
# It's probably dated but at least should provide some info on how to
# use the library.
Source1:        camlimages-2.2.0-htmlref.tar.gz

# https://bitbucket.org/camlspotter/camlimages/issue/9
Patch0:         ocaml-camlimages-4.1.0-exifcheck.patch

BuildRequires:  ocaml, ocaml-findlib-devel, ocaml-omake
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  ocaml-x11, xorg-x11-server-utils
BuildRequires:  lablgtk, libpng-devel, libjpeg-devel, libexif-devel
BuildRequires:  libXpm-devel, ghostscript-devel, freetype-devel
BuildRequires:  giflib-devel
BuildRequires:  libtiff-devel
BuildRequires:  gtk2-devel
Requires:       xorg-x11-server-utils

%description
This is an image processing library, which provides some basic
functions of image processing and loading/saving various image file
formats. In addition the library can handle huge images that cannot be
(or can hardly be) stored into the memory (the library automatically
creates swap files and escapes them to reduce the memory usage).

%package        devel
Summary:        Development files for camlimages
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release} 


%description    devel
The camlimages-devel package provides libraries and headers for 
developing applications using camlimages

Includes documentation provided by ocamldoc

%prep
%setup -q -n camlspotter-camlimages-668faa3494fe
%setup -q -T -D -a 1 -n camlspotter-camlimages-668faa3494fe
%patch0 -p1

%build
omake CFLAGS="$RPM_OPT_FLAGS"

%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
omake install

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/ocaml-camlimages
cp -pr License.txt htmlref $RPM_BUILD_ROOT/usr/share/doc/ocaml-camlimages

%files
%doc README License.txt
%{_libdir}/ocaml/camlimages
%exclude %{_libdir}/ocaml/camlimages/*.a
%exclude %{_libdir}/ocaml/camlimages/*.cmxa
# There aren't any *.cmx files
#%exclude %{_libdir}/ocaml/camlimages/*.cmx
%exclude %{_libdir}/ocaml/camlimages/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc htmlref
%{_libdir}/ocaml/camlimages/*.a
%{_libdir}/ocaml/camlimages/*.cmxa
# There aren't any *.cmx files
#%{_libdir}/ocaml/camlimages/*.cmx
%{_libdir}/ocaml/camlimages/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 4.1.0-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 25 2013 Ville Skyttä <ville.skytta@iki.fi> - 4.1.0-3
- Fix -debuginfo, enable exif and rgb.txt support (#1009155).

* Fri Sep 27 2013 Bruno Wolff III <bruno@wolff.to> - 4.1.0-2
- Try to get actual debug output

* Sun Sep 15 2013 Bruno Wolff III <bruno@wolff.to> - 4.1.0-1
- Update to 4.1.0
- Enable debug output
- Patch for recent libpng is no longer needed

* Sat Sep 14 2013 Bruno Wolff III <bruno@wolff.to> - 4.0.1-13
- Rebuild for OCaml 4.01.0

* Sun Aug 11 2013 Bruno Wolff III <bruno@wolff.to> - 4.0.1-12
- Move to unversioned doc directory
- Fixes FTBFS bug 992390

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 4.0.1-9
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 4.0.1-8
- rebuild against new libjpeg

* Wed Oct 17 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-7
- Rebuild for ocaml 4.0.1

* Sun Jul 29 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-6
- Rebuild for ocaml 4.0.0 final

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-4
- Rebuild for new ocaml

* Fri May 11 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-3
- Rebuild for new libtiff

* Sat Mar 10 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-2
- Fixup "should fixes" from review

* Sun Jan 29 2012 Bruno Wolff III <bruno@wolff.to> - 4.0.1-1
- Resurrect ocaml-camlimages
