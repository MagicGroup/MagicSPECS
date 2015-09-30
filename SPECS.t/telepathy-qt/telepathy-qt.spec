
%if 0%{?build_from_snapshot}
%global snap 20140403
%global git_commit 0191a6ddf0c094d9ae61b9ee48f1b282e13a9ef2
%global git_hash   0191a6dd
%endif

%if 0%{?fedora} > 20
%global farstream 1
%endif
%global qt5 1

## unit tests
%global enable_tests -DENABLE_TESTS:BOOL=ON

Name:    telepathy-qt
Version: 0.9.6.1
Release: 1%{?dist}
Summary: High-level bindings for Telepathy

License: LGPLv2+
URL:     http://telepathy.freedesktop.org/doc/telepathy-qt/
%if 0%{?snap:1}
# git clone http://anongit.freedesktop.org/git/telepathy/telepathy-qt.git; cd telepathy-qt
# git archive --prefix=telepathy-qt-0.9.3.1/ 0191a6ddf0c094d9ae61b9ee48f1b282e13a9ef2 | gzip -9 >
Source0: telepathy-qt-%{version}-%{git_hash}.tar.gz
%else
Source0: http://telepathy.freedesktop.org/releases/telepathy-qt/telepathy-qt-%{version}.tar.gz
%endif

## upstreamable patches
Patch1:  telepathy-qt-0.9.5-static_fPIC.patch

# workaround fact that included FindGStreamer.cmake is limited, only allows for single INCLUDE_DIR,
# this one supports INCLUDE_DIRS and a whole lot more.
# a *proper* fix, imho, would be to not re-invent pkg-config wheel and just use
# PKG_CHECK_MODULES(TELEPATHY_FARSTREAM telepathy-farstream) for all cflags/libs -- rex
Source10: https://raw.githubusercontent.com/WebKit/webkit/master/Source/cmake/FindGStreamer.cmake
# accomodates GSTREAMER_INCLUDE_DIR => GSTREAMER_INCLUDE_DIRS change
Patch2:  telepathy-qt-0.9.6.1-gst1.5.patch

## upstream patches

BuildRequires: cmake
BuildRequires: dbus-python python2-devel
BuildRequires: doxygen
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtNetwork) pkgconfig(QtXml)
%if 0%{?farstream}
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(farstream-0.2)
BuildRequires: pkgconfig(telepathy-farstream) >= 0.6
BuildRequires: pkgconfig(telepathy-glib) >= 0.18
%else
Obsoletes: telepathy-qt4-farstream < %{version}-%{release}
%endif

%if 0%{?enable_tests:1}
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(telepathy-glib) >= 0.18
%endif

Obsoletes: telepathy-qt4-farsight < 0.9.3
Requires: telepathy-mission-control

%description
Telepathy-qt are high level bindings for Telepathy and provides both
the low level 1:1 auto generated API, and a high-level API build
on top of that, in the same library.

%package -n telepathy-qt4
Summary: High-level Qt4 bindings for Telepathy
Requires: telepathy-mission-control
%description -n telepathy-qt4
Telepathy-qt4 are high level bindings for Telepathy and provides both
the low level 1:1 auto generated API, and a high-level API build
on top of that, in the same library.

%package -n telepathy-qt4-devel
Summary: Development files for telepathy-qt4
Provides: telepathy-qt-devel = %{version}-%{release}
Requires: telepathy-qt4%{?_isa} = %{version}-%{release}
Requires: telepathy-filesystem
Obsoletes: telepathy-qt4-farstream-devel < 0.9.1-2
%if 0%{?farstream}
Requires: telepathy-qt4-farstream%{?_isa} = %{version}-%{release}
Provides:  telepathy-qt4-farstream-devel = %{version}-%{release}
Provides:  telepathy-qt-farstream-devel = %{version}-%{release}
%endif
%description -n telepathy-qt4-devel
%{summary}.

