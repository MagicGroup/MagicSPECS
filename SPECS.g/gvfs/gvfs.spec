Summary: Backends for the gio framework in GLib
Name: gvfs
Version: 1.15.1
Release: 3%{?dist}
License: GPLv3 and LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org

Source: http://download.gnome.org/sources/gvfs/1.15/gvfs-%{version}.tar.xz
BuildRequires: pkgconfig
BuildRequires: glib2-devel >= 2.33.12
# for post-install update-gio-modules and overall functionality
Requires: glib2 >= 2.33.12
BuildRequires: dbus-glib-devel
BuildRequires: /usr/bin/ssh
BuildRequires: libcdio-paranoia-devel
BuildRequires: libgudev1-devel
BuildRequires: libsoup-devel >= 2.34.0
BuildRequires: avahi-glib-devel >= 0.6
BuildRequires: libsecret-devel
BuildRequires: intltool
BuildRequires: gettext-devel
BuildRequires: libudisks2-devel
Requires: udisks2
BuildRequires: expat-devel
BuildRequires: libbluray-devel
BuildRequires: systemd-devel >= 44
BuildRequires: libxslt-devel
BuildRequires: gtk3-devel
BuildRequires: docbook-style-xsl

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

# The patch touches Makefile.am files:
BuildRequires: automake autoconf
BuildRequires: libtool

# http://bugzilla.gnome.org/show_bug.cgi?id=567235
Patch0: gvfs-archive-integration.patch

Obsoletes: gnome-mount <= 0.8
Obsoletes: gnome-mount-nautilus-properties <= 0.8

%description
The gvfs package provides backend implementations for the gio
framework in GLib. It includes ftp, sftp, cifs.


%package devel
Summary: Development files for gvfs
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The gvfs-devel package contains headers and other files that are
required to develop applications using gvfs.


%package fuse
Summary: FUSE support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: fuse-devel
Requires: fuse

%description fuse
This package provides support for applications not using gio
to access the gvfs filesystems.


%package smb
Summary: Windows fileshare support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libsmbclient-devel >= 3.2.0-1.pre2.8
BuildRequires: libtalloc-devel >= 1.3.0-0

%description smb
This package provides support for reading and writing files on windows
shares (SMB) to applications using gvfs.


%package archive
Summary: Archiving support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libarchive-devel >= libarchive-2.7.1-1

%description archive
This package provides support for accessing files inside Zip and Tar archives,
as well as ISO images, to applications using gvfs.


%ifnarch s390 s390x
%package obexftp
Summary: ObexFTP support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: obex-data-server >= 0.3.4-6
BuildRequires: bluez-libs-devel >= 3.12
Obsoletes: gnome-vfs2-obexftp <= 0.4

%description obexftp
This package provides support for reading files on Bluetooth mobile phones
and devices through ObexFTP to applications using gvfs.
%endif


%package gphoto2
Summary: gphoto2 support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libgphoto2-devel
BuildRequires: libusb-devel
BuildRequires: libexif-devel

%description gphoto2
This package provides support for reading and writing files on
PTP based cameras (Picture Transfer Protocol) and MTP based
media players (Media Transfer Protocol) to applications using gvfs.


%ifnarch s390 s390x
%package afc
Summary: AFC support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: usbmuxd
BuildRequires: libimobiledevice-devel >= 0.9.7

%description afc
This package provides support for reading files on mobile devices
including phones and music players to applications using gvfs.
%endif


%package afp
Summary: AFP support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libgcrypt-devel >= 1.2.2
# this should ensure having this new subpackage installed on upgrade from older versions
Obsoletes: %{name} < 1.9.4-1

%description afp
This package provides support for reading and writing files on
Mac OS X and original Mac OS network shares via Apple Filing Protocol
to applications using gvfs.


%prep
%setup -q
%patch0 -p1 -b .archive-integration

%build
# Needed for gvfs-0.2.1-archive-integration.patch
libtoolize --force  || :
aclocal  || :
autoheader  || :
automake  || :
autoconf  || :

%configure \
        --disable-hal \
        --disable-gdu \
        --enable-udisks2 \
        --enable-keyring
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

# trashlib is GPLv3, include the license
cp -p daemon/trashlib/COPYING COPYING.GPL3

%find_lang gvfs

