Summary:        Shared code for mate-panel, mate-session, mate-file-manager, etc
Name:           mate-desktop
License:        GPLv2+ and LGPLv2+ and MIT
%if 0%{?fedora} > 20
Version:        1.8.0
Release:        3%{?dist}
Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
%else
Version:        1.6.2
Release:        1%{?dist}
Source0:        http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
%endif
URL:            http://mate-desktop.org

# fix fedora backgrounds and
# workaround for x-caja-desktop window issue
Source1:        mate-fedora.gschema.override
Source2:        gnu-cat.gif
Source3:        gnu-cat_navideno_v3.png
Source4:        mate-fedora-f20.gschema.override
Source5:        mate-fedora-f21.gschema.override

#enable gnucat
%if 0%{?fedora} > 20
Patch0:         mate-desktop_enable_gnucat-f21.patch
%else
Patch0:         mate-desktop_enable_gnucat.patch
%endif


BuildRequires:  dconf-devel
BuildRequires:  desktop-file-utils
BuildRequires:  mate-common
BuildRequires:  startup-notification-devel
BuildRequires:  unique-devel
%if 0%{?fedora} > 20
BuildRequires:  itstool
%else
BuildRequires:  mate-doc-utils
%endif

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: redhat-menus
Requires: pygtk2
Requires: xdg-user-dirs-gtk
Requires: mate-control-center-filesystem
Requires: mate-panel

Obsoletes: libmate
Obsoletes: libmate-devel
Obsoletes: libmatecanvas
Obsoletes: libmatecanvas-devel
Obsoletes: libmatecomponent
Obsoletes: libmatecomponent-devel
Obsoletes: libmatecomponentui
Obsoletes: libmatecomponentui-devel
Obsoletes: libmateui
Obsoletes: libmateui-devel
Obsoletes: mate-conf
Obsoletes: mate-conf-devel
Obsoletes: mate-conf-editor
Obsoletes: mate-conf-gtk
Obsoletes: mate-mime-data
Obsoletes: mate-mime-data-devel
Obsoletes: mate-vfs
Obsoletes: mate-vfs-devel
Obsoletes: mate-vfs-smb
# switch to gnome-keyring > f19
%if 0%{?fedora} > 19
Obsoletes: libmatekeyring
Obsoletes: libmatekeyring-devel
Obsoletes: mate-keyring
Obsoletes: mate-keyring-pam
Obsoletes: mate-keyring-devel
%endif
# temporarily solution for f20 until mate-bluetooth
# is ported to bluez5
%if 0%{?fedora} > 19
Obsoletes: mate-bluetooth < 1:1.6.0-6
Obsoletes: mate-bluetooth-libs < 1:1.6.0-6
Obsoletes: mate-bluetooth-devel < 1:1.6.0-6
%endif
%if 0%{?fedora} > 20
Obsoletes: mate-doc-utils
Obsoletes: mate-character-map
Obsoletes: mate-character-map-devel 
Obsoletes: libmatewnck
Obsoletes: libmatewnck-devel
%endif


%description
The mate-desktop package contains an internal library
(libmatedesktop) used to implement some portions of the MATE
desktop, and also some data files and other shared components of the
MATE user environment.

%package libs
Summary:   Shared libraries for libmate-desktop
License:   LGPLv2+

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:    Libraries and headers for libmate-desktop
License:    LGPLv2+
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.

%prep
%setup -q
%patch0 -p1 -b .gnucat
cp %SOURCE2 mate-about/gnu-cat.gif
cp %SOURCE3 mate-about/gnu-cat_navideno_v3.png

# needed for gnucat patch
autoreconf -fi

%build
%if 0%{?fedora} > 20
%configure                                                 \
     --enable-desktop-docs                                 \
     --disable-schemas-compile                             \
     --with-gtk=2.0                                        \
     --with-x                                              \
     --disable-static                                      \
     --enable-unique                                       \
     --enable-mpaste                                       \
     --with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"      \
     --enable-gtk-doc-html
%else
%configure \
     --disable-scrollkeeper                                \
     --disable-schemas-compile                             \
     --with-gtk=2.0                                        \
     --with-x                                              \
     --disable-static                                      \
     --enable-unique                                       \
     --with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"      \
     --with-omf-dir=%{_datadir}/omf/mate-desktop           \
     --enable-gnucat
%endif

