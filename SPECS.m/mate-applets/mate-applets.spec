# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.9

# Settings used for build from snapshots.
%{!?rel_build:%global commit c3b48ea39ab358b45048e300deafaa3f569748ad}
%{!?rel_build:%global commit_date 20140211}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-applets
Version:        1.9.0
Release:        2%{?dist}
#Release:        0.1%{?git_rel}%{?dist}
Summary:        MATE Desktop panel applets
Summary(zh_CN.UTF-8): MATE 桌面面板小部件
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-applets.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

#Add patch to fix cpufreq compilation (Thanks Wolfgang)
Patch0:  cpufreq.patch

BuildRequires: libgtop2-devel
BuildRequires: libnotify-devel
BuildRequires: libmateweather-devel
BuildRequires: libwnck-devel
BuildRequires: libnm-gtk-devel
BuildRequires: libxml2-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: mate-common
BuildRequires: mate-settings-daemon-devel
BuildRequires: mate-desktop-devel
BuildRequires: mate-icon-theme-devel
BuildRequires: mate-notification-daemon
BuildRequires: mate-panel-devel
BuildRequires: polkit-devel
BuildRequires: unique-devel
BuildRequires: pygobject3-devel
BuildRequires: startup-notification-devel
Buildrequires: upower-devel
Buildrequires: gtksourceview2-devel
%ifnarch s390 s390x sparc64
BuildRequires: kernel-tools-libs-devel
%endif

Requires: hicolor-icon-theme


%description
MATE Desktop panel applets

%description -l zh_CN.UTF-8
MATE 桌面面板小部件

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .cpufreq
# needed for cpufreq patch
autoreconf -fi

# needed for git snapshots
#NOCONFIGURE=1 ./autogen.sh

%build
%configure   \
    --disable-schemas-compile                \
    --with-gtk=2.0                           \
    --disable-static                         \
    --with-x                                 \
    --enable-polkit                          \
    --enable-networkmanager                  \
    --enable-ipv6                            \
    --enable-stickynotes                     \
    --libexecdir=%{_libexecdir}/mate-applets

make %{?_smp_mflags} V=1

%install
%{make_install}

# remove of gsettings,convert file, no need for this in fedora
# because MATE starts with gsettings in fedora.
rm -f %{buildroot}%{_datadir}/MateConf/gsettings/stickynotes-applet.convert

#make python script executable
#http://forums.fedoraforum.org/showthread.php?t=284962
chmod a+x %{buildroot}%{python_sitelib}/mate_invest/chart.py
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/mate-invest-chart
%{_bindir}/mate-cpufreq-selector
%{python_sitelib}/mate_invest
%{_libexecdir}/mate-applets
%config(noreplace) %{_sysconfdir}/sound/events/mate-battstat_applet.soundlist
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.mate.CPUFreqSelector.conf
%{_datadir}/mate-applets
%{_datadir}/mate-panel/applets
%{_datadir}/dbus-1/services/org.mate.panel.applet.CommandAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.TimerAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.AccessxStatusAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.BattstatAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.CharpickerAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.DriveMountAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.GeyesAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.StickyNotesAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.TrashAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.InvestAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.MateWeatherAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.MultiLoadAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.CPUFreqAppletFactory.service
%{_datadir}/dbus-1/system-services/org.mate.CPUFreqSelector.service
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.battstat.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.charpick.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.geyes.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.multiload.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.stickynotes.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.cpufreq.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.command.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.panel.applet.timer.gschema.xml
%{_datadir}/polkit-1/actions/org.mate.cpufreqselector.policy
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-eyes-applet.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-sticky-notes-applet.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-invest-applet.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-cpu-frequency-applet.svg
%{_datadir}/icons/mate/48x48/apps/ax-applet.png
%{_datadir}/mate/ui/accessx-status-applet-menu.xml
%{_datadir}/mate/ui/battstat-applet-menu.xml
%{_datadir}/mate/ui/charpick-applet-menu.xml
%{_datadir}/mate/ui/drivemount-applet-menu.xml
%{_datadir}/mate/ui/geyes-applet-menu.xml
%{_datadir}/mate/ui/stickynotes-applet-menu.xml
%{_datadir}/mate/ui/trashapplet-menu.xml
%{_datadir}/mate/ui/mateweather-applet-menu.xml
%{_datadir}/mate/ui/multiload-applet-menu.xml
%{_datadir}/mate/ui/cpufreq-applet-menu.xml
%{_datadir}/pixmaps/mate-accessx-status-applet
%{_datadir}/pixmaps/mate-stickynotes
%{_datadir}/pixmaps/mate-cpufreq-applet


%changelog
* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release
- remove gucharmap BR for GTK2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- rebuild for libgtop2 soname bump

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.2-0.1.git20140211.c3b48ea
- update to git snapshot from 2014.02.11
- add improved snapshot usage
- add gtksourceview2-devel BR for stickynotes
- update configure flags
- sort file section

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.1-1
- Update to 1.7.1

* Mon Jan 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.0-1
- update to 1.7.0 release
- update BR's
- add --with-gnome --all-name for find language
- use modern 'make install' macro
- clean up file section
- build without gucharmap support
- update configure flags

* Wed Jan 1 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to 1.6.2 release
- remove upstreamed upower patches

* Sun Nov 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-8
- improve upower-1.0 adjustments

* Thu Nov 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-7
- add patch for build against upower-1.0
- clean up BRs

* Fri Nov 01 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- disable upower BR > f20, until we know to handle upower-1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Dan Horák <dan[at]danny.cz> - 1.6.1-4
- kernel-tools-libs-devel isn't built on s390(x) and sparc64

* Sun Jun 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-3
- bump version

* Sun Jun 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- activate cpufreq applet
- build against mate-character-map instead of gurchmap
- remove stickynotes-applet.convert gsettings convert file
- add runtime require hicolor-icon-theme
- use polkit-devel as BR
- add BR libICE-devel and libSM-devel
- sort files section

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 12 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-2
- Add libnotify-devel and hard requires on libnotify. mate-notification-daemon was switched to libnotify.

* Mon Mar 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to latest upstream release

* Sun Feb 03 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-5
- Fix conflicts with gnome by adding libexec configure flag

* Sun Feb 03 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-4
- Fix dist tag
- Remove duplicate files
- Sort BRs in alphabetical order

* Sat Jan 26 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-3
- bump

* Sat Jan 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-2
- Add missing BR

* Fri Jan 25 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Initial build
