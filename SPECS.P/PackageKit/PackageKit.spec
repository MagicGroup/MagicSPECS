%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:   Package management service
Name:      PackageKit
Version:   0.8.1
Release:   6%{?dist}
License:   GPLv2+ and LGPLv2+
URL:       http://www.packagekit.org
Source0:   http://www.packagekit.org/releases/%{name}-%{version}.tar.xz

# Fedora-specific: set Vendor.conf up for Fedora.
Patch0:    PackageKit-0.3.8-Fedora-Vendor.conf.patch

# Fedora specific: the yum backend doesn't do time estimation correctly
Patch1:    PackageKit-0.4.4-Fedora-turn-off-time.conf.patch

# Upstreamable?  allow use of xulrunner2 for browser-plugin support
Patch4: PackageKit-0.7.4-xulrunner2.patch

# Upstream already
Patch5: PackageKit-0.8.1-master.patch

Requires: PackageKit-glib = %{version}-%{release}
Requires: PackageKit-backend
Requires: shared-mime-info
Requires: comps-extras
Requires: systemd
Requires: preupgrade

# required by patch4
BuildRequires: automake gtk-doc libtool
BuildRequires: glib2-devel >= 2.16.1
BuildRequires: dbus-devel  >= 1.1.1
BuildRequires: dbus-glib-devel >= 0.74
BuildRequires: pam-devel
BuildRequires: libX11-devel
BuildRequires: xmlto
BuildRequires: sqlite-devel
BuildRequires: NetworkManager-devel
BuildRequires: polkit-devel >= 0.92
BuildRequires: libtool
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: docbook-utils
BuildRequires: gnome-doc-utils
BuildRequires: python-devel
BuildRequires: perl(XML::Parser)
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libgudev1-devel
%ifnarch mips64el
BuildRequires: xulrunner-devel
%endif
BuildRequires: libarchive-devel
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
BuildRequires: qt4-devel
BuildRequires: cppunit-devel
BuildRequires: pango-devel
BuildRequires: pm-utils-devel
BuildRequires: fontconfig-devel
BuildRequires: systemd-devel
BuildRequires: gobject-introspection-devel
BuildRequires: zif-devel >= 0.2.5

# functionality moved to udev itself
Obsoletes: PackageKit-udev-helper < %{version}-%{release}
Obsoletes: udev-packagekit < %{version}-%{release}

# No more GTK+-2 plugin
Obsoletes: PackageKit-gtk-module < %{version}-%{release}

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%package yum
Summary: PackageKit YUM backend
Group: System Environment/Libraries
Requires: yum >= 3.2.19
# python(gio)
Requires: pygobject2
Requires: %{name} = %{version}-%{release}
Provides: PackageKit-backend

%description yum
A backend for PackageKit to enable yum functionality.

%package zif
Summary: PackageKit Zif backend
Group: System Environment/Libraries
Requires: zif >= 0.2.5
Requires: %{name} = %{version}-%{release}
Provides: PackageKit-backend

%description zif
A backend for PackageKit to enable Zif functionality.

%package smart
Summary: PackageKit SMART backend
Group: System Environment/Libraries
Requires: smart
Requires: %{name} = %{version}-%{release}

%description smart
A backend for PackageKit to enable SMART functionality.

%package docs
Summary: Documentation for PackageKit
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
API docs for PackageKit.

%package yum-plugin
Summary: Tell PackageKit to check for updates when yum exits
Group: System Environment/Base
Requires: yum >= 3.0
Requires: PackageKit
Requires: dbus-python
Obsoletes: yum-packagekit < %{version}-%{release}

%description yum-plugin
PackageKit-yum-plugin tells PackageKit to check for updates when yum exits.
This way, if you run 'yum update' and install all available updates, puplet
will almost instantly update itself to reflect this.

%package glib
Summary: GLib libraries for accessing PackageKit
Group: Development/Libraries
Requires: dbus >= 1.1.1
Requires: %{name} = %{version}-%{release}
Requires: gobject-introspection
Obsoletes: PackageKit-libs < %{version}-%{release}
Provides: PackageKit-libs = %{version}-%{release}

%description glib
GLib libraries for accessing PackageKit.

%package qt
Summary: QT libraries for accessing PackageKit
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description qt
QT libraries for accessing PackageKit.

%package cron
Summary: Cron job and related utilities for PackageKit
Group: System Environment/Base
Requires: cronie
Requires: %{name} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%package debug-install
Summary: Facility to install debugging packages using PackageKit
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Obsoletes: PackageKit-debuginfo-install <= 0.5.2-0.1.20090902git.fc12

%description debug-install
Provides facility to install debugging packages using PackageKit.

%package glib-devel
Summary: GLib Libraries and headers for PackageKit
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel >= 1.1.1
Requires: sqlite-devel
Requires: PackageKit-glib = %{version}-%{release}
Obsoletes: PackageKit-devel < %{version}-%{release}
Provides: PackageKit-devel = %{version}-%{release}

%description glib-devel
GLib headers and libraries for PackageKit.

%package qt-devel
Summary: Qt Libraries and headers for PackageKit
Group: Development/Libraries
Requires: %{name}-qt = %{version}-%{release}

