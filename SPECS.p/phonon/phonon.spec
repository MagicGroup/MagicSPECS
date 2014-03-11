
# enabling for the build sanity, the results
# aren't all that useful, yet.
%define phonon_build_tests -DPHONON_BUILD_TESTS:BOOL=ON

## split -experimental subpkgs
#define experimental 1

Summary: Multimedia framework api
Name:    phonon
Version: 4.6.0
Release: 8%{?dist}
Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://phonon.kde.org/
%if 0%{?snap}
Source0: phonon-%{version}-%{snap}.tar.bz2
%else
Source0: ftp://ftp.kde.org/pub/kde/stable/phonon/%{version}/src/phonon-%{version}.tar.xz
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# phonon_backend ... could not be loaded
# http://bugzilla.redhat.com/760039
Patch50: phonon-4.5.57-plugindir.patch 
Patch51: phonon-4.6.0-syntax.patch
# https://git.reviewboard.kde.org/r/103423
Patch52: phonon-4.6.0-rpath.patch
#临时补丁，修正rootDir问题
Patch53: phonon-4.6.0-fixusr.patch

## Upstream patches

BuildRequires: automoc4 >= 0.9.86
BuildRequires: cmake >= 2.6.0
BuildRequires: pkgconfig
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libpulse-mainloop-glib) > 0.9.15
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(QtGui) >= 4.7.2
BuildRequires: pkgconfig(QZeitgeist)
BuildRequires: pkgconfig(xcb)

%global pulseaudio_version %(pkg-config --modversion libpulse 2>/dev/null || echo 0.9.15)

## Beware bootstrapping, have -Requires/+Requires this for step 0, then build at least one backend
Requires: phonon-backend%{?_isa} => 4.4
#Provides: phonon-backend%{?_isa} = 4.4
Requires: pulseaudio-libs%{?_isa} >= %{pulseaudio_version}
Requires: qt4%{?_isa} >= %{_qt4_version}

%if ! 0%{?experimental}
#Obsoletes: phonon-experimental < %{version}-%{release}
Provides:  phonon-experimental = %{version}-%{release}
%endif

%description
%{summary}.

%package devel
Summary: Developer files for %{name}
Group:   Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Requires: pkgconfig
%if ! 0%{?experimental}
#Obsoletes: phonon-experimental-devel < %{version}-%{release}
Provides:  phonon-experimental-devel = %{version}-%{release}
%endif
%description devel
%{summary}.

%if 0%{?experimental}
%package experimental
Summary: Experimental interfaces for %{name}
Group:   System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description experimental 
%{summary}.

%package experimental-devel
Summary: Developer files for %{name}-experimental
Group:   System Environment/Libraries
Requires: %{name}-experimental%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description experimental-devel
%{summary}.
Includes experimental and unstable apis.
%endif


%prep
%setup -q 

%patch50 -p1 -b .plugindir
%patch51 -p1 -b .syntax
%patch52 -p1 -b .rpath
%patch53 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  %{?phonon_build_tests} \
  -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# symlink for qt/phonon compatibility
ln -s ../KDE/Phonon %{buildroot}%{_includedir}/phonon/Phonon

# own these dirs
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/plugins/phonon_backend/
mkdir -p %{buildroot}%{_kde4_datadir}/kde4/services/phononbackends/
magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion phonon)" = "%{version}"
%if 0%{?phonon_build_tests:1}
# many of these fail currently (4/10)
make test -C %{_target_platform} ||:
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_libdir}/libphonon.so.4*
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{_qt4_plugindir}/designer/libphononwidgets.so
%dir %{_datadir}/phonon/
%dir %{_kde4_libdir}/kde4/plugins/phonon_backend/
%dir %{_kde4_datadir}/kde4/services/phononbackends/

%if 0%{?experimental}
%post experimental -p /sbin/ldconfig
%postun experimental -p /sbin/ldconfig

%files experimental
%defattr(-,root,root,-)
%endif
%{_libdir}/libphononexperimental.so.4*

