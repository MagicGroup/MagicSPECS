# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
#global branch 1.8

# Settings used for build from snapshots.
%{!?rel_build:%global commit c0f0c63c670d799dee4fa7577083d0cbace56db4}
%{!?rel_build:%global commit_date 20140210}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Summary:         Mate user file sharing
Summary(zh_CN.UTF-8): Mate 用户文件共享
Name:            mate-user-share
Version: 1.11.0
Release: 2%{?dist}
#Release: 1%{?dist}
License:         GPLv2+
Group:           System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:             http://mate-desktop.org

%define branch %(echo %{version} | awk -F. '{print $1"."$2}')
# for downloading the tarball use 'spectool -g -R mate-user-share.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  caja-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  yelp-tools
BuildRequires:  gtk2-devel
BuildRequires:  httpd
BuildRequires:  libcanberra-devel
BuildRequires:  libICE-devel
BuildRequires:  libnotify-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  caja-devel
BuildRequires:  mod_dnssd
BuildRequires:  perl(XML::Parser)
BuildRequires:  unique-devel

# disable bluetooth support for bluez5
#BuildRequires: mate-bluetooth-devel
BuildRequires: caja-devel

Requires: httpd
# obsolete with bluez5
%if 0%{?fedora} > 19
#Requires: obex-data-server
%else
Requires: obex-data-server
%endif
Requires: mod_dnssd

%description
mate-user-share is a small package that binds together various free
software projects to bring easy to use user-level file sharing to the
masses.

The program is meant to run in the background when the user is logged
in, and when file sharing is enabled a webdav server is started that
shares the $HOME/Public folder. The share is then published to all
computers on the local network using mDNS/rendezvous, so that it shows
up in the Network location in MATE.

The program also allows to share files using ObexFTP over Bluetooth.

%description -l zh_CN.UTF-8
MATE 用户文件共享。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# nedded to create missing configure and make files
# for git snapshot builds, comment out for release builds
#NOCONFIGURE=1 ./autogen.sh

%build
# disable bluetooth support for bluez5
%configure \
    --disable-static \
    --disable-bluetooth \
    --disable-schemas-compile
make %{?_smp_mflags}

%install
%{make_install}

rm -f $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la

# no need to provide a convert file for mateconf user settings,
# because Mate started with gsettings in f17/18
rm -f $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-user-share.convert
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

# disable bluetooth support for bluez5
rm -f ${RPM_BUILD_ROOT}/%{_sysconfdir}/xdg/autostart/mate-user-share-obexftp.desktop
rm -f desktop-file-validate ${RPM_BUILD_ROOT}/%{_sysconfdir}/xdg/autostart/mate-user-share-obexpush.desktop
desktop-file-validate ${RPM_BUILD_ROOT}/%{_datadir}/applications/mate-user-share-properties.desktop
desktop-file-validate ${RPM_BUILD_ROOT}/%{_sysconfdir}/xdg/autostart/mate-user-share-webdav.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor >&/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc README COPYING NEWS
%{_bindir}/mate-file-share-properties
%{_libexecdir}/mate-user-share
%{_datadir}/mate-user-share/
%{_datadir}/applications/mate-user-share-properties.desktop
# disable bluetooth support for bluez5
%{_sysconfdir}/xdg/autostart/mate-user-share-webdav.desktop
%{_datadir}/icons/hicolor/*/apps/mate-obex-server.png
%{_libdir}/caja/extensions-2.0/*.so
%{_datadir}/glib-2.0/schemas/org.mate.FileSharing.gschema.xml
%{_mandir}/man1/mate-file-share-properties.1.*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.gitc0f0c63
- no need of using 0.4 for a release build
- use latest git snapshot for switch to yelp
- remove --disable-scrollkeeper flag for > f20
- use yelp-tools as BR instead of gnome-doc-utils
- add --with-gnome flag to find_language, needed for yelp
- restore caja-devel as BR
 
* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0
- Remove unused patches
- Add gnome-doc-utils to BR
- Make spec file a little bit easier to read

* Sat Dec 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.4.git20130919.77a6040
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use BR caja-devel for f21

* Thu Nov 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.3.git77a6040
- do not use download dir for incoming bluetooth downloads if mate-bluetooth
- isn't installed, rhbz #(1031307)

* Thu Sep 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.2.git77a6040
- update to latest git snapshot
- remove runtime require obex-data-server for > f19
- remove upstreamed patches

* Sun Aug 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-0.1.git48b2c97
- update latest git snapshot
- add manpage
- update to apache-2.24
- use mate-session to track the active session, remove consolkit
- add dbus requires patch
- add OpenBSD suffers from the same httpd race condition as the other BSDs patch
- add fix turning on sharing not starting mate-user-share
- add bluetooth support optional
- add BR libICE-devel
- add BR libSM-devel
- remove runtime require hicolor-icon-theme
- disable bluetooth support for fedora > f19
- update make install macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- remove %%check
- add a comment for usage of autogen.sh

* Sat May 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- remove gsettings.convert file
- add requires high-color-icon-theme
- add desktop file check for mate-user-share.desktop

* Wed Apr 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-1
- update to 1.6.0
- remove upstreamed desktop file fix
- switch to libnotify as BR

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-2
- initial build for fedora

* Thu Sep 27 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-1
- build against official fedora Mate-Desktop

* Sun Sep 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-0101
- fix desktop files

* Sun Sep 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-0100
- improve spec file
- security update

* Fri Jul 20 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-1
- remove mate-user-share_fix_rpm-scriplet-output.patch, it's upstreamed

* Thu Jul 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- initial package
- spec file is based on gnome-user-share-2.30.2-4.fc15 spec file
- add mate-user-share_fix_rpm-scriplet-output.patch
