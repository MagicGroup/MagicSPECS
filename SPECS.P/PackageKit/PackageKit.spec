%global _changelog_trimtime %(date +%s -d "1 year ago")

%define gitdate 20141015

%define _default_patch_fuzz 2

Summary:   Package management service
Name:      PackageKit
Version: 1.0.10
Release: 2%{?dist}
License:   GPLv2+ and LGPLv2+
URL:       http://www.freedesktop.org/software/PackageKit/
Source0:   http://www.freedesktop.org/software/PackageKit/releases/%{name}-%{version}.tar.xz

# generated using contrib/generate-md-archive.sh in the PackageKit source tree
Source1:   http://apt.linuxfans.org/magic/3.0/sources/SOURCES.P/PackageKit/cached-metadata.tar

# Fedora-specific: set Vendor.conf up for Fedora.
Patch0:    PackageKit-0.3.8-Fedora-Vendor.conf.patch

Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: shared-mime-info
Requires: comps-extras
Requires: systemd

BuildRequires: glib2-devel >= 2.32.0
BuildRequires: dbus-devel  >= 1.1.1
BuildRequires: dbus-glib-devel >= 0.74
BuildRequires: pam-devel
BuildRequires: libX11-devel
BuildRequires: xmlto
BuildRequires: gtk-doc
BuildRequires: gcc-c++
BuildRequires: sqlite-devel
BuildRequires: NetworkManager-devel
BuildRequires: polkit-devel >= 0.92
BuildRequires: libtool
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: docbook-utils
BuildRequires: gnome-doc-utils
BuildRequires: perl(XML::Parser)
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libgudev1-devel
BuildRequires: xulrunner-devel
BuildRequires: libarchive-devel
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: pango-devel
BuildRequires: fontconfig-devel
BuildRequires: libappstream-glib-devel
BuildRequires: systemd-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libhif-devel >= 0.1.6
%if !0%{?rhel}
BuildRequires: bash-completion
%endif

# functionality moved to udev itself
Obsoletes: PackageKit-udev-helper < %{version}-%{release}
Obsoletes: udev-packagekit < %{version}-%{release}

# No more GTK+-2 plugin
Obsoletes: PackageKit-gtk-module < %{version}-%{release}

# No more zif, smart or yum in Fedora
Obsoletes: PackageKit-smart < %{version}-%{release}
Obsoletes: PackageKit-yum < 0.9.1
Obsoletes: PackageKit-yum-plugin < 0.9.1
Obsoletes: PackageKit-zif < 0.8.13-2

# components now built-in
Obsoletes: PackageKit-debug-install < 0.9.1
Obsoletes: PackageKit-hawkey < 0.9.1
Obsoletes: PackageKit-backend-devel < 0.9.6

# Udev no longer provides this functionality
Obsoletes: PackageKit-device-rebind < 0.8.13-2

# remove F22
Provides: PackageKit-debug-install = %{version}-%{release}
Provides: PackageKit-device-rebind = %{version}-%{release}
Provides: PackageKit-hawkey = %{version}-%{release}
Provides: PackageKit-yum = %{version}-%{release}
Provides: PackageKit-yum-plugin = %{version}-%{release}
Provides: PackageKit-zif = %{version}-%{release}

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%package glib
Summary: GLib libraries for accessing PackageKit
Requires: dbus >= 1.1.1
Requires: gobject-introspection
Obsoletes: PackageKit-libs < %{version}-%{release}
Provides: PackageKit-libs = %{version}-%{release}

%description glib
GLib libraries for accessing PackageKit.

%package cached-metadata
Summary: Cached metadata for PackageKit
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cached-metadata
Cached metadata allows application installers to start instantly on the
LiveCD or installed system without downloading files from the internet or
regenerating the SAT caches. It can safely removed if not required.

%package cron
Summary: Cron job and related utilities for PackageKit
Requires: crontabs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%package glib-devel
Summary: GLib Libraries and headers for PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: dbus-devel%{?_isa} >= 1.1.1
Requires: sqlite-devel%{?_isa}
Obsoletes: PackageKit-devel < %{version}-%{release}
Provides: PackageKit-devel = %{version}-%{release}
Obsoletes: PackageKit-docs < %{version}-%{release}
Provides: PackageKit-docs = %{version}-%{release}

