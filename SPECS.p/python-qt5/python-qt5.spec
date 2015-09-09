
%if 0%{?fedora}
%global with_python3 1
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")
#global python3_dbus_dir %(d=%{python3_sitearch}/dbus/mainloop; [ -d $d ] || d=%{python3_sitelib}/dbus/mainloop; echo $d)
%endif
%global with_python2 1
%global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")
#global python2_dbus_dir %(d=%{python2_sitearch}/dbus/mainloop; [ -d $d ] || d=%{python2_sitelib}/dbus/mainloop; echo $d)

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Summary: Python bindings for Qt5
Name: 	 python-qt5 
Version: 5.5
Release: 1%{?dist}

# all BSD, except for GPLv2+ dbus bindings and examples
License: BSD and GPLv2+
Url:     http://www.riverbankcomputing.com/software/pyqt/
%if 0%{?snap:1}
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt5/PyQt-gpl-%{version}%{?snap:-snapshot-%{snap}}.tar.gz
%else
#Source0: http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-%{version}/PyQt-gpl-%{version}.tar.gz
Source0: http://www.riverbankcomputing.com/static/Downloads/PyQt5/PyQt-gpl-%{version}.tar.gz
%endif
Source1: macros.pyqt5
# wrapper, see https://bugzilla.redhat.com/show_bug.cgi?id=1193107#c9
Source2: pyuic5.sh

## upstream patches

## upstreamable patches
Patch0: python-qt5_sipdir.patch

BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5Core) >= 5.3
BuildRequires: pkgconfig(Qt5Bluetooth)
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Declarative)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Gui) pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Location)
BuildRequires: pkgconfig(Qt5Nfc)
BuildRequires: pkgconfig(Qt5Network) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Quick) pkgconfig(Qt5QuickWidgets)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Sensors)
BuildRequires: pkgconfig(Qt5SerialPort)
BuildRequires: pkgconfig(Qt5Sql) pkgconfig(Qt5Svg) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Xml) pkgconfig(Qt5XmlPatterns)
BuildRequires: pkgconfig(Qt5WebChannel)
BuildRequires: pkgconfig(Qt5WebKit) pkgconfig(Qt5WebKitWidgets)
BuildRequires: pkgconfig(Qt5WebSockets)
BuildRequires: python2-devel
BuildRequires: sip-devel >= 4.16.9
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-sip-devel >= 4.16.8
BuildRequires: python3-dbus
%endif # with_python3

Requires: dbus-python
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%filter_provides_in %{python_sitearch} %{?_qt5_plugindir}
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch} %{?_qt5_plugindir}
%endif
%filter_setup

Provides: PyQt5 = %{version}-%{release}
Provides: PyQt5%{?_isa} = %{version}-%{release}

%description
These are Python bindings for Qt5.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
Requires: sip-devel
Provides: PyQt5-devel = %{version}-%{release}
%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt5 classes (e.g. KDE or your own).

%package -n python3-qt5
Summary: Python 3 bindings for Qt5
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
Provides: python3-PyQt5 = %{version}-%{release}
Requires: python3-dbus
%description -n python3-qt5
%{summary}.

%package -n python3-qt5-devel
Summary: Python 3 bindings for Qt5
Requires: python3-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
Requires: python3-sip-devel
Provides: python3-PyQt5-devel = %{version}-%{release}
%description -n python3-qt5-devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt5 classes

%package doc
Summary: Developer documentation for %{name} 
Provides: PyQt5-doc = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n PyQt-gpl-%{version}%{?snap:-snapshot-%{snap}}
%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
PATH=%{_qt5_bindir}:$PATH ; export PATH

# Python 2 build:
%if 0%{?with_python2}
%{__python2} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt5_qmake} \
  --qsci-api --qsci-api-destdir=%{_qt5_datadir}/qsci \
  --verbose 

make %{?_smp_mflags}
%endif # with_python2

# Python 3 build:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt5_qmake} \
  --no-qsci-api \
  --verbose

make %{?_smp_mflags}
popd
%endif # with_python3


%install

# Python 3 build:
%if 0%{?with_python3}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{py3dir}
# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python3_sitearch}/PyQt5/*.so %{buildroot}%{python3_dbus_dir}/pyqt5.so ; do
chmod a+rx $i
done
%endif # with_python3

