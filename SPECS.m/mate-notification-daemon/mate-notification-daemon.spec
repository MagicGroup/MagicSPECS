# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch %(echo %{version} | awk -F. '{print $1"."$2}')

# Settings used for build from snapshots.
%{!?rel_build:%global commit 0280831e27ff5dc2d7c7473cd3bf9041f805299e}
%{!?rel_build:%global commit_date 20131227}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-notification-daemon
Version: 1.11.0
#Release: 1%{?dist}
Release: 2%{?dist}
Summary:        Notification daemon for MATE Desktop
Summary(zh_CN.UTF-8): MATE 桌面的通知服务
License:        GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-notification-daemon.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libcanberra-devel
BuildRequires:  libnotify-devel
BuildRequires:  libwnck-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel

Provides:       desktop-notification-daemon

%description
Notification daemon for MATE Desktop

%description -l zh_CN.UTF-8
MATE 桌面的通知服务。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# needed for git snapshots
#NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-schemas-compile   \
           --with-gtk=2.0

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
        --delete-original                          \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/mate-notification-properties.desktop

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-notification-daemon.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/mate-notification-properties
%{_datadir}/applications/mate-notification-properties.desktop
%{_datadir}/dbus-1/services/org.freedesktop.mate.Notifications.service
%{_datadir}/mate-notification-daemon/mate-notification-properties.ui
%{_libexecdir}/mate-notification-daemon
%{_datadir}/icons/hicolor/*/apps/mate-notification-properties.*
%{_datadir}/glib-2.0/schemas/org.mate.NotificationDaemon.gschema.xml
%{_mandir}/man1/mate-notification-properties.1.gz
%{_libdir}/mate-notification-daemon


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- update to 1.7.0

* Sat Dec 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git20131227.0280831
- make maintainers life easier and use better git snapshot usage, thanks to Björn Esser
- use latest git snapshot, fix rhbz (#1046716)
- add missing changelog entry from package owner
- use --with-gnome --all-name for find locale
- use modern 'make install' macro

* Sat Dec 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-0.1.git9f4203a1
- update to latest git snapshot for rawhide

* Fri Oct 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add provide desktop-notification-daemon , needed for using
- libnotify, otherwise we run in yum probs with other DE's
- remove require libnotify, already called by rpm through BR
- remove BR gsettings-desktop-schemas-devel
- remove gsettings convert file


* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1 release
- Update configure flags
- Update icon scriptlets
- Switch back to old BR style
- Sort BR's in alphabetical order
- Remove explicit variable for libtool in make

* Tue Oct 30 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- change build requires style
- fix ldconfig scriptlet

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-9
- Fix mate-conf scriptlets (again)

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Fix mate-conf scriptlets and bump release version

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Fix post and postun scriptlets

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Add desktop-file-validate and remove only showin for < f18 since desktop-file-utils was updated to the latest version. 

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Remove unneeded pre scriptlet and move post postun scriptlets before install scriptlet

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-4
- fix schema scriptlets
- drop uneeded update-desktop-database scriptlets
- License: GPLv2+
- %%doc AUTHORS COPYING README

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Switch from gconf scriptlets to mate conf scriptlets

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove po_package and add provides field.

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
-Initial build