%description glib-devel
GLib headers and libraries for PackageKit.

%package browser-plugin
Summary: Browser Plugin for PackageKit
Requires: gtk2
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: mozilla-filesystem

%description browser-plugin
The PackageKit browser plugin allows web sites to offer the ability to
users to install and update packages from configured repositories
using PackageKit.

%package gstreamer-plugin
Summary: Install GStreamer codecs using PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Obsoletes: codeina < 0.10.1-10
Provides: codeina = 0.10.1-10

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%package gtk3-module
Summary: Install fonts automatically using PackageKit
Requires: pango
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%package command-not-found
Summary: Ask the user to install command line programs automatically
Requires: bash
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%prep
%setup -q
%patch0 -p1 -b .fedora

%build
%configure \
        --disable-static \
%if 0%{?rhel} == 0
        --enable-hif \
        --enable-introspection \
        --enable-bash-completion \
%else
        --disable-bash-completion \
%endif
        --disable-local \
        --disable-silent-rules

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libpackagekit*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/packagekit-plugin.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit-1/extensions/libpackagekit-action-lookup.la

touch $RPM_BUILD_ROOT%{_localstatedir}/cache/PackageKit/groups.sqlite

# create a link that GStreamer will recognise
#pushd ${RPM_BUILD_ROOT}%{_libexecdir} > /dev/null
#ln -s pk-gstreamer-install gst-install-plugins-helper
#popd > /dev/null

# create a link that from the comps icons to PK, as PackageKit frontends
# cannot add /usr/share/pixmaps/comps to the icon search path as some distros
# do not use comps. Patching this in the frontend is not a good idea, as there
# are multiple frontends in multiple programming languages.
#pushd ${RPM_BUILD_ROOT}%{_datadir}/PackageKit > /dev/null
#ln -s ../pixmaps/comps icons
#popd > /dev/null

# ship cached metadata on the LiveCD
# http://blogs.gnome.org/hughsie/2014/08/29/putting-packagekit-metadata-on-the-fedora-livecd/
tar -xf %{SOURCE1} --directory=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %name

%post
# Remove leftover symlinks from /etc/systemd; the offline update service is
# instead now hooked into /usr/lib/systemd/system/system-update.target.wants
systemctl disable packagekit-offline-update.service > /dev/null 2>&1 || :

%post glib -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS NEWS
%dir %{_datadir}/PackageKit
%dir %{_datadir}/PackageKit/helpers
%dir %{_sysconfdir}/PackageKit
%dir %{_localstatedir}/lib/PackageKit
%dir %{_localstatedir}/cache/PackageKit
%ghost %verify(not md5 size mtime) %{_localstatedir}/cache/PackageKit/groups.sqlite
%dir %{_localstatedir}/cache/PackageKit/downloads
%dir %{_localstatedir}/cache/PackageKit/metadata
%if !0%{?rhel}
%{_datadir}/bash-completion/completions/pkcon
%endif
%dir %{_libdir}/packagekit-backend
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%config %{_sysconfdir}/dbus-1/system.d/*
%dir %{_datadir}/PackageKit/helpers/test_spawn
%{_datadir}/PackageKit/icons
%{_datadir}/PackageKit/helpers/test_spawn/*
%{_datadir}/man/man1/pkcon.1.gz
%{_datadir}/man/man1/pkmon.1.gz
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*
%{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_libexecdir}/packagekitd
%{_libexecdir}/packagekit-direct
%{_bindir}/pkmon
%{_bindir}/pkcon
%exclude %{_libdir}/libpackagekit*.so.*
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%ghost %verify(not md5 size mtime) %{_localstatedir}/lib/PackageKit/transactions.db
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_unitdir}/packagekit-offline-update.service
%{_unitdir}/packagekit.service
%{_unitdir}/system-update.target.wants/
%{_libexecdir}/pk-*offline-update
%if 0%{?rhel} == 0
%{_libdir}/packagekit-backend/libpk_backend_hif.so
%endif

%files cached-metadata
%{_datadir}/PackageKit/hawkey/
%{_datadir}/PackageKit/metadata/

%files glib
%{_libdir}/*packagekit-glib2.so.*
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files cron
%config %{_sysconfdir}/cron.daily/packagekit-background.cron
%config(noreplace) %{_sysconfdir}/sysconfig/packagekit-background

%files browser-plugin
%{_libdir}/mozilla/plugins/packagekit-plugin.so

%files gstreamer-plugin
%{_libexecdir}/pk-gstreamer-install
%{_libexecdir}/gst-install-plugins-helper

%files gtk3-module
%{_libdir}/gtk-2.0/modules/*.so
%{_libdir}/gtk-3.0/modules/*.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop

%files command-not-found
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf

%files glib-devel
%{_libdir}/libpackagekit-glib2.so
%{_libdir}/pkgconfig/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%dir %{_includedir}/PackageKit/packagekit-glib2
%{_includedir}/PackageKit/packagekit-glib*/*.h
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gtk-doc/html/PackageKit

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.0.10-2
- 更新到 1.0.10

