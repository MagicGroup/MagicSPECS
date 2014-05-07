Name:           mate-session-manager
Version:        1.8.1
Release:        1%{?dist}
Summary:        MATE Desktop session manager
License:        GPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  pangox-compat-devel
BuildRequires:  systemd-devel
BuildRequires:  xmlto
BuildRequires:  libXtst-devel
BuildRequires:  xorg-x11-xtrans-devel
BuildRequires:  tcp_wrappers-devel

Requires: system-logos
# Needed for mate-settings-daemon
Requires: mate-control-center
# we need an authentication agent in the session
Requires: mate-polkit
# and we want good defaults
Requires: polkit-desktop-policy
Requires: hicolor-icon-theme

%description
This package contains a session that can be started from a display
manager such as MDM. It will load all necessary applications for a
full-featured user session.

%prep
%setup -q

%build
%configure                    \
    --disable-static          \
    --enable-ipv6             \
    --with-gtk=2.0            \
    --with-default-wm=marco   \
    --with-systemd            \
    --disable-upower          \
    --enable-docbook-docs     \
    --disable-schemas-compile \
    --with-x

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
        --delete-original                          \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-session-properties.desktop

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-session.convert

%find_lang %{name} --with-gnome --all-name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
      /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
      /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
      /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-session
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-wm
%{_datadir}/applications/mate-session-properties.desktop
%{_datadir}/mate-session-manager
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop


%changelog
* Sun Mar 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1
- use modern 'make install' macro
- removed upstreamed patches
- add --with-gnome --all-name for find language
- use pangox-compat-devel BR
- re-worked configure flags
- cleanup spec file

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Nov 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- make suspend/hibernate button work without upower

* Thu Oct 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- disable upower support for > f20, upower-1.0 is landed

* Wed Oct 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- switch to gnome-keyring for > f19
- add mate-session-manager_systemd-session_id.patch

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- initial attempt at systemd-login1 suspend/hibernate support

* Fri Jul 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- drop comment out patch from spec file
- remove unnecessary BRs
- add pangox-compat-devel instead as pango-devel as BR
- add BR libXtst-devel
- add BR xorg-x11-xtrans-devel
- add BR tcp_wrappers-devel
- remove NOCONFIGURE=1 ./autogen.sh
- add some runtime requires
- remove needless gsettings convert file
- change doc dir for f20
- fix file section for 1.6.1 release

* Mon Jun 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-4
- Drop the caja patch
- Build against latest systemd
- Disable building docbook docs
- Clean up BRs

* Thu May 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Add patch for caja race condition

* Tue May 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add systemd-devel to BR and enable systemd support
- Build docbook docs
- Own mate-session doc dir

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Fri Feb 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release
- Convert to old BR style

* Mon Feb 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-3
- Fix ten caja windows on login

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.0-2
- Add mate-session-manager-1.5.0-fix_schema.patch: fix segfault preventing
  hibernation/suspend - BZ#888184
- Add missing dependency for pangox-devel
- Improved spec for readability

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- remove the desktop validate for the xsession file
- change build requires style

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-9
- Add mate.desktop to desktop-file-install

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-8
- Add MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 to install section

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-7
- Fix configure flags
- Remove no replace macro from schemas

* Sun Oct 07 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-6
- Remove kdm

* Sat Oct 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-5
- Add kdm to the requires field. mate-session-manager has no dm builtin yet

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Update post/postun/poststrans scriptlets to match files section for hicolor
- Update licensing to GPLv2+ only

* Sat Sep 29 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-3
- Fix buildrequires/requires field

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-2
- Fix mateconf scriptlets

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-1
-Initial build
