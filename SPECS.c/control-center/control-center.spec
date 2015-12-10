%define gettext_package gnome-control-center-2.0

%define glib2_version 2.37.7
%define gtk3_version 3.9.12
%define gsd_version 3.7.3
%define gnome_desktop_version 3.9.90
%define desktop_file_utils_version 0.9
%define redhat_menus_version 1.8
%define gnome_menus_version 3.7.90
%define libXrandr_version 1.2.99

Summary: Utilities to configure the GNOME desktop
Summary(zh_CN.UTF-8): 配置 GNOME 桌面的工具
Name: control-center
Version: 3.18.2
Release: 1%{?dist}
Epoch: 1
License: GPLv2+ and GFDL
#VCS: git:git://git.gnome.org/gnome-control-center
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gnome-control-center/%{majorver}/gnome-control-center-%{version}.tar.xz
URL: http://www.gnome.org

# https://bugzilla.gnome.org/show_bug.cgi?id=695691
Patch0: distro-logo.patch

Requires: gnome-settings-daemon >= %{gsd_version}
Requires: magic-menus >= %{redhat_menus_version}
Requires: gnome-icon-theme
Requires: alsa-lib
Requires: gnome-menus >= %{gnome_menus_version}
Requires: gnome-desktop3 >= %{gnome_desktop_version}
Requires: dbus-x11
Requires: control-center-filesystem = %{epoch}:%{version}-%{release}
# we need XRRGetScreenResourcesCurrent
Requires: libXrandr >= %{libXrandr_version}
# for user accounts
Requires: accountsservice
# For the user languages
Requires: iso-codes
# For the sharing panel
Requires: rygel vino
# For the sound panel
Requires: gnome-icon-theme-symbolic
# For the printers panel
Requires: cups-pk-helper
# For the network panel
Requires: nm-connection-editor
# For the info/details panel
Requires: glx-utils
# For the keyboard panel
Requires: /usr/bin/gkbd-keyboard-display
# For the color panel
Requires: colord

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gdk-pixbuf2-devel >= 2.23.0
BuildRequires: librsvg2-devel
BuildRequires: gnome-desktop3-devel >= %{gnome_desktop_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: libXcursor-devel
BuildRequires: libXrandr-devel >= %{libXrandr_version}
BuildRequires: gettext
BuildRequires: gnome-menus-devel >= %{gnome_menus_version}
BuildRequires: gnome-settings-daemon-devel >= %{gsd_version}
BuildRequires: intltool >= 0.37.1
BuildRequires: libsmbclient-devel
BuildRequires: libsoup-devel
BuildRequires: libXxf86misc-devel
BuildRequires: libxkbfile-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libxml2-devel
BuildRequires: libcanberra-devel
BuildRequires: chrpath
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: pulseaudio-libs-devel libcanberra-devel
BuildRequires: upower-devel
BuildRequires: accountsservice-devel
BuildRequires: ModemManager-glib-devel
BuildRequires: NetworkManager-glib-devel >= 0.9.8
BuildRequires: libnm-gtk-devel >= 0.9.8
BuildRequires: polkit-devel
BuildRequires: gnome-common
BuildRequires: cups-devel
BuildRequires: libgtop2-devel
BuildRequires: iso-codes-devel
BuildRequires: cheese-libs-devel >= 1:3.0.1
BuildRequires: clutter-gtk-devel
BuildRequires: gnome-online-accounts-devel
BuildRequires: colord-devel
BuildRequires: colord-gtk-devel
BuildRequires: libnotify-devel
BuildRequires: docbook-style-xsl
BuildRequires: systemd-devel
BuildRequires: libpwquality-devel
BuildRequires: ibus-devel
BuildRequires: grilo-devel
%ifnarch s390 s390x
BuildRequires: gnome-bluetooth-devel >= 3.9.3
BuildRequires: libwacom-devel
%endif

Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(post): shared-mime-info
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): shared-mime-info

Provides: control-center-extra = %{epoch}:%{version}-%{release}
Obsoletes: control-center-extra < 1:2.30.3-3
Obsoletes: accountsdialog <= 0.6
Provides: accountsdialog = %{epoch}:%{version}-%{release}
Obsoletes: desktop-effects <= 0.8.7-3
Provides: desktop-effects = %{epoch}:%{version}-%{release}
Provides: control-center-devel = %{epoch}:%{version}-%{release}
Obsoletes: control-center-devel < 1:3.1.4-2

%description
This package contains configuration utilities for the GNOME desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.

