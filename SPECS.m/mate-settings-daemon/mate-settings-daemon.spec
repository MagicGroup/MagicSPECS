Name:           mate-settings-daemon
Version: 1.9.1
Release: 1%{?dist}
Summary:        MATE Desktop settings daemon
Summary(zh_CN.UTF-8): MATE 桌面的设置服务
License:        GPLv2+
URL:            http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

# To generate tarball
# wget http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-{_internal_version}.tar.xz -O %%{name}-%%{version}.git%%{_internal_version}.tar.xz
#Source0: http://raveit65.fedorapeople.org/Mate/git-upstream/%{name}-%{version}.git%{_internal_version}.tar.xz

BuildRequires:  dbus-glib-devel
BuildRequires:  dconf-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libmatekbd-devel
BuildRequires:  libnotify-devel
BuildRequires:  libSM-devel
BuildRequires:  libXxf86misc-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-polkit-devel
BuildRequires:  nss-devel
BuildRequires:  pulseaudio-libs-devel

Requires:       libmatekbd%{?_isa} >= 0:1.6.1-1
# needed for xrandr capplet
Requires:       mate-control-center-filesystem

%description
This package contains the daemon which is responsible for setting the
various parameters of a MATE session and the applications that run
under it.

%description -l zh_CN.UTF-8
MATE 桌面的设置服务。

%package devel
Summary:        Development files for mate-settings-daemon
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the daemon which is responsible for setting the
various parameters of a MATE session and the applications that run
under it.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q 

%build
%configure                             \
   --enable-pulse                      \
   --disable-static                    \
   --disable-schemas-compile           \
   --enable-polkit                     \
   --disable-gstreamer                 \
   --with-x                            \
   --with-nssdb

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'

# remove needless gsettings convert file
rm -f %{buildroot}%{_datadir}/MateConf/gsettings/mate-settings-daemon.convert

desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/mate-settings-daemon
%dir %{_sysconfdir}/mate-settings-daemon/xrandr
%config %{_sysconfdir}/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_libdir}/mate-settings-daemon
%{_libexecdir}/mate-settings-daemon
%{_libexecdir}/msd-datetime-mechanism
%{_libexecdir}/msd-locate-pointer
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/icons/mate/*/*/*
%{_datadir}/mate-settings-daemon
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy
%{_mandir}/man1/mate-settings-daemon.1.*

%files devel
%{_includedir}/mate-settings-daemon
%{_libdir}/pkgconfig/mate-settings-daemon.pc

%changelog
* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.1-1
- 更新到 1.9.1

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-4
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- use --with-gnome --all-name for find locale
- use modern 'make install' macro
- add man dir

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.3.gitd2d3aa7
- enable pulsaudio support

* Tue Oct 01 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.2.gitd2d3aa7
- add misssing directory for xrandr-capplet function 'system-wide installation'
- add runtime requires mate-control-center-filesystem for xrandr-capplet

* Mon Sep 23 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.1.gitd2d3aa7
- update to latest snapshot
- fix https://github.com/mate-desktop/mate-settings-daemon/issues/32
- remove runtime require mate-icon-theme, no need of it
- remove %%config from desktop file
- remove needless find '*.a'
- switch to pulseaudio, fix rhbz (#1008011)
- cleanup BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1.2
- remove BR gsettings-desktop-schemas-devel
- remove needless gsettings convert file
- clean up BR's
- add versioned runtime require libmatekbd

* Mon Jun 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Sat Jun 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Update libnotify.patch with latest upstream commits

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add libnotify patch

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.7-1
- Update to latest upstream release

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
-Update to latest upstream release
-Convert back to old BR style
-Own dirs we are supposed to own

* Tue Jan 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-3
- Fix icon scriptlets

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.4-2
- Fix broken gstreamer support:
  + add gstreamer BuildRequires
  + disable pulse so we build with gstreamer support
- Add '--disable-static' to %%configure and remove find entries
- Improve description, overall readability, order dependencies and
  minor improvements

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Latest upstream release

* Fri Nov 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-5
- Remove archlinux configure.ac bits.
- REALLY fix CVE-2012-5560

* Fri Nov 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-4
- stop generating version specific libdirs for plugins and fix CVE-2012-5560

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-3
- fix build failures

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- drop mate-corba from br as it is deprecated

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- change build requires style

* Wed Oct 10 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- fix icon scriptlets

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-5
- remove local quirks not needed for fedora buildsys
- simplify %%files, fix some dir-ownership
- cosmetics: move scriptlets to be next to %%files

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Own mate-settings-daemon directory, update build requires and configure flags

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix mateconf scritplets, switch back to upstream source.

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Move shared libs to main package and update buildrequires to add libSM-devel add mateconf scriptlets

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
