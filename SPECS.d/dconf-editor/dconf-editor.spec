Name:           dconf-editor
Version:        3.19.2
Release:        1%{?dist}
Summary:        Configuration editor for dconf

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/dconf
Source0:        https://download.gnome.org/sources/dconf-editor/3.19/dconf-editor-%{version}.tar.xz

BuildRequires:  /usr/bin/appstream-util
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  vala

%description
Graphical tool for editing the dconf configuration database.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%find_lang dconf

%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/ca.desrt.dconf-editor.appdata.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ca.desrt.dconf-editor.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f dconf.lang
%license COPYING
%{_bindir}/dconf-editor
%{_datadir}/appdata/ca.desrt.dconf-editor.appdata.xml
%{_datadir}/applications/ca.desrt.dconf-editor.desktop
%{_datadir}/dbus-1/services/ca.desrt.dconf-editor.service
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_datadir}/icons/hicolor/*/apps/dconf-editor.png
%{_datadir}/icons/hicolor/scalable/apps/dconf-editor-symbolic.svg
%{_mandir}/man1/dconf-editor.1*

%changelog
* Tue Nov 24 2015 Kalev Lember <klember@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Fri Nov 13 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Ship the man page

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-3
- Fix unowned HighContrast icon theme directories (#1197898)

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-2
- Fix appdata screenshot URL
- Validate appdata during %%check

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Initial Fedora packaging
