# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch %(echo %{version} | awk -F. '{print $1"."$2}')

# Settings used for build from snapshots.
%{!?rel_build:%global commit d5b35083e4de1d7457ebd937172bb0054e1fa089}
%{!?rel_build:%global commit_date 20140125}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-screensaver
Version: 1.12.0
Release: 1%{?dist}
#Release: 1%{?dist}
Summary:        MATE Screensaver
Summary(zh_CN.UTF-8): MATE 屏幕保护
License:        GPLv2+ and LGPLv2+
URL:            http://pub.mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-screensaver.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Requires:       magic-menus
Requires:       system-logos

# switch to gnome-keyring > f19
Requires:       gnome-keyring-pam

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXxf86misc-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libmatekbd-devel
BuildRequires:  libnotify-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-menus-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pam-devel
BuildRequires:  systemd-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xmlto

%description
mate-screensaver is a screen saver and locker that aims to have
simple, sane, secure defaults and be well integrated with the desktop.

%description -l zh_CN.UTF-8
MATE 的屏幕保护程序。

%package devel
Summary: Development files for mate-screensaver
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-screensaver

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# needed for git snapshots
#NOCONFIGURE=1 ./autogen.sh

%build
%configure                          \
            --with-x                \
            --with-gtk=2.0          \
            --disable-schemas-compile \
            --enable-docbook-docs   \
            --with-mit-ext          \
            --with-xf86gamma-ext    \
            --with-libgl            \
            --with-shadow           \
            --enable-locking        \
            --with-systemd          \
            --enable-pam

make %{?_smp_mflags} V=1


%install
%{make_install}

desktop-file-install --delete-original             \
  --dir %{buildroot}%{_datadir}/applications    \
%{buildroot}%{_datadir}/applications/mate-screensaver-preferences.desktop

desktop-file-install                                          \
   --delete-original                                          \
   --dir %{buildroot}%{_datadir}/applications/screensavers    \
%{buildroot}%{_datadir}/applications/screensavers/*.desktop

# remove needless gsetting convert file
rm -f %{buildroot}%{_datadir}/MateConf/gsettings/org.mate.screensaver.gschema.migrate

# fix versioned doc dir
mkdir -p %{buildroot}%{_datadir}/doc/mate-screensaver
mv %{buildroot}%{_datadir}/doc/mate-screensaver-%{version}/mate-screensaver.html %{buildroot}%{_datadir}/doc/mate-screensaver/mate-screensaver.html
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS NEWS README COPYING
%{_bindir}/mate-screensaver*
%{_sysconfdir}/pam.d/mate-screensaver
%{_sysconfdir}/xdg/menus/mate-screensavers.menu
%{_sysconfdir}/xdg/autostart/mate-screensaver.desktop
%{_libexecdir}/mate-screensaver-*
%{_libexecdir}/mate-screensaver/
%{_datadir}/applications/mate-screensaver-preferences.desktop
%{_datadir}/applications/screensavers/*.desktop
%{_datadir}/mate-screensaver/
%{_datadir}/backgrounds/cosmos/
%{_datadir}/pixmaps/mate-logo-white.svg
%{_datadir}/pixmaps/gnome-logo-white.svg
%{_datadir}/desktop-directories/mate-screensaver.directory
%{_datadir}/glib-2.0/schemas/org.mate.screensaver.gschema.xml
%{_datadir}/mate-background-properties/cosmos.xml
%{_datadir}/dbus-1/services/org.mate.ScreenSaver.service
%{_mandir}/man1/*

%files devel
%{_libdir}/pkgconfig/*
%{_docdir}/mate-screensaver/mate-screensaver.html

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.1-2
- 更新到 1.11.1

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-3
- 为 Magic 3.0 重建

* Sun Jul 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0.2
- fix 'has_separator'_deprecation

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release

* Sun Jan 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git20140125.d5b3508
- update to git snapshot from 2014.01.25
- fix rhbz (#1057402) and (#1056591)
- make Maintainers life easier and use better git snapshot usage

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- update to 1.7.0 release
- add --with-gnome --all-name for find language
- removed upstreamed systemd-login patch
- removed --with-console-kit configure flag
- use modern 'make install' macro
- add BR xmlto
- reworked configure flags, use --with-gtk=2.0, --disable-schemas-compile
- --enable-docbook-docs
- fixed versioned doc dir
- use one style for ownning directories

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.0-1.1.git0460034
- Update to 1.7.0

* Sat Oct 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- switch to gnome-keyring for > f19

* Sat Oct 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-3
- improve systemd-login support

* Fri Aug 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- bump version to 1.6.1-2

* Fri Aug 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- Update to 1.6.1
- Drop patches
- move doc dir for > f19

* Wed Jul 17 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- add upstream patch to fix idle activation time
- remove unrecognized configure options --with-libgl
- clean up runtime requires
- add pam and systemd configure flags
- remove gsettings convert file

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to latest upstream release
- Redo configure flags
- Update configure flags
- Own dirs we are supposed to own

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Nelson Marques <nmo.marques@gmail.com> - 1.5.1-3
- Add missing dependencies for proper build and conditionals for
  using systemd or CK dependending on version.
- Rework %%configure

* Wed Dec 05 2012 Nelson Marques <nmo.marques@gmail.com> - 1.5.1-2
* add mate-screensaver-1.5.1-only_allow_one_instance.patch: fix double
  password prompt when returning from hibernate/suspend. Only allow one
  instance per user.

* Fri Nov 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- drop upstream commits patch

* Mon Nov 12 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-3
- clean up commits patch

* Mon Nov 12 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- add upstream commits patch
- add buildrequires systemd-devel

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Tue Oct 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- add V=1 to make
- use autogen instead of autoreconf

* Fri Oct 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build

