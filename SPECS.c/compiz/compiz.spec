%global    core_plugins    blur clone cube decoration fade ini inotify minimize move place png regex resize rotate scale screenshot switcher video water wobbly zoom fs obs commands wall annotate svg matecompat
 
# List of plugins passed to ./configure.  The order is important
 
%global    plugins         core,png,svg,video,screenshot,decoration,clone,place,fade,minimize,move,resize,switcher,scale,wall,obs


Name:           compiz
URL:            http://www.compiz.org
License:        GPLv2+ and LGPLv2+ and MIT
Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version:        0.8.8
Release:        30%{?dist}
Epoch:          1
Summary:        OpenGL window and compositing manager
Summary(zh_CN.UTF-8): OpenGL 窗口管理器
 
# libdrm is not available on these arches
ExcludeArch:   s390 s390x
 
Source0:       http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
Source1:       compiz-mate-gtk
Source2:       compiz-mate-gtk.desktop
Source3:       compiz-mate-emerald
Source4:       compiz-mate-emerald.desktop
Source5:       compiz-lxde-emerald
Source6:       compiz-lxde-emerald.desktop
Source7:       compiz-xfce-emerald
Source8:       compiz-xfce-emerald.desktop
Source9:       compiz-decorator-gtk
Source10:      gtk-decorator.desktop
Source11:      compiz-decorator-emerald
Source12:      emerald-decorator.desktop
Source13:      compiz-plugins-main_plugin-matecompat.svg
Source14:      emerald-decorator.svg
Source15:      gtk-decorator.svg

# build for aarch64
Patch0:        compiz-aarch64.patch 
# usage of matecompat plugin and marco for gtk-windows-decorator
Patch1:        compiz_new_mate.patch
# Patches that are not upstream
Patch2:        compiz_disable_gdk_disable_deprecated.patch
Patch3:        compiz_composite-cube-logo.patch
Patch4:        compiz_fedora-logo.patch
Patch5:        compiz_redhat-logo.patch
Patch6:        compiz-0.8.6-wall.patch
Patch7:        compiz-0.8.6-new_unloadpluginfix.patch
Patch8:        compiz-0.8.8_incorrect-fsf-address.patch
Patch9:        compiz_new_add-cursor-theme-support.patch
Patch10:       compiz-fix-gtk-window-decorator-no-argb-crash.patch
Patch11:       compiz_fix-no-border-window-shadow.patch
Patch12:       compiz_draw_dock_shadows_on_desktop.patch
Patch13:       compiz_optional-fbo.patch
Patch14:       compiz_call_glxwaitx_before_drawing.patch
Patch15:       compiz_always_unredirect_screensaver_on_nvidia.patch
Patch16:       compiz_fullscreen_stacking_fixes.patch
Patch17:       compiz_damage-report-non-empty.patch
Patch18:       compiz_stacking.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=909657
Patch19:       compiz_primary-is-control.patch
# those patches belongs together, removal of keybindings, mate-windows-settings
# kde, gconf/mateconf, dbus, glib and old metacity checks
Patch20:       compiz_new_remove-keybindings-and-mate-windows-settings-files.patch
Patch21:       compiz_new_remove-kde.patch
# gtk-windows-decorator
Patch22:       compiz_new_remove_mateconf_dbus_glib.patch
Patch23:       compiz_clean_potfiles.patch
Patch24:       compiz_new_remove_old_metacity_checks.patch
Patch25:       compiz_commandline_options_for_button_layout_and_titlebar_font.patch
# new patch series
Patch26:       compiz_get_smclient-id_from_DESKTOP-AUTOSTART-ID.patch
Patch27:       compiz_automake-1.13.patch
Patch28:       compiz_cube-set-opacity-during-rotation-to-70-as-default.patch
# clean dbus
#Patch28:       compiz_remove-rest-of-dbus-code.patch
# clean gconf/mateconf code in gtk-windows-decorator
#Patch29:       compiz_new_removal-gconf.patch

BuildRequires: libX11-devel
BuildRequires: libdrm-devel
BuildRequires: libwnck-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXmu-devel
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: librsvg2-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: fuse-devel
BuildRequires: cairo-devel
BuildRequires: libtool
BuildRequires: libxslt-devel
BuildRequires: marco-devel

Requires:       system-logos
Requires:       glx-utils
# this is an inverse require which is needed for build without gtk-windows-decorator
Requires:       emerald
Requires:       hicolor-icon-theme

# obsolete old compiz versions from f15/f16, rhbz (#997557)
Obsoletes: %{name}-gconf < %{epoch}:%{version}-%{release}
Obsoletes: %{name}-gnome < %{epoch}:%{version}-%{release}
Obsoletes: %{name}-gtk < %{epoch}:%{version}-%{release}
Obsoletes: %{name}-kde < %{epoch}:%{version}-%{release}

 
 
%description
Compiz is one of the first OpenGL-accelerated compositing window
managers for the X Window System. The integration allows it to perform
compositing effects in window management, such as a minimization
effect and a cube work space. Compiz is an OpenGL compositing manager
that use Compiz use EXT_texture_from_pixmap OpenGL extension for
binding redirected top-level windows to texture objects.
 