%post
/sbin/ldconfig
# Reload .mount files:
killall -USR1 gvfsd >&/dev/null || :
update-desktop-database &> /dev/null || :
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


# Reload .mount files when single subpackage is installed:
%post smb
killall -USR1 gvfsd >&/dev/null || :
%post archive
killall -USR1 gvfsd >&/dev/null || :
%post gphoto2
killall -USR1 gvfsd >&/dev/null || :
%ifnarch s390 s390x
%post obexftp
killall -USR1 gvfsd >&/dev/null || :
%post afc
killall -USR1 gvfsd >&/dev/null || :
%endif

%files -f gvfs.lang
%doc AUTHORS COPYING COPYING.GPL3 NEWS README
%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount
%{_datadir}/gvfs/mounts/cdda.mount
%{_datadir}/gvfs/mounts/computer.mount
%{_datadir}/gvfs/mounts/dav.mount
%{_datadir}/gvfs/mounts/dav+sd.mount
%{_datadir}/gvfs/mounts/http.mount
%{_datadir}/gvfs/mounts/localtest.mount
%{_datadir}/gvfs/mounts/burn.mount
%{_datadir}/gvfs/mounts/dns-sd.mount
%{_datadir}/gvfs/mounts/network.mount
%{_datadir}/gvfs/mounts/ftp.mount
%{_datadir}/gvfs/mounts/recent.mount
%{_datadir}/dbus-1/services/org.gtk.Private.UDisks2VolumeMonitor.service
%{_datadir}/dbus-1/services/gvfs-daemon.service
%{_datadir}/dbus-1/services/gvfs-metadata.service
%{_datadir}/gvfs/remote-volume-monitors/udisks2.monitor
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.xml
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gvfs
%{_libdir}/libgvfscommon.so.*
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
%{_libexecdir}/gvfsd
%{_libexecdir}/gvfsd-ftp
%{_libexecdir}/gvfsd-sftp
%{_libexecdir}/gvfsd-trash
%{_libexecdir}/gvfsd-cdda
%{_libexecdir}/gvfsd-computer
%{_libexecdir}/gvfsd-dav
%{_libexecdir}/gvfsd-http
%{_libexecdir}/gvfsd-localtest
%{_libexecdir}/gvfsd-burn
%{_libexecdir}/gvfsd-dnssd
%{_libexecdir}/gvfsd-network
%{_libexecdir}/gvfsd-metadata
%{_libexecdir}/gvfs-udisks2-volume-monitor
%{_libexecdir}/gvfsd-recent
%{_bindir}/gvfs-cat
%{_bindir}/gvfs-copy
%{_bindir}/gvfs-info
%{_bindir}/gvfs-less
%{_bindir}/gvfs-ls
%{_bindir}/gvfs-mime
%{_bindir}/gvfs-mkdir
%{_bindir}/gvfs-monitor-dir
%{_bindir}/gvfs-monitor-file
%{_bindir}/gvfs-mount
%{_bindir}/gvfs-move
%{_bindir}/gvfs-open
%{_bindir}/gvfs-rename
%{_bindir}/gvfs-rm
%{_bindir}/gvfs-save
%{_bindir}/gvfs-trash
%{_bindir}/gvfs-tree
%{_bindir}/gvfs-set-attribute
%doc %{_mandir}/man1/gvfs-*
%doc %{_mandir}/man1/gvfsd.1.gz
%doc %{_mandir}/man1/gvfsd-metadata.1.gz
%doc %{_mandir}/man7/gvfs.7.gz

%files devel
%dir %{_includedir}/gvfs-client
%dir %{_includedir}/gvfs-client/gvfs
%{_includedir}/gvfs-client/gvfs/gvfsurimapper.h
%{_includedir}/gvfs-client/gvfs/gvfsuriutils.h
%{_libdir}/libgvfscommon.so


%files fuse
%{_libexecdir}/gvfsd-fuse
%doc %{_mandir}/man1/gvfsd-fuse.1.gz

%files smb
%{_libexecdir}/gvfsd-smb
%{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount


%files archive
%{_datadir}/applications/mount-archive.desktop
%{_libexecdir}/gvfsd-archive
%{_datadir}/gvfs/mounts/archive.mount


%files gphoto2
%{_libexecdir}/gvfsd-gphoto2
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_libexecdir}/gvfs-gphoto2-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor

