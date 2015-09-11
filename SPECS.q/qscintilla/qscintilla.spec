
%global scintilla_ver 3.5.4

# bootstrapping -python
# undef python macros if you'd like to build qscintilla sans -python subpkg (which requires PyQt4)
%global python 1
%global python3 1
# experimental qt5 support
%global qt5 1

Summary: A Scintilla port to Qt
Name:    qscintilla
Version: 2.9
Release: 4%{?dist}

License: GPLv3
Url:     http://www.riverbankcomputing.com/software/qscintilla/
%if 0%{?snap:1}
Source0: http://www.riverbankcomputing.com/static/Downloads/QScintilla2/QScintilla-gpl-%{version}-snapshot-%{snap}.tar.gz
%else
Source0: http://downloads.sf.net/pyqt/QScintilla-gpl-%{version}.tar.gz
%endif

## Upstreamable patches
# fix qt5 mkspecs install path
Patch1: QScintilla-gpl-2.9-qt5_mkspecs.patch
# make qt5 build parallel-installable
Patch2: QScintilla-gpl-2.9-qt5.patch

BuildRequires: pkgconfig(QtDesigner) pkgconfig(QtGui) pkgconfig(QtScript) pkgconfig(QtXml)
%if 0%{?qt5}
BuildRequires: pkgconfig(Qt5Designer) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets)
%endif

Provides: bundled(scintilla) = %{scintilla_ver}

%description
QScintilla is a port of Scintilla to the Qt GUI toolkit.

%{?scintilla_ver:This version of QScintilla is based on Scintilla v%{scintilla_ver}.}

%package devel
Summary:  QScintilla Development Files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel 
%description devel
%{summary}.

%if 0%{?python}
%package python
Summary:  QScintilla python bindings
BuildRequires: PyQt4-devel
BuildRequires: sip-devel >= 3.16
Provides: python-qscintilla = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: PyQt4
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description python
%{summary}.

%package python-devel
Summary:  Development files for QScintilla python bindings
Provides: python-qscintilla-devel = %{version}-%{release}
Requires: PyQt4-devel
BuildArch: noarch
%description python-devel
%{summary}.
%endif

%if 0%{?python3}
%package -n python3-qscintilla
Summary:  QScintilla python3 bindings
BuildRequires: python3-PyQt4-devel
BuildRequires: sip-devel >= 3.16
Provides: %{name}-python3 = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-PyQt4
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description -n python3-qscintilla
%{summary}.

%package -n python3-qscintilla-devel
Summary:  Development files for QScintilla python3 bindings
Provides: %{name}-python3-devel = %{version}-%{release}
Requires: python3-PyQt4-devel
BuildArch: noarch
%description -n python3-qscintilla-devel
%{summary}.
%endif

%if 0%{?qt5}
%package qt5
Summary: A Scintilla port to Qt5
%description qt5
%{summary}.

%package qt5-devel
Summary:  QScintilla Development Files
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
%description qt5-devel
%{summary}.

%if 0%{?python3}
%package -n python3-qscintilla-qt5
Summary:  QScintilla-qt5 python3 bindings
BuildRequires: python3-qt5
BuildRequires: python-qt5-devel
BuildRequires: sip-devel >= 3.16
Provides: %{name}-qt5-python3 = %{version}-%{release}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: python3-qt5
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description -n python3-qscintilla-qt5
%{summary}.

%package -n python3-qscintilla-qt5-devel
Summary:  Development files for QScintilla-qt5 python3 bindings
Provides: %{name}-qt5-python3-devel = %{version}-%{release}
Requires: python-qt5-devel
BuildArch: noarch
%description -n python3-qscintilla-qt5-devel
%{summary}.

%endif
%endif


%prep
%setup -q -n QScintilla-gpl-%{version}%{?snap:-snapshot-%{snap}}

%patch1 -p1 -b .qt5_mkspecs
%patch2 -p1 -b .qt5


%build
PATH=%{_qt4_bindir}:$PATH; export PATH

cp -a Qt4Qt5 Qt4/
pushd Qt4
%{_qt4_qmake} qscintilla.pro
make %{?_smp_mflags}
popd

# set QMAKEFEATURES to ensure just built lib/feature is found
QMAKEFEATURES=`pwd`/Qt4/features; export QMAKEFEATURES

cp -a designer-Qt4Qt5 designer-Qt4/
pushd designer-Qt4
%{_qt4_qmake} designer.pro INCLUDEPATH+=../Qt4 LIBS+=-L../Qt4
make %{?_smp_mflags}
popd

