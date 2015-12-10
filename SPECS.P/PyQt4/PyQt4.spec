%global with_python3 1
%global qscintilla 1
%global qtassistant 1
%global webkit 1

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

%endif
%{!?__python2:%global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}
%global python2_dbus_dir %(%{__python2} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])")

Summary: Python bindings for Qt4
Summary(zh_CN.UTF-8): Qt4 的 Python 绑定
Name: 	 PyQt4
Version: 4.11.4
Release: 3%{?dist}

# GPLv2 exceptions(see GPL_EXCEPTIONS*.txt)
License: GPLv3 or GPLv2 with exceptions
Group: 	 Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Url:     http://www.riverbankcomputing.com/software/pyqt/
Source0:  http://downloads.sourceforge.net/pyqt/PyQt-x11-gpl%{?snap:-snapshot}-%{version}%{?snap:-%{snap}}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


## upstreamable patches
# fix multilib conflict because of timestamp
Patch50:  PyQt-x11-gpl-4.9.5-timestamp_multilib.patch 
Patch52:  PyQt-x11-gpl-4.10.4-pyuic_shbang.patch

## upstream patches
# fix FTBFS on ARM
Patch60:  qreal_float_support.diff

# rhel patches
Patch300: PyQt-x11-gpl-4.10-webkit.patch

BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1) pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(python)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtNetwork)
%if 0%{?fedora}
# beware of PyQt4/qscintilla bootstap issues
BuildRequires: qscintilla
BuildRequires: pkgconfig(QtWebKit)
%endif
BuildRequires: sip-devel >= 4.14.6

%if 0%{?with_python3}
BuildRequires: python3-devel 
BuildRequires: python3-sip-devel >= 4.14.2
%endif # with_python3

Requires: dbus-python
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}

%if 0%{?fedora}
# could theoretically enumerate all the modules built/packaged here, but this
# should be good start (to ease introduction of -webkit for epel-6+ for example)
Provides: %{name}-webkit = %{version}-%{release}
Provides: %{name}-webkit%{?_isa} = %{version}-%{release}
%endif

Provides: python-qt4 = %{version}-%{release}
Provides: pyqt4 = %{version}-%{release}

%description
These are Python bindings for Qt4.

%description -l zh_CN.UTF-8
Qt4 的 Python 绑定。

%package devel
Summary: Files needed to build other bindings based on Qt4
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:	 Development/Languages
Group(zh_CN.UTF-8): 开发/语言
%if 0%{?fedora}
Provides: %{name}-webkit-devel = %{version}-%{release}
Provides: %{name}-webkit-devel%{?_isa} = %{version}-%{release}
%endif
Provides: pyqt4-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
Requires: sip-devel

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt4 classes (e.g. KDE or your own).

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: PyQt4 developer documentation and examples
Summary(zh_CN.UTF-8): %{name} 的文档和样例
BuildArch: noarch
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-doc = %{version}-%{release}
%description doc
%{summary}.

%description doc -l zh_CN.UTF-8
 %{name} 的文档和样例。

# split-out arch'd subpkg, since (currently) %%_qt4_datadir = %%_qt4_libdir
%package qsci-api
Summary: Qscintilla API file support
Summary(zh_CN.UTF-8): Qscintilla API 文档支持包
# when split happened, upgrade path
Obsoletes: PyQt4-devel < 4.10.3-6
Obsoletes: python3-PyQt4-devel < 4.10.3-6
Provides: python-qt4-qsci-api = %{version}-%{release}
%description qsci-api
%{summary}.

%description qsci-api -l zh_CN.UTF-8
Qscintilla API 文档支持包。

%if 0%{?qtassistant}
%package assistant
Summary: Python bindings for QtAssistant
Summary(zh_CN.UTF-8): QtAssistant 的 Python 绑定
Provides: python-qt4-assistant = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description assistant
%{summary}.
%description assistant -l zh_CN.UTF-8
QtAssistant 的 Python 绑定。
%endif

# The bindings are imported as "PyQt4", hence it's reasonable to name the
# Python 3 subpackage "python3-PyQt4", despite the apparent tautology
%package -n python3-%{name}
Summary: Python 3 bindings for Qt4
Summary(zh_CN.UTF-8): Qt4 的 Python3 绑定
Group:   Development/Languages
Group(zh_CN.UTF-8): 开发/语言
# The dbus Python bindings have not yet been ported to Python 3:
# Requires: dbus-python
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if 0%{?fedora}
Provides: python3-%{name}-webkit = %{version}-%{release}
Provides: python3-%{name}-webkit%{?_isa} = %{version}-%{release}
%endif
Provides: python3-qt4 = %{version}-%{release}

%description -n python3-%{name}
These are Python 3 bindings for Qt4.

%description -n python3-%{name} -l zh_CN.UTF-8
Qt4 的 Python3 绑定。

