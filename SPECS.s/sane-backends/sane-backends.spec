#if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
#global needs_multilib_quirk 0
#else
# let -devel require drivers to make them available as multilib
%global needs_multilib_quirk 1
#endif

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global _hardened_build 1
%endif

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global udevdir %{_prefix}/lib/udev
%else
%global udevdir /lib/udev
%endif
%global udevrulesdir %{udevdir}/rules.d
%global udevhwdbdir %{udevdir}/hwdb.d

%if !0%{?fedora}%{?rhel} || 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global libusb1 1
%else
%global libusb1 0
%endif

%define __provides_exclude_from ^%{_libdir}/sane/.*\.so.*$
%define __requires_exclude ^libsane-.*\.so\.[0-9]*(\(\).*)?+$

%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 20 || 0%{?rhel} >= 8
%define _maindocdir %{_docdir}/%{name}
%define _docdocdir %{_docdir}/%{name}-doc
%else
%define _maindocdir %{_docdir}/%{name}-%{version}
%define _docdocdir %{_docdir}/%{name}-doc-%{version}
%endif

Summary: Scanner access software
Summary(zh_CN.UTF-8): 扫描仪访问软件
Name: sane-backends
Version: 1.0.24
Release: 18%{?dist}
# lib/ is LGPLv2+, backends are GPLv2+ with exceptions
# Tools are GPLv2+, docs are public domain
# see LICENSE for details
License: GPLv2+ and GPLv2+ with exceptions and Public Domain
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Alioth Download URLs are amazing.
Source0: https://alioth.debian.org/frs/download.php/latestfile/176/sane-backends-%{version}.tar.gz
Source1: sane.png

# Fedora-specific, not generally applicable:
Patch0: sane-backends-1.0.24-udev.patch
# Upstream commit b491261f0c0f6df47d1e4859cde88448f98718dd
Patch1: sane-backends-1.0.21-epson-expression800.patch
# Fedora-specific (for now): don't use the same SONAME for backend libs and
# main lib
Patch2: sane-backends-1.0.23-soname.patch
# Fedora-specific (for now): make installed sane-config multi-lib aware again
Patch3: sane-backends-1.0.23-sane-config-multilib.patch
# Upstream commit 3b96baef65ea6c315937f5cd2253c6b6c62636d8
Patch4: sane-backends-1.0.24-hwdb.patch
# Upstream commit d35d6326cb00fcbb19b41599bdff7faf5d79225e
Patch5: sane-backends-1.0.24-pixma_bjnp-crash.patch
# Upstream commit 252ccdd926bb28bd6064da7b652e646664226572
# Upstream commit 66cb9b55c2e60503d537d7ed927f5a5aef3658d2
# Upstream commit cf9129d62fe7e84479e8daf6018cd2495d53bcc9
# Upstream commit 575f40a0790bb5e20ffd7ccae1c9272e481bbe51
# Upstream commit b53a58c4b534b9e6897c1b0a6301d2bf76dc3499
# Upstream commit 101f76c516cd42cafe9e142aefe751094a125e73
# Upstream commit 2d89e37f365cb8e54ee44aa686a62320e2837b50
# Upstream commit a3fe2c1ea5b4f6b1e55435f6abc44f402ff32b4d
# Upstream commit 602d6ecdfe5f3146867799fabf3ac87582c26461
# Upstream commit 5d7f7ffefb22e7e64789e97af0356b7859d61814
# Upstream commit dc76e7cce464f04e46aab2bb0c269b4742161c59
# Upstream commit d835d9d565118d52c2339c2e79890f57d0616077
Patch6: sane-backends-1.0.24-static-code-check.patch
# Upstream commit 758731489d0d58bab6e4b70db9556038c9f4bb67
Patch7: sane-backends-1.0.24-scsi-permissions.patch
# Upstream commit 8082a42ec4f3b3cf2cffc30a45dda5fc41d55576
Patch8: sane-backends-1.0.24-format-security.patch
# Update lib/snprintf.c to latest from LPRng to resolve
# license issue (#1102520)
Patch9: sane-backends-1.0.24-snprintf-cleanroom.patch
# Upstream commit 73cb422f860a84aca7a19114936ead1794d77890
Patch10: sane-backends-1.0.24-usb3-xhci.patch

URL: http://www.sane-project.org

BuildRequires: %{_bindir}/latex
%if %libusb1
BuildRequires: libusbx-devel
%else
BuildRequires: libusb-devel
%endif
BuildRequires: libieee1284-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: libv4l-devel
BuildRequires: gettext
BuildRequires: gphoto2-devel
Requires: systemd >= 196
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if 0%{?fedora}%{?rhel} && (0%{?fedora} < 25 || 0%{?rhel} < 8)
Obsoletes: sane-backends < 1.0.23-10
Conflicts: sane-backends < 1.0.23-10
%endif