%if 0%{?python}
cp -a Python Python2-qt4
pushd Python2-qt4
%{__python2} \
  configure.py \
    --no-timestamp \
    --qsci-incdir=../Qt4 --qsci-libdir=../Qt4

make %{?_smp_mflags}
popd
%endif

%if 0%{?python3}
cp -a Python Python3-qt4
pushd Python3-qt4
%{__python3} \
  configure.py \
    --no-timestamp \
    --pyqt-sipdir=/usr/share/python3-sip/PyQt4 \
    --qsci-incdir=../Qt4 --qsci-libdir=../Qt4 \
    --sip=/usr/bin/python3-sip

make %{?_smp_mflags}
popd
%endif

%if 0%{?qt5}
PATH=%{_qt5_bindir}:$PATH; export PATH

cp -a Qt4Qt5 Qt5/
pushd Qt5
%{qmake_qt5} qscintilla.pro
make %{?_smp_mflags}
popd

# set QMAKEFEATURES to ensure just built lib/feature is found
QMAKEFEATURES=`pwd`/Qt5/features; export QMAKEFEATURES

cp -a designer-Qt4Qt5 designer-Qt5/
pushd designer-Qt5
%{qmake_qt5} designer.pro INCLUDEPATH+=../Qt5 LIBS+=-L../Qt5
make %{?_smp_mflags}
popd

%if 0%{?python3}
cp -a Python Python3-qt5
pushd Python3-qt5
%{__python3} \
  configure.py \
    --no-timestamp \
    --pyqt=PyQt5 --qsci-incdir=../Qt5 --qsci-libdir=../Qt5

make %{?_smp_mflags}
popd
%endif

%endif


%install
make -C Qt4 install INSTALL_ROOT=%{buildroot}
make -C designer-Qt4 install INSTALL_ROOT=%{buildroot}
%if 0%{?python}
make -C Python2-qt4 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so || \
chmod a+x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%endif
%if 0%{?python3}
make -C Python3-qt4 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so || \
chmod a+x %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so
%endif

%if 0%{?qt5}
make -C Qt5 install INSTALL_ROOT=%{buildroot}
make -C designer-Qt5 install INSTALL_ROOT=%{buildroot}
%if 0%{?python3}
make -C Python3-qt5 install DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot}
test -x   %{buildroot}%{python3_sitearch}/PyQt5/Qsci.so || \
chmod a+x %{buildroot}%{python3_sitearch}/PyQt5/Qsci.so
%endif
%endif

%find_lang qscintilla --with-qt
grep "%{_qt4_translationdir}" qscintilla.lang > qscintilla-qt4.lang
grep "%{_qt5_translationdir}" qscintilla.lang > qscintilla-qt5.lang

%if !0%{?python} && !0%{?python3}
# unpackaged files
rm -rfv %{buildroot}%{_qt4_datadir}/qsci/
%endif


%check
# verify python module(s) permissions and libqscintilla2 linkage
# https://bugzilla.redhat.com/show_bug.cgi?id=1104559
ldd     %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so | grep libqscintilla2 || exit 1
test -x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%if 0%{?python3}
ldd     %{buildroot}%{python3_sitearch}/PyQt4/Qsci.so | grep libqscintilla2 || exit 1
test -x %{buildroot}%{python2_sitearch}/PyQt4/Qsci.so
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f qscintilla-qt4.lang
%doc NEWS README
%license LICENSE
%{_qt4_libdir}/libqscintilla2.so.12*
%{_qt4_plugindir}/designer/libqscintillaplugin.so

%files devel
%doc doc/html-Qt4Qt5 doc/Scintilla example-Qt4Qt5
%{_qt4_headerdir}/Qsci/
%{_qt4_libdir}/libqscintilla2.so
%{_qt4_datadir}/mkspecs/features/qscintilla2.prf

%if 0%{?python}
%files python
%{python2_sitearch}/PyQt4/Qsci.so
%{_qt4_datadir}/qsci/

%files python-devel
%{_datadir}/sip/PyQt4/Qsci/
%endif

%if 0%{?python3}
%files -n python3-qscintilla
%{python3_sitearch}/PyQt4/Qsci.so
%{_qt4_datadir}/qsci/

%files -n python3-qscintilla-devel
%{_datadir}/python3-sip/PyQt4/Qsci/
%endif

%if 0%{?qt5}
%files qt5 -f qscintilla-qt5.lang
%doc NEWS README
%license LICENSE
%{_qt5_libdir}/libqscintilla2-qt5.so.12*
%{_qt5_plugindir}/designer/libqscintillaplugin.so

