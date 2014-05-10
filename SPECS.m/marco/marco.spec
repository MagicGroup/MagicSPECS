# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.8

# Settings used for build from snapshots.
%{!?rel_build:%global commit 62a708d461e08275d6b85985f5fa13fa8fbc85f7}
%{!?rel_build:%global commit_date 20131212}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           marco
Version:        %{branch}.0
Release:        4%{?dist}
#Release:       0.5%{?git_rel}%{?dist}
Summary:        MATE Desktop window manager
License:        LGPLv2+ and GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R marco.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

# needed for fixing initial-setup issue, rhbz (#962009)
Source1:        mini-window.png
Source2:        stock_delete.png
Source3:        stock_maximize.png
Source4:        stock_minimize.png
Source5:        window.png

# needed for fixing initial-setup issue, rhbz (#962009)
Patch0:         marco_add-pixbuf-inline-icons.patch

BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel
BuildRequires: libcanberra-devel
BuildRequires: libgtop2-devel
BuildRequires: libSM-devel
BuildRequireS: libsoup-devel
BuildRequires: libXdamage-devel
BuildRequires: mate-common
BuildRequires: mate-dialogs
BuildRequires: startup-notification-devel
BuildRequires: yelp-tools

# http://bugzilla.redhat.com/873342
# https://bugzilla.redhat.com/962009
Provides: firstboot(windowmanager) = marco

%if 0%{?fedora} && 0%{?fedora} <= 25
Provides: mate-window-manager%{?_isa} = %{version}-%{release}
Provides: mate-window-manager = %{version}-%{release}
Obsoletes: mate-window-manager < %{version}-%{release}
%endif

%description
MATE Desktop window manager

%package devel
Summary: Development files for mate-window-manager
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} <= 25
Provides: mate-window-manager-devel%{?_isa} = %{version}-%{release}
Provides: mate-window-manager-devel = %{version}-%{release}
Obsoletes: mate-window-manager-devel < %{version}-%{release}
%endif

%description devel
Development files for marco

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

# needed for missing `po/Makefile.in.in'
cp %{SOURCE1} src/mini-window.png
cp %{SOURCE2} src/stock_delete.png
cp %{SOURCE3} src/stock_maximize.png
cp %{SOURCE4} src/stock_minimize.png
cp %{SOURCE5} src/window.png

%patch0 -p1 -b .inline-icons

# needed for the patch and for git snapshot builds
autoreconf -if

%build
%configure --disable-static           \
           --disable-schemas-compile  \
           --with-gtk=2.0             \
           --with-x

# fix rpmlint unused-direct-shlib-dependency warning
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -vf {} ';'

desktop-file-install                                \
        --delete-original                           \
        --dir=%{buildroot}%{_datadir}/applications  \
%{buildroot}%{_datadir}/applications/marco.desktop

# remove needless gsettings convert file
rm -f  %{buildroot}%{_datadir}/MateConf/gsettings/marco.convert

%find_lang %{name} --with-gnome --all-name


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
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
%dir %{_datadir}/marco
%dir %{_datadir}/marco/icons
%{_datadir}/marco/icons/marco-window-demo.png
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%{_datadir}/mate/wm-properties
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
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
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-4
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- rebuild for libgtop2 soname bump

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- add 1.7.90 release

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0.2
- re-work marco_add-pixbuf-inline-icons.patch

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Fri Dec 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.5.git20131212.62a708d
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use modern 'make install' macro
- improve obsoletes/provides, add limits

* Sat Dec 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.4.git0403454e
- remove isa tags from obsoletes/provides
 
* Wed Dec 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.3.git0403454e
- using 8 digets in git version to update mate-window-manager

* Wed Dec 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git0403454
- rename mate-window-manager to marco

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1.1.git0403454
- Update to 1.7.0 git snapshot

* Wed Nov 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-6
- start with side-by-side-tiling and windows-snapping-top-screen support for f20

* Fri Sep 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-5
- fix initial-setup issue, rhbz (#962009)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- remove gsettings convert file

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2-2
- Add libgtop2-devel to BR's

* Sat Jun 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2-1
- Update to latest upstream release
- Update datadir to mate-window-manager instead of marco

* Sat Jun 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-2
- Fix initial-setup, hopefully.

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