%description
Scanner Access Now Easy (SANE) is a universal scanner interface.  The
SANE application programming interface (API) provides standardized
access to any raster image scanner hardware (flatbed scanner,
hand-held scanner, video and still cameras, frame-grabbers, etc.).

%description -l zh_CN.UTF-8
扫描仪访问软件。

%package doc
Summary: SANE backends documentation
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
BuildArch: noarch
# Don't drag around obsoletes forever
%if 0%{?fedora}%{?rhel} && (0%{?fedora} < 25 || 0%{?rhel} <= 8)
Obsoletes: sane-backends < 1.0.23-10
Conflicts: sane-backends < 1.0.23-10
%endif

%description doc
This package contains documentation for SANE backends.
%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package libs
Summary: SANE libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
This package contains the SANE libraries which are needed by applications that
want to access scanners.
%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary: SANE development toolkit
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if %needs_multilib_quirk
Requires: sane-backends-drivers-scanners%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-drivers-cameras%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
%if %libusb1
Requires: libusbx-devel
%else
Requires: libusb-devel
%endif
Requires: libieee1284-devel
Requires: libjpeg-devel
Requires: libtiff-devel
Requires: pkgconfig

%description devel
This package contains libraries and header files for writing Scanner Access Now
Easy (SANE) modules.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package drivers-scanners
Summary: SANE backend drivers for scanners
Summary(zh_CN.UTF-8): 扫描仪的驱动
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if 0%{?rhel} && 0%{?rhel} < 8
Obsoletes: sane-backends < 1.0.22-4
Obsoletes: sane-backends-libs < 1.0.22-4
Conflicts: sane-backends < 1.0.22-4
Conflicts: sane-backends-libs < 1.0.22-4
%endif

%description drivers-scanners
This package contains backend drivers to access scanner hardware through SANE.

%description drivers-scanners -l zh_CN.UTF-8
扫描仪的驱动。

%package drivers-cameras
Summary: Scanner backend drivers for digital cameras
Summary(zh_CN.UTF-8): 数码相机的驱动
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: sane-backends = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: sane-backends-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Don't drag around obsoletes forever
%if 0%{?rhel} && 0%{?rhel} < 8
Obsoletes: sane-backends-libs-gphoto2 < 1.0.22-4
Conflicts: sane-backends-libs-gphoto2 < 1.0.22-4
Provides: sane-libs-gphoto2 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: sane-libs-gphoto2%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description drivers-cameras
This package contains backend drivers to access digital cameras through SANE.
%description drivers-cameras -l zh_CN.UTF-8
数码相机的驱动。

%prep
%setup -q

%patch0 -p1 -b .udev
%patch1 -p1 -b .epson-expression800
%patch2 -p1 -b .soname
%patch3 -p1 -b .sane-config-multilib
%patch4 -p1 -b .hwdb
%patch5 -p1 -b .pixma_bjnp-crash
%patch6 -p1 -b .static-code-check
%patch7 -p1 -b .scsi-permissions
%patch8 -p1 -b .format-security
%patch9 -p1 -b .snprintf-cleanroom
%patch10 -p1 -b .usb3-xhci

%build
CFLAGS="%optflags -fno-strict-aliasing"
%if ! 0%{?_hardened_build}
# use PIC/PIE because SANE-enabled software is likely to deal with data coming
# from untrusted sources (client <-> saned via network)
CFLAGS="$CFLAGS -fPIC"
LDFLAGS="-pie"
%endif
%configure \
    --with-gphoto2=%{_prefix} \
    --with-docdir=%{_maindocdir} \
    --disable-locking --disable-rpath \
%if %libusb1
    --enable-libusb_1_0 \
%endif
    --enable-pthread
make %{?_smp_mflags}

# Write udev/hwdb files
_topdir="$PWD"
pushd tools
./sane-desc -m udev+hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.rules
./sane-desc -m hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.hwdb

popd

