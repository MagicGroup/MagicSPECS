%global	core_plugins	blur clone commands compiztoolbox composite copytex cube dbus decor fade imgpng imgsvg ini inotify move obs opengl place regex resize rotate scale screenshot switcher water wobbly zoom

%global	gtk_plugins	annotate gnomecompat

%global	obsolete_plugins	decoration fs gconf glib kconfig minimize png svg video

%global	plugins_compiz	%(echo %{core_plugins} %{gtk_plugins} | sed -e 's/\\</compiz-/g')
%global	obsolete_plugins_compiz	%(echo %{obsolete_plugins} | sed -e 's/\\</compiz-/g')

# the plugins to enable by default
# based on intuition and some cribbing from Ubuntu. don't put imgpng
# in here, it will cause pain
%global	default_plugins core composite opengl copytex compiztoolbox decor scale resize gnomecompat staticswitcher place move mousepoll vpswitch regex snap session wall workarounds ezoom

%global git_snapshot e676f1b12eb8db3a76978eed5bfc7c2cf9a0b6ce

Name:           compiz
URL:            http://www.compiz.org
License:        GPLv2+ and LGPLv2+ and MIT
Group:          User Interface/Desktops
Version:        0.9.5.92.1
Release:        0.1.git%{git_snapshot}%{?dist}

Summary:        OpenGL window and compositing manager

# libdrm is not available on these arches
ExcludeArch:   s390 s390x

Requires:	system-logos
Requires: 	glx-utils

BuildRequires:  libX11-devel, libdrm-devel, libwnck-devel
BuildRequires:  libXfixes-devel, libXrandr-devel, libXrender-devel
BuildRequires:  libXcomposite-devel, libXdamage-devel, libXext-devel
BuildRequires:  libXt-devel, libXmu-devel, libICE-devel, libSM-devel
BuildRequires:  gnome-desktop-devel
BuildRequires:  control-center
BuildRequires:  GConf2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  dbus-devel
BuildRequires:  librsvg2-devel
BuildRequires:  metacity-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  kdebase4-workspace-devel plasma-devel
BuildRequires:  fuse-devel
BuildRequires:	cairo-devel
BuildRequires:	libtool
BuildRequires:  libxslt-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  boost-devel
BuildRequires:  glibmm24-devel
#Source0:        http://releases.compiz.org/%{version}/compiz-%{version}.tar.bz2
# git snapshot
# http://gitweb.compiz.org/?p=compiz/core;a=snapshot;h=%{git_snapshot};sf=tgz
Source0:        core-%{git_snapshot}.tar.gz
Source1:        compiz-gtk
Source2:        compiz-gtk.desktop
Source3:        compiz-gnome.desktop
Source4:        compiz-gnome.session

# Patches that are not upstream
#Patch103: composite-cube-logo.patch
Patch105: compiz-0.9-fedora-logo.patch
Patch106: compiz-0.9-redhat-logo.patch
#Patch110: scale-key.patch

# Allow installation of GNOME keybindings without GNOME window manager
# settings stuff (sent upstream)
Patch122: compiz-0.9.2.1-keybindings.patch

%description
Compiz is one of the first OpenGL-accelerated compositing window
managers for the X Window System. The integration allows it to perform
compositing effects in window management, such as a minimization
effect and a cube workspace.  Compiz is an OpenGL compositing manager
that use Compiz use EXT_texture_from_pixmap OpenGL extension for
binding redirected top-level windows to texture objects.

This package contains only the core components necessary for compiz
itself to run. To provide something more usable, you may wish to
install the compiz-gnome, compiz-kde or compiz-gtk package.

%package devel
Summary: Development packages for compiz
Group: Development/Libraries
Requires: compiz = %{version}-%{release}
Requires: pkgconfig
Requires: libXcomposite-devel libXfixes-devel libXdamage-devel libXrandr-devel
Requires: libXinerama-devel libICE-devel libSM-devel libxml2-devel
Requires: libxslt-devel startup-notification-devel

%description devel
The compiz-devel package includes the header files,
and developer docs for the compiz package.

Install compiz-devel if you want to develop plugins for the compiz
windows and compositing manager.