make %{?_smp_mflags} V=1


%install
%{make_install}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-about.desktop

%if 0%{?fedora} > 20
desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-user-guide.desktop
%endif

%if 0%{?fedora} > 19
%if 0%{?fedora} > 20
install -D -m 0644 %SOURCE5 %{buildroot}%{_datadir}/glib-2.0/schemas/mate-fedora.gschema.override
%else
install -D -m 0644 %SOURCE4 %{buildroot}%{_datadir}/glib-2.0/schemas/mate-fedora.gschema.override
%endif
%else
install -D -m 0644 %SOURCE1 %{buildroot}%{_datadir}/glib-2.0/schemas/mate-fedora.gschema.override
%endif

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/mate-desktop.convert

%if 0%{?fedora} > 20
# remove conflicting files with gnome
rm -fr %{buildroot}%{_datadir}/help/*/fdl
rm -fr %{buildroot}%{_datadir}/help/*/gpl
rm -fr %{buildroot}%{_datadir}/help/*/lgpl
%endif

%find_lang %{name} --with-gnome --all-name


%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans libs
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%if 0%{?fedora} > 20
%{_bindir}/mate-about
%{_bindir}/mate-gsettings-toggle
%{_bindir}/mpaste
%{_datadir}/applications/mate-about.desktop
%{_datadir}/applications/mate-user-guide.desktop
%{_datadir}/mate-about
%{_datadir}/glib-2.0/schemas/mate-fedora.gschema.override
%{_mandir}/man1/*
%{_datadir}/pixmaps/gnu-cat.gif
%{_datadir}/pixmaps/gnu-cat_navideno_v3.png
%{_datadir}/help/*/mate-user-guide
%else
%{_bindir}/mate-about
%{_bindir}/mate-gsettings-toggle
%{_datadir}/applications/mate-about.desktop
%{_datadir}/mate
%{_datadir}/omf/mate-desktop
%{_datadir}/mate-about
%{_datadir}/glib-2.0/schemas/mate-fedora.gschema.override
%{_mandir}/man1/*
%{_datadir}/pixmaps/gnu-cat.gif
%{_datadir}/pixmaps/gnu-cat_navideno_v3.png
%endif

%files libs -f %{name}.lang
%{_libdir}/libmate-desktop-2.so.*
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files devel
%{_libdir}/libmate-desktop-2.so
%{_libdir}/pkgconfig/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0
%doc %{_datadir}/gtk-doc/html/mate-desktop


%changelog
* Sat Mar 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-3
- add new f21 gsettings overrride file
- remove caja-autostart override
- add mate-panel-menubar override
- enable fedora.layout for mate-panel in override file
- obsolete mate-doc-utils and mate-character-map for f21
- remove BR mate-doc-utils for f21
- use more conditionals to make spec file usable for every fedora branch
- remove configure flag --with-omf-dir for f21

* Wed Mar 05 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- enable desktop-docs
- remove conficting files during build
- obsolete libmatewnck, compiz is updated in rawhide

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Thu Feb 13 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.5-3
- comment out obsoletes tag for libmatewnck
- libmatewnck is currently needed for compiz

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.5-2
- Add obsoletes tag for libmatewnck

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.5-1
- update to 1.7.5 release
- add mate-user-guide desktop file
- rename patch for f21

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.3-1
- update to 1.7.3 release
- enable gnucat
- clean up spec file

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.1 release
- move gtk-doc dir to -devel subpackage
- use modern 'make install' macro
- remove obsolete configure flags
- enable mpaste

* Fri Dec 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-2
- fix previous build, add forgotten fedora's override file again!!!!!

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Nov 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.12.git81c245b
- BlueMenta is now default theme in fedora 20

* Thu Nov 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.11.git81c245b
- use Menta-Blue as default theme in fedora 20, change gesettings overrides

* Tue Nov 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.10.git81c245b
- add gsettings overrides again for caja f20

* Thu Nov 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.9.git81c245b
- use Menta-Blue as default theme in fedora 20, change gesettings overrides

* Tue Nov 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.8.git81c245b
- let caja starts with mate-session-manager for > f19
- adjust mate-fedora gesettings override file

* Sat Oct 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.7.git81c245b
- switch to gnome-keyring for > f19

* Fri Oct 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.6.git81c245b
- Fix typo

* Tue Oct 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.5.git81c245b
- remove gsettings overrides from last update

* Wed Oct 09 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.4.git81c245b
- Further fix for #886029 (disable background-fade)


* Wed Oct 09 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.3.git81c245b
- Possible fix for #886029 (disable background draw and mate-settings-daemon background plugin)

* Fri Oct 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2-0.2.git81c245b
- Get rid of obsoletes tag as we no longer need it. (#1015335)

* Mon Sep 23 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.1.git81c245b
- update to latest git snapshot
- fix https://github.com/mate-desktop/mate-settings-daemon/issues/32

* Sat Sep 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-14
- versioned mate-bluetooth obsolete

* Sat Sep 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-13
- obsolete mate-bluetooth-libs and mate-bluetooth-devel too

* Fri Sep 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-12
- obsolete mate-bluetooth for f20

* Wed Aug 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-11
- move schemas and locale to -libs subpackage to fix rhbz #988944
- add better font rendering settings to gsettings.override file
- use mate-control-center-filesystem instead of control-center-filesystem
- as runtime require
- clean up BRs, most of them are already called
- remove BR gsettings-desktop-schemas-devel
- remove BRs gtk2-devel and gtk3-devel
- remove BR gtk-doc
- remove BR pangox-compat-devel
- remove runtime require libnotify, no need of this anymore

* Sun Jul 28 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-10
- Undo obsolete consolekit RHBZ 989208

* Sat Jul 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-9
- obsolete ConsoleKit

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-8
- remove gsettings convert file

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-7
- Obsolete more packages to fix RHBZ 972548
- Remove obsolete for libmatenotify for debugging purposes
- Add control-center-filesystem for debugging purposes

* Fri May 31 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-6
- Obsolete all mate-conf packages for depsolving issues.
- Keep changelogs in sync and bump release version.

* Tue May 28 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-5
- Remove mate-notification-daemon from hard requires.

* Sat May 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-4
- Own mateconf gsettings dir

* Fri May 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Obsolete mate-conf as compiz no longer uses it, obsoleted upstream.
- Add requires mate-notification-daemon as nothing else does.

* Fri May 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- workaround for x-caja-desktop window issue
- add mate-fedora.gschema.override file

* Thu May 23 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release
- Readd gnucat

* Fri May 03 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Own dirs we are supposed to own (961950)
- Move docs to main package and mark them with doc macro
- Add pangox-compat-devel to BRs

* Mon Apr 22 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Remove obsletes for libmatenotify as compiz requires it.

* Tue Apr 02 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 release.

* Mon Mar 25 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.8-1
-Update to latest upstream release

* Fri Feb 22 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.7-1
-Update to latest upstream release

* Fri Feb 08 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-1
-Update to latest upstream release

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 release

* Sun Nov 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.4-1
- update to 1.5.4 release
- no need to drop upstream commits patch as some twat blew it away

* Sat Nov 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-7
- Add disable schemas compile configure flag

* Wed Nov 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-6
- add upstream commits patch

* Thu Nov 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-5
- remove omf directory hack and do it properly

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-4
- add requires xdg-user-dirs-gtk
- set default directories

* Mon Nov 05 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-3
- Fix tabs/spaces
- Switch to new buildroot macro instead of old RPM_BUILD_ROOT macro

* Sat Nov 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- enable gnucat

* Sat Nov 03 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-2
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- remove all the false mate requires (breached package guidelines)
- remove unused build require and change style
- add schema scriptlets
- clean up spec file
- fix Summary

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.1-12
- Add runtime requirements to avoid confusion

* Wed Sep 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-11
- drop problematic bg-crossfade patch (breaks mate-settings-daemon)
- remove .desktop Only-Show-In mods

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-10
- fix deps wrt -libs subpkg

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-9
- add isa tag to -libs

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-8
- change file section for own directories
- change 'to avoid conflicts with gnome' part
- add libs subpackage for shared libraries

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-7
- add desktop file install for mate-about.desktop
- add BuildRequires desktop-file-utils
- remove BuildRequires intltool gtk-doc

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-6
- start initial for fedora
- remove unnecessary buildRequires
- Drop pycairo from Requires
- change --with-pnp-ids-path="/usr/share/hwdata/pnp.ids" to
- --with-pnp-ids-path="%%{_datadir}/hwdata/pnp.ids"

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-desktop.spec based on gnome-desktop-2.32.0-9.fc16 spec
