%define po_package gnome-vfs-2.0

# don't use HAL from F-16 on
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%bcond_with hal
%else
%bcond_without hal
%endif

Summary: The GNOME virtual file-system libraries
Name: gnome-vfs2
Version: 2.24.4
Release: 10%{?dist}
License: LGPLv2+ and GPLv2+
# the daemon and the library are LGPLv2+
# the modules are LGPLv2+ and GPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/gnome-vfs
Source0: http://download.gnome.org/sources/gnome-vfs/2.24/gnome-vfs-%{version}.tar.bz2
URL: http://www.gnome.org/
Requires(post): GConf2 
Requires(pre): GConf2 
Requires(preun): GConf2 
BuildRequires: GConf2-devel 
BuildRequires: libxml2-devel, zlib-devel
BuildRequires: glib2-devel 
BuildRequires: popt, bzip2-devel, ORBit2-devel, openjade
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: autoconf
BuildRequires: gtk-doc 
BuildRequires: perl-XML-Parser 
BuildRequires: libsmbclient-devel 
BuildRequires: openssl-devel gamin-devel
BuildRequires: krb5-devel
BuildRequires: avahi-glib-devel 
%if %{with hal}
BuildRequires: hal-devel
%endif
BuildRequires: dbus-devel 
BuildRequires: dbus-glib-devel 
BuildRequires: gettext
BuildRequires: libacl-devel
BuildRequires: keyutils-libs-devel
# For gvfs-open
Requires: gvfs

Patch3: gnome-vfs-2.9.90-modules-conf.patch

# remove gnome-mime-data dependency
Patch4: gnome-vfs-2.24.1-disable-gnome-mime-data.patch

# CVE-2009-2473 neon, gnome-vfs2 embedded neon: billion laughs DoS attack
# https://bugzilla.redhat.com/show_bug.cgi?id=518215
Patch5: gnome-vfs-2.24.3-CVE-2009-2473.patch

# send to upstream
Patch101:	gnome-vfs-2.8.2-schema_about_for_upstream.patch

# Default
Patch104:	gnome-vfs-2.8.2-browser_default.patch

# Applied upstream.
# Patch201: gnome-vfs-2.8.1-console-mount-opt.patch

# RH bug #197868
Patch6: gnome-vfs-2.15.91-mailto-command.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=333041
# https://bugzilla.redhat.com/show_bug.cgi?id=335241
Patch300: gnome-vfs-2.20.0-ignore-certain-mountpoints.patch


# backported from upstream

# gnome-vfs-daemon exits on dbus, and constantly restarted causing dbus/hal to hog CPU
# https://bugzilla.redhat.com/show_bug.cgi?id=486286
Patch404: gnome-vfs-2.24.xx-utf8-mounts.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=435653
Patch405: 0001-Add-default-media-application-schema.patch

# from upstream
Patch7: gnome-vfs-2.24.5-file-method-chmod-flags.patch


%description
GNOME VFS is the GNOME virtual file system. It is the foundation of
the Nautilus file manager. It provides a modular architecture and
ships with several modules that implement support for file systems,
http, ftp, and others. It provides a URI-based API, backend
supporting asynchronous file operations, a MIME type manipulation
library, and other features.

%package devel
Summary: Libraries and include files for developing GNOME VFS applications
Group: Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries for writing
GNOME VFS modules and applications that use the GNOME VFS APIs.

%package smb
Summary: Windows fileshare support for gnome-vfs
Group: System Environment/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: libsmbclient

%description smb
This package provides support for reading and writing files on windows
shares (SMB) to applications using GNOME VFS.

%prep
%setup -q -n gnome-vfs-%{version} 

%patch3 -p1 -b .modules-conf
%patch4 -p1 -b .mime-data
%patch5 -p1 -b .CVE-2009-2473

%patch6 -p1 -b .mailto-command
%patch7 -p1 -b .file-method-chmod-flags

# send to upstream
%patch101 -p1 -b .schema_about