%ifnarch s390 s390x
%files obexftp
%{_libexecdir}/gvfsd-obexftp
%{_datadir}/gvfs/mounts/obexftp.mount

%files afc
%{_libexecdir}/gvfsd-afc
%{_datadir}/gvfs/mounts/afc.mount
%{_libexecdir}/gvfs-afc-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.Private.AfcVolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/afc.monitor
%endif

%files afp
%{_libexecdir}/gvfsd-afp
%{_libexecdir}/gvfsd-afp-browse
%{_datadir}/gvfs/mounts/afp.mount
%{_datadir}/gvfs/mounts/afp-browse.mount

%changelog
* Mon Jan 07 2013 Adrian Reber <adrian@lisas.de> - 1.15.1-3
- Rebuilt for libcdio-0.90

* Wed Dec 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.15.1-2
- Rebuilt for new udisks

* Tue Dec 18 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Fri Dec  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.15.0-3
- Enable verbose build messages
- Remove deprecated Encoding key from mount-archive.desktop

* Tue Nov  6 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.15.0-2
- Clarify licensing
- Explicitly disable HAL

* Mon Oct 29 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.15.0-1
- Update to 1.15.0

* Tue Sep 25 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Tue Sep 18 2012 Matthias Clasen <mclasen@redhat.com> - 1.13.9-1
- Update to 1.13.9

* Wed Sep  5 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.8-1
- Update to 1.13.8

* Wed Aug 29 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.7-3
- Bring archive mounter back

* Mon Aug 27 2012 Cosimo Cecchi <cosimoc@redhat.com> - 1.13.7-2
- Make sure keyring integration is enabled

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.13.7-1
- Update to 1.13.7

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 1.13.4-1
- Update to 1.13.4

* Tue Aug  7 2012 Jindrich Novy <jnovy@redhat.com> - 1.13.3-4
- add BR: docbook-style-xsl so that gvfs actually builds

* Sun Aug  5 2012 Jindrich Novy <jnovy@redhat.com> - 1.13.3-3
- add patch to fix gvfs build against libgphoto2 (inspired by SUSE)

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.3-1
- Update to 1.13.3

* Mon Jul 16 2012 Nils Philippsen <nils@redhat.com> - 1.13.2-2
- rebuild for new libgphoto2

* Tue Jun 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.2-1
- Update to 1.13.2

* Mon Jun  4 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.1-1
- Update to 1.13.1

* Wed May  2 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.13.0-1
- Update to 1.13.0

* Fri Apr 27 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.12.2-1
- Update to 1.12.2
- Backport multiseat patches from master

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.1-3
- Silence rpm scriptlet output

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.1-2
- Rebuild again for new libimobiledevice and usbmuxd

* Tue Apr 17 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Thu Apr 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.12.0-2
- Rebuild for new libimobiledevice and usbmuxd

* Mon Mar 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Tue Mar 20 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.5-1
- Update to 1.11.5

* Fri Feb 24 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.4-1
- Update to 1.11.4

* Tue Feb  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.3-1
- Update to 1.11.3

* Fri Feb  3 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.3-0.4.20120120
- Exclude the obexftp package from s390 builds

* Wed Jan 25 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.3-0.3.20120120
- Rebuilt for new libarchive

* Tue Jan 24 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.3-0.2.20120120
- Add udisks2 runtime Requires

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 1.11.3-0.1.20120120-1
- Prelease that works with udisks2

* Wed Jan 18 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Tue Dec 13 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.11.0-5
- Rebuilt for new libbluray

* Sun Nov 20 2011 Adrian Reber <adrian@lisas.de> - 1.11.0-4
- Rebuild for libcdio-0.83

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.11.0-3
- Rebuild for new libarchive

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2
- Rebuilt for glibc bug#747377

* Wed Oct 26 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Mon Oct 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 1.9.5-1
- Update to 1.9.5

* Tue Aug 30 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.9.4-1
- Update to 1.9.4
- New AFP backend in separate subpackage

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 1.9.3-1
- Update to 1.9.3
- Drop obsolete patches
- Clean up spec a bit

* Wed Jul 27 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.9.2-1
- Update to 1.9.2
- Enable real statfs calls in the fuse daemon

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Mon May 09 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.9.0-1
- Update to 1.9.0

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 1.8.1-2
- Update gsettings scriptlet

