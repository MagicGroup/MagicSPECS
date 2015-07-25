
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global qt5 1

Name:            polkit-qt
Version:         0.112.0
Release:         5%{?dist}
Summary:         Qt bindings for PolicyKit

License:         GPLv2+
URL:             https://projects.kde.org/projects/kdesupport/polkit-qt-1 
Source0:         http://download.kde.org/stable/apps/KDE4.x/admin/polkit-qt-1-%{version}.tar.bz2 
Source1:         Doxyfile

Patch0:          polkit-qt-0.95.1-install-cmake-find.patch

## upstream patches

Source10:        macros.polkit-qt

BuildRequires:   automoc4
BuildRequires:   cmake
BuildRequires:   doxygen
BuildRequires:   pkgconfig(polkit-agent-1) pkgconfig(polkit-gobject-1)
BuildRequires:   pkgconfig(QtDBus) pkgconfig(QtGui) pkgconfig(QtXml)
%if 0%{?qt5}
BuildRequires:   pkgconfig(Qt5DBus) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets) pkgconfig(Qt5Xml)
%endif

Obsoletes:       polkit-qt-examples < 0.10

Provides:        polkit-qt-1 = %{version}-%{release}

%description
Polkit-qt is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package devel
Summary: Development files for PolicyKit Qt bindings
Provides: polkit-qt-1-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Doxygen documentation for the PolkitQt API
BuildArch: noarch
%description doc
%{summary}.

%if 0%{?qt5}
%package -n polkit-qt5-1
Summary: PolicyKit Qt5 bindings
Provides: polkit-qt5 = %{version}-%{release}
%description -n polkit-qt5-1
Polkit-qt is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package -n polkit-qt5-1-devel
Summary: Development files for PolicyKit Qt5 bindings
Provides: polkit-qt5-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description -n polkit-qt5-1-devel
%{summary}.
%endif


%prep
%setup -q -n %{name}-1-%{version}

# temporary patch - installs FindPolkitQt-1.cmake until we decide how to deal with cmake 
# module installation
%patch0 -p1 -b .install-cmake-find


%build
mkdir -p %{_target_platform}
pushd    %{_target_platform}
%{cmake} \
  -DUSE_QT4:BOOL=ON -DUSE_QT5:BOOL=OFF \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DDATA_INSTALL_DIR:PATH=%{_datadir} \
  ..
popd
make %{?_smp_mflags} -C %{_target_platform}

%if 0%{?qt5}
mkdir -p %{_target_platform}-qt5
pushd    %{_target_platform}-qt5
%{cmake} \
  -DUSE_QT4:BOOL=OFF -DUSE_QT5:BOOL=ON \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DDATA_INSTALL_DIR:PATH=%{_datadir} \
  ..
popd
make %{?_smp_mflags} -C %{_target_platform}-qt5
%endif

## build docs
doxygen %{SOURCE1}
# Remove installdox file - it is not necessary here
rm -fv html/installdox


%install
%if 0%{?qt5}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-qt5
%endif
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

install -p -m644 -D %{SOURCE10} %{buildroot}%{rpm_macros_dir}/macros.polkit-qt


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/libpolkit-qt-core-1.so.1*
%{_libdir}/libpolkit-qt-gui-1.so.1*
%{_libdir}/libpolkit-qt-agent-1.so.1*

