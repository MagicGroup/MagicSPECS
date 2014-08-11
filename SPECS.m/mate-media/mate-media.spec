Name:           mate-media
Version:        1.8.0
Release:        2%{?dist}
Summary:        MATE media programs
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  libxml2-devel
BuildRequires:  libcanberra-devel
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-common
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  unique-devel

%description
This package contains a few media utilities for the MATE desktop,
including a volume control.


%prep
%setup -q

%build
%configure \
        --disable-static \
        --disable-schemas-compile \
        --with-gtk=2.0 \
        --enable-pulseaudio

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'

desktop-file-install                                                    \
        --delete-original                                               \
        --dir=%{buildroot}%{_datadir}/applications                      \
%{buildroot}%{_datadir}/applications/mate-volume-control.desktop

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_mandir}/man1/*
%{_bindir}/mate-volume-control
%{_bindir}/mate-volume-control-applet
%{_sysconfdir}/xdg/autostart/mate-volume-control-applet.desktop
%{_datadir}/mate-media/
%{_datadir}/sounds/mate/
%{_datadir}/applications/mate-volume-control.desktop


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- remove --disable-scrollkeeper configure flag
- goodby gst-mixer for f21, fix rhbz (#1045742)
- switch complete to pulse-audio

* Mon Jan 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.7.0-1
- update to 1.7.0 release
- use modern 'make install' macro
- change BR's
- add --with-gnome --all-name for find language
- clean up file section

* Fri Jan 3 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release
- removed upstreamed multimedia category patch

* Sun Sep 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- enable pulseaudio, fix rhbz (#1008011)
- cleanup BRs
- remove --all-name from find locale
- sort file section
- remove needless gsettings convert file
- show-mixer-controls-in-multimedia-category

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.2-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 22 2012 Nelson Marques <nmo.marques@gmail.com> - 1.5.1-3
- mate-settings-daemon was build with gstreamer, we want to make
  sure we also have proper gstreamer support here. Only from MATE
  1.8 we will be able to support both backends

* Tue Dec 11 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-2
- Remove duplicate configure flag
- Fix gstreamer applet compilation error the right way

* Mon Dec 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Bump to latest upstream version
- Add patch to fix compilation errors for gstreamer applet
- Clean up spec file
- Add update-desktop-database scriptlet
- Switch to buildroot macro

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- drop devel sub-package and obsolete it

* Sat Nov 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Rebuild to fix autoqa bug on bodhi

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-3
- add Icon Cache scriptlets

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- add LGPLv2+ to license

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build

