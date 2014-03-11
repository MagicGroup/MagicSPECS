Name:           mate-control-center
Version:        1.4.0
Release:        10%{?dist}
Summary:        MATE Desktop control-center
License:        LGPLv2+ and GPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz

BuildRequires: gtk2-devel
BuildRequires: desktop-file-utils
BuildRequires: icon-naming-utils
BuildRequires: mate-common
BuildRequires: mate-conf-devel
BuildRequires: mate-corba-devel
BuildRequires: mate-settings-daemon-devel
BuildRequires: mate-desktop-devel
BuildRequires: mate-doc-utils
BuildRequires: mate-menus-devel
BuildRequires: dbus-glib-devel
BuildRequires: libmatekbd-devel
BuildRequires: libmatenotify-devel
BuildRequires: libxklavier-devel
BuildRequires: nss-devel
BuildRequires: polkit-devel
BuildRequires: unique-devel
BuildRequires: mate-window-manager-devel
BuildRequires: librsvg2-devel
BuildRequires: libICE-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libXext-devel
BuildRequires: libXxf86misc-devel
BuildRequires: libxkbfile-devel
BuildRequires: libcanberra-devel
BuildRequires: libSM-devel

Requires(pre): mate-conf
Requires(preun): mate-conf
Requires(post): mate-conf

%description
MATE Desktop Control Center

%package devel
Summary:        Development files for mate-settings-daemon
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-control-center

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh


%build
%configure --disable-static \
           --disable-update-mimedb \
           --disable-schemas-install \
           --disable-scrollkeeper

make %{?_smp_mflags} V=1


%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'
magic_rpm_clean.sh

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/at-properties.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/default-applications.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/display-properties.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/keyboard.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-appearance-properties.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-font-viewer.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-keybinding.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-network-properties.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-settings-mouse.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/mate-theme-installer.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/matecc.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/window-properties.desktop


%pre
%mateconf_schema_prepare control-center fontilus mate-control-center

%preun
%mateconf_schema_remove control-center fontilus mate-control-center

%post
/usr/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
%mateconf_schema_upgrade control-center fontilus mate-control-center

%postun
/usr/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /usr/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_sysconfdir}/mateconf/schemas/control-center.schemas
%{_sysconfdir}/mateconf/schemas/fontilus.schemas
%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas
%{_sysconfdir}/xdg/autostart/mate-at-session.desktop
%{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-appearance-properties
%{_bindir}/mate-at-mobility
%{_bindir}/mate-at-properties
%{_bindir}/mate-at-visual
%{_bindir}/mate-control-center
%{_bindir}/mate-default-applications-properties
%{_bindir}/mate-display-properties
%{_bindir}/mate-font-viewer
%{_bindir}/mate-keybinding-properties
%{_bindir}/mate-keyboard-properties
%{_bindir}/mate-mouse-properties
%{_bindir}/mate-network-properties
%{_bindir}/mate-thumbnail-font
%{_bindir}/mate-typing-monitor
%{_bindir}/mate-window-properties
%{_libdir}/libmate-window-settings.so.1
%{_libdir}/libmate-window-settings.so.1.0.0
%{_libdir}/window-manager-settings/
%{_sbindir}/mate-display-properties-install-systemwide
%{_datadir}/applications/at-properties.desktop
%{_datadir}/applications/default-applications.desktop
%{_datadir}/applications/display-properties.desktop
%{_datadir}/applications/keyboard.desktop
%{_datadir}/applications/mate-appearance-properties.desktop
%{_datadir}/applications/mate-font-viewer.desktop
%{_datadir}/applications/mate-keybinding.desktop
%{_datadir}/applications/mate-network-properties.desktop
%{_datadir}/applications/mate-settings-mouse.desktop
%{_datadir}/applications/mate-theme-installer.desktop
%{_datadir}/applications/matecc.desktop
%{_datadir}/applications/mimeinfo.cache
%{_datadir}/applications/window-properties.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-network-properties.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-preferences-desktop-display.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-typing-monitor.svg
%{_datadir}/mate-control-center/
%{_datadir}/mate/cursor-fonts/*.pcf
%{_datadir}/mate/help/mate-control-center/
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/omf/mate-control-center/
%{_datadir}/polkit-1/actions/org.mate.randr.policy

%files devel
%{_includedir}/mate-window-settings-2.0/
%{_libdir}/pkgconfig/mate-window-settings-2.0.pc
%{_libdir}/libmate-window-settings.so
%{_datadir}/pkgconfig/mate-default-applications.pc
%{_datadir}/pkgconfig/mate-keybindings.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.0-10
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- move unversioned .so back to main package
- fix directory ownership
- fix scriplets
- add missing build requires

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Add disable-update-mimedb to configure flag and update files section

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Remove noreplace bit for schemas 
- Remove ownership of XMLnamespaces and aliases folders
- Remove desktop-file-utils from post and postun requires field
- Add mate-conf to post requires field

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Remove unnecessary explicit libexecdir configure flag, remove explicit requires field

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Fix spelling error on schema install.

* Sun Sep 30 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update BR and remove about-me

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Add excludes to files section as per package review.

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Update files section as per review, update build requires.

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