%package gtk
Summary: Compiz GTK+ integration bits
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: libcompizconfig
# A lot of really important plugins are in this
Requires: compiz-plugins-main > 0.9
# For the GNOME keybindings files (doesn't introduce any major deps)
Requires: control-center-filesystem
Requires(post):	desktop-file-utils
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2
Obsoletes: compiz < 0.5.2-8
Conflicts: compiz-gnome < 0.9.2.2-0.6.git619abc05b1
Obsoletes: emerald < 0.8.5-0.5.git90c9604441
Obsoletes: emerald-devel < 0.8.5-0.5.git90c9604441
Obsoletes: emerald-themes < 0.5.2-7

%description gtk
The compiz-gtk package contains gtk-window-decorator,
and other GTK+ integration related stuff.

%package gnome
Summary: Compiz GNOME session
Group: User Interface/Desktops
Requires: compiz-gtk = %{version}-%{release}
Requires: metacity
Requires: gnome-panel
# For now, this is using the ini backend due to a bug when using gconf
# but it should be switched to gconf backend (in libcompizconfig) and
# these requires activated once that's fixed
#Requires: compiz-gconf = %{version}-%{release}
#Requires: compizconfig-backend-gconf > 0.9

%description gnome
The compiz-gnome package contains a session definition which will make
display managers provide a session named 'Classic GNOME with Compiz'
that you can log in to. This session will start a GNOME 2-style desktop
(with gnome-panel, not GNOME Shell) with Compiz as the window manager.
This method is the recommended replacement for the old method of using
desktop-effects to select Compiz as the window manager for a GNOME
session.

%package gconf
Summary: GConf schemas for %{name}
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

%description gconf
This package contains the GConf schemas for plugins in the %{name}
package. Only install it if you wish to use the deprecated GConf
configuration storage scheme for Compiz. Typically you should not
install this.

%package kde
Summary: Compiz KDE integration bits
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: compiz-manager
Requires: compizconfig-backend-kconfig4
Requires: compiz-plugins-main > 0.9

%description kde
The compiz-kde package contains kde4-window-decorator,
and other kde integration related stuff.


%prep
%setup -q -n core

%if 0%{?fedora}
%patch105 -p1 -b .fedora-logo
%else
%patch106 -p1 -b .redhat-logo
%endif
%patch122 -p1 -b .keybindings

%build
rm -rf $RPM_BUILD_ROOT
mkdir build
pushd build
%cmake -DCOMPIZ_DEFAULT_PLUGINS="%{default_plugins}" -DCOMPIZ_PACKAGING_ENABLED=ON -DBUILD_GNOME_KEYBINDINGS=OFF -DCOMPIZ_BUILD_WITH_RPATH=OFF -DCOMPIZ_DISABLE_SCHEMAS_INSTALL=ON -DCOMPIZ_INSTALL_GCONF_SCHEMA_DIR=%{_sysconfdir}/gconf/schemas ..
# Parallel build with -j16 on the cluster failed, though with -j4 on
# dual-core, dual-thread it worked
make VERBOSE=1 
popd

%install
pushd build
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install || exit 1

# This should work, but is buggy upstream:
# make DESTDIR=$RPM_BUILD_ROOT findcompiz_install
# So we do this instead:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
%__cmake -E copy ../cmake/FindCompiz.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules

popd

install %SOURCE1 $RPM_BUILD_ROOT/%{_bindir}

# set up an X session
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions
install %SOURCE3 $RPM_BUILD_ROOT/%{_datadir}/xsessions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-session/sessions
install %SOURCE4 $RPM_BUILD_ROOT/%{_datadir}/gnome-session/sessions

# create compiz keybindings file based on the metacity ones
# lifted straight from Ubuntu, as long as installation of the upstream
# ones is broken at least (I've reported this upstream)
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-launchers.xml > $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-launchers.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-navigation.xml > $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-screenshot.xml > $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-screenshot.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-system.xml > $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-system.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-windows.xml > $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml
	sed -i 's#key=\"/apps/metacity/general/num_workspaces\" comparison=\"gt\"##g' $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
	sed -i 's#key=\"/apps/metacity/general/num_workspaces\" comparison=\"gt\"##g' $RPM_BUILD_ROOT/%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml

desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE2


find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'


%find_lang compiz

cat compiz.lang > core-files.txt