%package -n python3-%{name}-assistant
Summary: Python 3 bindings for QtAssistant
Summary(zh_CN.UTF-8): QtAssistant 的 Python3 绑定
Provides: python3-qt4-assistant = %{version}-%{release}
Requires: python3-%{name}%{?_isa} = %{version}-%{release}
%description -n python3-%{name}-assistant
%{summary}.

%description -n python3-%{name}-assistant -l zh_CN.UTF-8
QtAssistant 的 Python3 绑定。

%package -n python3-%{name}-devel
Summary: Python 3 bindings for Qt4
Summary(zh_CN.UTF-8): %{name}-python3 的开发包
Group:   Development/Languages
Group(zh_CN.UTF-8): 开发/语言
%if 0%{?fedora}
Provides: python3-%{name}-webkit-devel = %{version}-%{release}
Provides: python3-%{name}-webkit-devel%{?_isa} = %{version}-%{release}
%endif
Requires: python3-%{name}%{?_isa} = %{version}-%{release}
Requires: python3-sip-devel
%description -n python3-%{name}-devel
Files needed to build other Python 3 bindings for C++ classes that inherit
from any of the Qt4 classes (e.g. KDE or your own).

%description -n python3-%{name}-devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n PyQt-x11-gpl%{?snap:-snapshot}-%{version}%{?snap:-%{snap}} 

%patch50 -p1 -b .timestamp
# skip -b on this one, so the backup copy doesnt end up packaged too
%patch52 -p1
# save orig for comparison later
cp -a ./sip/QtGui/opengl_types.sip ./sip/QtGui/opengl_types.sip.orig
%patch60 -p1 -b .arm
%if ! 0%{?webkit}
%patch300 -p1 -b .webkit
%endif

# permissions, mark examples non-executable
find examples/ -name "*.py" | xargs chmod a-x
chmod a+rx pyuic/uic/pyuic.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build

QT4DIR=%{_qt4_prefix}
PATH=%{_qt4_bindir}:$PATH ; export PATH

# Python 2 build:
%{__python2} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt4_qmake} \
  %{?qscintilla:--qsci-api --qsci-api-destdir=%{_qt4_datadir}/qsci } \
  --verbose 

make %{?_smp_mflags}

# Python 3 build:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py \
  --assume-shared \
  --confirm-license \
  --no-timestamp \
  --qmake=%{_qt4_qmake} \
  --sipdir=%{_datadir}/python3-sip/PyQt4 \
  --verbose 

make %{?_smp_mflags}
popd
%endif # with_python3


%install

# Install Python 3 first, and move aside any executables, to avoid clobbering
# the Python 2 installation:
%if 0%{?with_python3}
make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} -C %{py3dir}
%endif # with_python3

make install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}

# fix multilib conflict (symlink pointing to python_sitearch)
# by avoiding symlinks and just copy pyuic
# http://bugzilla.redhat.com/509415
# and followup
# https://bugzilla.redhat.com/1076346
cp -a  %{buildroot}%{python2_sitearch}/PyQt4/uic/pyuic.py \
       %{buildroot}%{_bindir}/pyuic4

# remove Python 3 code from Python 2.6 directory, fixes FTBFS (#564633)
rm -rfv %{buildroot}%{python2_sitearch}/PyQt4/uic/port_v3/

# likewise, remove Python 2 code from the Python 3.1 directory:
rm -rfv %{buildroot}%{python3_sitearch}/PyQt4/uic/port_v2/

# qscintilla
%if ! 0%{?qscintilla}
rm -rf %{buildroot}%{python3_sitearch}/PyQt4/uic/wiGroup(zh_CN.UTF-8):et-plugins/qscintilla* \
       %{buildroot}%{python2_sitearch}/PyQt4/uic/wiGroup(zh_CN.UTF-8):et-plugins/qscintilla*
%endif

# webkit
%if ! 0%{?webkit}
rm -rf %{buildroot}%{python3_sitearch}/PyQt4/uic/wiGroup(zh_CN.UTF-8):et-plugins/qtwebkit* \
       %{buildroot}%{python2_sitearch}/PyQt4/uic/wiGroup(zh_CN.UTF-8):et-plugins/qtwebkit*
%endif
magic_rpm_clean.sh

%check
# verify opengl_types.sip sanity
diff -u ./sip/QtGui/opengl_types.sip.orig \
        ./sip/QtGui/opengl_types.sip ||:


%clean
rm -rf %{buildroot}

