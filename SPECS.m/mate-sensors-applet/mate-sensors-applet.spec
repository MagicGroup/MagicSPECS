Name:           mate-sensors-applet
Version:        1.8.0
Release:        3%{?dist}
Summary:        MATE panel applet for hardware sensors
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

Patch0:         mate-sensors-applet_fix-german-translation.patch

BuildRequires:  dbus-glib-devel
BuildRequires:  libatasmart-devel
BuildRequires:  libnotify-devel
BuildRequires:  libXNVCtrl-devel   
BuildRequires:  lm_sensors-devel
BuildRequires:  mate-common
BuildRequires:  mate-panel-devel

%description
MATE Sensors Applet is an applet for the MATE Panel to display readings
from hardware sensors, including CPU and system temperatures, fan speeds
and voltage readings under Linux.
Can interface via the Linux kernel i2c modules, or the i8k kernel modules
Includes a simple, yet highly customization display and intuitive 
user-interface.
Alarms can be set for each sensor to notify the user once a certain value
has been reached, and can be configured to execute a given command at given
repeated intervals.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The mate-sensors-applet-devel package contains libraries and header files for
developing applications that use mate-sensors-applet.

%prep
%setup -q

%patch0 -p1 -b .translation

%build
%configure \
    --disable-static \
    --disable-schemas-compile \
    --enable-libnotify \
    --with-nvidia

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
%{make_install}

find $RPM_BUILD_ROOT -name "*.la" -exec rm -rf {} ';'

%find_lang %{name} --with-gnome --all-name


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libexecdir}/mate-sensors-applet
%{_libdir}/libmate-sensors-applet-plugin.so.*
%{_libdir}/mate-sensors-applet/
%{_datadir}/mate-sensors-applet/ui/
%{_datadir}/pixmaps/mate-sensors-applet/
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/dbus-1/services/org.mate.panel.applet.SensorsAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.sensors-applet.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.sensors-applet.sensor.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.applets.sensors-applet.mate-panel-applet

%files devel
%{_libdir}/libmate-sensors-applet-plugin.so
%{_includedir}/mate-sensors-applet/


%changelog
* Fri Jul 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0.3
- fix german translation

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- use modern 'make install' macro
- add --with-gnome --all-name for find language
- remove --disable-scrollkeeper configure flag

* Sat Jan 4 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- fix bogus date in change log

* Thu Apr 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add --disable-schemas-compile configure flag
- organized %%postun scpriptlet section
- droped specific versioning from BR's
- fix usage of spaces and tabs in spec file
- change BR dbus-glib-devel to gtk2-devel

* Wed Apr 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-1
- update to 1.6.0

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.2-1
- correct source0 download link
- update to 1.5.2 release
- remove unused-direct-shlib-dependency
- remove upstreamed patch
- switch to use libnotify instead of libmatenotify
- fix bogus date in %%changelog:

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.1-2
- initial build for fedora

* Sun Jan 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.1-1
- update to 1.5.1 which fixed
- https://github.com/mate-desktop/mate-sensors-applet/issues/7

* Wed Jan 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-1
- build against official fedora
- remove epoch
- remove BR scrollkeeper

* Mon Nov 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:1.4.0-0102
- add epoch

* Sat Oct 06 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0101
- improve and review spec file
- remove scrollkeeper post and postun requires
- fix scriplet section
- change patch name
- fix license information
- fix postin/un-without-ldconfig
- fix description

* Mon Aug 27 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0100
- build for f18

* Wed Jul 18 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0

* Sun Mar 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-1
- update to 1.2.0

* Tue Feb 21 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686
- enable fedora patches

* Thu Jan 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-1
- update to version 1.1.1

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-sensors-applet.spec based on gnome-applet-sensors-2.2.7-4.fc15 spec

* Thu Nov 18 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2.7-4
- patch and rebuild for new libnotify 0.7.0

