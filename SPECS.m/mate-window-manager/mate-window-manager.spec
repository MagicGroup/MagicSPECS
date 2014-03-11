Name:           mate-window-manager
Version:        1.6.1
Release:        1%{?dist}
Summary:        MATE Desktop window manager
License:        LGPLv2+ and GPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz

BuildRequires: desktop-file-utils
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: gtk2-devel
BuildRequires: libcanberra-devel
BuildRequires: libSM-devel
BuildRequireS: libsoup-devel
BuildRequires: libXdamage-devel
BuildRequires: mate-common
BuildRequires: mate-dialogs
BuildRequires: mate-doc-utils
BuildRequires: rarian-compat
BuildRequires: rarian-devel
BuildRequires: startup-notification-devel

# http://bugzilla.redhat.com/873342
Provides: firstboot(windowmanager) = mate-window-manager

%description
MATE Desktop window manager

%package devel
Summary: Development files for mate-window-manager
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-window-manager

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-static           \
           --disable-scrollkeeper     \
           --disable-schemas-compile  \
           --with-gtk=2.0             \
           --with-x

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

find %{buildroot} -name '*.la' -exec rm -vf {} ';'

desktop-file-install                                \
        --delete-original                           \
        --dir=%{buildroot}%{_datadir}/applications  \
%{buildroot}%{_datadir}/applications/marco.desktop

%find_lang marco


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f marco.lang
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/marco
%{_bindir}/marco-message
%{_datadir}/applications/marco.desktop
%{_datadir}/themes/ClearlooksRe
%{_datadir}/themes/Dopple-Left
%{_datadir}/themes/Dopple
%{_datadir}/themes/DustBlue
%{_datadir}/themes/Spidey-Left
%{_datadir}/themes/Spidey
%{_datadir}/themes/Splint-Left
%{_datadir}/themes/Splint
%{_datadir}/themes/WinMe
%{_datadir}/themes/eOS
%{_datadir}/marco
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%{_datadir}/mate/help/creating-marco-themes/C/creating-marco-themes.xml
%{_datadir}/mate/wm-properties
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
%{_datadir}/MateConf/gsettings/marco.convert
%{_libdir}/libmarco-private.so.0*
%{_mandir}/man1/*

%files devel
%{_bindir}/marco-theme-viewer
%{_bindir}/marco-window-demo
%{_includedir}/marco-1
%{_libdir}/libmarco-private.so
%{_libdir}/pkgconfig/libmarco-private.pc
%{_mandir}/man1/marco-theme-viewer.1.*
%{_mandir}/man1/marco-window-demo.1.*


%changelog
* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Bug fix release. See changelog.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
- Update to latest upstream release
- Own dirs that we are supposed to owp

* Fri Feb 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Update to latest upstream release

* Mon Feb 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-4
- Add latest upstream commits

* Tue Jan 29 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-3
- Add some configure flags

* Fri Jan 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- Sort BR's
- Remove unneeded obsoletes tag

* Mon Jan 14 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-1
- Update to latest upstream release

* Fri Jan 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-11
- Convert back to old BR format
- Drop unneeded BRs
- Own directories that are supposed to be owned (marco-1)
- Fix missing "X-Mate" category.
- Add gsettings data convert file for users upgrading from 1.4
- Fix update of gsettings enum preferences

* Mon Dec 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-10
- Rebuild for ARM

* Sun Nov 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-9
- Remove hard requires on mwm and mate-themes.

* Sun Nov 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-8
- Add xdamage as it is required for build

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-7
- move development files to devel
- remove the config.h defines from %%build section

* Tue Nov 13 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-6
- Update configure flags, add disable scrollkeeper mainly

* Tue Nov 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-5
- add patch to fix startup rendering effect with composite enabled 

* Tue Nov 06 2012 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-4
- Provides: firstboot(windowmanager) (#873342)

* Mon Nov 05 2012 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-3
- drop Provides: firstboot(windowmanager) until bug #873342 is fixed

* Sat Nov 03 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-2
- Provides firstboot(windowmanager) mate-window-manager

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel and dconf-devel
- change build requires style

* Wed Oct 17 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-12
- Fix crash if you have lots of workspaces

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-11
- filter provides
- fix build requires
- fix reqires
- define some defaults
- Add patch to allow breaking out from maximization during mouse resize
  (gnome bz 622517)

* Wed Sep 26 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-10
- fix ldconfig scriptlets
- use desktop-file-validate again
- own %%{_datadir}/mate/wm-properties/

* Tue Sep 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-9
- Remove mateconf obsolete scriplet

* Mon Sep 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-8
- rerefix mate-conf scriptlets. Add export line to REALLY not install schemas with make install.
- comment out desktop-file-validate.

* Mon Sep 17 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-7
- fix/simplify dir ownership
- omit not-needed/broken Obsoletes
- (re)fix scriptlets :)

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-6
- Move post and postun scriptlets to proper location

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-5
- Remove onlyshowin since it is not needed any more with updated desktop-file-utils

* Sat Sep 15 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-4
- Update source to note git version.

* Sun Sep 09 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-3
- Fix broken dependencies, update to latest github version which contains fixes for desktop-file-utils

* Mon Sep 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-2
- Add environment variable to install section and further obsoletes to prevent dependency breakage

* Sun Sep 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.1-1
- Upgrade to new upstream version.

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-5
- drop unneeded python-related build deps
- %%configure --disable-schemas-install
- fix/simplify some parent-dir ownership

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org>  1.4.0-4
- main pkg Requires: %%name-libs
- drop needless icon scriptlets
- s|MATE|X-MATE| .desktop Categories on < f18 only
- License: GPLv2+

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Own theme directories that are being installed, switch from po_package to namefor lang files, bump release version

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Add mateconf scriptlets

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