%description qt-devel
Qt headers and libraries for PackageKit.

%package backend-devel
Summary: Headers to compile out of tree PackageKit backends
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description backend-devel
Headers to compile out of tree PackageKit backends.

%ifnarch mips64el
%package browser-plugin
Summary: Browser Plugin for PackageKit
Group: Development/Libraries
Requires: gtk2
Requires: PackageKit-glib = %{version}-%{release}
Requires: mozilla-filesystem

%description browser-plugin
The PackageKit browser plugin allows web sites to offer the ability to
users to install and update packages from configured repositories
using PackageKit.
%endif

%package gstreamer-plugin
Summary: Install GStreamer codecs using PackageKit
Group: Development/Libraries
Requires: gstreamer
Requires: PackageKit-glib = %{version}-%{release}
Obsoletes: codeina < 0.10.1-10
Provides: codeina = 0.10.1-10

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%package gtk3-module
Summary: Install fonts automatically using PackageKit
Group: Development/Libraries
Requires: pango
Requires: PackageKit-glib = %{version}-%{release}

%description gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%package command-not-found
Summary: Ask the user to install command line programs automatically
Group: Development/Libraries
Requires: bash
Requires: PackageKit-glib = %{version}-%{release}

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%package device-rebind
Summary: Device rebind functionality for PackageKit
Group: Development/Libraries
Requires: PackageKit-glib = %{version}-%{release}

%description device-rebind
The device rebind functionality offer the ability to re-initialize devices
after firmware has been installed by PackageKit. This removes the need for the
user to restart the computer or remove and re-insert the device.

%prep
%setup -q
%patch0 -p1 -b .fedora
%patch1 -p1 -b .no-time
%patch4 -p1 -b .xulrunner2
%patch5 -p1 -b .master
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
        --disable-static \
        --enable-yum \
        --enable-zif \
        --enable-smart \
        --enable-introspection \
        --with-default-backend=auto \
        --disable-local \
        --disable-strict \
        --disable-tests

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libpackagekit*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/packagekit-plugin.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit-1/extensions/libpackagekit-action-lookup.la

touch $RPM_BUILD_ROOT%{_localstatedir}/cache/PackageKit/groups.sqlite

# create a link that GStreamer will recognise
pushd ${RPM_BUILD_ROOT}%{_libexecdir} > /dev/null
ln -s pk-gstreamer-install gst-install-plugins-helper
popd > /dev/null

# create a link that from the comps icons to PK, as PackageKit frontends
# cannot add /usr/share/pixmaps/comps to the icon search path as some distros
# do not use comps. Patching this in the frontend is not a good idea, as there
# are multiple frontends in multiple programming languages.
pushd ${RPM_BUILD_ROOT}%{_datadir}/PackageKit > /dev/null
ln -s ../pixmaps/comps icons
popd > /dev/null
magic_rpm_clean.sh
%find_lang %name || touch %name.lang

%post
update-mime-database %{_datadir}/mime &> /dev/null || :
systemctl enable packagekit-offline-update.service &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :

