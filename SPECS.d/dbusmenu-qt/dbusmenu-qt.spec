
%define snapshot 20150604
%global tarballversion 0.9.2

Summary: A Qt implementation of the DBusMenu protocol 
Name:    dbusmenu-qt
Version: 0.9.3
Release: 0.11.%{snapshot}%{?dist}

License: LGPLv2+
URL: https://launchpad.net/libdbusmenu-qt/
%if 0%{?snapshot}
# bzr branch lp:libdbusmenu-qt && cd libdbusmenu-qt && bzr export --root=libdbusmenu-qt-%{version}-%{snapshot}bzr.tar.gz
Source0:  libdbusmenu-qt-%{version}-%{snapshot}bzr.tar.gz
%else
Source0:  https://launchpad.net/libdbusmenu-qt/trunk/%{version}/+download/libdbusmenu-qt-%{version}.tar.bz2
%endif


## upstream patches

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: pkgconfig
BuildRequires: pkgconfig(QJson)
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtGui) 
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Widgets)
# test-suite
BuildRequires: xorg-x11-server-Xvfb dbus-x11

Provides: libdbusmenu-qt = %{version}-%{release}

%description
This library provides a Qt implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.

%package devel
Summary: Development files for %{name}
Provides: libdbusmenu-qt-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Development and API documentation for %{name}
BuildArch: noarch
# when -doc content was moved here
Conflicts: dbusmenu-qt-devel < 0.9.3
%description doc
%{summary}.

%package -n dbusmenu-qt5
Summary: A Qt implementation of the DBusMenu protocol
Provides: libdbusmenu-qt5 = %{version}-%{release}
%description -n dbusmenu-qt5
This library provides a Qt5 implementation of the DBusMenu protocol.

The DBusMenu protocol makes it possible for applications to export and import
their menus over DBus.

%package -n dbusmenu-qt5-devel
Summary: Development files for dbusmenu-qt5
Provides: libdbusmenu-qt5-devel = %{version}-%{release}
Requires: dbusmenu-qt5%{?_isa} = %{version}-%{release}
%description -n dbusmenu-qt5-devel
%{summary}.


%prep
%setup -q -n libdbusmenu-qt-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DUSE_QT4:BOOL=ON \
  -DUSE_QT5:BOOL=OFF \
  -DWITH_DOC:BOOL=ON

popd

make %{?_smp_mflags} -C %{_target_platform}

mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%cmake .. \
  -DUSE_QT4:BOOL=OFF \
  -DUSE_QT5:BOOL=ON \
  -DWITH_DOC:BOOL=OFF

popd

make %{?_smp_mflags} -C %{_target_platform}-qt5


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5

# unpackaged files
rm -rfv %{buildroot}%{_docdir}/libdbusmenu-qt*-doc


%check
# verify pkg-config version
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion dbusmenu-qt)" = "%{tarballversion}"
test "$(pkg-config --modversion dbusmenu-qt5)" = "%{tarballversion}"
# test suite
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a dbus-launch --exit-with-session make -C %{_target_platform} check ARGS="--output-on-failure --timeout 300" ||:


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%license COPYING
%{_libdir}/libdbusmenu-qt.so.2*

%files devel
%doc %{_target_platform}/html/
%{_includedir}/dbusmenu-qt/
%{_libdir}/libdbusmenu-qt.so
%{_libdir}/cmake/dbusmenu-qt/
%{_libdir}/pkgconfig/dbusmenu-qt.pc

%files doc
%doc %{_target_platform}/html/

%post -n dbusmenu-qt5 -p /sbin/ldconfig
%postun -n dbusmenu-qt5 -p /sbin/ldconfig

%files -n dbusmenu-qt5
%doc README
%license COPYING
%{_libdir}/libdbusmenu-qt5.so.2*

%files -n dbusmenu-qt5-devel
%{_includedir}/dbusmenu-qt5/
%{_libdir}/libdbusmenu-qt5.so
%{_libdir}/pkgconfig/dbusmenu-qt5.pc
%{_libdir}/cmake/dbusmenu-qt5/



%changelog
* Thu Dec 17 2015 Liu Di <liudidi@gmail.com> - 0.9.3-0.11.20150604
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-0.10.20150604
- consolidate dbusmenu-qt5 here (instead of using a separate module)
- fresh(er) 20150604 snapshot
- -doc noarch subpkg

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.2-9
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-6
- .spec cleanup, %%check harder

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 08 2012 Than Ngo <than@redhat.com> - 0.9.2-3
- fix url

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-2
- fix %%check

* Sat Oct 01 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- 0.9.0
- pkgconfig-style deps

* Thu Jun 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-2
- rebuild

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- 0.8.2

* Fri May 20 2011 Rex Dieter <rdieter@fedoraproject.org> 0.6.6-1
- 0.6.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.6.3-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Rex Dieter <rdieter@fedoraproject.org> 0.6.3-1
- dbusmenu-qt-0.6.3
- include kubuntu_00_external_contributions.diff 

* Fri Aug 06 2010 Rex Dieter <rdieter@fedoraproject.org> 0.5.2-1
- dbusmenu-qt-0.5.2

* Fri May 21 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- dbusmenu-qt-0.3.3

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-2
- pkg rename s/libdbusmenu-qt/dbusmenu-qt/
- Provides: libdbusmenu-qt(-devel)

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- dbusmenu-qt-0.3.2

