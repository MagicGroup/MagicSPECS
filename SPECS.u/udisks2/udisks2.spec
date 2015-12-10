%define glib2_version                   2.31.13
%define gobject_introspection_version   1.30.0
%define polkit_version                  0.101
%define systemd_version                 184
%define libatasmart_version             0.12
%define dbus_version                    1.4.0

Summary: Disk Manager
Summary(zh_CN.UTF-8): 磁盘管理程序
Name: udisks2
Version:	2.1.6
Release:	3%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.freedesktop.org/wiki/Software/udisks
Source0: http://udisks.freedesktop.org/releases/udisks-%{version}.tar.bz2

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: intltool
BuildRequires: libatasmart-devel >= %{libatasmart_version}
BuildRequires: libgudev1-devel >= %{systemd_version}
BuildRequires: gtk-doc
BuildRequires: systemd-devel
BuildRequires: libacl-devel

# needed to pull in the system bus daemon
Requires: dbus >= %{dbus_version}
# needed to pull in the udev daemon
Requires: systemd >= %{systemd_version}
# we need at least this version for bugfixes / features etc.
Requires: libatasmart >= %{libatasmart_version}
# for mount, umount, mkswap
Requires: util-linux
# for mkfs.ext3, mkfs.ext3, e2label
Requires: e2fsprogs
# for mkfs.xfs, xfs_admin
Requires: xfsprogs
# for mkfs.vfat
Requires: dosfstools
# for partitioning
Requires: parted
Requires: gdisk
# for LUKS devices
Requires: cryptsetup-luks
# for ejecting removable disks
Requires: eject

# for MD-RAID
Requires: mdadm

Requires: libudisks2 = %{version}-%{release}

# for mkntfs (not available on rhel or on ppc/ppc64)
%if ! 0%{?rhel}
%ifnarch ppc ppc64
Requires: ntfsprogs
%endif
%endif

# for /proc/self/mountinfo, only available in 2.6.26 or higher
Conflicts: kernel < 2.6.26


%description
udisks provides a daemon, D-Bus API and command line tools for
managing disks and storage devices. This package is for the udisks 2.x
series.

%description -l zh_CN.UTF-8
磁盘管理服务。

%package -n libudisks2
Summary: Dynamic library to access the udisks daemon
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+

%description -n libudisks2
This package contains the dynamic library libudisks2, which provides
access to the udisks daemon. This package is for the udisks 2.x
series.

%description -n libudisks2 -l zh_CN.UTF-8
%{name} 的运行库。

%package -n libudisks2-devel
Summary: Development files for libudisks2
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libudisks2 = %{version}-%{release}
Requires: pkgconfig
License: LGPLv2+

%description -n libudisks2-devel
This package contains the development files for the library
libudisks2, a dynamic library, which provides access to the udisks
daemon. This package is for the udisks 2.x series.

%description -n libudisks2-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n udisks-%{version}

%build
# we can't use _hardened_build here, see
# https://bugzilla.redhat.com/show_bug.cgi?id=892837
export CFLAGS='-fPIC %optflags'
export LDFLAGS='-pie -Wl,-z,now -Wl,-z,relro'
%configure --enable-gtk-doc
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh
%find_lang %{name} || :

%post -n libudisks2 -p /sbin/ldconfig

%postun -n libudisks2 -p /sbin/ldconfig

%files -f %{name}.lang
%doc README AUTHORS NEWS COPYING HACKING

%dir %{_sysconfdir}/udisks2

%{_sysconfdir}/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{_datadir}/bash-completion/completions/udisksctl
%{_prefix}/lib/systemd/system/udisks2.service
%{_prefix}/lib/udev/rules.d/80-udisks2.rules
%{_sbindir}/umount.udisks2

%dir %{_prefix}/libexec/udisks2
%{_prefix}/libexec/udisks2/udisksd

%{_bindir}/udisksctl

%{_mandir}/man1/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/org.freedesktop.udisks2.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service

# Permissions for local state data are 0700 to avoid leaking information
# about e.g. mounts to unprivileged users
%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks2

%files -n libudisks2
%{_libdir}/libudisks2.so.*
%{_libdir}/girepository-1.0/UDisks-2.0.typelib