%package devel
Summary: Development packages for compiz
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: libXcomposite-devel libXfixes-devel libXdamage-devel libXrandr-devel
Requires: libXinerama-devel libICE-devel libSM-devel libxml2-devel
Requires: libxslt-devel startup-notification-devel
 
%description devel
The compiz-devel package includes the header files,
and developer docs for the compiz package.
Install compiz-devel if you want to develop plugins for the compiz
windows and compositing manager.

%package mate
Summary: Compiz mate integration bits
Group: User Interface/Desktops
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
 
%description mate
The compiz-mate package contains the matecompat plugin
and start scripts to start Compiz with emerald and
gtk-windows-decorator.

%package xfce
Summary: Compiz xfce integration bits
Group: User Interface/Desktops
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
 
%description xfce
The compiz-xfce package contains a start script to start
Compiz with emerald.

%package lxde
Summary: Compiz lxde integration bits
Group: User Interface/Desktops
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
 
%description lxde
The compiz-lxde package contains a start script to start
Compiz with emerald.

 
%prep
%setup -q
%patch0 -p1 -b .aarch64
%patch1 -p1 -b .mate
%patch2 -p1 -b .disable_deprecated
%patch3 -p1 -b .composite-cube-logo
%if 0%{?fedora}
%patch4 -p1 -b .fedora-logo
%else
%patch5 -p1 -b .redhat-logo
%endif
%patch6 -p1 -b .wall
%patch7 -p1 -b .unloadfix
%patch8 -p1 -b .incorrect-fsf-address
%patch9 -p1 -b .cursor-theme-support
%patch10 -p1 -b .gtk-window-decorator-no-argb-crash
%patch11 -p1 -b .no-border-window-shadow
%patch12 -p1 -b .draw_dock_shadows
%patch13 -p1 -b .fbo
%patch14 -p1 -b .glxwaitx_before_drawing
%patch15 -p1 -b .always_unredirect_screensaver
%patch16 -p1 -b .fullscreen_stacking
%patch17 -p1 -b .damage-report
%patch18 -p1 -b .stacking
%patch19 -p1 -b .primary-is-control
%patch20 -p1 -b .remove_keybindings
%patch21 -p1 -b .remove_kde
%patch22 -p1 -b .remove_mateconf_dbus_glib
%patch23 -p1 -b .potfiles
%patch24 -p1 -b .old_metacity_checks
%patch25 -p1 -b .commandline_options
%patch26 -p1 -b .get_smclient-id
%patch27 -p1 -b .automake
%patch28 -p1 -b .rotation
#%patch28 -p1 -b .compiz_remove-rest-of-dbus-code.patch
#%patch29 -p1 -b .gconf
 
%build
autoreconf -f -i

%configure \
    --enable-librsvg \
    --enable-gtk \
    --enable-marco \
    --enable-mate \
    --with-default-plugins=%{plugins}
 
make %{?_smp_mflags} imagedir=%{_datadir}/pixmaps
 
 
%install
make DESTDIR=$RPM_BUILD_ROOT install || exit 1

install %SOURCE1 $RPM_BUILD_ROOT%{_bindir}
install %SOURCE3 $RPM_BUILD_ROOT%{_bindir}
install %SOURCE5 $RPM_BUILD_ROOT%{_bindir}
install %SOURCE7 $RPM_BUILD_ROOT%{_bindir}
install %SOURCE9 $RPM_BUILD_ROOT%{_bindir}
install %SOURCE11 $RPM_BUILD_ROOT%{_bindir}

desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE2
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE4
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE6
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE8
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE10
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE12

# matecompat icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
cp -f %SOURCE13 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/plugin-matecompat.svg
# emerald-decorator icon
cp -f %SOURCE14 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/emerald-decorator.svg
# gtk-decorator icon
cp -f %SOURCE15 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/gtk-decorator.svg

rm $RPM_BUILD_ROOT%{_datadir}/applications/compiz.desktop
 
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%find_lang %{name}
 
cat %{name}.lang > core-files.txt
 