* Tue Apr 26 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Fri Apr 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.8.0-3
- Build without HAL -> expect obexftp breakage.

* Mon Apr 18 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.8.0-2
- Fix threadsafety of closing channels
- Fix d-bus messages leaks
- Fix /dev symlink checks in gdu volume monitor

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Sun Dec 26 2010 Bastien Nocera <bnocera@redhat.com> 1.7.1-1
- Update to 1.7.1

* Thu Dec  2 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 1.6.5-1
- Update to 1.6.5
- Drop upstreamed patches

* Mon Nov  1 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.4-4
- Use correct "usb:" address for GPhoto mounts with gudev (#642836)

* Wed Oct 13 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.4-3
- FUSE: Add O_TRUNC support for open()

* Mon Oct  4 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.4-2
- Fix sftp poll timeout

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 1.6.4-1
- Update to 1.6.4

* Wed Sep  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.3-3
- Fix smb daemons deadlock due to GConf initialization

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> - 1.6.3-2
- s390(x) machines can't connect mobile phones or players

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 1.6.3-1
- Update to 1.6.3

* Thu May 27 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Tue May  4 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.1-3
- Fix Nautilus 100% CPU after trashing a file with an emblem (#584784)

* Mon Apr 26 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.1-2
- Explicitly require minimal glib2 version (#585912)

* Mon Apr 26 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 1.6.0-2
- Use update-gio-modules

* Mon Mar 29 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Mon Mar 22 2010 Bastien Nocera <bnocera@redhat.com> 1.5.5-3
- Fix build with new libimobiledevice
- Don't mount both gphoto and AFC mounts on AFC devices

* Sun Mar 21 2010 Peter Robinson <pbrobinson@gmail.com> 1.5.5-2
- Rebuild for new stable libimobiledevice 

* Mon Mar  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.5-1
- Update to 1.5.5

* Thu Feb 25 2010 Matthias Clasen <mclasen@redhat.com> - 1.5.4-2
- Re-add missing service files

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Mon Feb 15 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.3-2
- sftp: fix crash on unmount

* Tue Feb  9 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.3-1
- Update to 1.5.3

* Mon Feb  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.2-5
- ftp: backport several PASV/EPSV fixes from master (#542205, #555033)

* Fri Feb  5 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.2-4
- AFC: Use new libimobiledevice library

* Tue Jan 26 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.2-3
- Fix AFC build against new libiphone

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 1.5.2-2
- Update the GIO module cache

* Mon Jan 25 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Fri Jan 22 2010 Adrian Reber <adrian@lisas.de> - 1.5.1-6
- Rebuild for libcdio-0.82

* Mon Jan 18 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-5
- Avoid crash on race to mount gvfstrash (#555337)
- Nuke HAL volume monitor

* Tue Jan 12 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-4
- Don't leak mount job operation (#552842)
- Recognize gphoto2 cameras which don't implement get storageinfo (#552856)
- ObexFTP: Use a private D-Bus connection for obex-data-server (#539347)

* Tue Dec 15 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-3
- Rebuilt against new libiphone

* Mon Nov 30 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-2
- Metadata fixes
- SMB: Fix free space calculation for older samba servers
- fuse: Fix setting timestamps

* Wed Nov 18 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-1
- Update to 1.5.1
- AFC: temporarily disable setting file modification times

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> 1.4.1-6
- Add obsoletes for gnome-mount

* Thu Nov 12 2009 Bastien Nocera <bnocera@redhat.com> 1.4.1-5
- Add obsoletes for gnome-vfs2-obexftp

* Tue Nov 10 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.1-4
- SMB: Support querying filesystem size and free space

* Tue Nov  3 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.1-3
- gdu-volume-monitor: don't crash on NULL devices (#529982)

* Mon Nov  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.1-2
- Reload .mount files when single package is installed

* Tue Oct 20 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Fri Oct 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.0-7
- HTTP: Support g_file_input_stream_query_info()
- HTTP: Use libsoup header parsing function
- Set correct MIME type for MTP music players

* Wed Oct 14 2009 Bastien Nocera <bnocera@redhat.com> 1.4.0-6
- Fix crasher in ObexFTP (#528181)

* Fri Oct  9 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.0-5
- Don't always overwrite on trash restore
- Separate "Safely Remove Drive" from "Eject"
- Don't advertise can_poll for drives not using removable media
- Disallow mounting empty drives
- Disallow ejecting empty drives
- Silently drop eject error messages when detaching drive

* Thu Oct  8 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.0-4
- Fix Nautilus not displaying friendly icons for SSH-connected system (#526892)
- Actually apply the logical partitions patch

* Thu Oct  1 2009 Matthias Clasen <mclasen@redhat.com> - 1.4.0-3
- Consider logical partitions when deciding if a drive should be ignored

* Tue Sep 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.4.0-2
- Fix the lack of icons in the http backend

* Mon Sep 21 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.3.6-2
- Rebuilt with new fuse

* Mon Sep  7 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.6-1
- Update to 1.3.6

* Wed Aug 26 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.5-2
- Don't mount interactively during login

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.5-1
- Update to 1.3.5

* Mon Aug 17 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.4-7
- Fix Nautilus can't create "untitled folder" on sftp mounts (#512611)

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 1.3.4-6
- Update AFC patch

* Thu Aug 13 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.4-5
- More complete fix for DAV mount path prefix issues

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 1.3.4-4
- Fix crash on startup for the afc volume monitor

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 1.3.4-3
- libgudev-devel is required for the gphoto2 monitor

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 1.3.4-2
- Add AFC backend

* Mon Aug 10 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Fri Aug  7 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.3-3
- Fix bad mount prefix stripping (part of #509612)
- Fix gvfsd-sftp segfault when asking a question
- Enable tar+xz in the archive mounter

* Tue Aug  4 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.3-2
- Fix gedit crashed with SEGV in strlen()
- Fix SMB protocol not handled when opening from a bookmark (#509832)

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Mon Jul 27 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.2-3
- Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Drop upstreamed patches

* Mon Jun 22 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.3.1-2
- Bump version requirements
- Backport FTP and Computer backend patches from master

* Mon Jun 15 2009 Matthias Clasen <mclasen@redhat.com> - 1.3.1-1
- Update to 1.3.1
- Drop obsolete patches

* Fri Jun 12 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.2.3-3
- Move bash-completion out of profile.d (#466883)

* Mon Jun  8 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.2.3-2
- SFTP: Increase timeout (#504339)

* Mon May 18 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.2.3-1
- Update to 1.2.3
- Prevent deadlocks in dnssd resolver (#497631)

* Tue May 12 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.2.2-5
- Require separate libtalloc to fix libsmbclient
- Ref the infos in next_files_finish (gnome #582195)
- FTP: parse file sizes > 4GB correctly (#499286)
- CDDA: allow query well-formed filenames only (#499266)

* Sat May 02 2009 David Zeuthen <davidz@redhat.com> - 1.2.2-4
- Don't show drives that are supposed to be hidden (#498649)
- Only automount if media or drive was just inserted - this fixes
  a problem with spurious automounts when partitioning/formatting

* Wed Apr 15 2009 David Zeuthen <davidz@redhat.com> - 1.2.2-3
- Sync with the gdu-volume-monitor branch

* Mon Apr 13 2009 Alexander Larsson <alexl@redhat.com> - 1.2.2-2
- Add ssh-auth-sock patch from svn

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Allow eject even on non-ejectable devices

* Sat Apr 11 2009 David Zeuthen <davidz@redhat.com> - 1.2.1-5
- Don't show drives in computer:/// if media is available but
  no volumes are recognized (#495152)

* Sat Apr 11 2009 Matthias Clasen <mclasen@redhat.com> - 1.2.1-4
- No need for bash completion to be executable

* Thu Apr  9 2009 David Zeuthen <davidz@redhat.com> - 1.2.1-3
- Clean up gdu patches and bump BR for gdu to 0.3
- Avoiding showing volume for ignored mounts (#495033)

* Thu Apr  9 2009 David Zeuthen <davidz@redhat.com> - 1.2.1-2
- Avoid automounting device-mapper devices and similar (#494144)

* Thu Apr  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Wed Mar 18 2009 David Zeuthen <davidz@redhat.com> - 1.2.0-2
- GNOME #575728 - crash in Open Folder: mounting a crypto volume

* Mon Mar 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Wed Mar 11 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.8-2
- Fix 100% cpu usage when connecting to a ssh key and denying key access
- Fix monitors leak

* Tue Mar 10 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.8-1
- Update to 1.1.8

* Mon Mar  9 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.7-5
- Expose device file attribute for all items in computer://

* Fri Mar  6 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.7-4
- Fix volume lists not filled correctly

* Wed Mar  4 2009 David Zeuthen <davidz@redhat.com> - 1.1.7-3
- Update GVfs gdu patch to fix mount detection confusion (#488399)

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.1.7-2
- Port to DeviceKit-disks

* Mon Mar  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.7-1
- Update to 1.1.7

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.6-1
- Update to 1.1.6

* Mon Feb  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.5-1
- Update to 1.1.5

* Wed Jan 28 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-2
- ObexFTP write support

* Tue Jan 20 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.4-1
- Update to 1.1.4

* Tue Jan 13 2009 Adrian Reber <adrian@lisas.de> - 1.1.3-4
- Rebuild for libcdio-0.81

* Mon Jan 12 2009 Matthias Clasen  <mclasen@redhat.com> - 1.1.3-3
- Fix dav+sd.mount

* Fri Jan  9 2009 Matthias Clasen  <mclasen@redhat.com> - 1.1.3-2
- Support moving files in the burn backend

* Tue Jan  6 2009 Tomas Bzatek <tbzatek@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Wed Dec 17 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.1.2-2
- Update the smb-browse auth patch

* Tue Dec 16 2008 Matthias Clasen  <mclasen@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Fri Dec 12 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.1.1-5
- FTP: Fix PASV connections

* Tue Dec  9 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.1.1-4
- Add support for .tar.lzma archives in archive mounter

* Fri Dec  5 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.1.1-3
- Added experimental smb-browse auth patch

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 1.1.1-2
- Update file lists to include the dav+sd backend

* Tue Dec  2 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Mon Dec  1 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Fri Nov  7 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.0.2-4
- SMB: timestamp setting support (#461505)

* Tue Nov  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.0.2-3
- Return an empty array on success when no content type
  matches (#468946)

* Fri Oct 24 2008 Alexander Larsson <alexl@redhat.com> - 1.0.2-2
- Don't return generic fallback icons for files,
  as this means custom mimetypes don't work (from svn)

* Mon Oct 20 2008 Tomas Bzatek <tbzatek@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Tue Oct  7 2008 Tomas Bzatek <tbzatek@redhat.com>  - 1.0.1-5
- Don't make warnings fatal (resolves #465693)

* Wed Oct  1 2008 David Zeuthen <davidz@redhat.com>  - 1.0.1-4
- Add patch for reverse mapping FUSE paths (bgo #530654)

* Mon Sep 29 2008 Matthias Clasen <mclasen@redhat.com>  - 1.0.1-3
- Fix mounting

* Mon Sep 29 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.1-2
- Update obexftp patch from upstream

* Wed Sep 24 2008 Matthias Clasen <mclasen@redhat.com>  - 1.0.1-1
- Update to 1.0.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com>  - 1.0.0-2
- Update to 1.0.0

* Fri Sep 19 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.8-6
- Update patch for missing file

* Fri Sep 19 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.8-5
- Updated patch, fixed deadlock whilst mounting

* Wed Sep 17 2008 Tomas Bzatek <tbzatek@redhat.com>  - 0.99.8-4
- Actually apply the kerberos patch

* Tue Sep 16 2008 Tomas Bzatek <tbzatek@redhat.com>  - 0.99.8-3
- SMB: Fix kerberos authentication

* Mon Sep 15 2008 Matthias Clasen <mclasen@redhat.com>  - 0.99.8-2
- Update to 0.99.8

* Mon Sep 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.7.1-4
- Update for BlueZ and obex-data-server D-Bus API changes

* Thu Sep 11 2008 Matthias Clasen <mclasen@redhat.com>  - 0.99.7.1-3
- Rebuild 

* Tue Sep 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.7.1-2
- Somebody made the build system be obnoxious and point out my
  errors in obvious ways

* Tue Sep 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.7.1-1
- Update to 0.99.7.1

* Tue Sep  2 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.99.6-1
- Update to 0.99.6

* Thu Aug 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.99.5-3
- Add a comma

* Wed Aug 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.99.5-2
- Update some descriptions

* Wed Aug 20 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.99.5-1
- Update to 0.99.5

* Mon Aug  4 2008 Matthias Clasen  <mclasen@redhat.com> - 0.99.4-1
- Update to 0.99.4

* Sun Jul 27 2008 Matthias Clasen  <mclasen@redhat.com> - 0.99.3-2
- Use standard icon names

* Wed Jul 23 2008 Matthias Clasen  <mclasen@redhat.com> - 0.99.3-1
- Update to 0.99.3

* Tue Jul 22 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.99.2-1
- Update to 0.99.2
- Split out backends to separate packages

* Tue Jun 24 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.99.1-3
- gvfsd-trash: Skip autofs mounts

* Thu Jun 12 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.99.1-2
- Fix transfer of whole directories from FTP (#448560)

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 0.99.1-1
- Update to 0.99.1

* Tue May 27 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-10
- Add application/zip to the supported mime types for the archive
  backend (launchpad #211697)

* Sun Apr 19 2008 David Zeuthen <davidz@redhat.com> - 0.2.3-9
- Ensure archive mounts are read-only and turn on thumbnailing on them
- Update fuse threading patch

* Fri Apr 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-8
- Fix thread-safety issues in gvfs-fuse-daemon
- Prevent dbus from shutting us down unexpectedly

* Thu Apr 17 2008 David Zeuthen <davidz@redhat.com> - 0.2.3-7
- Put X-Gnome-Vfs-System=gio into mount-archarive.desktop (See #442835)

* Wed Apr 16 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-6
- Reenable gphoto automounting 
- Support unmounting all mounts for a scheme

* Wed Apr 16 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-5
- Fix hangs when unmounting gphoto mounts

* Wed Apr 16 2008 David Zeuthen <davidz@redhat.com> - 0.2.3-4
- Only show mounts in /media and inside $HOME (#442189)

* Mon Apr 14 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-3
- Fix a bug that causes application crashes (#441084)

* Fri Apr 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-2
- Fix a crash of the fuse daemon on 64bit

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Fri Mar 28 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Tue Mar 25 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.2.1-4
- Moved fuse stuff to a dedicated package

* Thu Mar 20 2008 Alexander Larsson <alexl@redhat.com> - 0.2.1-3
- Add patch with simple archive backend UI integration

* Tue Mar 19 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.2.1-2
- Added libarchive dependency for archive backend
- Require new libsmbclient in order to get smb backend working again

* Tue Mar 18 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.2.1-1
- Update to 0.2.1 (archive backend temporarily disabled)

* Mon Mar 17 2008 Matthias Clasen  <mclasen@redhat.com> - 0.2.0.1-2
- Silence %%post

* Mon Mar 10 2008 Matthias Clasen  <mclasen@redhat.com> - 0.2.0.1-1
- Update to 0.2.0.1

* Thu Mar  6 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.1.11-2
- Add patch that fixes a deadlock when foreign volume is removed

* Tue Mar  4 2008 Matthias Clasen  <mclasen@redhat.com> - 0.1.11-1
- Update to 0.1.11

* Tue Mar 04 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-1
- Update to 0.1.10

* Mon Feb 25 2008 Alexander Larsson <alexl@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Thu Feb 14 2008 Alexander Larsson <alexl@redhat.com> - 0.1.7-3
- Add patch that fixes a smb bug that can cause short reads when copying files

* Tue Feb 12 2008 Alexander Larsson <alexl@redhat.com> - 0.1.7-2
- Fix double free in hal volume monitor
- Ensure gconf module is built by adding build dep

* Mon Feb 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.7-1
- Update to 0.1.7

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.5-1
- Update to 0.1.5
- Reenable http/dav 

* Mon Jan 21 2008 Alexander Larsson <alexl@redhat.com> - 0.1.4-2 
- Remove the http/dav stuff for now, as we don't have the latest libsoup

* Mon Jan 21 2008 Alexander Larsson <alexl@redhat.com> - 0.1.4-1
- Update to 0.1.4
- Send USR1 in post to reload config

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> 0.1.2-1
- Update to 0.1.2

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> 0.1.1-1
- Update to 0.1.1

* Thu Dec 20 2007 Matthias Clasen <mclasen@redhat.com> 0.1.0-1
- Initial packaging
