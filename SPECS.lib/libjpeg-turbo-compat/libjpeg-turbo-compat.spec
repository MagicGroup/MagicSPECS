%global		_includedir %{_includedir}/libjpeg-turbo-compat

Name:		libjpeg-turbo-compat
Version:	1.2.1
Release:	6%{?dist}
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files

Group:		System Environment/Libraries
License:	BSD
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-%{version}.tar.gz

BuildRequires:	autoconf, automake, libtool
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

# Don't obsolete/provide libjpeg, the libjpeg-turbo pkg does it

Patch0:		libjpeg-turbo12-noinst.patch

%description
The libjpeg-turbo-compat package contains a libjpeg6b API/ABI compatible
library of functions for manipulating JPEG images.

%package devel
Summary:	Headers for the libjpeg-turbo-compat library
Group:		Development/Libraries
# This compat pkg doesn't obsolete/provide libjpeg-devel, libjpeg-turbo-devel does it
Requires:	libjpeg-turbo-compat%{?_isa} = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the libjpeg-turbo-compat library.

%package static
Summary:	Static version of the libjpeg-turbo-compat library
Group:		Development/Libraries
# Don't obsolete/provide libjpeg-static, libjpeg-turbo-static does it
Requires:	libjpeg-turbo-compat-devel%{?_isa} = %{version}-%{release}

%description static
The libjpeg-turbo-compat-static package contains static library for
manipulating JPEG images.

%prep
%setup -q -n libjpeg-turbo-%{version}

%patch0 -p1 -b .noinst

%build
autoreconf -fiv

%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Fix perms
chmod -x README-turbo.txt

# Move libjpeg.{so,a} into libdir/libjpeg-turbo-compat
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/libjpeg-turbo-compat
ln -s ../libjpeg.so.62 $RPM_BUILD_ROOT/%{_libdir}/libjpeg-turbo-compat/libjpeg.so
rm -f $RPM_BUILD_ROOT/%{_libdir}/libjpeg.so
mv $RPM_BUILD_ROOT/%{_libdir}/{libjpeg.a,libjpeg-turbo-compat/}

# Remove unwanted files
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib{,turbo}jpeg.la

# Don't distribute libjpegturbo
rm -f $RPM_BUILD_ROOT/%{_libdir}/libturbojpeg.*
rm -f $RPM_BUILD_ROOT/%{_includedir}/turbojpeg.h

# Don't distribute helper utilities and their's manpages
rm -rf $RPM_BUILD_ROOT/%{_bindir}
rm -rf $RPM_BUILD_ROOT/%{_mandir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README README-turbo.txt change.log ChangeLog.txt
%{_libdir}/libjpeg.so.*

%files devel
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_libdir}/libjpeg-turbo-compat/libjpeg.so

%files static
%{_libdir}/libjpeg-turbo-compat/libjpeg.a

%changelog
* Mon Dec 17 2012 Adam Tkac <atkac redhat com> 1.2.1-6
- don't obsolete/provide libjpeg (#887013)

* Wed Oct 24 2012 Adam Tkac <atkac redhat com> 1.2.1-5
- move libjpeg.a into libdir/libjpeg-turbo-compat/
- some review related fixes

* Mon Oct 22 2012 Adam Tkac <atkac redhat com> 1.2.1-4
- split out libjpeg-turbo compat library for jpeg6b API/ABI compatible library

* Thu Oct 18 2012 Adam Tkac <atkac redhat com> 1.2.1-3
- minor provides tuning (#863231)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Adam Tkac <atkac redhat com> 1.2.1-1
- update to 1.2.1

* Thu Mar 08 2012 Adam Tkac <atkac redhat com> 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Orion Poplawski <orion cora nwra com> 1.1.1-3
- Make turobojpeg-devel depend on turbojpeg

* Fri Oct 7 2011 Orion Poplawski <orion cora nwra com> 1.1.1-2
- Ship the turbojpeg library (#744258)

* Mon Jul 11 2011 Adam Tkac <atkac redhat com> 1.1.1-1
- update to 1.1.1
  - ljt11-rh688712.patch merged

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.1.0-2
- handle broken JPEGs better (#688712)

* Tue Mar 01 2011 Adam Tkac <atkac redhat com> 1.1.0-1
- update to 1.1.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-1
- update to 1.0.90
- libjpeg-turbo10-rh639672.patch merged

* Fri Oct 29 2010 Adam Tkac <atkac redhat com> 1.0.1-3
- add support for arithmetic coded files into decoder (#639672)

* Wed Sep 29 2010 jkeating - 1.0.1-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> 1.0.1-1
- update to 1.0.1
  - libjpeg-turbo10-rh617469.patch merged
- add -static subpkg (#632859)

* Wed Aug 04 2010 Adam Tkac <atkac redhat com> 1.0.0-3
- fix huffman decoder to handle broken JPEGs well (#617469)

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-2
- add libjpeg-devel%%{_isa} provides to -devel subpkg to satisfy imlib-devel
  deps

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- patches merged
  - libjpeg-turbo-programs.patch
  - libjpeg-turbo-nosimd.patch
- add libjpeg provides to the main package to workaround problems with broken
  java-1.6.0-openjdk package

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 0.0.93-13
- remove libjpeg provides from -utils subpkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-12
- move Obsoletes: libjpeg to main pkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-11
- -utils: Requires: %%name ...

* Wed Jun 30 2010 Adam Tkac <atkac redhat com> 0.0.93-10
- add Provides = libjpeg to -utils subpackage

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 0.0.93-9
- merge review related fixes (#600243)

* Wed Jun 16 2010 Adam Tkac <atkac redhat com> 0.0.93-8
- merge review related fixes (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-7
- obsolete -static libjpeg subpackage (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-6
- improve package description a little (#600243)
- include example.c as %%doc in the -devel subpackage

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.0.93-5
- don't use "fc12" disttag in obsoletes/provides (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-4
- fix compilation on platforms without MMX/SSE (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-3
- package review related fixes (#600243)

* Wed Jun 09 2010 Adam Tkac <atkac redhat com> 0.0.93-2
- package review related fixes (#600243)

* Fri Jun 04 2010 Adam Tkac <atkac redhat com> 0.0.93-1
- initial package