%files qt5-devel
%doc doc/html-Qt4Qt5 doc/Scintilla example-Qt4Qt5
%{_qt5_headerdir}/Qsci/
%{_qt5_libdir}/libqscintilla2-qt5.so
%{_qt5_archdatadir}/mkspecs/features/qscintilla2.prf

%if 0%{?python3}
%files -n python3-qscintilla-qt5
%{python3_sitearch}/PyQt5/Qsci.so
%{_qt5_datadir}/qsci/

%files -n python3-qscintilla-qt5-devel
%{_datadir}/sip/PyQt5/Qsci/
%endif
%endif


%changelog
* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-4
- fix libqscintillaplugin.so linkage (#1231721)

* Sun Apr 26 2015 Rex Dieter <rdieter@fedoraproject.org> - 2.9-3
- use %%qmake_qt4 macroo
- Qt5 qscintilla2.prf is installed in bad location (#1215380)

* Thu Apr 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-2
- Provides: bundled(scintilla) = 3.5.4

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-1
- 2.9

* Wed Feb 18 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.4-3
- Rebuild for gcc 5 C++11

* Sun Dec 28 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.4-2
- enable -qt5 support

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.4-1
- QScintiall-2.8.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.3-1
- QScintiall-2.8.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-0.3.9b7b5393f228
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-0.2.9b7b5393f228
- QScintilla-gpl-2.8.3-snapshot-9b7b5393f228
- python: explicitly set QMAKEFEATURES (bug #1104559)

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.3-0.1.f7b1c9821894
- QScintiall-2.8.3-f7b1c9821894 snapshot (2.8.2 FTBFS)

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 17 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.1-3
- enable python3 bindings (#1065223)

* Mon Mar 17 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.1-2
- designer plugin: Undefined reference to QsciScintilla::QsciScintilla... (#1077146)

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 2.8.1-1
- QScintilla-2.8.1
- Provides: python-qscintilla
- experimental qt5/python3 support (not enabled yet)

* Fri Nov 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2.8-1
- QScintilla-2.8

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.2-3
- rebuild (PyQt4), refresh incpath patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.7.2-1
- QScintilla-2.7.2
- prune changelog

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.1-2
- rebuild (sip)

* Sun Mar 03 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.1-1
- 2.7.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Rex Dieter <rdieter@fedoraproject.org> 2.7-1
- 2.7

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-3
- rebuild (sip)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-1
- 2.6.2

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.1-1
- 2.6.1
- pkgconfig-style deps

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-2
- rebuild (sip/PyQt4)

* Sat Dec 03 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-1
- 2.6

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-2
- rebuild (sip)

* Fri May 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-1
- 2.5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.6-1
- 2.4.6

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.5-1
- 2.4.5

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.4-1
- 2.4.4

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.3-1
- 2.4.3

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.2-1
- 2.4.2

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.1-1
- 2.4.1 
- pyqt4_version 4.7

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4-10 
- rebuild (sip)

* Fri Nov 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-9
- -python: Requires: sip-api(%%_sip_api_major) >= %%_sip_api
- -python-devel: Requires: sip-devel

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-8 
- rebuild (for qt-4.6.0-rc1, f13+)

* Wed Nov 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-7
- pyqt4_version 4.6.1

* Wed Oct 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-6
- autocomplete_popup patch

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-5
- rebuild (PyQt4)

* Tue Aug 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-4
- -python-devel: make noarch, drop dep on -python

* Sat Aug 08 2009 Rex Dieter <rdieter@fedoraproject.org - 2.4-3
- include designer plugin in main pkg, Obsoletes: qscintilla-designer

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-1
- QScintilla-gpl-2.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3.2-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.2-1
- Qscintilla-gpl-2.3.2
- soname bump 4->5

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- Qscintilla-gpl-2.3.1

* Mon Sep 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3-1
- Qscintilla-gpl-2.3
- scintilla_ver is missing (#461777)

* Fri Jul 18 2008 Dennis Gilmore <dennis@ausil.us> - 2.2-3
- rebuild for newer PyQT4
- fix #449423 properly

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-2
- fix build (#449423)

* Mon May 05 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-1
- Qscintilla-gpl-2.2
- License: GPLv3 or GPLv2 with exceptions

* Thu Feb 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.1-4
- use %%_qt4_* macros (preparing for qt4 possibly moving %%_qt4_datadir)
- -python: fix Requires
- -python-devel: new pkg
- omit Obsoletes: PyQt-qscintilla 
  (leave that to PyQt, that can get the versioning right)

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-3
- fix typo in Obsoletes: on python package

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-2
- remove dumb require on di from qscintilla-python

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-1
- update to 2.1 branch