%files devel
%{rpm_macros_dir}/macros.polkit-qt
%{_includedir}/polkit-qt-1/
%{_libdir}/libpolkit-qt-core-1.so
%{_libdir}/libpolkit-qt-gui-1.so
%{_libdir}/libpolkit-qt-agent-1.so
%{_libdir}/pkgconfig/polkit-qt-1.pc
%{_libdir}/pkgconfig/polkit-qt-core-1.pc
%{_libdir}/pkgconfig/polkit-qt-gui-1.pc
%{_libdir}/pkgconfig/polkit-qt-agent-1.pc
%{_libdir}/cmake/PolkitQt-1/
%{_datadir}/cmake/Modules/*.cmake

%files doc
%doc html/*

%if 0%{?qt5}
%post -n polkit-qt5-1 -p /sbin/ldconfig
%postun -n polkit-qt5-1 -p /sbin/ldconfig

%files -n polkit-qt5-1
%doc AUTHORS COPYING README
%{_libdir}/libpolkit-qt5-core-1.so.1*
%{_libdir}/libpolkit-qt5-gui-1.so.1*
%{_libdir}/libpolkit-qt5-agent-1.so.1*

%files -n polkit-qt5-1-devel
%{rpm_macros_dir}/macros.polkit-qt
%{_includedir}/polkit-qt5-1/
%{_libdir}/libpolkit-qt5-core-1.so
%{_libdir}/libpolkit-qt5-gui-1.so
%{_libdir}/libpolkit-qt5-agent-1.so
%{_libdir}/pkgconfig/polkit-qt5-1.pc
%{_libdir}/pkgconfig/polkit-qt5-core-1.pc
%{_libdir}/pkgconfig/polkit-qt5-gui-1.pc
%{_libdir}/pkgconfig/polkit-qt5-agent-1.pc
%{_libdir}/cmake/PolkitQt5-1/
%endif


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.112.0-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Oct 24 2014 Rex Dieter <rdieter@fedoraproject.org> 0.112.0-3
- build polkit-qt5-1(-devel) here 

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.112.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Martin Bříza <mbriza@redhat.com> - 0.112.0-1
- polkit-qt-1-0.112.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.103.0-10
- -devel: use %%_rpmconfigdir/macros.d (where supported)
- .spec cleanup

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.103.0-9
- pull in some more upstream fixes (from mbriza)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.103.0-7
- pull in some upstream patches
- .spec cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Than Ngo <than@redhat.com> - 0.103.0-5
- fix url

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Than Ngo <than@redhat.com> - 0.103.0-3
- fix build issue with doxygen-1.8.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Jaroslav Reznik <jreznik@redhat.com> 0.103.0-1
- polkit-qt-1-0.103.0

* Mon Dec 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-3
- upstream crash patch (kde#258916,#684625)
- pull a couple more upstream patches
- -devel: drop Req: polkit-devel

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.99.0-1
- polkit-qt-1-0.99.0

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> -  0.98.1-1.20101120
- polkit-qt-1-0.98.1-20101120 snapshot

* Fri Oct 15 2010 Radek Novacek <rnovacek@redhat.com> - 0.96.1-4
- Next attempt of fix-deprecated-warnings patch

* Thu Oct 14 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.96.1-3
- Revert fix-deprecated-warnings as it causes kde#254150

* Thu Oct 07 2010 Radek Novacek <rnovacek@redhat.com> 0.96.1-2
- Fixed deprecation warning with polkit-0.98
- Fixed typo in url
- Null checking patch (might be fix for #637064)

* Tue Sep 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.96.1-1
- polkit-qt-1-0.96.1

* Thu Jan 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-3
- macros.polkit-qt : %%_polkit_qt_policydir, %%_polkit_qt

* Thu Jan 14 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-2
- Installs FindPolkitQt-1.cmake

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-1
- Update to release version

* Sun Dec 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.95-0.3.20091119svn
- Provides: polkit-qt-1(-devel) ...
- doc: make noarch

* Wed Dec 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org>  - 0.95-0.2.20091119svn
- Obsoletes: polkit-qt-examples < 0.10 for upgrade path

* Mon Nov 23 2009 Radek Novacek <rnovacek@redhat.com> - 0.95-0.1.20091119svn
- Added -doc subpackage
- Added command to obtaining the source code

* Fri Nov 20 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.1.20091119svn
- SPEC file fixes
- removed -examples subpackage

* Thu Nov 19 2009 Radek Novacek <rnovacek@redhat.com> - 0.1.20091119svn
- Initial build of snapshot from svn