%if 0%{?farstream}
%package -n telepathy-qt4-farstream
Summary: Farstream telepathy-qt4 bindings
Requires: telepathy-qt4%{?_isa} = %{version}-%{release}
Provides:  telepathy-qt-farstream = %{version}-%{release}
Provides:  telepathy-qt-farstream%{?_isa} = %{version}-%{release}
%description -n telepathy-qt4-farstream
%{summary}.
%endif

%if 0%{?qt5}
%package -n telepathy-qt5
Summary: High-level Qt5 bindings for Telepathy
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Network) pkgconfig(Qt5Xml)
Requires: telepathy-mission-control
%description -n telepathy-qt5
Telepathy-qt5 are high level bindings for Telepathy and provides both
the low level 1:1 auto generated API, and a high-level API build
on top of that, in the same library.

%package -n telepathy-qt5-devel
Summary: Development files for telepathy-qt5
Requires: telepathy-qt5%{?_isa} = %{version}-%{release}
Requires: telepathy-filesystem
%if 0%{?farstream}
Requires: telepathy-qt5-farstream%{?_isa} = %{version}-%{release}
%endif
%description -n telepathy-qt5-devel
%{summary}.

%if 0%{?farstream}
%package -n telepathy-qt5-farstream
Summary: Farstream telepathy-qt5 bindings
Requires: telepathy-qt5%{?_isa} = %{version}-%{release}
%description -n telepathy-qt5-farstream
%{summary}.
%endif
%endif


%prep
%autosetup -n telepathy-qt-%{version} -p1

install -m644 -p %{SOURCE10} --backup --suffix=.gst1.5 cmake/modules/FindGStreamer.cmake 


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING=release \
  -DDESIRED_QT_VERSION=4 \
  -DDISABLE_WERROR:BOOL=ON \
  %{?enable_tests}%{!?enable_tests:-DENABLE_TESTS:BOOL=OFF} \
  %{?farstream:-DENABLE_FARSTREAM:BOOL=ON} \
  %{!?farstream:-DENABLE_FARSTREAM:BOOL=OFF}
popd

make %{?_smp_mflags} -C %{_target_platform}

%if 0%{?qt5}
mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%{cmake} .. \
  -DCMAKE_BUILD_TYPE:STRING=release \
  -DDESIRED_QT_VERSION=5 \
  -DDISABLE_WERROR:BOOL=ON \
  %{?enable_tests}%{!?enable_tests:-DENABLE_TESTS:BOOL=OFF} \
  %{?farstream:-DENABLE_FARSTREAM:BOOL=ON} \
  %{!?farstream:-DENABLE_FARSTREAM:BOOL=OFF}
popd

make %{?_smp_mflags} -C %{_target_platform}-qt5
%endif


%install
%if 0%{?qt5}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5
%endif
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -n telepathy-qt4 -p /sbin/ldconfig
%postun -n telepathy-qt4 -p /sbin/ldconfig

%files -n telepathy-qt4
%doc COPYING AUTHORS NEWS README ChangeLog
%{_libdir}/libtelepathy-qt4.so.2*

%if 0%{?farstream}
%post -n telepathy-qt4-farstream -p /sbin/ldconfig
%postun -n telepathy-qt4-farstream -p /sbin/ldconfig

%files -n telepathy-qt4-farstream
%{_libdir}/libtelepathy-qt4-farstream.so.2*
%endif

%files -n telepathy-qt4-devel
%doc HACKING
%dir %{_includedir}/telepathy-qt4/
%{_includedir}/telepathy-qt4/TelepathyQt/
%{_libdir}/libtelepathy-qt4.so
%{_libdir}/pkgconfig/TelepathyQt4.pc
%{_libdir}/pkgconfig/TelepathyQt4Service.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/TelepathyQt4/
%{_libdir}/cmake/TelepathyQt4Service/
%{_libdir}/libtelepathy-qt4-service.a
%if 0%{?farstream}
%{_libdir}/libtelepathy-qt4-farstream.so
%{_libdir}/pkgconfig/TelepathyQt4Farstream.pc
%{_libdir}/cmake/TelepathyQt4Farstream/
%endif