%files -n libudisks2-devel
%{_libdir}/libudisks2.so
%dir %{_includedir}/udisks2
%dir %{_includedir}/udisks2/udisks
%{_includedir}/udisks2/udisks/*.h
%{_datadir}/gir-1.0/UDisks-2.0.gir
%dir %{_datadir}/gtk-doc/html/udisks2
%{_datadir}/gtk-doc/html/udisks2/*
%{_libdir}/pkgconfig/udisks2.pc

# Note: please don't forget the %{?dist} in the changelog. Thanks
%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2.1.6-3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2.1.6-2
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 2.1.6-1
- 更新到 2.1.6

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 2.1.3-3
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 2.1.3-2
- 为 Magic 3.0 重建

* Thu Mar 27 2014 Tomas Bzatek <tbzatek@redhat.com> - 2.1.3-1%{?dist}
- Update to 2.1.3

* Mon Mar 10 2014 Jan Safranek <jsafrane@redhat.com>- 2.1.2-2%{?dist}
- Fix CVE-2014-0004: stack-based buffer overflow when handling long path names
  (#1074459)

* Wed Jan 15 2014 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1%{?dist}
- Update to 2.1.2

* Wed Aug 21 2013 Tomas Bzatek <tbzatek@redhat.com> - 2.1.1-1%{?dist}
- Update to 2.1.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Tomas Bzatek <tbzatek@redhat.com> - 2.1.0-2%{?dist}
- Fix firewire drives identification (#909010)

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Matthias Clasen <mclasen@redhat.com> - 2.0.91-2%{?dist}
- Hardened build

* Mon Jan 07 2013 David Zeuthen <davidz@redhat.com> - 2.0.91-1%{?dist}
- Update to release 2.0.91

* Tue Dec 18 2012 David Zeuthen <davidz@redhat.com> - 2.0.90-1%{?dist}
- Update to release 2.0.90

* Fri Oct 02 2012 David Zeuthen <davidz@redhat.com> - 2.0.0-1%{?dist}
- Update to release 2.0.0

* Fri Jul 27 2012 David Zeuthen <davidz@redhat.com> - 1.99.0-1%{?dist}
- Update to release 1.99.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 David Zeuthen <davidz@redhat.com> - 1.98.0-1%{?dist}
- Update to release 1.98.0

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 1.97.0-4
- rebuild for libudev1

* Tue May 22 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.97.0-3
- Add upstream patch to fix issue with rootfs being on a bound mount

* Fri May 18 2012 Matthias Clasen <mclasen@redhat.com> - 1.97.0-2%{?dist}
- Add a Requires for eject (#810882)

* Wed May 09 2012 David Zeuthen <davidz@redhat.com> - 1.97.0-1%{?dist}
- Update to release 1.97.0

* Thu May 03 2012 David Zeuthen <davidz@redhat.com> - 1.96.0-2%{?dist}
- Include patch so Fedora Live media is shown

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.96.0-1%{?dist}
- Update to release 1.96.0

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-3%{?dist}
- BR: gnome-common

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-2%{?dist}
- Make daemon actually link with libsystemd-login

* Mon Apr 30 2012 David Zeuthen <davidz@redhat.com> - 1.95.0-1%{?dist}
- Update to release 1.95.0

* Tue Apr 10 2012 David Zeuthen <davidz@redhat.com> - 1.94.0-1%{?dist}
- Update to release 1.94.0

* Tue Apr 03 2012 David Zeuthen <davidz@redhat.com> - 1.93.0-2%{?dist}
- Don't inadvertently unmount large block devices (fdo #48155)

* Mon Mar 05 2012 David Zeuthen <davidz@redhat.com> - 1.93.0-1%{?dist}
- Update to release 1.93.0

* Thu Feb 23 2012 David Zeuthen <davidz@redhat.com> - 1.92.0-2%{?dist}
- Fix build

* Thu Feb 23 2012 David Zeuthen <davidz@redhat.com> - 1.92.0-1%{?dist}
- Update to release 1.92.0

* Wed Feb 22 2012 David Zeuthen <davidz@redhat.com> - 1.91.0-2%{?dist}
- Avoid using $XDG_RUNTIME_DIR/media for now

* Mon Feb 06 2012 David Zeuthen <davidz@redhat.com> - 1.91.0-1%{?dist}
- Update to release 1.91.0

* Fri Jan 21 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-3%{?dist}
- Manually set PATH, if not set

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-2%{?dist}
- Rebuild

* Fri Jan 20 2012 David Zeuthen <davidz@redhat.com> - 1.90.0-1%{?dist}
- Update to release 1.90.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.90.0-0.git20111128.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 David Zeuthen <davidz@redhat.com> - 1.90.0-0.git20111128%{?dist}
- Updated for review comments (#756046)

* Mon Nov 22 2011 David Zeuthen <davidz@redhat.com> - 1.90.0-0.git20111122%{?dist}
- Initial packaging of udisks2