%description -l zh_CN.UTF-8
GNOME 桌面环境的配置工具。

%package filesystem
Summary: GNOME Control Center directories
Summary(zh_CN.UTF-8): %{name} 的目录
# NOTE: this is an "inverse dep" subpackage. It gets pulled in
# NOTE: by the main package an MUST not depend on the main package

%description filesystem
The GNOME control-center provides a number of extension points
for applications. This package contains directories where applications
can install configuration files that are picked up by the control-center
utilities.

%description filesystem -l zh_CN.UTF-8
%{name} 的目录。

%prep
%setup -q -n gnome-control-center-%{version}

%build
%configure \
        --disable-static \
        --disable-update-mimedb \
        --with-libsocialweb=no \
        --enable-systemd \
        CFLAGS="$RPM_OPT_FLAGS -Wno-error"

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --delete-original			\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  --add-only-show-in GNOME				\
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# we do want this
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties

# we don't want these
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/cursor-fonts

# remove useless libtool archive files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gnome-control-center

%find_lang %{gettext_package} --all-name --with-gnome

%post
/sbin/ldconfig
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{gettext_package}.lang
%doc AUTHORS COPYING NEWS README
%{_datadir}/gnome-control-center/keybindings/*.xml
%{_datadir}/gnome-control-center/pixmaps
#{_datadir}/gnome-control-center/datetime/
%{_datadir}/appdata/gnome-control-center.appdata.xml
%{_datadir}/gnome-control-center/sounds/gnome-sounds-default.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/gnome-control-center/icons/
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.*.policy
%{_datadir}/pkgconfig/gnome-keybindings.pc
%{_datadir}/sounds/gnome/default/*/*.ogg
%{_bindir}/gnome-control-center
%{_libexecdir}/cc-remote-login-helper
%{_libexecdir}/gnome-control-center-search-provider
%{_datadir}/pixmaps/faces
%{_datadir}/man/man1/gnome-control-center.1.*
%{_datadir}/dbus-1/services/org.gnome.ControlCenter.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.ControlCenter.service
%{_datadir}/gnome-shell/search-providers/gnome-control-center-search-provider.ini
%{_datadir}/polkit-1/rules.d/gnome-control-center.rules
%{_datadir}/bash-completion/completions/gnome-control-center

%files filesystem
%dir %{_datadir}/gnome/wm-properties
%dir %{_datadir}/gnome-control-center
%dir %{_datadir}/gnome-control-center/keybindings
%dir %{_datadir}/gnome-control-center/sounds


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1:3.18.1-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:3.18.1-3
- 更新到 3.18.1

* Tue Dec 23 2014 Liu Di <liudidi@gmail.com> - 1:3.14.2-2
- 更新到 3.14.2

* Thu Jul 17 2014 Liu Di <liudidi@gmail.com> - 1:3.13.3-2
- 更新到 3.13.3

* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 1:3.12.0-2
- 更新到 3.12.0

* Thu Mar 13 2014 Liu Di <liudidi@gmail.com> - 1:3.11.91-2
- 更新到 3.11.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.90-2
- Rebuilt for gnome-desktop soname bump

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.5-1
- Update to 3.11.5

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 1:3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 1:3.11.2-1
- Update to 3.11.2

* Wed Nov 13 2013 Bastien Nocera <bnocera@redhat.com> - 1:3.11.1-2
- Add vino dependency

* Thu Oct 31 2013 Florian Müllner <fmuellner@redhat.com> - 1:3.11.1-1
- Update to 3.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.92-1
- Update to 3.9.92

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.91-1
- Update to 3.9.91

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.90.1-2
- Rebuilt for libgnome-desktop soname bump

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.90.1-1
- Update to 3.9.90.1

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.90-1
- Update to 3.9.90
- Drop obsolete build deps

* Thu Aug 15 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.5-2
- Rebuilt with bluetooth support

* Wed Jul 31 2013 Adam Williamson <awilliam@redhat.com> - 1:3.9.5-1
- Update to 3.9.5
- buildrequires libsoup-devel

* Tue Jul 30 2013 Richard Hughes <rhughes@redhat.com> - 1:3.9.3-2
- Rebuild for colord soname bump

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 1:3.9.3-1
- Update to 3.9.3

* Wed Jun 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:3.9.2.1-2
- Add 'Requires: rygel' for the sharing panel

* Mon Jun 03 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.2.1-1
- Update to 3.9.2.1

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 1:3.8.2-1
- Update to 3.8.2