%post glib -p /sbin/ldconfig
%post qt -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING
%dir %{_datadir}/PackageKit
%dir %{_datadir}/PackageKit/helpers
%dir %{_sysconfdir}/PackageKit
%dir %{_sysconfdir}/PackageKit/events
%dir %{_sysconfdir}/PackageKit/events/post-transaction.d
%dir %{_sysconfdir}/PackageKit/events/pre-transaction.d
%{_sysconfdir}/PackageKit/events/*.d/README
%dir %{_localstatedir}/lib/PackageKit
%dir %{python_sitelib}/packagekit
%dir %{_localstatedir}/cache/PackageKit
%ghost %verify(not md5 size mtime) %{_localstatedir}/cache/PackageKit/groups.sqlite
%dir %{_localstatedir}/cache/PackageKit/downloads
%{python_sitelib}/packagekit/*py*
%dir %{_sysconfdir}/bash_completion.d
%dir %{_libdir}/packagekit-backend
%config %{_sysconfdir}/bash_completion.d/pk-completion.bash
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%config %{_sysconfdir}/dbus-1/system.d/*
%dir %{_datadir}/PackageKit/helpers/test_spawn
%dir %{_datadir}/PackageKit/icons
%{_datadir}/PackageKit/helpers/test_spawn/*
%{_datadir}/man/man1/pkcon.1.gz
%{_datadir}/man/man1/pkmon.1.gz
%{_datadir}/man/man1/pkgenpack.1.gz
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/mime/packages/packagekit-*.xml
%{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_libexecdir}/packagekitd
%{_libexecdir}/pk-trigger-offline-update
%{_bindir}/pkmon
%{_bindir}/pkcon
%{_bindir}/pkgenpack
%{_bindir}/packagekit-bugreport.sh
%exclude %{_libdir}/libpackagekit*.so.*
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/PackageKit/transactions.db
%{_datadir}/dbus-1/system-services/*.service
%{_libdir}/pm-utils/sleep.d/95packagekit
%{_libdir}/packagekit-plugins/*.so
%{_libdir}/girepository-1.0/PackageKitPlugin-1.0.typelib
%{_datadir}/dbus-1/interfaces/*.xml
/usr/lib/systemd/system/packagekit-offline-update.service
%{_libexecdir}/pk-*offline-update
%{_libdir}/gtk-2.0/modules/libpk-gtk-module.so

%files docs
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/PackageKit

%if 0%{?rhel} == 0
%files smart
%defattr(-,root,root,-)
%{_libdir}/packagekit-backend/libpk_backend_smart.so
%dir %{_datadir}/PackageKit/helpers/smart
%{_datadir}/PackageKit/helpers/smart/*
%endif

%files yum
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/PackageKit/Yum.conf
%{_libdir}/packagekit-backend/libpk_backend_yum.so
%dir %{_datadir}/PackageKit/helpers/yum
%{_datadir}/PackageKit/helpers/yum/*

%if 0%{?rhel} == 0
%files zif
%defattr(-,root,root,-)
%{_libdir}/packagekit-backend/libpk_backend_zif.so
%dir %{_datadir}/PackageKit/helpers/zif
%{_datadir}/PackageKit/helpers/zif/*
%endif

%files yum-plugin
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/yum/pluginconf.d/refresh-packagekit.conf
/usr/lib/yum-plugins/refresh-packagekit.*

%files glib
%defattr(-,root,root,-)
%{_libdir}/*packagekit-glib2.so.*
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files qt
%defattr(-,root,root,-)
%{_libdir}/*packagekit-qt*.so.*

%files cron
%defattr(-,root,root,-)
%config %{_sysconfdir}/cron.daily/packagekit-background.cron
%config(noreplace) %{_sysconfdir}/sysconfig/packagekit-background

%files debug-install
%defattr(-,root,root,-)
%{_bindir}/pk-debuginfo-install
%{_datadir}/man/man1/pk-debuginfo-install.1.gz

%ifnarch mips64el
%files browser-plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/packagekit-plugin.so
%endif

%files gstreamer-plugin
%defattr(-,root,root,-)
%{_libexecdir}/pk-gstreamer-install
%{_libexecdir}/gst-install-plugins-helper

%files gtk3-module
%defattr(-,root,root,-)
%{_libdir}/gtk-3.0/modules/*.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml

%files command-not-found
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf

%files device-rebind
%defattr(-,root,root,-)
%{_sbindir}/pk-device-rebind
%{_datadir}/man/man1/pk-device-rebind.1.gz

%files glib-devel
%defattr(-,root,root,-)
%{_libdir}/libpackagekit-glib2.so
%{_libdir}/pkgconfig/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%dir %{_includedir}/PackageKit/packagekit-glib2
%{_includedir}/PackageKit/packagekit-glib*/*.h
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gir-1.0/PackageKitPlugin-1.0.gir