%patch104 -p1 -b .browser_default

%patch300 -p1 -b .ignore-certain-mount-points

%patch404 -p1 -b .utf8-mounts

%patch405 -p1 -b .default-media

# for patch 10 and 4
autoheader
autoconf

%build
if pkg-config openssl ; then
	CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
	LDFLAGS=`pkg-config --libs-only-L openssl`; export LDFLAGS
fi

CFLAGS="%optflags -fno-strict-aliasing" %configure \
    --with-samba-includes=/usr/include/samba-4.0 \
    --disable-gtk-doc \
%if %{with hal}
    --enable-hal \
%endif
    --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

# strip unneeded translations from .mo files
# ideally intltool (ha!) would do that for us
# http://bugzilla.gnome.org/show_bug.cgi?id=474987
cd po
grep -v ".*[.]desktop[.]in[.]in$\|.*[.]server[.]in[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --pot
PO_FAKE_DATE="2009-08-03 18:00+0200"   # fake this to be equal in every build
PO_FAKE_DATE_EXPR='\(.*POT-Creation-Date: *\)\(.*\)\(\\n.*\)'
sed --in-place "s/${PO_FAKE_DATE_EXPR}/\1${PO_FAKE_DATE}\3/" %{po_package}.pot
for p in *.po; do
  msgmerge $p %{po_package}.pot > $p.out
  msgfmt -o `basename $p .po`.gmo $p.out
done


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{po_package}