%install
make DESTDIR="%{buildroot}" install

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps
rm -f %{buildroot}%{_bindir}/gamma4scanimage
rm -f %{buildroot}%{_mandir}/man1/gamma4scanimage.1*
rm -f %{buildroot}%{_libdir}/sane/*.a %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/libsane*.la %{buildroot}%{_libdir}/sane/*.la

mkdir -p %{buildroot}%{udevrulesdir}
mkdir -p %{buildroot}%{udevhwdbdir}
install -m 0644 tools/udev/sane-backends.rules %{buildroot}%{udevrulesdir}/65-sane-backends.rules
install -m 0644 tools/udev/sane-backends.hwdb %{buildroot}%{udevhwdbdir}/20-sane-backends.hwdb

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 tools/sane-backends.pc %{buildroot}%{_libdir}/pkgconfig/

mkdir %{buildroot}%{_docdocdir}
pushd %{buildroot}%{_maindocdir}
for f in *; do
    if [ -d "$f" ]; then
        mv "$f" "%{buildroot}%{_docdocdir}/${f}"
    else
        case "$f" in
        AUTHORS|ChangeLog|COPYING|LICENSE|NEWS|PROBLEMS|README|README.linux)
            ;;
        backend-writing.txt|PROJECTS|sane-*.html)
            mv "$f" "%{buildroot}%{_docdocdir}/${f}"
            ;;
        *)
            rm -rf "$f"
            ;;
        esac
    fi
done
popd
magic_rpm_clean.sh
#find_lang %%name

%post
udevadm hwdb --update >/dev/null 2>&1 || :

%postun
udevadm hwdb --update >/dev/null 2>&1 || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%doc %{_maindocdir}
%dir /etc/sane.d
%dir /etc/sane.d/dll.d
%config(noreplace) /etc/sane.d/*.conf
%{udevrulesdir}/65-sane-backends.rules
%{udevhwdbdir}/20-sane-backends.hwdb
%{_datadir}/pixmaps/sane.png

%{_bindir}/sane-find-scanner
%{_bindir}/scanimage
%{_sbindir}/*

%exclude %{_mandir}/man1/sane-config.1*
%{_mandir}/*/*

%dir %{_libdir}/sane

%files doc
%defattr(-, root, root)
%doc %{_docdocdir}

%files libs
%defattr(-, root, root)
%{_libdir}/libsane*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/sane-config
%{_mandir}/man1/sane-config.1*
%{_includedir}/sane
%{_libdir}/libsane*.so
%{_libdir}/pkgconfig/sane-backends.pc