# Python 2 build:
%if 0%{?with_python2}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
# ensure .so modules are executable for proper -debuginfo extraction
for i in %{buildroot}%{python2_sitearch}/PyQt5/*.so %{buildroot}%{python2_dbus_dir}/pyqt5.so ; do
chmod a+rx $i
done
%endif # with_python2

# remove Python3 code from Python2 directory, fixes FTBFS like PyQt4 (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt5/uic/port_v3/
# remove Python2 code from Python3 directory (for when/if we support python3 here)
rm -rfv %{buildroot}%{python3_sitearch}/PyQt5/uic/port_v2/

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5

%if 0%{?_with_python3}
# install pyuic5 wrapper to handle both/either python2/python3
rm -fv %{buildroot}%{_bindir}/pyuic5
install -p -m755 -D %{SOURCE2} \
  %{buildroot}%{_bindir}/pyuic5
sed -i \
  -e "s|@PYTHON3@|%{__python3}|g" \
  -e "s|@PYTHON2@|%{__python2}|g" \
  %{buildroot}%{_bindir}/pyuic5
%endif


%if 0%{?with_python2}
%files
%doc NEWS README
%doc LICENSE
%{rpm_macros_dir}/macros.pyqt5
%{python2_dbus_dir}/pyqt5.so
%{_qt5_plugindir}/PyQt5/
%dir %{python2_sitearch}/PyQt5/
%{python2_sitearch}/PyQt5/__init__.py*
%{python2_sitearch}/PyQt5/Qt.so
%{python2_sitearch}/PyQt5/QtBluetooth.so
%{python2_sitearch}/PyQt5/QtCore.so
%{python2_sitearch}/PyQt5/QtDBus.so
%{python2_sitearch}/PyQt5/QtDesigner.so
%{python2_sitearch}/PyQt5/QtGui.so
%{python2_sitearch}/PyQt5/QtHelp.so
%{python2_sitearch}/PyQt5/QtLocation.so
%{python2_sitearch}/PyQt5/QtMultimedia.so
%{python2_sitearch}/PyQt5/QtMultimediaWidgets.so
%{python2_sitearch}/PyQt5/QtNetwork.so
%{python2_sitearch}/PyQt5/QtNfc.so
%{python2_sitearch}/PyQt5/QtOpenGL.so
%{python2_sitearch}/PyQt5/QtPositioning.so
%{python2_sitearch}/PyQt5/QtPrintSupport.so
%{python2_sitearch}/PyQt5/QtQml.so
%{python2_sitearch}/PyQt5/QtQuick.so
%{python2_sitearch}/PyQt5/QtQuickWidgets.so
%{python2_sitearch}/PyQt5/QtSensors.so
%{python2_sitearch}/PyQt5/QtSerialPort.so
%{python2_sitearch}/PyQt5/QtSql.so
%{python2_sitearch}/PyQt5/QtSvg.so
%{python2_sitearch}/PyQt5/QtTest.so
%{python2_sitearch}/PyQt5/QtWebChannel.so
%{python2_sitearch}/PyQt5/QtWebKit.so
%{python2_sitearch}/PyQt5/QtWebKitWidgets.so
%{python2_sitearch}/PyQt5/QtWebSockets.so
%{python2_sitearch}/PyQt5/QtWidgets.so
%{python2_sitearch}/PyQt5/QtX11Extras.so
%{python2_sitearch}/PyQt5/QtXml.so
%{python2_sitearch}/PyQt5/QtXmlPatterns.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_2_0.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_2_1.so
%{python2_sitearch}/PyQt5/_QOpenGLFunctions_4_1_Core.so
%{python2_sitearch}/PyQt5/uic/
%{_qt5_plugindir}/designer/libpyqt5.so

%files devel
%{_bindir}/pylupdate5
%{_bindir}/pyrcc5
%{_bindir}/pyuic5
%{_datadir}/sip/PyQt5/
%endif

%if 0%{?with_python3}
%files -n python3-qt5
%doc NEWS README
%doc LICENSE
%{rpm_macros_dir}/macros.pyqt5
%{python3_dbus_dir}/pyqt5.so
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/PyQt5/__pycache__/
%{python3_sitearch}/PyQt5/__init__.py*
%{python3_sitearch}/PyQt5/Qt.so
%{python3_sitearch}/PyQt5/QtBluetooth.so
%{python3_sitearch}/PyQt5/QtCore.so
%{python3_sitearch}/PyQt5/QtDBus.so
%{python3_sitearch}/PyQt5/QtDesigner.so
%{python3_sitearch}/PyQt5/QtGui.so
%{python3_sitearch}/PyQt5/QtHelp.so
%{python3_sitearch}/PyQt5/QtLocation.so
%{python3_sitearch}/PyQt5/QtMultimedia.so
%{python3_sitearch}/PyQt5/QtMultimediaWidgets.so
%{python3_sitearch}/PyQt5/QtNetwork.so
%{python3_sitearch}/PyQt5/QtNfc.so
%{python3_sitearch}/PyQt5/QtOpenGL.so
%{python3_sitearch}/PyQt5/QtPositioning.so
%{python3_sitearch}/PyQt5/QtPrintSupport.so
%{python3_sitearch}/PyQt5/QtQml.so
%{python3_sitearch}/PyQt5/QtQuick.so
%{python3_sitearch}/PyQt5/QtQuickWidgets.so
%{python3_sitearch}/PyQt5/QtSensors.so
%{python3_sitearch}/PyQt5/QtSerialPort.so
%{python3_sitearch}/PyQt5/QtSql.so
%{python3_sitearch}/PyQt5/QtSvg.so
%{python3_sitearch}/PyQt5/QtTest.so
%{python3_sitearch}/PyQt5/QtWebChannel.so
%{python3_sitearch}/PyQt5/QtWebKit.so
%{python3_sitearch}/PyQt5/QtWebKitWidgets.so
%{python3_sitearch}/PyQt5/QtWebSockets.so
%{python3_sitearch}/PyQt5/QtWidgets.so
%{python3_sitearch}/PyQt5/QtX11Extras.so
%{python3_sitearch}/PyQt5/QtXml.so
%{python3_sitearch}/PyQt5/QtXmlPatterns.so
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_0.so
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_1.so
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_4_1_Core.so
%{python3_sitearch}/PyQt5/uic/

%files -n python3-qt5-devel
%{_bindir}/pylupdate5
%{_bindir}/pyrcc5
%{_bindir}/pyuic5
%{_datadir}/python3-sip/PyQt5/
%endif # with_python3

%files doc
%doc doc/*
%doc examples/
# avoid dep on qscintilla-python, own %_qt5_datadir/qsci/... here for now
%dir %{_qt5_datadir}/qsci/
%dir %{_qt5_datadir}/qsci/api/
%dir %{_qt5_datadir}/qsci/api/python/
%doc %{_qt5_datadir}/qsci/api/python/PyQt5.api


%changelog
* Thu Jul 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5-1
- 5.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- 5.4.2

* Fri Jun 05 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-5
- wrong python release used in pyuic5 launch script (#1193107)
- -doc: add qsci doc QyQt5.api content
- enable Qt5WebChannel/Qt5WebSockets support

* Fri Jun 05 2015 Sandro Mani <manisandro@gmail.com> - 5.4.1-4
- Add patch to fix python3 sip installation dir (#1228432)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- rebuild (sip)

* Thu Feb 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-6
- rebuild (sip)

* Tue Jan 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-5
- +macros.pyqt5

* Fri Jan 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-4
- -devel: restore dep on base pkg

* Sun Dec 28 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4-3
- python3-qt5-devel subpkg

* Sat Dec 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-2
- ensure .so modules are executable (for proper -debuginfo extraction)

* Fri Dec 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-1
- 5.4

* Thu Nov 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-6
- restore python3 support

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-5
- pkgconfig(QtOpenGL) being satisfied by qt4 devel (#1162415)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- try to determine dbus-python install paths dynamically (#1161121)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-3
- Build failure in sipQtWebKitWidgestQWebInspector: qprinter.h not found (#1160932)
- python2_sitelib should be python2_sitearch (#1161121)

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- PyQt-gpl-5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-1
- PyQt-gpl-5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-2
- python3: (Build)Requires: python3-dbus

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-1
- PyQt-gpl-5.3
- +Qt5Bluetooth,Qt5Quick,Qt5SerialPorts support

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (f21-python)
- +Qt5Positioning,Qt5Sensors support

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- PyQt-5.2.1

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2-5
- Rebuild against fixed qt5-qtbase to fix -debuginfo (#1065636)

* Sat Feb 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-4
- python3-qt5 support

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-3
- Provides: PyQt5

* Thu Feb 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-2
- BR: python2-devel, use %%__python2 macro

* Wed Jan 08 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-1
- PyQt-5.2