for f in %{core_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> core-files.txt

for f in %{gtk_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> gtk-files.txt

for f in %{core_plugins} %{gtk_plugins}; do
  echo %{_sysconfdir}/gconf/schemas/compiz-$f.schemas
done >> gconf-files.txt

# I don't care how crazy you are, I'm not letting you store your
# compiz-kde configuration in GConf
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/compiz-kde.schemas

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post gtk
update-desktop-database -q %{_datadir}/applications
%gconf_schema_upgrade gwd

%post gconf
%gconf_schema_upgrade %{plugins_compiz}

%pre gconf
%gconf_schema_prepare %{plugins_compiz}
%gconf_schema_obsolete %{obsolete_plugins_compiz}

%pre gtk
%gconf_schema_prepare gwd

%preun gconf
%gconf_schema_remove %{plugins_compiz}

%preun gtk
%gconf_schema_remove gwd

%post kde
update-desktop-database -q %{_datadir}/applications/kde
touch --no-create %{_datadir}/icons/hicolor

%postun kde
touch --no-create %{_datadir}/icons/hicolor


%clean
rm -rf $RPM_BUILD_ROOT


%files -f core-files.txt
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING* README TODO
%{_bindir}/compiz
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%dir %{_datadir}/compiz
%{_datadir}/compiz/cube/images
%{_datadir}/compiz/core.xml
%{_datadir}/compiz/icon.png

%files gtk -f gtk-files.txt
%defattr(-, root, root)
%{_bindir}/compiz-gtk
%{_bindir}/gtk-window-decorator
%{_datadir}/gnome-control-center/keybindings/50-compiz-*.xml
%{_datadir}/applications/compiz-gtk.desktop
# gtk-window-decorator only stores config in gconf at present
%{_sysconfdir}/gconf/schemas/gwd.schemas
#%exclude %{_datadir}/applications/compiz.desktop

%files gnome
%defattr(-, root, root)
%{_datadir}/xsessions/compiz-gnome.desktop
%{_datadir}/gnome-session/sessions/compiz-gnome.session

%files gconf -f gconf-files.txt
%defattr(-, root, root)
%{_sysconfdir}/gconf/schemas/compiz-core.schemas

%files kde
%defattr(-, root, root)
%{_bindir}/kde4-window-decorator
%{_libdir}/compiz/libkde.so
%{_datadir}/compiz/kde.xml

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_libdir}/pkgconfig/compiz-compiztoolbox.pc
%{_libdir}/pkgconfig/compiz-composite.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-opengl.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_datadir}/compiz/xslt
%{_datadir}/compiz/cmake
%{_datadir}/cmake/Modules/FindCompiz.cmake
%{_includedir}/compiz
%{_libdir}/libdecoration.so


%changelog
* Mon Oct 17 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.92.1-0.1.git%{git_snapshot}
- start using git snapshots as the releases suck

* Sat Sep 17 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-4
- more changes for emerald's retirement

* Sat Sep 17 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-3
- add changes for emerald's retirement

* Thu Jul 21 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-2
- rebuild against boost 1.47.0

* Fri Jul 15 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.5.0-1
- new release 0.9.5.0

* Thu Apr 07 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.4-3
- rebuilt against boost 1.46.1

* Mon Mar 28 2011 Adam Williamson <awilliam@redhat.com> - 0.9.4-2
- fix up the GNOME session stuff so it actually works

* Mon Mar 14 2011 Adam Williamson <awilliam@redhat.com> - 0.9.4-1
- new release 0.9.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-0.13.git619abc05b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Leigh Scott <leigh123linux@googlemail.com> - 0.9.2.2-0.12.git619abc05b1
- rebuilt for boost

* Sun Jan 23 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.11.git619abc05b1
- cflags.patch: don't overwrite passed-in CFLAGS

* Wed Jan 19 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.10.git619abc05b1
- adjust GNOME and KDE package requirements

* Tue Jan 18 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.9.git619abc05b1
- drop desktop-effects dependency

* Mon Jan 17 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.8.git619abc05b1
- drop rotate from the default plugin list (it goes with cube)
- tighten up dependencies and fix compiz-kde deps

* Mon Jan 17 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.7.git619abc05b1
- move gwd.schemas into compiz-gtk: seems that gtk-window-decorator is
  only able to store its config in gconf for now so we must include this