* Mon May 06 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.1.5-1
- Update to 3.8.1.5

* Fri May  3 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.8.1-3
- Improve the distro logo patch

* Tue Apr 16 2013 Ray Strode <rstrode@redhat.com> - 1:3.8.1-2
- Add a requires for the keyboard viewer

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 1:3.8.1-1
- Update to 3.8.1

* Mon Apr  1 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.8.0-3
- Apply the patch, too

* Sun Mar 31 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.8.0-2
- Show the Fedora logo in the details panel

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 1:3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.92-1
- Update to 3.7.92

* Tue Mar 05 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:3.7.91-1
- Update to 3.7.91

* Sat Feb 23 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.90-2
- Buildrequire libsmbclient-devel for the printer panel

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.90-1
- Update to 3.7.90

* Thu Feb 07 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.5.1-1
- Update to 3.7.5.1

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.5-1
- Update to 3.7.5

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:3.7.4-3
- Rebuild for new cogl

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.7.4-2
- Fix linking against libgd

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 1:3.7.4-1
- Update to 3.7.4

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.7.3-1
- Update to 3.7.3
- Drop upstreamed wacom-osd-window patch
- Adjust for the statically linked plugins and panel applet removal

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 1:3.7.1-1
- Update to 3.7.1

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.3-1
- Update to 3.6.3

* Wed Nov 07 2012 Bastien Nocera <bnocera@redhat.com> 3.6.2-2
- Require glx-utils for the info panel

* Tue Oct 23 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.2-1
- Update to 3.6.2

* Mon Oct 08 2012 Bastien Nocera <bnocera@redhat.com> 3.6.1-1
- Update to 3.6.1

* Fri Oct  5 2012 Olivier Fourdan <ofourdan@redhat.com> - 1:3.6.0-2
- Add Wacom OSD window from upstream bug #683567

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 1:3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.92-1
- Update to 3.5.92

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.91-1
- Update to 3.5.91

* Sun Aug 26 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.90-2
- Drop apg dependency, it is no longer used

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.90-1
- Update to 3.5.90