* Fri Jul 31 2015 Liu Di <liudidi@gmail.com> - 1.0.7-1
- 更新到 1.0.7

* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 1.0.6-1
- 更新到 1.0.6

* Fri Apr 03 2015 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Sat Mar 28 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.5-2
- Backport a crash fix from upstream (#1185544)
- Update cached metadata
- Use license macro for the COPYING file

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.5-1
- Update to 1.0.5
- Backport new missing gstreamer codecs API

* Fri Feb 06 2015 Richard Hughes <rhughes@redhat.com> - 1.0.4-2
- Adapt to the new hawkey API.

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 1.0.4-1
- New upstream release
- Actually inhibit logind when the transaction can't be cancelled
- Add 'quit' command to pkcon
- Automatically import metadata public keys when safe to do so
- Automatically install AppStream metadata
- Do not attempt to run command-not-found for anything prefixed with '.'
- Don't use PkBackendSpawn helpers in compiled backends
- Fix a hard-to-debug crash when cancelling a task that has never been run
- Look for unavailable packages during resolve
- Make pk_backend_job_call_vfunc() threadsafe
- Make pk_backend_repo_list_changed() threadsafe
- Return 'unavailable' packages for metadata-only repos
- Use a thread-local HifTransaction to avoid db3 index corruption

* Mon Nov 17 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.3-2
- Update cached metadata in preparation for F21 release

* Mon Nov 10 2014 Richard Hughes <rhughes@redhat.com> - 1.0.3-1
- New upstream release
- Add support for reinstallation and downgrades
- Be smarter when using the vendor cache

* Tue Oct 21 2014 Richard Hughes <rhughes@redhat.com> - 1.0.1-1
- New upstream release
- Add a KeepCache config parameter
- Do not install the python helpers
- Invalidate offline updates when the rpmdb changes
- Never allow cancelling a transaction twice

* Wed Oct 15 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.1-0.1.20141015
- Update to today's git snapshot

* Tue Sep 16 2014 Richard Hughes <rhughes@redhat.com> - 1.0.0-2
- Add a new subpackage designed for the workstation spin.
- See http://blogs.gnome.org/hughsie/2014/08/29/ for details.

* Fri Sep 12 2014 Richard Hughes <rhughes@redhat.com> - 1.0.0-1
- New upstream release
- Add a D-Bus interface and helpers for offline support
- Do not shutdown the daemon on idle by default
- Refresh the NetworkManager state when the daemon starts
- Remove pk-debuginfo-install
- Remove the events/pre-transaction.d functionality
- Remove the pkexec systemd helpers
- Remove the plugin interface
- Remove various options from the config file

* Tue Sep 02 2014 Richard Hughes <rhughes@redhat.com> - 0.9.5-1
- New upstream release
- Add a new tool called packagekit-direct that can run without a daemon
- Do not commit the transaction manually but instead set the correct state
- Do not log a critical warning when idle exiting
- Fix a crash when refreshing a repo that is not enabled
- Fix a crash when we are cancelling a transaction that has not yet been run
- Regenerate the SAT indexes when refreshing the cache
- Remove remaining time reporting

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.4-3
- Rebuilt for hawkey soname bump

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.4-2
- Rebuilt for gobject-introspection 1.41.4

* Thu Jul 17 2014 Richard Hughes <rhughes@redhat.com> - 0.9.4-1
- New upstream release
- Automatically switch to hif backend when the config file says hawkey
- Fix up a signature mismatch with a libhif signal handler
- Include both available and installed packages in NEWEST filter
- Plug a small leak in the gstreamer-plugin

* Mon Jun 23 2014 Richard Hughes <rhughes@redhat.com> - 0.9.3-1
- New upstream release
- Add PK_ROLE_ENUM_GET_OLD_TRANSACTIONS to get-roles response
- Fix crash when a plugin is using the backend in it's initialization stage
- Make the polkit policy not be desktop-centric
- Port to libhif and rename the backend to "Hif"

* Tue Jun 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.2-7
- Backport an offline updates fix

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.2-5
- Rebuilt for new hawkey

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed May 21 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.2-3
- Don't restart PackageKit after updating itself

* Tue May 13 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.2-2
- Fix parallel kernel package installation

* Tue Apr 29 2014 Richard Hughes <rhughes@redhat.com> - 0.9.2-1
- New upstream release
- Don't crash when polkit_authority_get_sync() fails
- Fix get-roles and remove trailing semicolon on repo-set-data
- Link gstreamer plugin against 1.0 as well
- Only search for packages when shell is interactive
- Reduce logging verbosity in systemd-updates
- Show the full package name and version in the systemd-updates logs

* Fri Apr 11 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.9.1-2
- gstreamer-plugin: Remove unnecessary outdated "Requires: gstreamer" (#1086199)

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 0.9.1-1
- New upstream release
- Assume we don't want to install source packages with pkcon
- Do not install into python_sitelib
- Fall back to a details search for 'pkcon search foo'
- gstreamer-plugin: Link with gstreamer 1.0
- hawkey: Add support for the 'source' filter for queries
- Set an idle IO priority for background threaded transactions
- Set the default cache-age to 'never'

* Fri Mar 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.1-0.8.20140226
- Update to today's master snapshot for an offline updates fix

* Wed Feb 26 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.1-0.7.20140226
- Drop an old xulrunner patch that's no longer needed

* Wed Feb 26 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.1-0.6.20140226
- Update to today's master snapshot

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 0.9.1-0.5.20140217
- Build a snapshot of master which includes all the API used by gnome-software

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-0.4.20140130
- fix Obsoletes (#1064635)

* Wed Feb 12 2014 Richard Hughes <rhughes@redhat.com> - 0.9.1-0.3.20140130
- Switch to using python3

* Tue Feb 04 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-0.2.20140130
- restore -backend-devel subpkg

* Thu Jan 30 2014 Richard Hughes <rhughes@redhat.com> - 0.9.1-0.1.20140130
- Build a snapshot of master which also bumps the soname

* Tue Jan 28 2014 Richard Hughes <rhughes@redhat.com> - 0.8.16-3
- Backport three patches from master
- Fixes using --cache-age when using the hawkey backend
- Adds the shutdown-after-offline-update mode

* Thu Jan 23 2014 Richard Hughes <rhughes@redhat.com> - 0.8.16-2
- Backport two patches from master to fix up problems in the hawkey backend.

* Mon Jan 20 2014 Richard Hughes <rhughes@redhat.com> - 0.8.16-1
- New upstream release
- hawkey: Do not fail when update details are no longer available
- hawkey: Do the refresh-cache transaction in a thread
- hawkey: Support .treeinfo DVD repos
- Set all the proxy settings when using pkcon
- Clear the prepared-updates file only when the update is invalidated
- Do not show an error if GetDepends is not supported
- Do not use the '…' character when talking to plymouth
- Don't use the default main context in sync PkClient methods
- Only scan .desktop files in the datadir

* Mon Jan 06 2014 Václav Pavlín <vpavlin@redhat.com> - 0.8.15-4
- Replace systemctl call with systemd-rpm macros and missing
  macros (#857376)
- Use macros instead of hardcoded paths

* Fri Dec 20 2013 Richard Hughes <rhughes@redhat.com> - 0.8.15-3
- Remove the internal requires of PackageKit-backend.

* Thu Dec 19 2013 Richard Hughes <rhughes@redhat.com> - 0.8.15-2
- Do not build the yum backend, and obsolete the subpackages.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 0.8.15-1
- New upstream release
- Do not update the role when doing the test transaction
- Ignore progressbar start text if it unchanged
- Only show some status values in pkcon after a small delay
- Resolve internally in pkcon to provide a better output
- Use the filter when removing and installing software using pkcon
- Use the system database location when compiling with --enable-local
- hawkey: Actually report progress when using DownloadPackages()
- hawkey: Allow upgrading packages using InstallFiles
- hawkey: Do not enable profiling by default
- hawkey: Do not return available packages that are already installed
- hawkey: Emit percentage events when processing a large transaction
- hawkey: Implement RepairSystem
- hawkey: List the packages in the downgrade warning
- hawkey: Never replace newer metadata with an older copy
- hawkey: Never use a cached sack when installing local packages
- hawkey: Return a better error when the rpmdb is hosed
- hawkey: Try harder to get the package name when cleaning up
- hawkey: Use 'local' for the package-id data for files
- hawkey: Use the correct error code when the lock is required

* Thu Dec 12 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.14-4
- Replace the PackageKit dependency in PackageKit-backend-devel
  with a dep on PackageKit-glib-devel (which it needs for its
  packagekit-plugin.pc file) to stop the multiarch composer from
  pulling in conflicting PackgeKit packages. (#972571)
- Add %%{?_isa} to dbus-devel and sqlite-devel deps.
- Fix group tag for -docs subpackage.
- Drop base package dep in -docs subpackage.

* Sat Dec 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.14-3
- PackageKit many broadcasts messages (#781807)

* Tue Dec 03 2013 Richard Hughes <rhughes@redhat.com> - 0.8.14-2
- Backport a patch from master to fix a crash when getting package history
- Resolves: #1036837

* Mon Dec 02 2013 Richard Hughes <rhughes@redhat.com> - 0.8.14-1
- New upstream release
- Cache the loaded hawkey sacks to save 280ms for repeat transactions
- Deprecate service packs, catalogs and messages
- Do not check processes when updating as this is racy
- Do not hardcode x86_64 as the native architecture for hawkey
- Many daemon speedups for common operations
- Remove PmUtils script helper as pm-utils is dead upstream
- Remove quite a few config options that didn't make sense
- Remove the Udev firmware loading functionality as it's removed from systemd
- Remove the zif backend as nearly all functionality is available in hawkey
- Speed up common operations in lipackagekit-glib

* Fri Nov 22 2013 Richard Hughes <rhughes@redhat.com> - 0.8.13-1
- New upstream release
- Add a systemd packagekit.service file
- Do not abort the daemon if we can't write to a database
- Do not proxy the action states when simulating
- Don't crash if ProxyHTTP is set
- Fix several small memory leaks
- Log all systemd-updates warnings and notices to the journal
- Raise the GLib dep to 2.32
- Remove duplicate assignment of pkcon '-y' option
- hawkey: Lots of bugfixes and new features
- yum: Do not auto-close the rpmdb when running a transaction

* Mon Nov 04 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.12-3
- own %%{_libdir}/packageKit-plugins

* Fri Nov 01 2013 Richard Hughes <rhughes@redhat.com> - 0.8.12-2
- Show some text progress when the offline update is going on

* Fri Oct 18 2013 Richard Hughes <rhughes@redhat.com> - 0.8.12-1
- New upstream release
- Destroy and re-create the control proxy if the server changes
- Do not have duplicate 'interactive' properties
- Do not send the backend a cache age of -308 when using UINT_MAX
- Make PkTask thread-default-context aware
- Resolves: #1016566

* Thu Oct 10 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 0.8.11-3
- -cron: require crontabs instead of cronie (#989090)

* Mon Sep 23 2013 Richard Hughes <rhughes@redhat.com> - 0.8.11-2
- Backport the package history functionality from master and some other
  related bug fixes for gnome-software.

* Mon Sep 02 2013 Richard Hughes <rhughes@redhat.com> - 0.8.11-1
- New upstream release
- Add a few missing subcommands to the help output
- Add a new backend using hawkey that also uses librepo
- Add offline update commands to the pkcon man page
- Make it possible to cancel an offline update
- yum: Do not check for infra packages when getting the update list
- yum: Do not use network access if we're filtering with ONLY_DOWNLOAD
- zif: Do not use network access if we're filtering with ONLY_DOWNLOAD

* Tue Aug 20 2013 Richard Hughes <rhughes@redhat.com> - 0.8.10-2
- Do not build the smart backend, it's about to be removed from Fedora.

* Fri Jul 26 2013 Richard Hughes <rhughes@redhat.com> - 0.8.10-1
- New upstream release
- Actually return the error if any PkClient methods failed
- Add a 'DOWNLOADED' filter to select only packages already in the cache
- Add three pkcon sub-commands for offline updates
- Local active users in the wheel group can install signed packages w/o a password
- Fix a potential segfault when getting the error code for the results
- If the transaction database is missing, show an error and cleanly shutdown
- Only search newest packages when resolving 'pkcon update foo'
- Raise the package process threshold to 5000
- systemd-updates: Do not exit with an error for a race condition
- yum: Only download the offline update packages if not already in the cache
- yum: Use yb.downloadPkgs() to download updates

* Sat Jun 22 2013 Matthias Clasen <mclasen@redhat.com> - 0.8.9-6
- Trim %%changelog

* Thu Jun 13 2013 Richard Hughes <rhughes@redhat.com> - 0.8.9-5
- Backport another fix from master to fix the passwordless install for users
  in wheel group only bug.
- Resolves: #975214

* Thu Jun 13 2013 Richard Hughes <rhughes@redhat.com> - 0.8.9-4
- Backport another fix from master to fix the offline updates feature.
- Resolves: #968936

* Thu Jun 06 2013 Richard Hughes <rhughes@redhat.com> - 0.8.9-3
- Backport 2 fixes from master to increase the maximum number of packages that
  can be processed, and also to fix a race in the offline updates feature.

* Tue May 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.8.9-2
- Make build without bash-completion actually work

* Mon May 20 2013 Richard Hughes <rhughes@redhat.com> - 0.8.9-1
- New upstream release
- Add 'pkcon backend-details' to be get details of the selected backend
- Do not rely on Python2 to write UTF-8 strings
- Update the comps->group mapping for Fedora 19
- When converting to unicode special case YumBaseError

* Thu May 09 2013 Richard Hughes <rhughes@redhat.com> - 0.8.8-2
- Backport a patch from master to fix package selection in gnome-packagekit
- Resolves: #960081

* Wed May 08 2013 Richard Hughes <rhughes@redhat.com> - 0.8.8-1
- New upstream release
- PackageKit now allow local active users to install signed software without
  prompting for authentication. If you need to change this you will need to
  either install a PolicyKit override or just patch the policy file.
- Added Provides property to retrieve which Provides the backend supports
- Allow clients to call org.freedesktop.DBus.Peer
- browser-plugin: Do not crash when running an installed package that is upgradable
- Do not install the bash-completion code in /etc
- Do not use _UTF8Writer when using python3
- Don't abort the daemon if the client requests a property that does not exist
- Don't use the default main context in sync PkClient methods
- Expose the transaction flags on the .Transaction object
- Pause for 10 seconds if an error occurred before restarting systemd-updates
- Remove the prepared-updates file if any relevant state was changed
- Support getting the distro-id from /etc/os-release
- Use PIE to better secure installed tools and also use full RELRO in the daemon
- Use the correct session method to fix font installation in pk-gtk-module
- Write a pre-failure status file in case the update transaction crashes
- yum: Ensure conf.cache is set before repo.cache is created
- yum: Ignore errors when removing packages to work out the requires list
- zif: Do not issue a critical warning when doing WhatProvides
- zif: Use the same speedup used in libzif upstream

* Thu Apr 04 2013 Kalev Lember <kalevlember@gmail.com> - 0.8.7-4
- Drop the dep on preupgrade

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 0.8.7-2
- Rebuilt for new libarchive

* Wed Jan 16 2013 Richard Hughes  <rhughes@redhat.com> - 0.8.7-1
- New upstream release
- Do not ask for authentication when the transaction is being simulated
- If a simulated only-trusted transaction returns with need-untrusted
  then re-simulate with only-trusted=FALSE
- systemd-updates: Don't show 'Update process 99% complete'
- The GStreamer provide name is gstreamer1() not gstreamer1.0()
- Use /dev/tty or /dev/console where available

* Mon Nov 26 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.6-1
- New upstream release
- Don't search in command-not-found if backend is known to be too slow
- Correctly match the installed file to a package when checking shared libraries
- Do not send the UpdatesChanged signal for only-download or simulate
- Don't throw a cryptic warning when 'pkcon update' has no packages needing an update
- Emit RequireRestart(system) in a PackageKit daemon plugin
- Move the libpackagekit-qt code to a separate project
- Perform the simulation of spawned transactions correctly
- Reinstate 'pkcon list-create' for the service pack functionality
- Show a progressbar if the user presses [esc] during the system update
- yum: Don't crash when resolving groups
- yum: Don't rely on a blacklist for RequireRestart
- yum: Handle NoMoreMirrorsRepoError when using repo.getPackage()
- yum: Only emit the package list once when using WhatProvides() with multiple search terms
- yum: Use a the error NoPackagesToUpdate when there are no updates available
- zif: Don't try to cancel the backend if it's not running

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.5-3
- -yum-plugin: make PK dep versioned

* Mon Oct 29 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.5-1
- New upstream release
- Remove upstreamed patches
- zif: Fix a critical warning when enabling a repository

* Mon Oct 08 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.4-4
- -yum: Requires: yum >= 3.4.3-45

* Thu Oct 04 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.4-3
- Backport some more patches from upstream:
- Never show the DBUS remote error to the user
- Fix the pango_language_matches() parameter list regression
- Don't crash when writing the offline-updates results file
- Only save interesting packages to offline-update-competed
- Resolves: #862161, #857908

* Tue Oct 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.4-2
- yum: Requires: yum >= 3.4.3-35
- PackageKit.conf: StateChangedTimeoutPriority=2 
- backport -qt api/abi change

* Mon Oct 01 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.4-1
- New upstream release
- Suggest a Linux binary if the Solaris name is used
- Use pkttyagent to request user passwords if required
- Ask PackageKit to quit when yum is started

* Tue Sep 18 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.3-4
- Ensure we cancel background transactions when an interactive
  transaction is scheduled.

* Mon Sep 07 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.3-3
- Rework the manaully added requires so that PackageKit-glib doesn't
  pull in so many deps.

* Fri Sep 07 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.3-2
- Work around a yum API break so that resolving still works
- In e42ea3dc0b02ba73a11211de4062e87abfb77a6a yum changed the public API
  so that str(repo) returned 'fedora/18/i386' rather than just 'fedora'.

* Mon Aug 06 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.3-1
- New upstream release
- This is the first release that allows transactions to run in parallel
- The zif backend can run in parallel by default, the yum backend still
  runs each transaction one at a time
- Save the transaction flags when removing packages
- Fix a python backtrace when removing a package
- Add GStreamer 1.0 support to the PackageKit plugin
- Add WritePreparedUpdates config item for admins

* Tue Jul 24 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.2-3
- Fix several reported problems with the offline-update funtionality.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.2-1
- New upstream release
- Bumped sonames for libpackagekit-glib and libpackagekit-qt
- Lots of fixes to systemd-updates offline update functionality
- Remove the Transaction.UpdateSystem() method
- Don't show a warning if /var/run/PackageKit/udev does not exist
- Never run any plugins for simulated actions

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.8.1-8
- fix UL vs ULL type mismatch in qt bindings (#839712)
- tighten subpkg deps with %%_isa

* Tue Jul 09 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-7
- Fix several reported problems with the offline-update funtionality.

* Mon Jul 09 2012 Richard Hughes  <rhughes@redhat.com> - 0.8.1-6
- Fix several reported problems with the offline-update funtionality.

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