* Mon Jan 17 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.6.git619abc05b1
- add a compiz-gnome package back again: this one provides a session
  definition so you can log into a classic GNOME plus Compiz session
  from the login manager

* Sun Jan 16 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.5.git619abc05b1
- drop imgpng from default plugins list (somehow this causes compiz-gtk
  to crash on start)
- generally simplify the default plugin set a bit

* Sun Jan 16 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.4.git619abc05b1
- move core gconf schema file to gconf subpackage

* Sun Jan 16 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.3.git619abc05b1
- move the GConf schemas to a separate subpackage so you can not
  install them unless you really want them
- rename the -gnome subpackage to -gtk as it's not really GNOME
  specific now

* Sun Jan 16 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.2.git619abc05b1
- drop the BR of metacity as we already BR metacity-devel
- don't load imgsvg by default, do load imgpng
- put all the GConf schemas in the GNOME subpackage, no point having
  them in main and weighing it down with dependencies
- drop the ancient beryl obsoletes
- drop --ignore-desktop-hints from compiz-gtk (no longer valid)

* Sat Jan 15 2011 Adam Williamson <awilliam@redhat.com> - 0.9.2.2-0.1.git619abc05b1
- bump to 0.9 git:
	+ drop several patches now upstreamed
	+ keybindings.patch replaces no-more-gnome-wm-settings.patch
- switch to new cmake buildsystem
- use gconf macros not snippets
- fix up compiz-gtk to just always launch with ccm, the test for gconf
  was done exactly the wrong way around and anyway using the gconf
  backend is a bad idea
- depend on new compiz-plugins-main as lots of vital plugins are in it

* Fri Dec 10 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.6-9
- remove the dupe BR dbus-devel and add BR dbus-glib-devel

* Wed Dec 08 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.6-8
- BR dbus-devel

* Tue Nov 30 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.6-7
- add more upstream gdk fixes

