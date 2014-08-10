
Summary:  MATE Keyboard LED indicator 
Name:     mate-applet-lockkeys
Version:  0.2.0
Release:  4%{?dist}
Group:    Applications/System
License:  GPLv2+
URL:      http://www.zavedil.com/mate-lock-keys-applet/
Source:   http://www.zavedil.com/wp-content/uploads/2013/02/%{name}-%{version}.tar.gz

BuildRequires: gettext
BuildRequires: gtk2-devel
BuildRequires: mate-panel-devel
BuildRequires: popt-devel

Requires: mate-panel

%description
Keyboard LED indicator applet for the MATE desktop environment.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/gschemas.compiled
rm -f $RPM_BUILD_ROOT%{_docdir}/mate-applet-lockkeys/*

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog COPYING README TODO
%{_libexecdir}/lockkeys_applet
%{_datadir}/pixmaps/*.xpm
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/applet_lockkeys.png
%{_datadir}/mate-panel/applets/org.mate.applets.LockkeysApplet.mate-panel-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.LockkeysApplet.service
%{_datadir}/mate-2.0/ui/lockkeys-applet-menu.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.LockkeysApplet.gschema.xml


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.2.0-2
- remvove News
- remove requires mate-panel

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.2.0-1
- initial build for fedora

