
Summary: Gstreamer phonon backend 
Name:    phonon-backend-gstreamer
Epoch:   2
Version: 4.6.2
Release: 2%{?dist}
Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://phonon.kde.org/
%if 0%{?snap}
Source0: phonon-backend-gstreamer-%{version}-%{snap}.tar.bz2
# run this script to generate a snapshot tarball
Source1: phonon-gstreamer_snapshot.sh
%else
Source0: http://download.kde.org/stable/phonon/phonon-backend-gstreamer/%{version}/src/phonon-backend-gstreamer-%{version}.tar.xz
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstream patches

BuildRequires: automoc4
BuildRequires: cmake
BuildRequires: pkgconfig(gstreamer-0.10) 
BuildRequires: pkgconfig(gstreamer-app-0.10) pkgconfig(gstreamer-audio-0.10) pkgconfig(gstreamer-video-0.10)
BuildRequires: pkgconfig(phonon) >= 4.5.50
BuildRequires: pkgconfig(QtOpenGL)

%global phonon_version %(pkg-config --modversion phonon 2>/dev/null || echo 4.5.0)

Provides: phonon-backend%{?_isa} = %{phonon_version}

Obsoletes: phonon-backend-gst < 4.2.0-4
Provides:  phonon-backend-gst = %{version}-%{release}

Obsoletes: phonon-gstreamer < 4.4.4-0.2
Provides:  phonon-gstreamer = %{version}-%{release}

# provide upgrade path for deprecated/removed -xine backend
Obsoletes: phonon-backend-xine < 4.5.0

Requires: gstreamer-plugins-good
# not *strictly* required, but strongly recommended by upstream when built
# with USE_INSTALL_PLUGIN
#Requires: PackageKit-gstreamer-plugin
Requires: phonon%{?_isa} => %{phonon_version}
Requires: qt4%{?_isa} >= %{_qt4_version}

%description
%{summary}.


%prep
%setup -q -n phonon-backend-gstreamer-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DUSE_INSTALL_PLUGIN:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:

%files
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_kde4_libdir}/kde4/plugins/phonon_backend/phonon_gstreamer.so
%{_kde4_datadir}/kde4/services/phononbackends/gstreamer.desktop
%{_datadir}/icons/hicolor/*/apps/phonon-gstreamer.*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2:4.6.2-2
- 为 Magic 3.0 重建

* Mon Aug 13 2012 Rex Dieter <rdieter@fedoraproject.org> 2:4.6.2-1
- 4.6.2

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 2:4.6.1-3
- upstream fixes for gapless/repeat issues seen in amarok (#841941)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> 4.6.1-1
- 4.6.1

* Fri Feb 17 2012 Rex Dieter <rdieter@fedoraproject.org> 4.6.0-1
- 4.6.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.5.90-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.90-4
- drop hard dep on PackageKit-gstreamer-plugin

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.90-3
- Obsoletes: phonon-backend-xine < 4.5.0

* Fri Sep 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.90-2
- 4.5.90
- pkgconfig-style deps

* Mon Jun 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.1-2
- drop old flac_mimetype patch, no longer needed

* Fri May 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.1-1
- 4.5.1

* Fri May 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.1-0.1.20110505
- 20110505 snapshot

* Sun Apr 10 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.5.0-1
- 4.5.0

* Tue Feb 15 2011 Rex Dieter <rdieter@fedoraproject.org> 2:4.4.4-3
- upstream patch for better(working) dvd playback

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:4.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.4.4-1
- phonon-backend-gstreamer-4.4.4

* Fri Jan 07 2011 Rex Dieter <rdieter@fedoraproject.org> - 2:4.4.4-0.4.20110104
- Requires: PackageKit-gstreamer-plugin , avoids potential crashers elsewhere 
  when built with USE_INSTALL_PLUGIN (kde#262308)

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 2:4.4.4-0.3.20110104
- %%doc COPYING.LIB
- add comment on pnonon-gstreamer_snapshot.sh usage

* Wed Jan 05 2011 Rex Dieter <rdieter@fedoraproject.org> - 2:4.4.4-0.2.20110104
- phonon-backend-gstreamer

* Tue Jan 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.4.4-0.1.20110104
- phonon-gstreamer-4.4.4-20110104 snapshot