%post
/sbin/ldconfig
%gconf_schema_upgrade system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%pre
%gconf_schema_prepare system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%preun
%gconf_schema_remove system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%dir %{_sysconfdir}/gnome-vfs-2.0
%dir %{_sysconfdir}/gnome-vfs-2.0/modules
%config %{_sysconfdir}/gnome-vfs-2.0/modules/*.conf
%exclude %{_sysconfdir}/gnome-vfs-2.0/modules/smb-module.conf
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%exclude %{_libdir}/gnome-vfs-2.0/modules/libsmb.so
%{_libdir}/gnome-vfs-2.0/modules
%dir %{_libdir}/gnome-vfs-2.0
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/dbus-1/services/gnome-vfs-daemon.service

%files devel
%defattr(-, root, root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_libdir}/gnome-vfs-2.0/include
%{_includedir}/*
%{_datadir}/gtk-doc/html/gnome-vfs-2.0

%files smb
%defattr(-, root, root,-)
%{_libdir}/gnome-vfs-2.0/modules/libsmb.so
%config %{_sysconfdir}/gnome-vfs-2.0/modules/smb-module.conf

%changelog
* Mon Dec 10 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.24.4-10
- Compile with -fno-strict-aliasing
- Backport file-method chmod flags patch from upstream

* Wed Nov 28 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.24.4-9
- Rebuilt for bug 878494
- Fix build against samba4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 21 2011 Nils Philippsen <nils@redhat.com> - 2.24.4-6
- build without HAL from F-16/EL-7 on

* Tue Apr 12 2011 Christopher Aillon <caillon@redhat.com> - 2.24.4-5
- Change the default http,https handler to gvfs-open

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.24.4-3
- Gconf2 scriptlet accepts schema file names without file extension.

* Fri Oct 15 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.24.4-2
- Merge-review cleanup (#225843)

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.4-1
- Update to 2.24.4

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Fri Mar 12 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.24.2-4
- ftp: Don't crash if we get a NULL symlink (#542006)

* Wed Dec  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.2-3
- Patch security hole in embedded neon (CVE-2009-2473)

* Wed Nov 04 2009 Bastien Nocera <bnocera@redhat.com> 2.24.2-2
- Set a default media player application in the schemas

* Thu Oct  8 2009 Alexander Larsson <alexl@redhat.com> - 2.24.2-1
- update to 2.24.2 - fixes mimetypes

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.24.1-9
- rebuilt with new openssl

* Fri Aug 14 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-8
- Drop gnome-mount and gnome-mime-data dependencies

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 2.24.1-7
- Convert specfile to UTF-8.

* Tue Aug  4 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-6
- Backport some upstream patches

* Mon Aug  3 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-5
- Fake POT-Creation-Date to prevent multilib issues (#514990)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.1-3
- Don't drop schemas translations from po files anymore

* Thu Apr  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-2
- Rebuilt to solve multilib issues (#492926)

* Tue Mar 17 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.24.0-4
- rebuild with new openssl

* Thu Sep 25 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-3
- Save some space

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0
- Drop upstreamed patches

* Thu Sep 11 2008 Matthias Clasen  <mclasen@redhat.com> - 2.23.0-1
- Rebuild against new bluez-libs

* Thu Jul 24 2008 Matthias Clasen  <mclasen@redhat.com> - 2.22.0-4
- Use newer xdgmime 

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22.0-3
- fix license tag
- don't apply Patch201, upstreamed

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Fix source url

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Dec  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-4
- Reinstate the gnome-mount BR

* Mon Dec  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-3
- Rebuild against new openssl
- Temporarily drop gnome-mount BR

* Mon Dec  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Build the mime.cache handling code

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (fixes a dns-sd crash)

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-4
- Rebuild against new dbus-glib

* Tue Oct 16 2007 David Zeuthen <davidz@redhat.com> - 2.20.0-3
- Also avoid showing /var/tmp as an icon on the desktop (#335241)

* Mon Oct 15 2007 David Zeuthen <davidz@redhat.com> - 2.20.0-2
- Don't show /var/log/audit on the desktop (#333041)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Wed Sep 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-2
- Fix a small memory leak

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Re-add gnome-mount dependency
- Update to 2.19.91
- Drop upstreamed posix patch

* Sun Sep  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-3
- Temporarily drop gnome-mount requires to break PolicyKit-gnome 
  dependency cycle

* Sat Aug 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-2
- Fix the build
- Update the license field

* Fri Jul 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue May  8 2007  <alexl@redhat.com> - 2.18.1-4
- Add keyutils-libs-devel build requires

* Tue May  8 2007 Alexander Larsson <alexl@redhat.com> - 2.18.1-3
- Fix ftp symlink crash (#435823)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 2.18.1-2
- Require libsmbclient, not samba-common

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Mar 13 2007 Alexander Larsson <alexl@redhat.com> - 2.18.0.1-1
- Update to 2.18.0.1

* Mon Mar 12 2007 Alexander Larsson <alexl@redhat.com> - 2.18.0-1
- update to 2.18.0

* Wed Mar  7 2007 Alexander Larsson <alexl@redhat.com> - 2.17.91-2
- Handle ipv6 link-local addresses better in network:/// (#212565)

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.3-1
- Update to 2.16.3
- Don't ship static libraries

* Tue Nov  7 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-2.fc7
- Update to 2.16.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Wed Oct 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-8
- Rebuild

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-6
- Fix scripts according to packaging guidelines

* Tue Oct 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-5
- Tighten up Requires (#203813)
- Require pkgconfig in the -devel package

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-3
- Prevent excessive warnings when dbus is not available (#207121)

* Tue Sep 19 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-2
- Backport fixes from cvs:
-  Fix crash on shutdown (gnome bug 347470)
-  Import gtk+ fixes to xdgmime

* Mon Sep  4 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-1
- update to 2.16.0

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-2
- Make error handling for http redirect more robust (203678)

* Mon Aug 21 2006 Alexander Larsson <alexl@redhat.com> - 2.15.92-1
- update to 2.15.92

* Fri Aug 11 2006 Matthew Barnes <mbarnes@redhat.com> - 2.15.91-2.fc6
- Add patch for RH bug #197868.

* Thu Aug 10 2006 Alexander Larsson <alexl@redhat.com> - 2.15.91-1
- update to 2.15.91

* Fri Aug  4 2006 Matthias Clasen <mclasen@redhat.com> -2.15.90-2.fc6
- Remove debug spew

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-7
- Disable gtk-doc to fix multilib conflicts

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-6
- Re-add gnome-mount dependency

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-5.1
- Temporarily break dependency cycle with gnome-mount

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-5
- Add BR for libselinux-devel

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.3-4
- Add patch to fix deprecated function

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 2.15.3-3
- Add BR for dbus-glib-devel

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-2 
- Rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Mon May 29 2006 Alexander Larsson <alexl@redhat.com> - 2.15.1-2
- buildrequires gettext (#193392)

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Sat Apr 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-4
- fix a typo

* Thu Apr 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- update to 2.14.1

* Wed Mar 15 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-2
- don't try to install a schema we don't ship anymore (bug 185549)

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0
- Drop upstreamed patches

* Tue Feb 28 2006 Alexander Larsson <alexl@redhat.com> - 2.13.92-3
- Fix smb browsing (#170922)

* Tue Feb 28 2006 Alexander Larsson <alexl@redhat.com> - 2.13.92-2
- Add patch (from cvs) that fixes permission reading

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.4-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.4-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb  4 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-7
- Fix requires

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-6
- Test build

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 2.13.4-5
- s/sed -ie/sed -i -e/

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 2.13.4-4
- fix fix for bonobo shlib multilib issue (bug 156982)

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 2.13.4-3
- fix bonobo shlib multilib issue (bug 156982)

* Tue Jan 17 2006 John (J5) Palmieri <johnp@redhat.com> 2.13.4-2
- Add a BuildRequires on gnome-mount-devel so we build with
  gnome-mount support

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-1
- Update to 2.13.4

* Mon Jan 09 2006 John (J5) Palmieri  <johnp@redhat.com> 2.13.3-3
- Add patch so --hal-udi is sent in when mounting and unmounting
 
* Mon Jan 09 2006 John (J5) Palmieri  <johnp@redhat.com> 2.13.3-2
- Add dependency on gnome-mount
- Add configure options for gnome-mount

* Thu Dec 15 2005 Matthias Clasen  <mclasen@redhat.com> 2.13.3-1
- Update to 2.13.3
- Drop upstreamed patches

* Tue Dec 13 2005 Alexander Larsson <alexl@redhat.com> 2.13.2-1
- update to 2.13.2

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 2.13.1-1.1
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.1-1
- Update to 2.13.1

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1.1-7
- rebuild for new dbus

* Tue Nov 22 2005 Alexander Larsson <alexl@redhat.com> - 2.12.1.1-6
- Update to use avahi 0.6

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 2.12.1.1-5
- rebuilt with new openssl

* Tue Nov  1 2005 Alexander Larsson <alexl@redhat.com> 2.12.1.1-4
- Remove XFree86-devel buildreq, as it doesn't exist anymore.
  I don't think we actually require it.

* Tue Oct 25 2005 Alexander Larsson <alexl@redhat.com> - 2.12.1.1-3
- Use avahi instead of howl

* Wed Oct 19 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1.1-2
- Fix the cache handling in xdgmime

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1.1-1
- Update to 2.12.1.1
- Drop upstreamed patches

* Tue Sep 27 2005 John (J5) Palmieir <johnp@redhat.com> 2.12.0-2
- Backported patch to fix bug #167985 which corrects the size of a
  readlink buffer
- Added a patch to fix bug #168743 which corrects the name of a
  data member from close to close_fn

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0
- Drop upstreamed patches

* Thu Aug 11 2005 David Zeuthen <davidz@redhat.com> 2.11.90-3
- Add system_storage.schemas to SCHEMAS (#165703)

* Wed Aug 10 2005 David Zeuthen <davidz@redhat.com> 2.11.90-2
- Disable a few patches that are upstream/irrelavant
- Add patch to detect mounts from drives we cannot poll

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- New upstream version
- Remove patches and sources for the desktop method, since
  we don't have start-here in the UI anymore.

* Fri Apr 29 2005 David Zeuthen <davidz@redhat.com> 2.10.0-5
- Tweak the patch a bit so it applies

* Fri Apr 29 2005 David Zeuthen <davidz@redhat.com> 2.10.0-4
- Make local neon copy support gssapi correctly (#150132)

* Tue Mar 29 2005 David Zeuthen <davidz@redhat.com> 2.10.0-3
- Rebuild

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> 2.10.0-2
- Drop a patch that was applied upstream

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> 2.10.0-1
- New upstream version

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-8
- More gcc 4.0 build fixes

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-7
- Rebuild

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-6
- Fix for gcc 4.0 build

* Mon Mar  7 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-5
- Build with patch for new hal/dbus API's - require hal-devel >= 0.5.0

* Wed Mar  2 2005 Tomas Mraz <tmraz@redhat.com> - 2.9.91-3
- rebuild with openssl-0.9.7e

* Wed Feb 16 2005 Alexander Larsson <alexl@redhat.com> - 2.9.91-2
- Add patch from cvs that fixes #144607

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> 2.9.91-1
- Update to 2.9.91

* Mon Dec 20 2004 Daniel Reed <djr@redhat.com> 2.8.2-10
- rebuild for new libhowl.so.0 library (for GnomeMeeting 1.2)

* Thu Nov 25 2004 Jeremy Katz <katzj@redhat.com> - 2.8.2-9
- rebuild to fix broken dep on x86_64 (#140679)

* Tue Oct 19 2004 Jonathan Blandford <jrb@redhat.com> 2.8.2-6
- add new samba requirement

* Mon Oct 18 2004  <jrb@redhat.com> - 2.8.2-4
- change default http/https handler to firefox

* Fri Oct 15 2004 Alexander Larsson <alexl@redhat.com> - 2.8.2-4
- Handle several mtab changes in the same second (#132976)

* Thu Oct 14 2004 David Zeuthen <davidz@redhat.com> 2.8.2-3
- Change console to pamconsole to support new util-linux and hal packages

* Wed Oct 13 2004 Alexander Larsson <alexl@redhat.com> - 2.8.2-2
- Fix bad buffer handling bug that broke ftp uploads

* Mon Oct 11 2004 Alexander Larsson <alexl@redhat.com> - 2.8.2-1
- Update to 2.8.2

* Fri Oct  8 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-8
- Backport some new fixes from cvs.

* Tue Oct  5 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-7
- update cvs backport with ssl http fix

* Tue Oct  5 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-6
- Add cvs-backport patch with various fixed from HEAD, including
  a partial fix for #134627
- Removed the patches that are in the cvs-backport patch.

* Fri Oct  1 2004 David Zeuthen <davidz@redhat.com> 2.8.1-5
- Build with hal patch

* Wed Sep 29 2004 David Zeuthen <davidz@redhat.com> 2.8.1-4
- Apply hal patch
- Support the console mount option

* Wed Sep 29 2004 Ray Strode <rstrode@redhat.com> 2.8.1-3
- Swap if and else in egg_desktop_entries_get_locale_encoding
  to prevent allocating massive amounts of unneeded ram.

* Mon Sep 27 2004 Mark McLoughlin <markmc@redhat.com> 2.8.1-2
- Remove menu-only-show-in patch - latest KDE packages don't use
  non-standard <OnlyShowIn> anymore

* Tue Sep 21 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- update to 2.8.1

* Thu Sep 16 2004 Mark McLoughlin <markmc@redhat.com> - 2.8.0-3
- Update to desktop-file-utils 0.8 and remove a bunch of
  upstreamed patches

* Tue Sep 14 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-2
- Backport some fixes from head, including ftp stuff

* Mon Sep 13 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0
- remove upstreamed patch

* Fri Sep  3 2004 GNOME <jrb@redhat.com> - 2.7.92-2
- remove mozilla as default browser

* Wed Sep  1 2004 Alexander Larsson <alexl@redhat.com> - 2.7.92-2
- add fstab_sync patch from upstream

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Thu Aug 19 2004 Alex Larsson <alexl@redhat.com> 2.7.91-1
- update to 2.7.91

* Tue Aug 10 2004 Alexander Larsson <alexl@redhat.com> - 2.7.90-3
- Build for new howl (requires patch)
- Add dns-sd schema

* Sun Aug  8 2004 Christopher Aillon <caillon@redhat.com> 2.7.90-2
- Add compiler fix for an enumerator with trailing comma.

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90
- Remove cvs-backport patch
- Add BuildRequires for krb5-devel, howl-devel and hal-devel
- Fixup the schema-about and mozilla patches

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 13 2004 Elliot Lee <sopwith@redhat.com> 2.6.0-8
- Patch61 (desktop-file-utils-0.6-pleasecreate.patch) to fix #119446

* Tue May 04 2004 Dan Williams <dcbw@redhat.com> 2.6.0-7
- Update to desktop-file-utils 0.6
- Implement monitoring to detect addition/deletion of .desktop files
- Fix RH #118553, crash when reading symlink that points to
    nothing in libmenu.so VFS backend

* Thu Apr 22 2004 Mark McLoughlin <markmc@redhat.com> - 2.6.0-6
- Fix crash when .desktop files aren't readable (bug #120014)

* Fri Apr 16 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-5
- Make mozilla default http handler since epi might not be installed

* Thu Apr 15 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-4
- New cvs backport with sftp fix

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-3
- install more schemas in post

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-2
- Add cvs fixes backport

* Tue Mar 23 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Thu Mar 18 2004 Warren Togami <wtogami@redhat.com> 2.5.91-3
- #118614 patches 100 and 101

* Wed Mar 17 2004 Dan Williams <dcbw@redhat.com> 2.5.91-2
- Support .directory file "NoDisplay" keys in libmenu.so VFS backend

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.5.91-1
- update to 2.5.91

* Fri Mar 12 2004 Dan Williams <dcbw@redhat.com> 2.5.90-3
- Make OnlyShowIn for .desktop files actually work

* Thu Mar 11 2004 Dan Williams <dcbw@redhat.com> 2.5.90-2
- Add desktop-file-utils to build the new libmenu.so VFS backend
    for .menu files.  Its a hack for now, and will eventually
    be replaced by upstreaming the d-f-u code

* Mon Mar  8 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.8-2
- fix some packaging issues (#115807)

* Mon Feb 23 2004 Alexander Larsson <alexl@redhat.com> 2.5.8-1
- update to 2.5.8
- fix smb filelist
- add devel docs

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Alexander Larsson <alexl@redhat.com> 2.5.7-1
- update to 2.5.7

* Mon Feb  9 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-4
- build-req fam-devel and openssl-devel (#111109)
- Own libdir/gnome-vfs-2.0/include (#113045)

* Fri Feb  6 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-3
- Clean up the patch list
- Fix the network: issue
- Remove core file from tarball

* Thu Feb  5 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-2
- Fix daemon server file

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-1
- update to 2.5.6

* Thu Jan 29 2004 Jonathan Blandford <jrb@redhat.com> 2.5.5-5
- re-add the vfolder patch

* Fri Jan 23 2004 Alexander Larsson <alexl@redhat.com> 2.5.5-4
- Split smb into its own subpackage

* Wed Jan 21 2004 Alexander Larsson <alexl@redhat.com> 2.5.5-3
- provide gnome-vfs-extras2

* Mon Jan 19 2004 Alexander Larsson <alexl@redhat.com> 2.5.5-2
- add shared-mime-info dep
- obsolete gnome-vfs2-extras

* Fri Jan 16 2004 Jonathan Blandford <jrb@redhat.com> 2.5.5-1
- new version for GNOME 2.5

* Wed Oct 15 2003 Alexander Larsson <alexl@redhat.com> 2.4.1-1
- Update to 2.4.1, fixes bug #107130

* Tue Sep  9 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- update to 2.4.0

* Tue Sep  2 2003 Alexander Larsson <alexl@redhat.com> 2.3.90-1
- update to 2.3.90

* Mon Aug 25 2003 Alexander Larsson <alexl@redhat.com> 2.3.8-1
- update to 2.3.8

* Mon Aug 11 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-1
- update for gnome 2.3

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.2.5-3
- rebuild, setting tagname to CC

* Tue Jul  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.5-2.E
- Rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 27 2003 Alexander Larsson <alexl@redhat.com> 2.2.5-1
- Update to 2.2.5

* Mon Mar 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-1
- Update to 2.2.4

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Mon Feb 24 2003 Alexander Larsson <alexl@redhat.com> 2.2.2-3
- Added patch to fix smb crash (#84982)

* Mon Feb 24 2003 Alexander Larsson <alexl@redhat.com> 2.2.2-2
- Add patch to fix notify race (#84668)

* Wed Feb 12 2003 Alexander Larsson <alexl@redhat.com> 2.2.2-1
- 2.2.2, fixes bad memleak (#83791)

* Tue Feb 11 2003 Havoc Pennington <hp@redhat.com> 2.2.1-3
- kill menu editing again, it was very very broken

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 2.2.1-2
- fix file list (#68226)
- prereq GConf2

* Mon Feb 10 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-1
- Update to 2.2.1. fixes gnome-theme-manager hang

* Thu Feb  6 2003 Havoc Pennington <hp@redhat.com> 2.2.0-7
- move to menu editing modules.conf by default, we'll see if it works

* Tue Jan 28 2003 Matt Wilson <msw@redhat.com> 2.2.0-6
- use LIBTOOL=/usr/bin/libtool

* Mon Jan 27 2003 Havoc Pennington <hp@redhat.com>
- it would help to *install* the stupid menu edit conf file
- update the vfolder-hacks patch with some fixes

* Fri Jan 24 2003 Havoc Pennington <hp@redhat.com>
- hack up editable vfolder backend to maybe work
  (still not the default config file)

* Wed Jan 22 2003 Havoc Pennington <hp@redhat.com>
- include a non-default config file to use new vfolder method
- build the new vfolder method

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com>
- Update to 2.2.0

* Mon Jan 13 2003 Havoc Pennington <hp@redhat.com>
- variation on the subfolders hack to try to fix it

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- fix bug where empty folders with empty subfolders would
  still be visible.

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- finish adapting desktop-method.c to underscore-prefixing action

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- adapt desktop-method.c to underscore-prefixing action

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- hardcode <DontShowIfEmpty>, it's stupid to ever override this.

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- make network:/// use libdesktop.so, and modify libdesktop.so 
  to support it

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- Revert to George's vfolder backend from gnome-vfs-2.0.2 or so
- put back libdesktop.so
- don't build the new vfolder backend

* Wed Jan  8 2003 Alexander Larsson <alexl@redhat.com> 2.1.6-2
- Removed __libdir fix that was fixed upstream

* Wed Jan  8 2003 Alexander Larsson <alexl@redhat.com> 2.1.6-1
- Update to 2.1.6

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.5-3
- rebuild

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 2.1.5-2
- rebuild

* Mon Dec 16 2002 Alexander Larsson <alexl@redhat.com> 2.1.5-1
- Update to 2.1.5

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use OpenSSL's pkg-config information, if available

* Wed Dec  4 2002 Havoc Pennington <hp@redhat.com>
- 2.1.3.1

* Sun Nov 10 2002 Havoc Pennington <hp@redhat.com>
- 2.1.3
- update moved-menu-files patch

* Wed Oct 23 2002 Havoc Pennington <hp@redhat.com>
- add patch for OnlyShowIn support
- use plain menu files for .vfolder-info-default
- don't install unused vfolder-info files

* Tue Oct  8 2002 Havoc Pennington <hp@redhat.com>
- require new gnome-mime-data in proper libdir
- 2.0.4
- drop most patches as they are now upstream or 
  don't apply to new vfolder code

* Fri Aug 30 2002 Owen Taylor <otaylor@redhat.com>
- Backport a gnome-vfs locking fix from CVS 
  (Hopefully fixes #71419)

* Fri Aug 23 2002 Havoc Pennington <hp@redhat.com>
- make vfolder method read-only #72208

* Mon Aug 19 2002 Jonathan Blandford <jrb@redhat.com>
- notice when new files are installed

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- don't include pointless .a files

* Fri Aug  2 2002 Havoc Pennington <hp@redhat.com>
- 2.0.2
- use vfolders for system-settings and server-settings

* Tue Jul 16 2002 Havoc Pennington <hp@redhat.com>
- fix OnlyShowIn

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.1, fix missing po files

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- put schema files in file list, and install them
- put libdir/vfs in file list

* Tue Jun 11 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun 11 2002 Havoc Pennington <hp@redhat.com>
- look for menus in redhat-menus

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.9.16

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon May 20 2002 Havoc Pennington <hp@redhat.com>
- 1.9.15
- comment out docdir patch for now

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.9.14

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.9.11
- update file list

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.9.7

* Thu Jan 31 2002 Owen Taylor <otaylor@redhat.com>
- Fix location of installed docs not to conflict with gnome-vfs1

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Rebuild with new libs

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan  3 2002 Havoc Pennington <hp@redhat.com>
- 1.0.4.91 snap

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- 1.9.4.90 snap
- require gnome-mime-data

* Sun Oct 28 2001 Havoc Pennington <hp@redhat.com>
- new snap, rebuild for glib 1.3.10

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- cvs snap

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- rebuild cvs snap with changes merged upstream
- fix a requires
- fix up requires/buildrequires a bit

* Tue Sep 18 2001 Havoc Pennington <hp@redhat.com>
- initial gnome-vfs2 build, remove all patches
- change config files not to be noreplace

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 20 2001 Havoc Pennington <hp@redhat.com>
- fix #51864 (Gimp can't handle file: URIs)

* Mon Aug 20 2001 Alexander Larsson <alexl@redhat.com> 1.0.1-15
- Moved gnome-conf and pkgconfig files to the devel package
- Fixes SHOULD-FIX bug #49795

* Mon Aug  6 2001 Alexander Larsson <alexl@redhat.com> 1.0.1-14
- Added a patch that fixed AbiWord mimetype handling.

* Fri Jul 27 2001 Jonathan Blandford <jrb@redhat.com>
- Add .desktop file sniffing

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- don't do the giant trash scan thing; did not play nice
  with NFS.

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- fix desktop-file.conf file

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- change some URI scheme names

* Fri Jul 20 2001 Alexander Larsson <alexl@redhat.com>
- Add pkgconfig and gnome-libs-devel build reqs.
- Remove dependency on gnome-vfs-devel by doing some
- CPPFLAGS and LDFLAGS magic

* Wed Jul 11 2001 Havoc Pennington <hp@redhat.com>
- add missing directories

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- fix a segv
- change which dirs the desktop VFS module points to

* Sun Jul 08 2001 Havoc Pennington <hp@redhat.com>
- add desktop VFS module hack

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove Distribution and Vendor
- Make the config files noreplace
- Move .so links to devel subpackage
- langify
- Add BuildRequires
- Don't mess with /etc/ld.so.conf
- Use %%{_tmppath}
- s/Copyright/License/

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed May  9 2001 Jonathan Blandford <jrb@redhat.com>
- New Version.

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- New Version.
- clean up spec file some.

* Mon Feb 19 2001 Gregory Leblanc <gleblanc@cu-portland.edu>
- fix paths and macros

* Tue Feb 22 2000 Ross Golder <rossigee@bigfoot.com>
- Integrate into source tree