%files
%doc NEWS README
%doc OPENSOURCE-NOTICE.TXT
%doc LICENSE.GPL2 GPL_EXCEPTION*.TXT
%doc LICENSE.GPL3
%{python2_dbus_dir}/qt.so
%dir %{python2_sitearch}/PyQt4/
%{python2_sitearch}/PyQt4/__init__.py*
%{python2_sitearch}/PyQt4/pyqtconfig.py*
%{python2_sitearch}/PyQt4/phonon.so
%{python2_sitearch}/PyQt4/Qt.so
%{python2_sitearch}/PyQt4/QtCore.so
%{python2_sitearch}/PyQt4/QtDBus.so
%{python2_sitearch}/PyQt4/QtDeclarative.so
%{python2_sitearch}/PyQt4/QtDesigner.so
%{python2_sitearch}/PyQt4/QtGui.so
%{python2_sitearch}/PyQt4/QtHelp.so
%{python2_sitearch}/PyQt4/QtMultimedia.so
%{python2_sitearch}/PyQt4/QtNetwork.so
%{python2_sitearch}/PyQt4/QtOpenGL.so
%{python2_sitearch}/PyQt4/QtScript.so
%{python2_sitearch}/PyQt4/QtScriptTools.so
%{python2_sitearch}/PyQt4/QtSql.so
%{python2_sitearch}/PyQt4/QtSvg.so
%{python2_sitearch}/PyQt4/QtTest.so
%if 0%{?webkit}
%{python2_sitearch}/PyQt4/QtWebKit.so
%endif
%{python2_sitearch}/PyQt4/QtXml.so
%{python2_sitearch}/PyQt4/QtXmlPatterns.so
%{python2_sitearch}/PyQt4/uic/
%{_qt4_plugindir}/designer/*

%if 0%{?qtassistant}
%files assistant
%{python2_sitearch}/PyQt4/QtAssistant.so
%endif

%files devel
%{_bindir}/pylupdate4
%{_bindir}/pyrcc4
%{_bindir}/pyuic4
%{_datadir}/sip/PyQt4/

%files doc
%doc doc/*
%doc examples/

%if 0%{?qscintilla}
%files qsci-api
# avoid dep on qscintilla-python, own %_qt4_datadir/qsci/... here for now
%dir %{_qt4_datadir}/qsci/
%dir %{_qt4_datadir}/qsci/api/
%dir %{_qt4_datadir}/qsci/api/python/
%{_qt4_datadir}/qsci/api/python/PyQt4.api
%endif

%if 0%{?with_python3}
%files -n python3-%{name}
%doc NEWS README
%doc OPENSOURCE-NOTICE.TXT
%doc LICENSE.GPL2 GPL_EXCEPTION*.TXT
%doc LICENSE.GPL3
%{python3_dbus_dir}/qt.so
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/__init__.py*
%{python3_sitearch}/PyQt4/__pycache__/
%{python3_sitearch}/PyQt4/pyqtconfig.py*
%{python3_sitearch}/PyQt4/phonon.so
%{python3_sitearch}/PyQt4/Qt.so
%{python3_sitearch}/PyQt4/QtCore.so
%{python3_sitearch}/PyQt4/QtDBus.so
%{python3_sitearch}/PyQt4/QtDeclarative.so
%{python3_sitearch}/PyQt4/QtDesigner.so
%{python3_sitearch}/PyQt4/QtGui.so
%{python3_sitearch}/PyQt4/QtHelp.so
%{python3_sitearch}/PyQt4/QtMultimedia.so
%{python3_sitearch}/PyQt4/QtNetwork.so
%{python3_sitearch}/PyQt4/QtOpenGL.so
%{python3_sitearch}/PyQt4/QtScript.so
%{python3_sitearch}/PyQt4/QtScriptTools.so
%{python3_sitearch}/PyQt4/QtSql.so
%{python3_sitearch}/PyQt4/QtSvg.so
%{python3_sitearch}/PyQt4/QtTest.so
%if 0%{?webkit}
%{python3_sitearch}/PyQt4/QtWebKit.so
%endif
%{python3_sitearch}/PyQt4/QtXml.so
%{python3_sitearch}/PyQt4/QtXmlPatterns.so
%{python3_sitearch}/PyQt4/uic/

%if 0%{?qtassistant}
%files -n python3-%{name}-assistant
%{python3_sitearch}/PyQt4/QtAssistant.so
%endif

%files -n python3-%{name}-devel
%{_datadir}/python3-sip/PyQt4/
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 4.11.4-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 4.11.4-2
- 更新到 4.11.4

* Tue Apr 14 2015 Liu Di <liudidi@gmail.com> - 4.11.3-1
- 更新到 4.11.3

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 4.9.6-2
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.6-1
- 4.9.6

* Sun Oct 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.5-3
- rebuild (sip)

* Thu Oct 11 2012 Than Ngo <than@redhat.com> - 4.9.5-2
- update webkit patch

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.5-1
- PyQt-4.9.5

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.9.4-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 4.9.4-4
- make with_python3 be conditional on fedora

* Mon Jul 30 2012 Than Ngo <than@redhat.com> - 4.9.4-3
- update webkit patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.4-1
- 4.9.4

* Sun Jun 24 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.3-1
- 4.9.3

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.2-1
- 4.9.2

* Thu Jun 21 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.1-4
- PyQt4 opengl-types.sip multilib conflict (#509415)

* Fri May 04 2012 Than Ngo <than@redhat.com> - 4.9.1-3
- add rhel/fedora condition