%files drivers-scanners
%defattr(-, root, root)
%{_libdir}/sane/*.so*
%exclude %{_libdir}/sane/*gphoto2.so*

%files drivers-cameras
%defattr(-, root, root)
%{_libdir}/sane/*gphoto2.so*

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.24-18
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.24-17
- 为 Magic 3.0 重建

* Fri Sep 25 2015 Liu Di <liudidi@gmail.com> - 1.0.24-16
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Nils Philippsen <nils@redhat.com> - 1.0.24-14
- reformat and rename snprintf-cleanroom patch
- backport USB3 xhci patch from upstream master (#1228954)

* Mon Jun 08 2015 Nils Philippsen <nils@redhat.com> - 1.0.24-14
- apply format-security patch, drop format-security2 patch

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.24-13
- Rebuild (libgphoto2)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Tom Callaway <spot@fedoraproject.org> - 1.0.24-10
- update lib/snprintf.c to resolve license issue (#1102520)

* Mon Apr 14 2014 Jaromir Capik <jcapik@redhat.com> - 1.0.24-9
- Fixing format-security flaws

* Wed Dec 04 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-8
- use string literals as format strings (#1037316)

* Wed Nov 20 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-7
- set correct permissions for SCSI devices (#1028549)

* Thu Nov 07 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-6
- epson: don't leak memory if realloc() fails

* Thu Nov 07 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-5
- fix issues found during static code check

* Tue Oct 29 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-4
- fix crash in pixma driver (#1021653)

* Thu Oct 24 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-3
- generate hwdb files correctly (#1018565)

* Wed Oct 16 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-2
- update udev hwdb on installation/removal

* Wed Oct 09 2013 Nils Philippsen <nils@redhat.com> - 1.0.24-1
- version 1.0.24
- use (hopefully stable) Alioth download URL
- update udev patch, remove obsolete patches
- use udev hwdb instead of huge rulesets

* Mon Sep 09 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-18
- build against libusb-1.0 on Fedora >= 18 (#1003193)
- require libusbx-devel instead of libusb1-devel which is obsolete

* Wed Sep 04 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.23-17
- Really build against libusb-1.0 on Fedora >= 19 (#1003193)

* Wed Sep 04 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-16
- don't drag around obsoletes forever (#1002141)

* Wed Aug 07 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-15
- use unversioned docdir from Fedora 20 on (#994067)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-13
- fix crash in genesys (gl646) backend (#983694)

* Mon Jul 08 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-12
- describe missing flag "-b" in scanimage man page
- add short help message to saned
- fix bogus changelog dates

* Tue Jun 25 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-11
- move documentation into separate doc subpackage (#977653)
- remove ancient, unneeded obsoletes and conflicts

* Mon Jun 24 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-10
- move some documentation to devel subpackage (#977103)

* Thu Jun 13 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-10
- don't ignore libsane-gphoto2.so

* Fri Apr 19 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-9
- use libusb1 instead of libusb from F-19 on

* Thu Apr 18 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-8
- fix building with -fno-strict-aliasing

* Fri Feb 01 2013 Nils Philippsen <nils@redhat.com> - 1.0.23-7
- filter out backend driver provides/requires
- update latex build dep
- umax: initialize reader_pid early in sane_start() (#853667)
- coolscan2/3: support multi-scan option of some devices

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.0.23-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.0.23-5
- rebuild against new libjpeg

* Mon Sep 10 2012 Nils Philippsen <nils@redhat.com> - 1.0.23-3
- udev: set up for generic user access rules, improve paths and dependencies

* Tue Sep 04 2012 Nils Philippsen <nils@redhat.com> - 1.0.23-2
- make installed sane-config multi-lib aware again

* Fri Aug 31 2012 Nils Philippsen <nils@redhat.com> - 1.0.23-1
- version 1.0.23
- update udev patch, remove obsolete patches
- use %%_hardened_build macro from F-16 on instead of tweaking flags manually
- don't use the same SONAME for backend libs and main lib

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.22-12
- rebuild (gphoto2)

* Wed Jun 06 2012 Nils Philippsen <nils@redhat.com> - 1.0.22-11
- multilib: enable -devel quirk regardless of version until a fixed mash gets
  into production (#829268)

* Tue Apr 17 2012 Nils Philippsen <nils@redhat.com> - 1.0.22-10
- fix avision device initialization (#706877)

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 1.0.22-9
- rebuild for gcc 4.7

* Wed Jan 04 2012 Nils Philippsen <nils@redhat.com> - 1.0.22-8
- fix Lexmark X1100 (#753489)

* Mon Nov 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.22-7
- libs shouldn't depends on base package. Properly fix #736310
- base package should obsolete -docs as it provides them not -libs
- update spec to current standard

* Fri Nov 18 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-6
- avision: reenable grayscale and lineart modes for AV220 (#700725)

* Mon Oct 10 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-5
- multilib: let -devel depend on -drivers-* on F-16 and earlier (#740992)
- multilib: make -drivers-scanners obsolete old -libs as well

* Fri Sep 16 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-4
- multilib: always use pkg-config in sane-config (#707910)
- add USB id for Epson Stylus SX125 (#703529)

* Thu Sep 15 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-4
- allow installing the libraries without the drivers (#736310): split off
  drivers into -drivers-scanners, rename -libs-gphoto2 to -drivers-cameras

* Tue May 10 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-3
- fix detection/handling of USB devices in xerox_mfp (#702983)

* Tue Apr 19 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-2
- remove obsolete lockdir, automake patches

* Wed Mar 16 2011 Nils Philippsen <nils@redhat.com> - 1.0.22-1
- version 1.0.22
- remove obsolete i18n, xerox-mfp-color-mode, epson2-fixes, open-macro patches
- update pkgconfig, udev, docs-utf8, v4l, man-encoding patches
- submit patches upstream where this is applicable, add comments
- manually install pkg-config file

* Wed Mar 09 2011 Dan Horák <dan[at]danny.cz> - 1.0.21-8
- updated for newer libv4l

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Nils Philippsen <nils@redhat.com> - 1.0.21-6
- backport fixes for epson2 backend (#667858, #671534)

* Tue Nov 23 2010 Nils Philippsen <nils@redhat.com> - 1.0.21-5
- build mustek_usb2 backend again, enable use of libpthread (#603321)

* Mon Nov 08 2010 Nils Philippsen <nils@redhat.com>
- let sane-backends require arch-specific version/release of -libs (#621217)

* Wed Nov 03 2010 Nils Philippsen <nils@redhat.com> - 1.0.21-4
- xerox_mfp: correct color mode malfunction (#614949)
- xerox_mfp: add USB id for SCX-4500W (#614948)

* Fri Jun 25 2010 Nils Philippsen <nils@redhat.com> - 1.0.21-3
- build with -fno-strict-aliasing
- use PIC/PIE because SANE-enabled software is likely to deal with data coming
  from untrusted sources (client <-> saned via network)

* Mon Jun 07 2010 Nils Philippsen <nils@redhat.com>
- rectify devel subpackage description

* Wed Jun 02 2010 Nils Philippsen <nils@redhat.com> - 1.0.21-2
- fix pkgconfig file (#598401)

* Wed May 05 2010 Nils Philippsen <nils@redhat.com> - 1.0.21-1
- version 1.0.21
- remove obsolete rpath, hal, genesys-gl841-registers patches
- update pkgconfig, udev, man-utf8->man-encoding, epson-expression800,
  docs-utf8 patches
- remove hal conditional
- package man pages

* Fri Feb 26 2010 Nils Philippsen <nils@redhat.com> - 1.0.20-12
- convert some documentation files to UTF-8
- fix permissions of pkgconfig file

* Tue Dec 29 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-11
- genesys_gl841: always send registers before trying to acquire a line
  (#527935)

* Mon Dec 28 2009 Nils Philippsen <nils@redhat.com>
- build v4l backend (#550119)
- don't use lockdir, fix make install

* Thu Oct 22 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-10
- don't set owner, group or mode as this may interfere with setting ACLs

* Thu Oct 22 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-9
- fix device file ownership and mode

* Thu Oct 22 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-8
- ship adapted udev rules from F-12 on (#512516)
- don't require pam anymore

* Mon Aug 31 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-7
- fix --enable-rpath

* Mon Aug 03 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-6
- remove ExcludeArch: s390 s390x

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-4
- separate HAL information and policy files (#457645)

* Thu Jun 18 2009 Nils Philippsen <nils@redhat.com>
- mark /etc/sane.d/dll.d as %%dir, not %%config

* Wed Jun 17 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-3
- disable rpath
- make sane-config multilib-aware

* Wed Jun 17 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-2
- fix permissions for Epson Expression 800 (#456656)

* Tue Jun 16 2009 Nils Philippsen <nils@redhat.com> - 1.0.20-1
- version 1.0.20
- rebase/remove patches
- use %%_isa for arch-specific requirements
- place HAL fdi files in the correct place (#457645)

* Sun Jun 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.19-16
- Don't claim ownership of %%_libdir/pkgconfig/ (#499659)

* Mon Mar 02 2009 Nils Philippsen <nils@redhat.com> - 1.0.19-15
- let sane-backends-devel require libjpeg-devel, libtiff-devel
- update rpath patch (no longer touch sane-config.in as that is replaced
  anyway)
- fix pkgconfig patch, bzip2 it

* Fri Feb 27 2009 Nils Philippsen <nils@redhat.com> - 1.0.19-14
- fix pkgconfig files

* Wed Feb 25 2009 Nils Philippsen <nils@redhat.com> - 1.0.19-13
- drop acinclude patch to not unnecessarily rebuild autoconf/libtool files
  which made libtool break builds on Rawhide
- use "make DESTDIR=... install" instead of "%%makeinstall"

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.19-12
- fix license tag

* Wed Sep 03 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-11
- update glibc-2.7 patch to apply without fuzz

* Thu Mar 27 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-10
- rename 60-libsane.fdi to 19-libsane.fdi so that hal-acl-tool callouts get
  added (#438827)

* Wed Mar 26 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-9
- cope with info.subsystem from new HAL versions as well as info.bus (#438827)

* Fri Mar 14 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-8
- add arch-specific provides/requires to/for libs-gphoto2 subpackage (#436657)

* Mon Mar 10 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-7
- remove ancient sane-devel obsoletes/provides
- remove libs/doc/gphoto2 conditionals
- fix build root
- add arch-specific provides/requires (#436657)

* Tue Feb 19 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-6
- move libsane-gphoto2.so into -libs-gphoto2
- recode spec file to UTF-8

* Thu Feb 14 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-5
- replace string-oob patch with uninitialized patch by upstream which covers
  more backends

* Thu Feb 14 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-4
- guard against out-of-bounds string access in fujitsu backend (#429338, patch
  by Caolan McNamara)

* Wed Feb 13 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-3
- add HAL policy for SCSI scanners

* Tue Feb 12 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-2
- add files missing from CVS to make autoconf work

* Tue Feb 12 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-1
- version 1.0.19 final

* Wed Feb 06 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.19-0.1.cvs20080206
- cvs snapshot 20080206
- handle access control through hal/PolicyKit instead of udev (#405211)
- drop obsolete badcode, logical_vs_binary, epson-cx5000, multilib, usb_reset,
  udev-symlink, udev-098 patches
- update pkgconfig patch

* Wed Jan 30 2008 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-21
- don't require libsane-hpaio (#430834)
- use %%bcond_without/with macros

* Fri Dec 07 2007 Jesse Keating <jkeating@redhat.com> - 1.0.18-20
- undo bootstrap setting now that hplip built.

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.0.18-19
- do a bootstrap build without hplip requirements

* Wed Nov 07 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-18
- move backend .so files out of -devel into main package (#209389)

* Tue Oct 02 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-17
- disable pint backend (which doesn't build without some BSD specific headers)

* Tue Oct 02 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-16
- enable dell1600n_net (#314081) and pint backends

* Wed Aug 15 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-15
- enable support for Epson CX-5000

* Wed Aug 08 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-14
- make udev rules more robust (#243953)
- bring code in shape for glibc-2.7

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 1.0.18-13
- rebuild for toolchain bug

* Tue Jul 24 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-12
- fix typo in spec file

* Tue Jul 24 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-11
- work around udev regexes not matching as they should (#244444)

* Sun Jul 22 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-10
- tweak udev rules generation (#244444)

* Fri Jul 20 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-9
- don't tweak device names in device configuration files anymore (obsolete)
- let udev rules cope with SUBSYSTEM=="usb" (#244444)
- tweak-udev-rules patch is udev-098 patch now

* Thu Jul 05 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-8
- tweak udev rules to conform with new udev syntax (#246849)

* Fri Jun 15 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-7
- call usb_reset() prior to usb_close() to workaround hanging USB hardware
  (#149027, #186766)

* Tue Apr 24 2007 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-6
- don't erroneously use logical "&&" instead of binary "&" at some places in
  the canon driver

* Fri Oct 13 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-5
- use %%rhel, not %%redhat

* Fri Oct 13 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-4
- don't ship generated docs in -libs but main package (#210572)

* Sun Sep 17 2006 Warren Togami <wtogami@redhat.com> - 1.0.18-3
- -devel req exact version-release

* Fri Sep 08 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-2
- remove unneeded programs subpackage
- clean up docs vs. libs pkg split, mark documentation as %%doc

* Mon Jul 24 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.18-1
- version 1.0.18
- unify spec file between OS releases
- update rpath patch
- remove obsolete newmodels patch
- use *.desc created udev rules

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.17-13.1
- rebuild

* Fri Jun 09 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-13
- split package into sane-backends, -devel, -libs, -programs to work around
  multilib issues (#135172)

* Wed Jun 07 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-12
- require libsane-hpaio to work around #165751

* Tue Jun 06 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-11
- add BuildRequires: gettext (#194163)

* Wed May 17 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-10
- add pkg-config support, re-write sane-config to use pkg-config to avoid
  multilib problems with conflicting sane-config scripts

* Tue Apr 25 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-9
- add support for Canon Lide 60 scanner (#189726)

* Wed Apr 05 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-8
- don't use automake

* Tue Apr 04 2006 Nils Philippsen <nphilipp@redhat.com>
- require gphoto2-devel in sane-backends-devel

* Fri Mar 24 2006 Nils Philippsen <nphilipp@redhat.com> 1.0.17-7
- don't include *.la files

* Thu Mar 23 2006 Than Ngo <than@redhat.com> 1.0.17-6
- rebuild against gphoto2 to get rid of gphoto2.la

* Tue Mar 14 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.17-5
- buildrequire automake, autoconf, libtool (#178596)
- don't require /sbin/ldconfig, /bin/mktemp, /bin/grep, /bin/cat, /bin/rm

* Wed Feb 22 2006 Nils Philippsen <nphilipp@redhat.com> - 1.0.17-4
- split off generated documentation into separate subpackage to avoid conflicts
  on multilib systems

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.17-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.17-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Bill Nottingham <notting@redhat.com> 1.0.17-3
- ship udev rules for device creation (#177650). Require udev

* Sun Jan 22 2006 Bill Nottingham <notting@redhat.com> 1.0.17-2
- disable hotplug dep. More later pending (#177650)

* Tue Dec 20 2005 Nils Philippsen <nphilipp@redhat.com> 1.0.17-1
- version 1.0.17
- reenable gphoto2 backend

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Fri Aug 19 2005 Nils Philippsen <nphilipp@redhat.com> 1.0.16-1
- version 1.0.16
- remove obsolete docdir patch

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com>
- Fixed libusbscanner comment (bug #162983).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.0.15-9
- Rebuild for new GCC.

* Fri Dec 10 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-8
- Further small fixes to libusbscanner script.

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com>
- Ship the correct libsane.usermap (part of bug #135802).

* Wed Dec  1 2004 Tim Waugh <twaugh@redhat.com>
- No longer need ep2400 patch.

* Tue Nov 30 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-7
- Updated libusbscanner script from Tomas Mraz, to use pam_console_apply.
- Requires pam >= 0.78-2 for targetted pam_console_apply.

* Thu Nov 25 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-6
- Random changes in libusbscanner.

* Tue Nov 23 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-5
- libusbscanner: Create /dev/usb if it doesn't exist after 30s.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-4
- Attempt to be more useful in libusbscanner by waiting a maximum of 30
  seconds.
- Add a chcon call to libusbscanner (bug #140059).  Based on contribution
  from W. Michael Petullo.

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.0.15-3
- Convert man pages to UTF-8

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com>
- Require hotplug's remover to work.

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-2
- Applied the libusbscanner part of the patch for bug #121511, by Ian
  Pilcher.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com> 1.0.15-1
- 1.0.15.

* Sun Oct 10 2004 Tim Waugh <twaugh@redhat.com> 1.0.14-6
- Make man pages identical on multilib installations.

* Thu Oct  7 2004 Tim Waugh <twaugh@redhat.com> 1.0.14-5
- Build requires libjpeg-devel (bug #134964).

* Thu Aug 26 2004 Tim Waugh <twaugh@redhat.com> 1.0.14-4
- Apply patch from David Zeuthen to fix hotplug script (bug #130755).

* Mon Aug  9 2004 Tim Waugh <twaugh@redhat.com> 1.0.14-3
- Mark config files noreplace.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1.0.14-1
- 1.0.14.

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- s/ftp.mostang.com/ftp.sane-project.org/.

* Fri May  7 2004 Tim Waugh <twaugh@redhat.com> 1.0.13-7
- Fix epson.conf for USB scanners (bug #122328).

* Tue May  4 2004 Tim Waugh <twaugh@redhat.com> 1.0.13-6
- Ship libusb.usermap (from sane-backends-1.0.14) and a pam_console-aware
  libusbscanner script.
- Fix epson.conf for Epson Perfection 2400 (bug #122328).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Tim Waugh <twaugh@redhat.com> 1.0.13-4
- Fixed compilation with GCC 3.4.

* Mon Dec 15 2003 Tim Waugh <twaugh@redhat.com> 1.0.13-3
- Take %%{_libdir}/sane out of ldconfig's search path altogether (Oliver
  Rauch).

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 1.0.13-2
- no rpath in sane-config anymore

* Sun Nov 23 2003 Tim Waugh <twaugh@redhat.com> 1.0.13-1
- 1.0.13.
- No longer need autoload, gt68xx patches.

* Thu Nov 20 2003 Tim Waugh <twaugh@redhat.com> 1.0.12-6
- Don't add %%{_libdir}/sane to ld.so.conf (bug #110419).

* Tue Nov 11 2003 Tim Waugh <twaugh@redhat.com> 1.0.12-5
- Updated gt68xx driver to fix timeout problems.

* Wed Oct  8 2003 Tim Waugh <twaugh@redhat.com>
- Avoided undefined behaviour in canon-sane.c (bug #106305).

* Mon Sep 29 2003 Tim Waugh <twaugh@redhat.com>
- Updated URL.

* Thu Jul 24 2003 Tim Waugh <twaugh@redhat.com> 1.0.12-4
- The devel package requires libieee1284-devel.

* Mon Jun 16 2003 Tim Waugh <twaugh@redhat.com> 1.0.12-3
- Use libtoolize and aclocal to fix build.
- Build requires libieee1284-devel (to fix bug #75849).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 25 2003 Tim Waugh <twaugh@redhat.com> 1.0.12-1
- 1.0.12.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 1.0.11-1
- Shipped libtool is broken; use installed script instead.
- Remove files not shipped.
- Fix some /usr/lib references.
- 1.0.11.
- Drop sane-sparc, errorchk, hp101, security patches.
- Update rpath, docdir patches.
- Use %%find_lang.

* Fri Mar  7 2003 Tim Waugh <twaugh@redhat.com>
- sane-backends-devel requires libusb-devel (bug #85742).

* Mon Feb 10 2003 Tim Waugh <twaugh@redhat.com> 1.0.9-5
- Fix saned problems.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.0.9-4
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 1.0.9-3
- hp-backend 1.01 for 'error during device I/O' workaround (bug #81835).

* Thu Jan  9 2003 Tim Waugh <twaugh@redhat.com> 1.0.9-2
- Better error checking in the Canon backend (bug #81332).

* Fri Oct 25 2002 Tim Waugh <twaugh@redhat.com> 1.0.9-1
- 1.0.9.

* Wed Oct 23 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-6
- Ship the installed documentation.
- Move sane-config to the devel subpackage (bug #68454).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-4
- Fix bug #62847.

* Tue Jun 18 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-3
- Fix dangling symlink (bug #66672).

* Wed Jun 12 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-2
- Don't tell SANE applications to use rpath (bug #66129, bug #66132).

* Mon May 27 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-1
- 1.0.8.

* Wed May 22 2002 Tim Waugh <twaugh@redhat.com> 1.0.8-0.20020522.1
- Update to CVS.  Release expected before the end of the month.
- No longer need defaultincl or argv patches.

* Wed May 15 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-7
- Unconditionally run ldconfig after installation (bug #64964).

* Mon Mar  4 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-6
- Re-apply the original 1.0.7-4 fix (oops):
  - Make sure to load SCSI modules if not already loaded (bug #59979).

* Mon Mar  4 2002 Tim Powers <timp@redhat.com> 1.0.7-5
- bump release number, wasn't bumped last time

* Mon Mar  4 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-4
- Update sparc patch (Tom "spot" Callaway).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-3
- Rebuild in new environment.
- Disable bad stdarg code in scanimage so that alpha builds succeed.

* Mon Feb 11 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-2
- Make sure sane-config doesn't specify the default include path
  (bug #59507).

* Mon Feb  4 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-1
- 1.0.7.

* Sun Jan 27 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-0.beta2.1
- 1.0.7-beta2.

* Wed Jan 23 2002 Tim Waugh <twaugh@redhat.com> 1.0.7-0.beta1.1
- 1.0.7-beta1.
- Patches no longer needed: scsi, microtek2, format.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.0.6-4
- automated rebuild

* Wed Nov 21 2001 Tim Waugh <twaugh@redhat.com> 1.0.6-3
- Fix default file names format in batch scans (bug #56542).

* Tue Nov 20 2001 Tim Waugh <twaugh@redhat.com> 1.0.6-2
- Apply Maurice Hilarius's patch to avoid kill(-1,SIGTERM) (bug #56540).

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 1.0.6-1
- 1.0.6.

* Fri Jul 20 2001 Florian La Roche <Florian.LaRoche@redhat.de> 1.0.5-4
- exclude s390, s390x

* Tue Jul 17 2001 Preston Brown <pbrown@redhat.com> 1.0.5-3
- sane.png included

* Tue Jul 10 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-2
- sane-backends-devel provides sane-devel.

* Sun Jul  1 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-1
- 1.0.5.

* Wed Jun 20 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010620.0
- 2001-06-20 CVS update.  PreReq /bin/cat, /bin/rm.

* Mon Jun 11 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010610
- 2001-06-10 CVS snapshot.  umax_pp update from CVS again to fix more
  build problems.

* Sun Jun  3 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010603.1000
- 2001-06-03 CVS snapshot (10:00).  Fixes umax_pp build problems.

* Sat Jun  2 2001 Tim Waugh <twaugh@redhat.com> 1.0.5-0.20010530
- sane-backends (sane-frontends is in a separate package now).
- 2001-05-30 CVS snapshot.
- include.patch no longer needed.
- sg3timeout.patch no longer needed.

* Mon Jan 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.3-10
- Fix up the libtool config file /usr/lib/libsane.la
  kscan should build now. ;)

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Increase timeout for SCSI commands sent via sg driver version 3
  (bug #23447)

* Mon Dec 25 2000 Matt Wilson <msw@redhat.com>
- rebuilt against gimp 1.2.0

* Thu Dec 21 2000 Matt Wilson <msw@redhat.com>
- rebuilt against gimp 1.1.32
- use -DGIMP_ENABLE_COMPAT_CRUFT=1 to build with compat macros

* Mon Dec 18 2000 Matt Wilson <msw@redhat.com>
- rebuilt against gimp 1.1.30

* Fri Dec  1 2000 Tim Waugh <twaugh@redhat.com>
- Rebuild because of fileutils bug.

* Thu Oct 26 2000 Bill Nottingham <notting@redhat.com>
- fix provides for ia64/sparc64

* Tue Aug 29 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't include xscanimage desktop entry - it's a gimp
  plugin. Doh. (part of #17076)
- add tetex-latex as a build requirement

* Wed Aug 23 2000 Matt Wilson <msw@redhat.com>
- built against gimp 1.1.25

* Tue Aug 22 2000 Preston Brown <pbrown@redhat.com>
- 1.0.3 bugfix release (#16726)
- rev patch removed, no longer needed

* Tue Aug 15 2000 Than Ngo <than@redhat.com>
- add triggerpostun to fix removing path from ld.so.conf at update

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add Swedish and German translations to desktop file, Bug #15317

* Sun Jul 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- use mktemp in post and postun scripts
- fix incorrect usage of rev in backend/Makefile

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- workarounds for weird bug (all so-files had names with "s="
  - except for sparc which has just "=" and IA64 which works)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul  3 2000 Matt Wilson <msw@redhat.com>
- rebuilt against gimp-1.1.24

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths
- work around ICE on intel.  FIX ME!

* Mon May 22 2000 Tim Powers <timp@redhat.com>
-  rebuilt w/ glibc-2.1.90

* Thu May 18 2000 Tim Powers <timp@redhat.com>
- updated to 1.0.2

* Wed Jul 21 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Tue May 11 1999 Bill Nottingham <notting@redhat.com>
- make it play nice with xsane, add ld.so.conf entries

* Wed Apr 21 1999 Bill Nottingham <notting@redhat.com>
- update to 1.0.1

* Tue Oct 13 1998 Michael Maher <mike@redhat.com>
- updated package

* Thu May 21 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 0.73

* Tue Jan 27 1998 Otto Hammersmith <otto@redhat.com>
- umax drivers were missing from the file list.

* Sun Dec  7 1997 Otto Hammersmith <otto@redhat.com>
- added wmconfig
- fixed library problem

* Tue Dec  2 1997 Otto Hammersmith <otto@redhat.com>
- added changelog
- got newer package from Sane web site than our old powertools one