%if 0%{?qt5}
%post -n telepathy-qt5 -p /sbin/ldconfig
%postun -n telepathy-qt5 -p /sbin/ldconfig

%files -n telepathy-qt5
%doc COPYING AUTHORS NEWS README ChangeLog
%{_libdir}/libtelepathy-qt5.so.0*

%if 0%{?farstream}
%post -n telepathy-qt5-farstream -p /sbin/ldconfig
%postun -n telepathy-qt5-farstream -p /sbin/ldconfig

%files -n telepathy-qt5-farstream
%{_libdir}/libtelepathy-qt5-farstream.so.0*
%endif

%files -n telepathy-qt5-devel
%doc HACKING
%dir %{_includedir}/telepathy-qt5/
%{_includedir}/telepathy-qt5/TelepathyQt/
%{_libdir}/libtelepathy-qt5.so
%{_libdir}/pkgconfig/TelepathyQt5.pc
%{_libdir}/pkgconfig/TelepathyQt5Service.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/TelepathyQt5/
%{_libdir}/cmake/TelepathyQt5Service/
%{_libdir}/libtelepathy-qt5-service.a
%if 0%{?farstream}
%{_libdir}/libtelepathy-qt5-farstream.so
%{_libdir}/pkgconfig/TelepathyQt5Farstream.pc
%{_libdir}/cmake/TelepathyQt5Farstream/
%endif
%endif


%changelog
* Sat Jun 20 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.6.1-1
- 0.9.6.1
- workaround FTBFS against gstreamer-1.5 (#1234051)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.5-4
- Rebuilt for GCC 5 C++11 ABI change

* Mon Feb 23 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.5-3
- build static libtelepathy-qt?-service.a with -fPIC
- pull in a couple minor upstream fixes

* Fri Oct 03 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.5-2
- bump deps for newer farstream/gst1
- Qt5 support
- rename base pkg to telepathy-qt (to match upstream), but...
- keep subpkg names the same (telepathy-qt4), for simple/obvious upgrade path

* Wed Sep 17 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.5.0-1
- Update to 0.9.5.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.1-0.4.20140403git0191a6dd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.3.1-0.3.20140403git0191a6dd
- build against farstream 0.2 and GStreamer 1 on F21+ (#1092654)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.1-0.2.20140403git0191a6dd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.3.1-0.1.20140403git0191a6dd
- 0.9.3.1 snapshot, fixes FTBFS

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-6
- respin farstream_compat patch

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-5
- fix build for newer compat-telepathy-farstream

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-4
- rework spec/macro conditionals a bit

* Tue Oct 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-3
- (Build)Requires: compat-telepathy-farstream-devel (f18+)

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-2
- rebuild (farstream)

* Fri Aug 03 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-1.1
- move Obsoletes: -farsight to main pkg

* Mon Jul 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-1
- telepathy-qt-0.9.3

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Tue May 22 2012 Radek Novacek <rnovacek@redhat.com> 0.9.1-4
- add rhel condition

* Thu Apr 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-3
- -farsight subpkg (f16)

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-2
- drop -farstream-devel subpkg

* Sat Mar 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- 0.9.1
- -farstream(-devel) subpkgs

* Tue Mar 06 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-3
- drop telepathy-farsight support (awaiting upstream -farstream love)

* Fri Feb 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-2
- Requires: telepathy-mission-control

* Wed Jan 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- telepathy-qt-0.9.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-2
- drop Requires: gnome-keyring

* Sat Nov 19 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- 0.8.0

* Mon Nov 07 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.3-1
- 0.7.3
- pkgconfig-style deps

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-1
- 0.7.2
- Requires: gnome-keyring

* Fri Jul 15 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.7.1-1
- initial package
