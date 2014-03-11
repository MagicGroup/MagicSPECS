Summary: Library for accessing digital cameras
Name: libgphoto2
Version: 2.4.13
Release: 3%{?dist}
# GPLV2+ for the main lib (due to exif.c) and most plugins, some plugins GPLv2
License: GPLv2+ and GPLv2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: http://downloads.sourceforge.net/gphoto/libgphoto2-%{version}.tar.bz2
Patch1: gphoto2-pkgcfg.patch
Patch2: gphoto2-storage.patch
Patch3: gphoto2-ixany.patch
Patch4: gphoto2-maxentries.patch
Patch5: gphoto2-device-return.patch
Url: http://www.gphoto.org/
Requires: lockdev
BuildRequires: libusb-devel >= 0.1.5
BuildRequires: lockdev-devel
BuildRequires: libexif-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig, sharutils
BuildRequires: libtool-ltdl-devel, popt-devel
BuildRequires: gd-devel
Obsoletes: gphoto2 < 2.4.0-11
Obsoletes: gphoto2-devel < 2.4.0-11

%description
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.

%package devel
Summary: Headers and links to compile against the libgphoto2 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, libusb-devel >= 0.1.5, libexif-devel
Obsoletes: gphoto2 < 2.4.0-11
Obsoletes: gphoto2-devel < 2.4.0-11
Provides: gphoto2-devel = %{version}-%{release}

%description devel
libgphoto2 is a library that can be used by applications to access
various digital cameras. libgphoto2 itself is not a GUI application,
opposed to gphoto. There are GUI frontends for the gphoto2 library,
however, such as gtkam for example.

This package contains files needed to compile applications that
use libgphoto2.

%prep
%setup -q
%patch1 -p1 -b .pkgcfg
%patch2 -p1 -b .storage
%patch3 -p1 -b .ixany
%patch4 -p1 -b .maxentries
%patch5 -p1 -b .device-return

for i in AUTHORS COPYING libgphoto2_port/AUTHORS libgphoto2_port/COPYING.LIB `find -name 'README.*'`; do
	mv ${i} ${i}.old
	iconv -f ISO-8859-1 -t UTF-8 < ${i}.old > ${i}
	touch -r ${i}.old ${i} || :
	rm -f ${i}.old
done

# FIXME: These .pc.in files aren't actually being installed?
cat > gphoto2.pc.in << \EOF
prefix=@prefix@
exec_prefix=@exec_prefix@
libdir=@libdir@
includedir=@includedir@
VERSION=@VERSION@

Name: gphoto2
Description: Library for easy access to digital cameras
Requires:
Version: @VERSION@
Libs: -L${libdir} -lgphoto2 -lgphoto2_port -lm
Cflags: -I${includedir} -I${includedir}/gphoto2
EOF
sed 's/Name: gphoto2/Name: gphoto2-port/' < gphoto2.pc.in > gphoto2-port.pc.in

%build
#libusb and libusb have shoved their .pc files into /lib[64]/pkgconfig
export PKG_CONFIG_PATH=/%{_lib}/pkgconfig
%configure \
	udevscriptdir='%{_prefix}/lib/udev' \
	--with-drivers=all \
	--with-doc-dir=%{_docdir}/%{name} \
	--disable-static \
	--disable-rpath

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libgphoto2_port/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libgphoto2_port/libtool

make %{?_smp_mflags}

%install
rm -rf "${RPM_BUILD_ROOT}"

make mandir=%{_mandir} DESTDIR=$RPM_BUILD_ROOT install

pushd packaging/linux-hotplug/
install -d -m755 %{buildroot}/usr/share/hal/fdi/information/20thirdparty/
export LIBDIR=$RPM_BUILD_ROOT%{_libdir}
export CAMLIBS=$RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
$RPM_BUILD_ROOT%{_libdir}/%{name}/print-camera-list hal-fdi | \
grep -v "<!-- This file was generated" > $RPM_BUILD_ROOT/%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi

# Output udev rules for device identification; this is used by GVfs gphoto2
# backend and others.
#
# Btw, since it's /lib/udev, never e.g. /lib64/udev, we hardcode the path
#
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d
$RPM_BUILD_ROOT%{_libdir}/%{name}/print-camera-list udev-rules version 136 > $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/40-libgphoto2.rules
popd

# remove circular symlink in /usr/include/gphoto2 (#460807)
rm -f %{buildroot}%{_includedir}/gphoto2/gphoto2

# remove unneeded print-camera-list from libdir (#745081)
rm -f %{buildroot}%{_libdir}/libgphoto2/print-camera-list

rm -rf %{buildroot}%{_libdir}/libgphoto2/*/*a
rm -rf %{buildroot}%{_libdir}/libgphoto2_port/*/*a
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

magic_rpm_clean.sh
%find_lang %{name}-2 || touch %{name}-2.lang
%find_lang %{name}_port-0 || touch %{name}_port-0.lang
cat libgphoto2*.lang >> %{name}.lang