for f in %{core_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> core-files.txt
 

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/compiz &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
 
%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/compiz &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/compiz &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/compiz &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post mate -p /sbin/ldconfig

%postun mate -p /sbin/ldconfig

 
 
%files -f core-files.txt
%doc AUTHORS ChangeLog COPYING.GPL COPYING.LGPL README TODO NEWS
%{_bindir}/compiz
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%dir %{_datadir}/compiz
%{_datadir}/compiz/*.png
%{_datadir}/compiz/core.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%files mate
%{_bindir}/gtk-window-decorator
%{_bindir}/compiz-mate-emerald
%{_bindir}/compiz-mate-gtk
%{_bindir}/compiz-decorator-gtk
%{_bindir}/compiz-decorator-emerald
%{_datadir}/applications/compiz-mate-emerald.desktop
%{_datadir}/applications/compiz-mate-gtk.desktop
%{_datadir}/applications/gtk-decorator.desktop
%{_datadir}/applications/emerald-decorator.desktop

%files xfce
%{_bindir}/compiz-xfce-emerald
%{_datadir}/applications/compiz-xfce-emerald.desktop

%files lxde
%{_bindir}/compiz-lxde-emerald
%{_datadir}/applications/compiz-lxde-emerald.desktop
 
%files devel
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_includedir}/compiz/
%{_libdir}/libdecoration.so


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1:0.8.8-30
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:0.8.8-29
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.8-28
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.8-27
- 为 Magic 3.0 重建

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-26
- change BR to marco-devel for f21
- rework remove-keybindings-and-mate-windows-settings-files patch
- rework remove-kde patch
- rwork compiz_remove_mateconf_dbus_glib.patch
- rework compiz_remove_old_metacity_checks.patch
- compiz_cube-set-opacity-during-rotation-to-70-as-default.patch
- switch to libwnck for f21

* Thu Aug 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-25
- obsolete old compiz versions from f15/f16, rhbz (#997557)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-23
- fix windows-decorator scripts and desktop files

* Sun May 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-22
- add patch to speed up start
- remove --sm-disable --ignore-desktop-hints from start scipts
- fix build for aarch64
- add xfce subpackage again with start script and desktop file
- move matecompat plugin to main package
- add requires hicolor-icon-theme
- add scripts and desktop files for switch the windows-decorator to
- mate subpackage
- remove useless compiz_new_add-cursor-theme-support.patch
- complete removal of gconf
- clean up patches
- rename patches and add more descriptions to spec file
- remove unnecessary desktop-file-validate checks
- update icon-cache scriptlets

* Wed May 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-21
- remove compiz-lxde-gtk script and desktop file

* Tue May 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-20
- DISABLE XFCE SUPPORT
- remove xfce subpackage
- move gwd decorator to a subpackage

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-19
- remove compiz-xfce-gtk start script

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-18
- rename compiz_disable_gtk_disable_deprecated.patch

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-17
- remove compiz-xfce-gtk.desktop

* Wed Apr 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-16
- enable gtk-windows-decorator based on marco (mate-window-manager)
- add compiz_disable_gdk_gtk_disable_deprecated patch
- remove dbus
- remove glib
- remove mateconf
- remove kde
- remove keybindings
- add start scripts for gtk-windows-decorator
- update start scripts for emerald
- add ldconfig scriptlet for mate subpackage
- using libmatewnck instead of libwnck

* Wed Feb 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-15
- fix primary-is-control in wall patch

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-14
- add compiz_primary-is-control.patch
- this will set all default configurations to pimary key
- change compiz-wall.patch for set primary is control key
- fix (#909657)

* Fri Jan 04 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-13
- add require emerald again

* Tue Dec 25 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-12
- remove require emerald until it is in fedora stable

* Sat Dec 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-11
- do some major changes
- disable mateconf and use libini text file configuration backend
- remove mateconf from scriptlet section
- move glib annotate svg plugins to core package
- disable gtk-windows-decorator
- drop compiz-mate-gtk compiz session script
- disable gtk-windows-decorator patches
- disable marco/metacity
- disable mate/gnome
- disable mate/gnome keybindings
- insert compiz-mate-emerald compiz session script
- insert compiz-xfce-emerald compiz session script
- insert compiz-lxde-emerald compiz session script
- add emerald as require
- add matecompat icon
- add icon cache scriptlets 


* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-10
- add %%global  plugins_schemas again

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-9
- revert scriptlet change

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- add %%global  plugins_schemas
- change mateconf scriptlets
- remove (Requires(post): desktop-file-utils)
- add some patches from Jasmine Hassan jasmine.aura@gmail.com
- remove (noreplace) from mateconf schema directory
- add desktop-file-validate
- disable mate keybindings for the moment

* Fri Oct 05 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:0.8.8-7
- remove and obsolete compiz-kconfig schema

* Fri Oct 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-6
- remove update update-desktop-database from %%post mate
- remove (noreplace) from mateconf schema dir
- remove Requires(post): desktop-file-utils
- add epoch tags

* Wed Sep 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-5
- change compiz-0.88_incorrect-fsf-address.patch

* Wed Sep 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-4
- remove upstreamed patches
- own include dir
- add compiz-mate-gtk source and compiz-mate-gtk.desktop file
- add keybinding sources
- change %%define to %%global entries
- rename no-more-gnome-wm-settings.patch to no-more-mate-wm-settings.patch
- add compiz-0.88_incorrect-fsf-address.patch
- clean up build section

* Sun Sep 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-3
- add isa tags
- remove kde stuff
- remove obsolete beryl stuff
- add comiz_mate_fork.patch
- remove %%defattr(-, root, root)
- add compiz_gtk_window_decoration_button_placement.patch
- enable some compiz keybindings

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- add compiz_mate_fix.patch

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

* Sun May 06 2012 Andrew Wyatt <andrew@fuduntu.org> - 0.8.8-1
- Update to latest stable release

* Tue Nov 30 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.6-6
- add more upstream gdk fixes