* Wed Nov 17 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.6-6
- Backport fix for corruption bug (RH #614542)

* Thu Oct 14 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.6-5
- Don't rely on deprecated gdk symbol gdk_display.
- Add Br libxslt-devel

* Wed Oct 06 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.8.6-4
- Remove kde-desktop-effects.sh ("Compiz Switcher"), use System Settings instead

* Fri Jul 30 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.6-3
- Some backports from upstream

* Thu Jul 15 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.6-2
- gnome-window-manager-settings is no more ...

* Tue Mar 30 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.6-1
- Update to 0.8.6
- Drop upstreamed patches
- Forward port crashfix from F-12

* Sun Feb 21 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.4-6
- Use ccp if present (RH #532229)

* Sat Feb 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.4-5
- Fix FTBFS (RH #555429)

* Mon Feb 08 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-4
- rebuilt for new kde api
- drop kde4_decorator_build patch
- add kde44-api patch
- drop build requires dbus-qt-devel as it is deprecated in F13

* Mon Jan 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.4-3
- Rebuild against new gnome-desktop

* Sat Jan 16 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-2
- add patch to fix kde decorator build error
- fix source url

* Sat Jan 16 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-1
- update to 0.8.4
- update compiz-0.8.2-wall patch
- drop upstream patches

* Tue Nov 24 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.8.2-21
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Sun Nov 08 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-20
- Remove some other unneeded provides / requires

* Sun Nov 08 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-19
- Remove outdated Conflicts/Requires, RH #528267

* Mon Oct 26 2009 Matthias Clasen <mclasen@redhat.com> - 0.8.2-18
- Better fix for keybindings

* Mon Oct 26 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-17
- Fix was wrong - revert it

* Mon Oct 26 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-16
- Don't ship broken keybindings files RH #530603

* Mon Sep 21 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-15
- Revert pageflip patch

* Mon Aug 24 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-14
- Fix build

* Mon Aug 24 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-13
- Drop desktop-effects
- Make compiz-gnome require desktop-effects
- Drop now redundant requires
- Update kde desktop effects to 0.0.6 (includes its own icon)

* Sat Aug 22 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-12
- Fix build

* Sat Aug 22 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-11
- Fix up the compiz-gtk script

* Fri Aug 07 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-10
- Enable direct rendering and always-swap by default
- Tearing free compiz for INTEL cards ;)

* Sat Aug 01 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-9
- Fix build

* Fri Jul 31 2009 Kristian Høgsberg <krh@redhat.com> - 0.8.2-8
- Add patch to add option to always use glXSwapBuffers.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-6
- Fix build

* Fri Jul 10 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-5
- Move wall plugin from fusion to the main compiz package
- Drop requires on compiz-fusion-gnome

* Fri Jul 10 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-4
- Replace compiz-0.8.2-pin-initial-plugins with a fixed up one
  by Philippe Troin <phil@fifi.org> (RH #473896)

* Mon Jun  8 2009 Matthias Clasen <mclasen@redhat.com> - 0.8.2-3
- Fix handling of --replace in compiz-gtk, _again_

* Tue May 26 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-2
- Add commands plugin
- Fix build

* Mon May 25 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.8.2-1
- Update to 0.8.2
- Drop upstreamed patches

* Sun Apr 05 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-18
- Direct rendering does not mean that we have hw 3D

* Mon Mar 16 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-17
- Fix compiz-gtk script RH #490383

* Sun Mar 15 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-16
- Revert to always using indirect rendering

* Sun Mar 15 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-15
- Improved tfp check, fixes "white screen of death"
- Use direct rendering if the driver supports it (DRI2)

* Sat Feb 28 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-14
- Backport gwd fix from upstream, should fix RH #484056

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-12
- Backport some KDE-4.2 fixes from upstream

* Tue Jan 27 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-11
- Make the terminal keybinding work (RH #439665)

* Thu Dec 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.8-10
- Rebuild against new gnome-desktop

* Mon Dec 08 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-9
- Remove direct rendering check for now

* Sun Dec 07 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-8
- Add 'obs' to default plugin list 
- Improve glx_tfp check

* Fri Dec 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-7
- Readd compiz-0.7.6-utility-windows.patch
- Fix memory leaks

* Thu Dec 04 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-6
- Bugfixes from git head:
	compiz-0.7.8-decoration-placement.patch (RH #218561)
	compiz-0.7.8-fullscreen-top.patch
- Fall back to metacity if GLX_tfp is not present (RH #457816)
- Don't allow command line passed (config) plugins to be unloaded

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.8-5
- Patch and rebuild for new libplasma, BR plasma-devel

* Wed Nov 26 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-4
- Rebuild against new gnome-desktop

* Sat Nov 08 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-3
- Add obs plugin

* Sat Nov 08 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-2
- Fix sources file

* Sat Nov 08 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.8-1
- Update to 0.7.8
- Dropped patches:
	compiz-0.7.6-decoration-size.patch
	compiz-0.7.6-metacity-spacer.patch
	compiz-0.7.6-utility-windows.patch
	compiz-0.7.6-multi-screen-fix.patch

* Mon Oct 27 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.6-17
- Update some translations for the desktop-effects capplet

* Wed Oct 22 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-15
- Fix handling of utility windows (RH #466622)
- Handle sync alarm events on all screens

* Wed Oct 22 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-14
- Add missing bits to the patch (RH #446457)

* Fri Oct 17 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-13
- Patch configure rather than configure.ac

* Wed Oct 15 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-12
- Backport upstream patch to fix RH #446457

* Thu Sep 25 2008 Jon McCann <jmccann@redhat.com> - 0.7.6-11
- Add compiz-gtk driver script and desktop file
- New desktop effects release

* Tue Aug 26 2008 Adam Jackson <ajax@redhat.com> 0.7.6-10
- Fixed Requires: Xorg >= foo to Conflicts: Xorg < foo.

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7.6-9
- fix license tag

* Tue Jul 15 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.7.6-8
- Rebuild for ppc64

* Mon Jun 23 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-7
- Speed up gconf schema installation

* Fri Jun 13 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-6
- Don't use desktops and viewports at the same time

* Wed Jun 11 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-5
- Revert to old gconf schmema install script

* Tue Jun 10 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-4
- Disable kde3 to fix local builds (RH #449123)

* Thu Jun 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-3
- Only move placed windows on decoration size changes

* Thu Jun 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-2
- Don't require compiz-fusion in the main package

* Thu Jun 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.6-1
- Update to 0.7.6
- Install all gconf schemas at once
- Drop unneeded patches
- Use wall instead of plane

* Thu Jun 05 2008 Caolán McNamara <caolanm@redhat.com> - 0.7.2-6
- rebuild for dependancies

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.2-5
- Rebuild for KDE 4.0.80

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.2-4
- Backport upstream patch to port kde4-window-decorator to KDE 4.1 libplasma

* Thu Mar 27 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.2-3
- Fix gconf plugin loop RH #438794, patch based on 
  older one from Guillaume Seguin
- Add core to default plugin list

* Wed Mar 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.2-2
- Reword kde-desktop-effects messages to mention Compiz by name (#438883)

* Mon Mar 24 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.2-7
- Autorebuild for GCC 4.3

* Thu Jan 17 2008 Kristian Høgsberg <krh@redhat.com> - 0.6.2-6
- Update to desktop-effects version 0.7.17 which include more
  translations and move desktop-effects translations to compiz-gnome.
- Fix spelling in beryl-core obsoletes.

* Mon Jan 07 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.2-5
- Update buildrequires (kwd uses the kde3 api) 

* Tue Nov  6 2007 Stepan Kasal <skasal@redhat.com> - 0.6.2-4
- Fix a typo in description of the main package.
- All descriptions should end with a dot (unlike the summary line)

* Thu Oct 25 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.2-3
- Include kde-desktop-effects in kde subpackage

* Tue Oct 23 2007 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.2-2
- Obsolete berly-core

* Mon Oct 22 2007 Warren Togami <wtogami@redhat.com> - 0.6.2-1
- 0.6.2

* Fri Oct 12 2007 Kristian Høgsberg <krh@redhat.com> - 0.6.0-2
- Disable scale corner initiate and install a GNOME key config entry.

* Wed Oct 10 2007 Warren Togami <wtogami@redhat.com> - 0.6.0-1
- 0.6.0 final
- always-restack-windows-on-map 

* Tue Oct  9 2007 Warren Togami <wtogami@redhat.com> - 0.5.2-14
- Make compiz behave with gnome-terminal (#304051)

* Fri Oct  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.2-13
- Also install gwd.schemas (#319621)

* Thu Sep 20 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-12
- Update to more recent 0.6 branch snapshot (fixes #253575).

* Fri Sep 14 2007 Warren Togami <wtogami@redhat.com> - 0.5.2-11
- compiz-gnome: install core schema so it actually works
- remove unnecessary gconf stuff from %%install

* Tue Aug 28 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-9
- Make compiz-gnome Obsolete the older compiz package so yum/anaconda
  will pull it in (thans to Adel Gadllah).

* Wed Aug 22 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-8
- Bump to desktop-effects 0.7.7 to avoid kill decorator when popping
  up dialog.
- Fix broken gconf install and uninstall rules.
- Pick up shadowman logo for RHEL builds (#232398).

* Tue Aug 21 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-7.0ec3ec
- Add more-sm-junk.patch so we set SM restart style to
  SmRestartIfRunning on exit (#247163, #245971).
- Add Requires to compiz-devel (#253407).
- Update to desktop-effects 0.7.6, which terminates decorator when
  switching to metacity or on compiz failure (#215247, #215032).

* Fri Aug 17 2007 Adel Gadllah <adel.gadllah@gmail.com> 0.5.2-6.0ec3ec
- Split into gnome and kde subpackages
- Minor cleanups

* Wed Aug 15 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-5.0ec3ec
- Reorder plugin list to avoid 'place' getting removed on startup.
- Add run-command-key.patch to put the run command key in the GNOME
  keyboard shortcut dialog (#213576).
- Drop a bunch of obsolete patches.
- Bump mesa-libGL and X server requires to fix TFP bugs for
  power-of-two textures (#251935).
- Rebase fedora-logo and composite-cube-logo patch.

* Tue Aug 14 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-4.0ec3ec
- Build with desktop-effects so we don't pick up metacity work spaces.
  Fixes #250568.

* Tue Aug 14 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-3.0ec3ec
- Build git snapshot from fedora branch at
  git://people.freedesktop.org/~krh/compiz, brances from 0.6 upstream
  branch.
- Fixes #237486.

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-3
- Require desktop-effects 0.7.3 and gnome-session 2.19.6-5 which pass
  'glib' on the command line too.

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-2
- Move xml meta data files to main package.

* Thu Aug  9 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-1
- Update to 0.5.2.
- Require at least gnome-session 2.19.6-2 so gnome-wm starts compiz
  with LIBGL_ALWAYS_INDIRECT set.

* Wed Jun 27 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.3.6-10
- Rebuild against new libwnck

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.3.6-9
- Don't install INSTALL

* Mon Apr 16 2007 Kristian Høgsberg <krh@hinata.boston.redhat.com> - 0.3.6-8
- Update metacity build requires to metacity-devel.

* Wed Apr  4 2007 Kristian Høgsberg <krh@hinata.boston.redhat.com> - 0.3.6-7
- Fix typo in ./configure option.

* Wed Apr  4 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-6
- Add place and clone plugins to default plugin list.

* Wed Mar 28 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-5
- Update URL (#208214).
- Require at least metacity 2.18 (#232831).
- Add close-session.patch to deregister from SM when replaced (#229113).

* Tue Mar 27 2007 Kristian Høgsberg <krh@redhat.com> 0.3.6-4
- Explicitly disable KDE parts (#234128).

* Mon Mar 26 2007 Matthias Clasen <mclasen@redhat.com> 0.3.6-3
- Fix some directory ownership issues (#233825)
- Small spec cleanups

* Tue Feb  6 2007 Kristian Høgsberg <krh@redhat.com> 0.3.6
- Require gnome-session > 2.16 so it starts gtk-window-decorator.
- Update to desktop-effects 0.7.1 that doesn't refuse to work with Xinerama.

* Tue Jan 16 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-1
- Update to 0.3.6, update patches.
- Drop autotool build requires.
- Drop glfinish.patch, cow.patch, resize-offset.patch and icon-menu-patch.
- Add libdecoration.so
- Update to desktop-effects-0.7.0, which spawns the right decorator
  and plays nicely with unknown plugins.

* Sat Nov 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.4-2
- Update the fedora logo patch (#217224)

* Thu Nov 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.2-2
- Use cow by default, bug 208044

* Fri Nov 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Drop upstreamed patches
- Work with new metacity theme api

* Mon Oct 2 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.32.20060818git.fc6
- Install the .desktop file with desktop-file-install. Add X-Red-Hat-Base to make it appear in "Preferences", rather than "More Preferences".

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.31.20060818git.fc6
- Add buildrequires on intltool

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.31.20060818git.fc6
- Build

* Fri Sep 29 2006 Soren Sandmann <sandmann@redhat.com>
- Update to desktop-effects-0.6.163, which has translation enabled. (Bug 208257)

* Thu Sep 28 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.30.20060817git.fc6
- Add patch to terminate keyboard moves when a mouse buttons is pressed. (Bug 207792).

* Thu Sep 28 2006 Soren Sandmann <sandmann@redhat.com>
- Change default plugin list to not include the plane plugin. (Bug 208448).
- Change default keybinding for shrink to be Pause (Bug 206187).

* Wed Sep 27 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to show a menu when the window icon is clicked. (Bug 201629).

* Tue Sep 26 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.29.20060817git.fc6
- Add restart.patch to make compiz ask the session manager to restart it
  if it crashes (bug 200280).

* Mon Sep 25 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.28.20060817git.fc6
- Change plane.patch to not do cyclical window movement in dimensions
  where the desktop has size 1 (bug 207263).

* Thu Sep 21 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix resizing smaller than minimum size (resize-offset.patch, bug 201623).

* Tue Sep 19 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.27.20060817git.fc6
- Change .plane patch to 
  (a) not set the background color to pink in the plane plugin. 
  (b) allow workspaces with horizontal sizes less then 4.

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.26.20060817git.fc6
- Change plane patch to correctly initialize the screen size to the
  defaults (bug 206088).

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com>
- Run update-desktop-database and gtk-update-icon-cache in post. Add icons
  to list of packaged files. Also bump to 0.6.137 of dialog (which just makes
  directories before attempting to install to them).

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com>
- Upgrade to 0.6.107 of the desktop-effects dialog box. Only change is
  that the new version has icons.

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix mispositioning of window decorator event windows (bug 201624)

* Fri Sep 15 2006 Soren Sandmann <sandamnn@redhat.com>
- Upgrade to version 0.6.83 of desktop-effects. (bug 206500)

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to only accept button 1 for close/minimize/maximize (bug 201628)

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix thumbnail sorting (bug 201605)

* Thu Sep 14 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix double clicking (bug 201783).

* Tue Sep 12 2006 Soren Sandmann <sandmann@redhat.com>
- Don't attempt to move the viewport when dx = dy = 0.(last bit of 206088).

* Tue Sep 12 2006 Soren Sandmann <sandamnn@redhat.com>
- Fix plane.patch to draw correctly when no timeout is running. (206088).

* Wed Sep  6 2006 Kristian Høgsberg <krh@redhat.com>
- Update fbconfig-depth-fix.patch to also skip fbconfigs without
  corresponding visuals.

* Tue Sep 5 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.25.20060817git.fc6
- Make number of vertical size configurable

* Tue Sep 5 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.24.20060817git.fc6
- Fix vertical viewport support in the plane patch.

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.23.20060817git.fc6
- Upgrade to 0.6.61 of the dialog

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add libtool to BuildRequires

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add automake and autoconf to BuildRequires 

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add a patch to put viewports on a plane.

* Wed Aug 30 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.21.20060817git.fc6
- Drop gl-include-inferiors.patch now that compiz uses COW and the X
  server evicts offscreen pixmaps automatically on
  GLX_EXT_texture_from_pixmap usage.

* Tue Aug 29 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.20.20060817git.fc6
- Add cow.patch to make compiz use the composite overlay window.

* Fri Aug 25 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.19-20060817git.fc6
- Rebase to desktop-effects 0.6.41

* Fri Aug 25 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.18.20060817git.fc6
- Rebase to desktop-effects 0.6.19 and drop
  desktop-effects-0.6.1-delete-session.patch

* Tue Aug 22 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.17.20060817git.fc6
- Add patch from upstream to also use sync protocol for override
  redirect windows (sync-override-redirect-windows.patch).

* Thu Aug 17 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.16.20060817git.fc6
- Rebase to latest upstream changes which has the rest of the bindings
  rewrite.  Add resize-move-keybindings.patch to make move and resize
  bindings work like metacity.
- Add back scale plugin.

* Thu Aug 10 2006 Ray Strode <rstrode@redhat.com> 0.0.13-0.15.20060721git.fc5.aiglx
- Add Requires: gnome-session 2.15.90-2.fc6 (bug 201473)
- unlink session file on changing wms (bug 201473)

* Thu Aug  3 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.14.20060721git.fc5.aiglx
- Add Requires: gnome-session 2.15.4-3

* Wed Aug  3 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.13.20060721git.fc5.aiglx
- New version of dialog box. Macro the version number.

* Wed Aug  2 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.13.20060721git.fc5.aiglx
- Add 'desktop effects' dialog box.

* Mon Jul 31 2006 Kristian Høgsberg <krh@redhat.com> 0.0.13-0.12.20060721git.fc5.aiglx
- Add libwnck requires.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.11.20060721git.fc5.aiglx
- Bump and build for fc5 AIGLX repo.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.12.20060721git
- Fix gconf hooks.

* Tue Jul 25 2006 Kristian Høgsberg <krh@redhat.com>
- Require system-logos instead.

* Mon Jul 24 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.10.20060721git
- Bump version to work around tagging weirdness.

* Mon Jul 24 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.9.20060721git
- Add devel package and require redhat-logos instead of fedora-logos (#199757).

* Fri Jul 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.8.20060720git
- Add workaround for AIGLX throttling problem.

* Thu Jul 20 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.7.20060720git
- Drop scale plugin from snapshot.

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 0.0.13-0.6.20060717git
- Don't build on s390

* Mon Jul 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.0.13-0.5.20060717git
- Do some changes forced upon us by package review

* Thu Jul 13 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-5.1
- Use sane numbering scheme.

* Fri Jul  7 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-4
- Drop the fullscreen hardcode patch and require X server that has
  GLX_MESA_copy_sub_buffer.

* Tue Jun 27 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-3
- Unbreak --replace.

* Thu Jun 15 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-2
- Add Requires, fix start-compiz.sh.

* Wed Jun 14 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-1
- Spec file for compiz, borrowing bits and pieces from Alphonse Van
  Assches spec file (#192432).