%files qt-devel
%defattr(-,root,root,-)
%{_libdir}/libpackagekit-qt*.so
%{_includedir}/PackageKit/packagekit-qt2/*
%{_libdir}/pkgconfig/packagekit-qt2.pc
%{_libdir}/cmake/packagekit-qt2/packagekit-qt2*.cmake

%files backend-devel
%defattr(-,root,root,-)
%dir %{_includedir}/PackageKit
%dir %{_includedir}/PackageKit/backend
%{_includedir}/PackageKit/backend/*.h
%{_includedir}/PackageKit/plugin
%{_libdir}/pkgconfig/packagekit-plugin.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.8.1-6
- 为 Magic 3.0 重建

* Thu Jul 05 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-5
- Correctly write the /var/lib/PackageKit/prepared-update file.

* Mon Jul 02 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-4
- Fix several reported problems with the offline-update funtionality.

* Fri Jun 29 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-3
- Fix several reported problems with the offline-update funtionality.

* Thu Jun 28 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-2
- Apply a combined patch from master to fix several reported issues
  with the OS update feature.

* Mon Jun 25 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-1
- New upstream release

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 0.7.4-8
- Rebuild

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 0.7.4-7
- Rebuild for new libzif

* Tue May 29 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.4-6
- Do not build the PackageKit-zif package on RHEL.

* Fri May 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.4-5
- re-enable -browser-plugin content
- make V=1

* Thu May 17 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.4-4
- Fix an obvious off-by-one when parsing the signature
- Resolves: #794927

* Fri May 11 2012 Nils Philippsen <nils@redhat.com> - 0.7.4-3
- yum: don't perceive all updates as untrusted (#821015)

* Wed Apr 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.4-2
- track sonames so abi bumps aren't a surprise
- -qt-devel: fix dir ownership

* Tue Apr 24 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.4-1
- New upstream release
- Add GType's for packagekit-glib2 enumerations
- Always set GPG checking members if present for yum.
- Do not allow an empty resolve call to be passed down to the backends
- Do not include the website in the tarball
- Drop --print-reply from dbus-send command used on suspend/resume
- Install pk-task-sync.h as part of the public API
- Speed up get_package_list

* Fri Apr 13 2012 Jindrich Novy <jnovy@redhat.com> - 0.7.3-2
- rebuild against new librpm

* Thu Mar 01 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.3-1
- New upstream release
- Remove upstreamed patches
- Use autoremove in the zif backend
- Fix several more crashers in the glib library from the move to GDBus

* Fri Jan 27 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.2-5
- Fix another gnome-settings-daemon crash

* Thu Jan 26 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.2-4
- Add back the preupgrade Require to fix a warning in g-s-d.

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.7.2-3
- Rebuilt for new libarchive

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 0.7.2-2
- Fix gnome-settings-daemon crashes

* Tue Jan 17 2012 Richard Hughes  <rhughes@redhat.com> - 0.7.2-1
- New upstream release.
- Remove upstreamed patches

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 09 2012 Nils Philippsen <nils@redhat.com> - 0.6.21-2
- yum: don't request authorization for trusted packages (#771746)

* Mon Dec 05 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.21-1
- New upstream release.
- Consistently use same logic to determine GPG checking.

* Mon Nov 07 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.20-1
- New upstream release.
- Remove upstreamed patches
- Add ourselves to YumBase.run_with_package_names
- Add command line option to keep environment

* Thu Oct 27 2011 Nils Philippsen <nils@redhat.com> - 0.6.19-3
- fix yum encoding issues seen with kpackagekit (#668282)

* Tue Oct 04 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.19-2
- It turns out the buildroot overrides take longer than just waiting
  for "koji wait-repo f16-build"

* Tue Oct 04 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.19-1
- New upstream release.
- Lots of Zif updates
- Offset the cache age by 30 minutes
- Use the newest filter when resolving for new packages to install

* Fri Sep 09 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.18-2
- Backport a patch from upstream as glib2 had an API change that
  affects PackageKit.

* Mon Sep 05 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.18-1
- New upstream release.
- Fix a small memory leak in the glib client library
- Ignore missing obsoleted updates rather than failing the update
- Fix a warning when doing 'pkcon repo-list --filter=~devel'
- Make the lsof plugin not lookup hostnames
- Remove the duplicate 'The software is not from a trusted source'

* Tue Aug 02 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.17-2
- Ensure the moc files are re-generated by manually deleting them.

* Mon Aug 01 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.17-1
- New upstream release.
- Manually convert the results of GetDetails to unicode.
- Parse the new style .discinfo files for F15
- Ignore local packages when calculating the simulate list
- Allow the user to remove PackageKit-yum if PackageKit-zif is installed
- Resolves: #719916, #709865

* Mon Jul 04 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.16-1
- New upstream release.
- Do not try to parse any arguments in command-not-found.
- Ensure we save the updates cache for the pre-transaction checks.

* Fri Jul 01 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.15-3
- Upstream yum recently changed the behaviour when checking signatures
  on a package. The commit added a new configuration key which only
  affects local packages, but the key was set by default to False.
- This meant that an end user could install a local unsigned rpm package
  using PackageKit without a GPG trust check, and the user would be told
  the untrusted package is itself trusted.
- To exploit this low-impact vulnerability, a user would have to
  manually download an unsigned package file and would still be required
  to authenticate to install the package.
- The CVE-ID for this bug is CVE-2011-2515
- See https://bugzilla.redhat.com/show_bug.cgi?id=717566 for details.
- Resolves #718127

* Thu Jun 09 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.15-2
- Rebuild for bumped libzif soname.

* Tue Jun 07 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.15-1
- New upstream release.
- More GIR fixes
- Allow the 'any' WhatProvides kind to match provide strings
- Do not prevent updating when firefox is running, we don't have all the
  client UI ready yet.

* Thu May 05 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.14-2
- Fix pkcon get-updates.

* Wed May 04 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.14-1
- New upstream release.
- Add annotations to make PackageKit-glib GIR usable
- Make DownloadPackages to save to the system cache if there is no path
- Do not output duplicates when searching with newest
- Do not abort in pk_catalog_init() if PackageKit is not available
- Resolves: #688280 and #585601

* Mon Mar 07 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.13-1
- New upstream release.
- Enable use of new callback mode on yum versions that support it
- Update for NetworkManager 0.9 snapshots

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.12-4
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.12-2
- Rebuild against newer gtk

* Tue Feb 01 2011 Richard Hughes  <rhughes@redhat.com> - 0.6.12-1
- New upstream release.
- Do not attempt to call yum.repos twice when using RHN
- Do not block the update list on infrastructure packages
- Update the cached comps group list when changing repos.
- Do not enable command not found debugging by default.
- Resolves #666254, #629049

* Fri Jan 21 2011 Christopher Aillon <caillon@redhat.com> - 0.6.11-5
- Rebuild

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.11-4
- Put the gir in the devel

* Wed Jan 12 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.6.11-3
- Backport: yum: Ensure the category data is valid UTF8 (rhughes, #668282)

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.11-2
- Rebuild against newer gtk3

* Mon Dec 13 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.11-1
- New upstream release.
- Many small bugfixes and performance increases.
- New experimental zif backend, which is not installed by default.

* Mon Nov 01 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.10-1
- New upstream release.
- Many small bugfixes and performance increases.
- Remove selinux-policy from InfrastructurePackages
- Allow frontends to specify the cache age manually, to reduce the
  amount of time users sit waiting for progress bars.
- Resolves #641311, #641691

* Tue Oct 12 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.9-2
- Add BR zif-devel to accelerate some simple transaction types.

* Mon Oct 04 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.9-1
- New upstream release of 0.6.9.
- Many small bugfixes and performance increases.
- Resolves #634628

* Wed Sep 29 2010 jkeating - 0.6.8-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.8-2
- Rebuild against newer gobject-introspection

* Wed Sep 08 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.8-1
- New upstream release of 0.6.8.
- Add selinux-policy to the list of infrastructure packages.
- Build gtk2 and gtk3 versions of the GTK module.

* Wed Aug 04 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.7-1
- New upstream release of 0.6.7.
- Add gnome-packagekit and kpackagekit to the list of infrastructure packages
- Do not issue RepoListChanged when we disable or enable the media repo automatically
- Ensure we disable the MediaRepo when the PackageKit backend has finished
- Wrap _getEVR in a try,catch block to deal with invalid version numbers. Fixes #612360
- If ProxyHTTP are set in PackageKit.conf then ignore the user proxy setting. Fixes #604317
- Don't ship README AUTHORS NEWS COPYING in all subpackages. Fixes #612332
- Recognise bluetooth connections as mobile networks. Fixes #609827
- Unbreak CNF after the daemon moved to libexec. Fixes #613514

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.6.6-2
- Rebuild against new gobject-introspection

* Thu Jul 01 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.6-1
- New upstream release of 0.6.6.
- Don't crash with an internal error if the .discinfo is malformed
- Add a MaxSearchTime entry in CommandNotFound.conf and default to 2000ms
- Build the gtk-module for gtk-3.0 as well as gtk-2.0 if available
- Move the packagekitd binary to libexec

* Wed Jun 02 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.5-1
- New upstream release of 0.6.5.
- Use the new PkTask API in pkcon so we can deal with Media and Eula queries.
- Attempt to use removable disk repos if they exist at backend startup.
- Catch and ignore the socket exception on oddball systems.
- Do not abort init when Yum.conf does not contain some required keys.
- Fix up the filter check when doing GetRepoList().
- Resolves: #596779 and #598697

* Thu May 06 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.4-1
- New upstream release of 0.6.4.
- Catch exceptions.IOError whenever we do a low-level yum call. Resolves #577549
- Do not abort if the package-id is not unique in the reposet
- Ensure the lock failure message is proper unicode. Resolves #585620
- Ensure we catch the exception if there are no groups. Resolves #587196
- Ensure we create /var/cache/PackageKit if the user nukes it
- Get the correct state for each update. Resolves #574658

* Mon Mar 29 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.3-1
- New upstream version
- Update to the latest version of the Fedora Packaging Guidelines
- Do not Require: pkgconfig
- Fix up a few file ownership issues
- Remove the custom BuildRoot
- Do not clean the buildroot before install

* Sat Mar 13 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.6.2-2
- -qt: add minimal qt4 runtime dependency

* Mon Mar 01 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.2-1
- New upstream release of 0.6.2.

* Fri Feb 19 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.2-0.1.20100219git
- Fix a race in the PkBackendSpawn code that sometimes lead to truncated package
  lists from repeated simple queries that needed to change the dispatcher.
- Resolves: #566200

* Tue Feb 09 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.2-0.1.20100209git
- Rebuild for twaugh's printer driver install F13 feature.
- Install the gir and typelib files in the correct directory.

* Mon Feb 01 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.1-1
- New upstream release of 0.6.1.
- Ensure we look in all update notices for a security update. Fixes #526279
- Show a message to the user if the repo could not be reached. Fixes #531838
- Enable introspection support in PackageKit-glib2

* Tue Jan 05 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.0-1
- New upstream release of 0.6.0.

* Mon Dec 07 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.5-1
- New upstream release of 0.5.5.
- Check the filename is valid before exploding. Fixes #537381
- Only check certain transaction elements, not all of them. Fixes #541645
- Handle the cnf error condition where the package name would be invalid. Fixes #533014
- After a successful cnf installation, re-exec new binary not command-not-found. Fixes #533554
- When cnf searches for available files, use our preferred arch. Fixes #534169
- Run the newly installed file sync so we can return a proper exit code. Fixes #540482
- Only email using cron when a useful action was done. Fixes #540949
- Do not split more than one locale hint to fix setting LC_ variables. Fixes #543716

* Mon Oct 05 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.3-1
- Update to 0.5.3.
- Fix double free in pk-gstreamer-install which causes a crash. Fixes #526600
- Exit pk-command-not-found with 127 when we have not run a program. Fixes #527044
- Fix crash in notification daemon under some conditions due to non-resident
  GTK module.
- Don't explicitly download the file lists when using pk-command-not-found

* Tue Sep 29 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.3-0.2.20090928git
- Do not build smart support on RHEL.

* Mon Sep 28 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.3-0.1.20090928git
- Update to a newer git snapshot from the 0.5.x series.
- Fixes command-not-found functionality
- Lots of updated translations
- Lots of updates and bugfixes to the experimental glib2 library

* Mon Sep 21 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.3-0.1.20090921git
- Update to a newer git snapshot from the 0.5.x series.
- Updates to the experimental glib2 bindings
- Lots of updated translations.
- Disable the self tests to reduce the build time
- Fix crasher for 64 bit users of the codec installer
- Fix 'pkcon remove foo', where foo needed reqs to be removed too.
- Fixes #523861

* Tue Sep 15 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.3-0.1.20090915git
- Update to a newer git snapshot from the 0.5.x series.
- Lots of updated translations.
- Refresh the free licenses from the Fedora wiki. Fixes #519394
- The fixed packagekit-qt should also now allow KPackageKit to build.

* Mon Sep 07 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.2-1
- Update to 0.5.2.
- Many new and updated translations.
- Many small bugfixes and speedups.
- Added the PostscriptDriver rpm provides functionality.

* Thu Sep 03 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.2-0.1.20090903git
- Update to a newer git snapshot from the 0.5.x series.
- Fixes NetworkManager build time configure check.
- Don't backtrace if we need to do yum-complete-transaction.

* Thu Sep  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.5.2-0.2.20090902git
- Rename -debuginfo-install to debug-install (#520965)

* Wed Sep 02 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.2-0.1.20090902git
- Update to a newer git snapshot from the 0.5.x series.
- Should fix some issues with KPackageKit.

* Sat Aug 29 2009 Christopher Aillon <caillon@redhat.com> - 0.5.2-0.2.20090824git
- Fix build against polkit, rebuild against newer libnm_glib

* Mon Aug 24 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.2-0.1.20090824git
- Update to a newer git snapshot from the 0.5.x series.
- Enable GUdev functionality and create a device-rebind subpackage.

* Wed Aug 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.2-0.1.20090819git
- Update to a git snapshot from the 0.5.x series.

* Mon Aug 03 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.1-1
- New upstream version, many bugfixes and performance fixes
- Fixes #491859, #513856, #510874, #513376, #472876, #514708 and #513557

* Mon Jul 27 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.1-0.1.20090727git
- Update to a git snapshot from the 0.5.x series.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.0-1
- New upstream version, many bugfixes and a few new features
- Fixes #483164, #504377, #504137, #499590, #506110 and #506649

* Thu Jun 25 2009 Richard Hughes  <rhughes@redhat.com> - 0.5.0-0.1.20090625git
- Update to a git snapshot from the 0.5.x series.
- Many PolicyKit fixes
- Fixes GetDistroUpgrades (#508022)

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.9-0.2.20090616git
- Apply a patch to convert to the PolKit1 API.
- Do autoreconf and automake as the polkit patch is pretty invasive
- Fix up file lists with the new polkit action paths

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.9-0.1.20090616git
- Don't hardcode network access to install or update packages
- Add subclasses to our registered mime-types
- Fix results from GetDistroUpgrades()
- Format the package_id before showing it in the error detail
- Download the ChangeLog data when we get the update list
- Never return FALSE from StateHasChanged()
- Fixes #506110, #504137, #499590 and #483164

* Mon Jun 05 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.8-1
- New upstream version, many bugfixes and performance fixes
- Fixes #487614, #500428 and #502399

* Tue May 05 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.7-1
- New upstream version, many bugfixes and performance fixes
- Remove upstreamed patches

* Tue Apr 14 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-3
- Backport 4 important patches from upstream.

* Thu Apr 02 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-2
- Fix installing local files with a unicode path. Fixes #486720
- Fix the allow cancel duplicate filtering with a patch from upstream.

* Mon Mar 30 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-1
- New upstream version

* Tue Mar 24 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-0.3.20090324git
- Update to todays git snapshot with fixed ChangeLog functionality.

* Mon Mar 23 2009 Matthias Clasen  <mclasen@redhat.com> - 0.4.6-0.2.2009319git
- Make the GTK+ module resident

* Thu Mar 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-0.1.20090319git
- Update to todays git snapshot so we can test the update ChangeLog feature.

* Mon Mar 16 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.5-2
- Add two patches from upstream:
 - Allow users to turn off update cache to try to debug #20559
 - Filter out duplicate updates to fix #488509

* Mon Mar 09 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.5-1
- New upstream version
- Add proper error handling to avoid exiting the script on correctable errors
- Add support for the 'any' provide search
- Updated QPackageKit soname version to 0.4.1
- Lots of translation updates

* Tue Feb 24 2009 Matthias Clasen <mclasen@redhat.com> - 0.4.4-4
- Make -docs noarch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.4-2
- Bump for rebuild.

* Mon Feb 23 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.4-1
- New upstream version
- Mainly bugfixes

* Mon Feb 02 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.3-1
- New upstream version
- Mainly bugfixes

* Mon Jan 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.2-1
- New upstream version
- Enable time estimation by default
- Remove the udev helper from PackageKit now the core functionality is in
  udev itself
- Lots of bug fixes

* Thu Jan 08 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.1-1
- New upstream version
- Use NetworkManager to get the network device type for session policy decisions
- Lots of bug fixes

* Tue Dec 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.4.0-1
- New upstream version
- Now integrates with BASH suggesting replacements and offering to install
  missing packages.
- Now integrates with Pango using a gtk-module to install missing fonts.
- Much tighter security model and new audit logging framework.
- Lots of new, untested, code so probably not a good idea for F10.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.11-2
- Rebuild for Python 2.6

* Mon Nov 24 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.11-1
- New upstream version
- http://gitweb.freedesktop.org/?p=packagekit.git;a=blob;f=NEWS

* Thu Nov 20 2008 Richard Hughes <rhughes@redhat.com> - 0.3.10-2
- Update the summary to be more terse.

* Tue Nov 11 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.10-1
- New upstream version
- Drop all upstreamed patches

* Wed Nov 05 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-4
- Increase the timeout for cleaning up unused transactions. Due to a bug
  in the PkClient library the new TID was not being requested, and the old
  TID was being re-used. This gave a DBUS error if the user spent longer than
  five seconds entering the password the very first time they used PackageKit
  to do an authentication.
  Apply a simple patch to mitigate this, as a more invasive (and correct)
  patch is upstream. A new release will follow in f10-updates. Fixes #469950

* Thu Oct 28 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-3
- Install the usr/share/cmake/Modules/FindQPackageKit.cmake file so we
  can build KPackageKit from svn head.
- Fix installing the preupgrade package when we check for distro upgrades
  on machines with 32 and 64 bit versions available. Fixes #469172

* Tue Oct 28 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-2
- Apply a couple of patches from upstream to fix development filtering
  and installing the web plugin.

* Mon Oct 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-1
- New upstream version
- Many new and updated translations.
- Lots of bugfixes (#468486, #466006, #468602), no new features.

* Fri Oct 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3.8-6
- Customize Vendor.conf for Fedora

* Fri Oct 24 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-5
- Bump as I forgot to add the patch.

* Fri Oct 24 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-4
- Add a patch from upstream to change the servicepack metadata format to be
  forwards compatible so we don't let the user create invalid packs.

* Thu Oct 23 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-3
- Add a patch from upstream to pkcon install foo

* Tue Oct 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.3.8-2
- Obsoletes: packagekit-qt(-devel)/qpackagekit(-devel)
- cleanup deps

* Mon Oct 20 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-1
- New upstream version
- Many new and updated translations.
- Merge in the QPackageKit QT library from Adrien BUSTANY

* Mon Oct 20 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.3.7-3
- -browser-plugin: Requires: mozilla-filesystem

* Mon Oct 20 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.7-2
- Rename as newest upstream has QT binding also:
 * PackageKit-libs -> PackageKit-glib
 * PackageKit-devel -> PackageKit-glib-devel
- Add a BR for comps, and create a link that from the comps icons for the
  new category group icons.
- Create a subpackage for devel files required for out-of-tree backends.

* Mon Oct 13 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.7-1
- New upstream version
- Add dynamic groups functionality to the API
- Many performance and other bugfixes

* Thu Oct 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-3
- Add a patch from upstream to fix #466290

* Mon Oct 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-2
- Upload new sources. Ooops.

* Mon Oct 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-1
- New upstream version
- Renice the spawned process so that we don't hog the system when doing updates

* Wed Oct 01 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.5-4
- Rename the subpackages before David blows a blood vessel.
- yum-packagekit  -> PackageKit-yum-plugin
- udev-packagekit -> PackageKit-udev-helper

* Tue Sep 30 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.5-3
- Fix a bug where the daemon could crash when cancelling a lot of transactions.
- Fix installing codecs with a 64 bit machine

* Tue Sep 30 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.5-2
- Obsolete more releases of codeina to fix upgrades on rawhide.

* Mon Sep 29 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.5-1
- New upstream version
- Add a helper which can be used by GStreamer to install codecs.
 
* Thu Sep 25 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-5
- When returning results from a cache we should always return finished in an
  idle loop so we can block and wait for a response
- This fixes the bug where if you have two GetUpdates in the queue the second
  would hang waiting for the first, even though it had already finished.

* Tue Sep 23 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-4
- Fix the error dialog when no mirrors are found

* Tue Sep 23 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-3
- Don't try to run all the committed transactions at once with a deep queue.
- This fixes the bug where the dispatcher would sometimes fail to run the
  next method and PkSpawn would warn the user with 'timeout already set'.

* Tue Sep 23 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-2
- Don't send ::Finished when the script exits because of a dispatcher exit.
- This only seems to happen when we are making the dispatcher be reloaded
  from multiple sessions with different locales.

* Mon Sep 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-1
- New upstream version

* Tue Sep 17 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.3-3
- Fix a silly typo where we might upgrade the kernel when we check for
  distro upgrades.

* Tue Sep 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.3-2
- Fix an error where we didn't connect up the GetDistroUpgrades in
  the new dispatcher code.

* Tue Sep 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.3-1
- New upstream version
- Fixes a nasty bug where the daemon could get locked under heavy load
- Adds collection support for group install and remove

* Wed Sep 10 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.2-3
- Fix an error where we don't check for existing packages in the catalog
  code properly. Also fixes the self tests.

* Wed Sep 10 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.2-2
- Fix a library error so we don't print (null) in the UI.

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.2-1
- New upstream version
- This is the first release with the dispatcher functionality that allows
  backend reuse. This speeds up packagekitd to native speeds when doing
  repeated similar transactions from the same session and locale.

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-7
- Enable the smart backend as it's nearly as complete as the yum backend
- Disable the yum2 backend (0.3.2 will have a dispatcher instead)
- Add subpackages yum and smart, and pull the former in as a dep by default

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-6
- Own /var/cache/PackageKit and /var/cache/PackageKit/downloads
- Fix up some other rpmlint warnings for docs and config(noreplace)

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-5
- Don't explicitly BR libarchive to silence rpmlint

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-4
- Split out a -docs subpackage, which shaves of 324Kb of docs from
  the main package

* Thu Aug 28 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-3
- The browser plugin file list was misordered in the merge, resulting
  in empty PackageKit-devel package.

* Wed Aug 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-2
- Bump as make chainbuild is broken, so we'll have to do this in two steps.

* Wed Aug 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-1
- New upstream version
- Also add two upstream patches to fix pkcon issues.

* Mon Aug 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.0-2
- Bump as the make tag step failed in an obscure way.

* Mon Aug 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.0-1
- Update to newest upstream version. This includes the fixed browser plugin.

* Mon Aug 04 2008 Robin Norwood <rnorwood@redhat.com> - 0.2.4-2
- Fix Source0 URL.

* Tue Jul 30 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.4-1
- New upstream version, only bugfixes.

* Tue Jul 15 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-6
- Silence the output of update-mime-database to fix #454782

* Mon Jun 23 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-5.20080618
- Own the /etc/bash_completion.d directory as we don't depend on the
  bash-completion package. Fixes #450964.

* Wed Jun 18 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-4.20080618
- Pull in a new snapshot from the unstable branch.
- Add the font installing provide hooks

* Mon Jun 11 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-3.20080611
- Pull in a new snapshot from the unstable branch.
- Fixes #450594 where there are insane length error messages
- Get the group for the package when we do ::Detail()

* Mon Jun 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-2.20080609
- Add intltool to the BR.

* Mon Jun 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-1.20080609
- Pull in a new snapshot from the unstable branch.

* Thu May 29 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.2-2.20080529
- Pull in a new snapshot from the unstable branch.

* Mon May 19 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.2-1.20080519
- Pull in a new snapshot from the unstable branch.

* Thu May 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.1-2.20080508
- Pull in a new snapshot from the unstable branch.

* Tue May 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.1-1.20080506
- Pull in a new snapshot from the unstable branch.

* Tue May 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.0-1
- Update to the latest _UNSTABLE_ upstream source

* Mon May  5 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.12-5.20080416git
- Apply patch to fix update detail unbound error.
- Fix rhbz#445086

* Wed Apr 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-4.20080416git
- Urgh, actually upload the correct tarball.

* Wed Apr 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-3.20080416git
- Pull in the new snapshot from the stable PACKAGEKIT_0_1_X branch.
- Fixes #439735.

* Tue Apr 15 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-2.20080415git
- Pull in the new snapshot from the stable PACKAGEKIT_0_1_X branch.
- Fixes #442286, #442286 and quite a few upstream bugs.

* Sat Apr 12 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-1.20080412git
- Pull in the new snapshot from the stable PACKAGEKIT_0_1_X branch.
- Fixes that were cherry picked into this branch since 0.1.11 was released can be viewed at:
  http://gitweb.freedesktop.org/?p=packagekit.git;a=log;h=PACKAGEKIT_0_1_X

* Sat Apr  5 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.11-1
- Update to 0.1.11

* Fri Mar 28 2008 Bill Nottingham <notting@redhat.com> - 0.1.10-1
- update to 0.1.10
- fix glib buildreq

* Fri Mar 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.9-3
- Fix a directory ownership oversight

* Mon Mar 17 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-2
- Make PackageKit require yum-packagekit
- Resolves: rhbz#437539

* Wed Mar  5 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-1
- Update to latest upstream version: 0.1.9
- Enable yum2 backend, but leave old yum backend the default for now

* Thu Feb 21 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.8-1
- Update to latest upstream version: 0.1.8

* Mon Feb 18 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.7-2
- Fix the yum backend.

* Thu Feb 14 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.7-1
- Update to latest upstream version: 0.1.7

* Sat Jan 19 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.6-1
- Update to latest upstream version: 0.1.6

* Fri Dec 21 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.5-1
- Update to latest upstream version: 0.1.5
- Remove polkit.patch for PolicyKit 0.7, no longer needed

* Mon Dec 17 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.4-3
- fix rpm -V issues by ghosting data files
- Resolves: rhbz#408401

* Sun Dec  9 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.4-2
- Make it build against PolicyKit 0.7

* Tue Nov 27 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.4-1
- Update to latest upstream version: 0.1.4
- Include spec file changes from hughsie to add yum-packagekit subpackage

* Sat Nov 10 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.3-1
- Update to latest upstream version: 0.1.3

* Thu Nov 01 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.2-1
- Update to latest upstream version: 0.1.2

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-5
- More issues from package review:
- Need to own all created directories
- PackageKit-devel doesn't really require sqlite-devel
- Include docs in PackageKit-libs

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-4
- use with-default-backend instead of with-backend

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-3
- Add BR: python-devel

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-2
- doc cleanups from package review

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-1
- Update to latest upstream version

* Wed Oct 17 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.0-3
- Add BR for docbook-utils

* Tue Oct 16 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.0-2
- Apply recommended fixes from package review

* Mon Oct 15 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.0-1
- Initial build (based upon spec file from Richard Hughes)