* Sat Aug 18 2012 Debarshi Ray <rishi@fedoraproject.org> - 1:3.5.6-2
- Add Requires: nm-connection-editor (RH #849268)

* Wed Aug 15 2012 Debarshi Ray <rishi@fedoraproject.org> - 1:3.5.6-1
- Update to 3.5.6

* Wed Aug 15 2012 Dan Horák <dan[at]danny.cz> - 1:3.5.5-4
- no wacom support on s390(x)

* Wed Aug 15 2012 Debarshi Ray <rishi@fedoraproject.org> - 1:3.5.5-3
- Rebuild against newer gnome-bluetooth

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.5-1
- Update to 3.5.5

* Mon Jul 02 2012 Dan Horák <dan[at]danny.cz> - 1:3.5.4-2
- fix build on s390(x) without Bluetooth

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.3-1
- Update to 3.5.3

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.2-1
- Update to 3.4.2

* Tue May 08 2012 Bastien Nocera <bnocera@redhat.com> 3.4.1-2
- Disable Bluetooth panel on s390

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.1-1
- Update to 3.4.1

* Thu Apr 12 2012 Marek Kasik <mkasik@redhat.com> - 3.4.0-2
- Add support for FirewallD1 API
- Resolves: #802381

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Tue Mar 20 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Mon Mar 05 2012 Bastien Nocera <bnocera@redhat.com> 3.3.91-1
- Update to 3.3.91

* Wed Feb 22 2012 Bastien Nocera <bnocera@redhat.com> 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> 3.3.5-1
- Update to 3.3.5

* Wed Jan 18 2012 Bastien Nocera <bnocera@redhat.com> 3.3.4.1-1
- Update to 3.3.4.1

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> 3.3.4-2
- Use systemd for session tracking

* Tue Jan 17 2012 Bastien Nocera <bnocera@redhat.com> 3.3.4-1
- Update to 3.3.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> 3.3.2-1
- Update to 3.3.2

* Fri Nov 11 2011 Bastien Nocera <bnocera@redhat.com> 3.2.2-1
- Update to 3.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Bastien Nocera <bnocera@redhat.com> 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90

* Mon Aug 22 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-3
- Fix a crash without configured layouts

* Fri Aug 19 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-2
- Obsolete control-center-devel

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Wed Aug 17 2011 Christoph Wickert <cwickert@fedoraproject.org> - 3.1.4-2
- Fix autostart behavior (#729271)

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Wed Jun 15 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1.1-4
- Rebuild against new gnome-desktop3 libs

* Wed Apr 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1.1-3
- Rebuild against newer cheese-libs

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1.1-1
- Update to 3.0.1.1

* Tue Apr 26 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-1
- Update to 3.0.1

* Thu Apr  7 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0.1-3
- Only autostart the sound applet in GNOME 3 (#693548)

* Wed Apr  6 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0.1-2
- Add a way to connect to hidden access points

* Wed Apr  6 2011 Matthias Clasen <mclasen@redhat.com> 3.0.0.1-1
- Update to 3.0.0.1

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> 2.91.93-1
- 2.91.93

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-4
- Rebuild against newer cheese

* Thu Mar 24 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-3
- Rebuild against NetworkManager 0.9

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update to 2.91.92

* Thu Mar 17 2011 Ray Strode <rstrode@redhat.com> 2.91.91-6
- Drop incomplete "Supervised" account type
  Resolves: #688363

* Tue Mar 15 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-5
- We now replace desktop-effects, with the info panel (#684565)

* Mon Mar 14 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-4
- Add gnome-icon-theme-symbolic dependency (#678696)

* Wed Mar 09 2011 Richard Hughes <rhughes@redhat.com> 2.91.91-3
- Ensure we have NetworkManager-glib-devel to get the network panel
- Explicitly list all the panels so we know if one goes missing

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-2
- Rebuild against NetworkManager 0.9, to get the network panel

* Tue Mar 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-1
- Update to 2.91.91
- Disable libsocialweb support until Flickr integration is fixed upstream

* Mon Feb 28 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.90-2
- Fix a typo in the autostart condition for the sound applet

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.90-1
- Update to 2.91.90

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 1:2.91.6-9
- Rebuild against new libxklavier

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com>  2.91.6-8
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-6
- Add missing apg Requires (#675227)

* Sat Feb 05 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-5
- Fix crasher running region and language with KDE apps installed

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-4
- Fix crasher running date and time on the live CD

* Thu Feb 03 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-3
- Add missing iso-codes dependencies

* Thu Feb 03 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-2
- Rebuild against newer GTK+ 3.x

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-1
- Update to 2.91.6

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Fri Dec 10 2010 Bill Nottingham <notting@redhat.com> 2.91.3-4
- user-accounts: require accountsserivce, obsolete accountsdialog

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-3
- Fix initial window size

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-2
- Rebuild against new gtk

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 2.91.3-1
- Update to 2.91.3

* Fri Nov 12 2010 Adam Williamson <awilliam@redhat.com> 2.91.2-2
- add upstream patch to fix sound module to link against libxml
  https://bugzilla.gnome.org/show_bug.cgi?id=634467

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-2
- Rebuild with a new gnome-settings-daemon

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 1:2.90.1-4
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Bastien Nocera <bnocera@redhat.com> 2.90.1-3
- Force enable libsocialweb support, it's disabled by default

* Fri Sep 24 2010 Bastien Nocera <bnocera@redhat.com> 2.90.1-2
- Add libsocialweb BR for the flickr support in background

* Wed Sep 22 2010 Bastien Nocera <bnocera@redhat.com> 2.90.1-1
- Update to 2.90.1

* Thu Aug 12 2010 Colin Walters <walters@verbum.org> - 1:2.31.6-1
- New upstream

* Wed Jul 21 2010 Bastien Nocera <bnocera@redhat.com> 2.31.5-2
- Trim BuildRequires
- Remove libgail-gnome dependency (#616632)

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.2-1
- Update to 2.31.4.2

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.1-1
- Update to 2.31.4.1

* Wed Jun 23 2010 Bastien Nocera <bnocera@redhat.com> 2.31.3-2
- Add patches to compile against GTK+ 3.x

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Wed Jun  2 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-3
- Add Provides/Obsoletes for the no-longer-existing -extra package

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-2
- Update to 2.31.2
- Remove vendor prefixes from desktop files, since that breaks
  the new shell

* Tue May 11 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-2
- Install PolicyKit policy for setting the default background
  in the right location

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Mon Mar 22 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-3
- Fix crash on exit in gnome-about-me (#574256)

* Wed Mar 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-2
- Remove obsoleted patches

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Wed Feb 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Mon Feb 15 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.90-2
- Properly initialize threads in the appearance capplet

* Wed Feb 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Sun Jan 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.4-2
- Rebuild

* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.4-1
- Update to 2.29.4
- Drop many upstreamed patches