%files devel
%defattr(-,root,root,-)
%{_datadir}/phonon/buildsystem/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/phonon/
%dir %{_includedir}/KDE
%{_includedir}/KDE/Phonon/
%{_includedir}/phonon/
%{_libdir}/pkgconfig/phonon.pc
%{_libdir}/libphonon.so
%{_qt4_datadir}/mkspecs/modules/qt_phonon.pri

%if 0%{?experimental}
%exclude %{_includedir}/KDE/Phonon/Experimental/
%exclude %{_includedir}/phonon/experimental/
%files experimental-devel
%defattr(-,root,root,-)
%endif
%{_includedir}/KDE/Phonon/Experimental/
%{_includedir}/phonon/experimental/
%{_libdir}/libphononexperimental.so


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.6.0-8
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 4.6.0-7
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 4.6.0-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-4
- refresh rpath patch

* Wed Mar 28 2012 Than Ngo <than@redhat.com> - 4.6.0-3
- fix syntax in *.pri file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-1
- 4.6.0

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-4.20111031
- fix plugindir usage (#760039)

* Wed Nov 02 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-3.20111031
- fix release

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-1.20111031
- 20111031 snapshot

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-2.20110914
- rebuild (qzeitgeist)

* Fri Sep 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.57-1.20110914
- 4.5.57 20110914 snapshot
- pkgconfig-style deps

* Tue May 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-3
- BR: libqzeitgeist-devel

* Fri Apr 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-2
- avoid Conflicts with judicious (Build)Requires: qt4(-devel) instead

* Fri Mar 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.5.0-1
- phonon-4.5.0
- qt-designer-plugin-phonon moved here (from qt)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.4.4-2
- re-instate allow-stop-empty-source match from mdv

* Fri Jan 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.4.4-1
- phonon-4.4.4

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-0.1.20110104
- Requires: phonon-backend

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-0.0.20110104
- phonon-4.4.4 snapshot (sans backends)
- bootstrap without Requires: phonon-backend

* Tue Nov 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-2
- recognize audio/flac in gstreamer backend (kde#257488)

* Wed Nov 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-1
- phonon-4.4.3

* Mon Nov 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.4.20101122
- phonon-4.4.3 20101122 snapshot

* Fri Nov 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.3.20101112
- phonon-4.4.3 20101112 snapshot

* Tue Oct 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.2.20100909
- Requires: kde-filesystem (#644571)
- own %%{_kde4_libdir}/kde4 (<f15) (#644571)

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.3-0.1.20100909
- phonon-4.4.3 20100909 snapshot

* Tue Jun 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.2-1
- phonon-4.4.2

* Sat Apr 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-2
- phonon-backend-xine-4.4.1 (with pulseaudio) = no audio (kde#235193)

* Thu Apr 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.1-1
- phonon-4.4.1

* Thu Apr 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-3
- add minimal pulseaudio runtime dep

* Wed Mar 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-2
- pa glib/qt eventloop patch (kde#228324)

* Tue Mar 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-1
- phonon-4.4.0 final

* Fri Mar 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-0.3
- phonon-4.3.80-pulse-devicemove-rejig.patch (from mdv)

* Wed Feb 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.4.0-0.2
- preliminary phonon-4.4.0 tarball

* Fri Jan 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-6
- sync w/mdv patches

* Fri Jan 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-5.2
- F11: patch/modularize pa device-manager bits 

* Fri Jan 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.80-5.1
- F11: port the old PA device priorities patch as we don't have PA integration

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-5
- no sound with phonon-xine/pulseaudio (kde#223662, rh#553945)

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-4
- snarf mdv patches

* Mon Jan 18 2010 Than Ngo <than@redhat.com> - 4.3.80-3
- backport GStreamer backend bugfixes, fix random disappearing sound under KDE

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-2
- phonon-4.3.80 (upstream tarball, yes getting ridiculous now)

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-1.20091203
- phonon-4.3.80 (20091203 snapshot)

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-6.20091203
- phonon-4.3.50 (20091203 snapshot)

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-5.20091124
- backend-gstreamer: Requires: gstreamer-plugins-good

* Fri Nov 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-4.20091124
- ln -s ../KDE/Phonon %%_includedir/phonon/Phonon (qt/phonon compat)

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-3.20091124
- phonon-4.3.50 (20091124 snapshot)
- enable pulseaudio integration (F-12+)

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-2.20091118
- phonon-4.3.50 (20091118 snapshot)

* Mon Oct 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.50-1.20091019
- phonon-4.3.50 (20091019 snapshot)

* Sat Oct 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-102
- Requires: qt4 >= 4.5.2-21 (f12+)

* Tue Sep 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-101
- revert to kde/phonon
- inflate to Release: 101
- -backend-gstreamer: Epoch: 2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-11
- fix for '#' in filenames

* Tue Jun 09 2009 Than Ngo <than@redhat.com> - 4.3.1-10
- make InitialPreference=9

* Sun Jun 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-9
- optimize scriptlets
- Req: phonon >= %%phonon_version_major

* Fri Jun 05 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-8
- restore patches to the xine backend

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.3.1-7
- only xine-backend

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-6
- phonon-backend-gstreamer multilib conflict (#501816)

* Wed May 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-5
- s/ImageMagick/GraphicsMagick/, avail on more secondary archs, is faster,
  yields better results.

* Mon May 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-4
- fix Source0 Url
- xine backend will not play files with non-ascii names (kdebug#172242)

* Sat Apr 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-3
- optimize scriptlets
- Provides/Requires: phonon-backend%%{_isa} ...

* Tue Mar  3 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.1-2
- backport GStreamer backend bugfixes (UTF-8 file handling, volume
fader)

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-5
- put icons in the right subpkg

* Thu Jan 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-4
- Requires: phonon-backend >= %%version
- move icons to hicolor theme and into -backend subpkgs
- BR: libxcb-devel
- move phonon-gstreamer.svg to sources

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-3
- BR: automoc4 >= 0.9.86

* Fri Jan 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.0-2
- fix typo in postun scriptlet (introduced in 4.2.96-3)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Thu Jan 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-3
- new tarball
- put icons/scriptlets into main pkg
- Requires: phonon-backend

* Thu Jan 08 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.96-2
- add gstreaer-logo.svg

* Thu Jan 08 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.96-1
- 4.2.96
- rebase phonon-4.2.0-pulseaudio.patch (-> phonon-4.2.96-pulseaudio.patch)
- rebase phonon-4.2.70-xine-pulseaudio.patch 
  (-> phonon-4.2.96-xine-pulseaudio.patch)

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.80-3
- rebuild for pkgconfig deps

* Tue Nov 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.80-2
- phonon-backend-xine: don't Obsolete/Provide itself, Provides: phonon-backend

* Tue Nov 25 2008 Than Ngo <than@redhat.com> 4.2.80-1
- 4.2.80

* Fri Nov 21 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.80-0.1.20081121svn887051
- Use subversion (4.2.80) snapshot
- phonon-backend-xine subpkg
- make VERBOSE=1
- make install/fast
- Xine backend is in phonon now, add xine-lib-devel as BR
- BR cmake >= 2.6.0
- forward-port xine pulseaudio patch

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.2.0-7
- fix tranparent issue by convert

* Tue Sep 30 2008 Than Ngo <than@redhat.com> 4.2.0-6
- add missing icon

* Wed Sep 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-5
- Requires: phonon-backend-xine

* Sun Aug 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-4
- rename -backend-gst back to -backend-gstreamer (longer name as -backend-xine)
  The GStreamer backend isn't ready to be the default, and KDE 4.1 also defaults
  to the Xine backend when both are installed.
- fix PulseAudio not being the default in the Xine backend (4.2 regression)

* Sat Aug 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-3
- -backend-gst: Obsoletes: -backend-gstreamer < 4.2.0-2

* Thu Jul 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-2
- rename -backend-gstreamer -> backend-gst

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-1
- phonon-4.2.0

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.4.beta2
- BR: automoc4
- -backend-gstreamer subpkg

* Tue Jul 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2-0.3.beta2
- drop automoc libsuffix patch, no longer needed

* Fri Jun 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.2.beta2
- phonon 4.2beta2 (aka 4.1.83)

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.2-0.1.20080614svn820634
- first try