%clean
rm -rf "${RPM_BUILD_ROOT}"

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS
%dir %{_libdir}/libgphoto2_port
%dir %{_libdir}/libgphoto2_port/*
%dir %{_libdir}/libgphoto2
%dir %{_libdir}/libgphoto2/*
%{_libdir}/libgphoto2_port/*/*.so
%{_libdir}/libgphoto2/*/*.so
%{_libdir}/*.so.*
%{_datadir}/hal/fdi/information/20thirdparty/10-camera-libgphoto2.fdi
%{_prefix}/lib/udev/rules.d/40-libgphoto2.rules
%{_prefix}/lib/udev/check-ptp-camera

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_datadir}/libgphoto2
%{_bindir}/gphoto2-config*
%{_bindir}/gphoto2-port-config
%{_includedir}/gphoto2
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.4.13-3
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 2.4.13-2
- 为 Magic 3.0 重建

* Thu Mar 21 2012 Jindrich Novy <jnovy@redhat.com> 2.4.13-1
- update to 2.4.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jindrich Novy <jnovy@redhat.com> 2.4.11-2
- remove unneeded print-camera-list from libdir (#745081)

* Mon Apr 18 2011 Jindrich Novy <jnovy@redhat.com> 2.4.11-1
- update to 2.4.11

* Wed Feb 09 2011 Jindrich Novy <jnovy@redhat.com> 2.4.10.1-1
- update to 2.4.10.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Caolán McNamara <caolanm@redhat.com> 2.4.10-4
- rebuild for dependencies

* Wed Oct 20 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-3
- move udev helper scripts to /lib/udev (#644552)

* Tue Sep 06 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-2
- BR: gd-devel because of ax203 and st2205 camlibs (#630570)

* Tue Aug 17 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-1
- update to 2.4.10

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> 2.4.9-2
- remove the need to call autoreconf

* Mon Apr 12 2010 Jindrich Novy <jnovy@redhat.com> 2.4.9-1
- update to 2.4.9

* Mon Jan 25 2010 Jindrich Novy <jnovy@redhat.com> 2.4.8-1
- update to 2.4.8

* Fri Dec 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-3
- remove circular symlink in /usr/include/gphoto2 (#460807)

* Fri Oct 23 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-2
- return the dual-mode device to kernel once we don't use it (#530545)

* Tue Aug 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-1
- update to 2.4.7
- drop udev patch, applied upstream
- update storage patch

* Sun Aug 09 2009 David Zeuthen <davidz@redhat.com> 2.4.6-3
- Add patch from http://sourceforge.net/tracker/?func=detail&aid=2801117&group_id=8874&atid=308874
  and generate generic udev rules for device identification (ID_GPHOTO2* properties)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Jindrich Novy <jnovy@redhat.com> 2.4.6-1
- update to 2.4.6
- new IDs for Kodak V803, M1063, Canon PowerShot A650IS, SD990 (aka IXUS 980IS),
  SD880IS, A480, Canon EOS 50D, Fuji FinePix S1000fd
- many Canon related fixes

* Wed Apr 08 2009 Jindrich Novy <jnovy@redhat.com> 2.4.5-1
- update to 2.4.5
- remove .canontimeout patch, applied upstream

* Wed Apr 01 2009 Jindrich Novy <jnovy@redhat.com> 2.4.4-4
- increase timeouts for Canon cameras (#476355), thanks to
  Andrzej Nowak and Russell Harrison

* Thu Mar 05 2009 Caolán McNamara <caolanm@redhat.com> - 2.4.4-3
- tweak BR to get to build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Jindrich Novy <jnovy@redhat.com> 2.4.4-1
- update to 2.4.4
- many fixes and improvements to Nikon and Canon cameras
- translation updates

* Thu Nov 13 2008 Rex Dieter <rdieter@fedoraproject.org> 2.4.3-2
- respin (libtool)

* Mon Oct 20 2008 Jindrich Novy <jnovy@redhat.com> 2.4.3-1
- update to libgphoto2-2.4.3

* Tue Sep 23 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-2
- convert all shipped docs to UTF-8

* Fri Aug 01 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-1
- update to 2.4.2
- contains many fixes in the Canon camera communication interface
- drop build patch, no more needed

* Mon Jul 07 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-6
- increase maximal number of entries in the camera list (#454245)

* Fri Jun 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.1-5
- fix pkgcfg patch to match actual .pc file names (fixes kdegraphics build)

* Thu Jun 12 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-3
- libgphoto2-devel requires libusb-devel and libexif-devel for
  pkgconfig

* Wed Jun 04 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-2
- fix obsoletes
- workaround problem with coreutils-6.12 and RHEL5-xen kernels
  what prevents libgphoto2 koji build

* Mon Jun 02 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-1
- update to 2.4.1 (#443515, #436138)

* Thu May 29 2008 Stepan Kasal <skasal@redhat.com> 2.4.0-3
- drop gphoto2-norpath.patch
- use quoted here-document in %%prep
- fix some typos in m4 sources
- run autoreconf to get autotools right

* Mon Apr 21 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-2
- apply patch to fix build with libusb

* Fri Apr 18 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-1
- backport patch from upstream to avoid segfault when
  data phase is skipped for certain devices (#435413)
- initial build

* Mon Apr 14 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-0.2
- review fixes, thanks to Hans de Goede: (#437285)
  - remove unused macro
  - don't exclude s390/s390x
  - preserve timestamps
  - fix license

* Thu Mar 13 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-0.1
- initial libgphoto2 packaging
