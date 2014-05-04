
%global qt_module qttools
%global system_clucene 1

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif

Summary: Qt5 - QtTool components
Name:    qt5-qttools
Version: 5.2.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

Patch1: qttools-system_clucene.patch

# help lrelease/lupdate use/prefer qmake-qt5
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch2: qttools-opensource-src-5.2.0-qmake-qt5.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

# %%check needs cmake (and don't want to mess with cmake28)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: cmake
%endif
BuildRequires: desktop-file-utils
BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-static
BuildRequires: qt5-qtdeclarative-static
BuildRequires: qt5-qtwebkit-devel

%if 0%{?system_clucene}
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: clucene09-core-devel
%else
BuildConflicts: clucene-core-devel > 2
BuildRequires: clucene-core-devel
%endif
%endif

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Provides: qt5-designer = %{version}-%{release}
Provides: qt5-linguist = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package -n qt5-assistant
Summary: Documentation browser for Qt5
Requires: %{name}%{?_isa} = %{version}-%{release}
%description -n qt5-assistant
%{summary}.

%package -n qt5-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
Requires: %{name}%{?_isa} = %{version}-%{release}
%description -n qt5-designer-plugin-webkit
%{summary}.

%package -n qt5-qdbusviewer
Summary: D-Bus debugger and viewer
%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%description -n qt5-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n qttools-opensource-src-%{version}%{?pre:-%{pre}}

%if 0%{?system_clucene}
%patch1 -p1 -b .system_clucene
# bundled libs
#mv src/assistant/3rdparty/clucene \
#   src/assistant/3rdparty/clucene.BAK
%endif
%patch2 -p1 -b .qmake-qt5


%build
%{_qt5_qmake}

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

# Add desktop files, --vendor=qt4 helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt5" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/designer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist.png
done

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

## work-in-progress... -- rex
%if 0%{?fedora} || 0%{?rhel} > 6
%check
export CMAKE_PREFIX_PATH=%{buildroot}%{_qt5_prefix}:%{buildroot}%{_prefix}
export PATH=%{buildroot}%{_qt5_bindir}:%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake ..
ctest --output-on-failure ||:
popd
%endif


%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files
%{_bindir}/qdbus-qt5
%{_bindir}/qtpaths
%{_qt5_bindir}/qdbus*
%{_qt5_bindir}/qtpaths
%{_qt5_libdir}/libQt5CLucene.so.5*
%{_qt5_libdir}/libQt5Designer.so.5*
%{_qt5_libdir}/libQt5DesignerComponents.so.5*
%{_qt5_libdir}/libQt5Help.so.5*
%{_qt5_datadir}/phrasebooks/

%post -n qt5-assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-assistant
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-assistant
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5-assistant
%{_bindir}/assistant-qt5
%{_qt5_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt5-designer-plugin-webkit
%{_qt5_plugindir}/designer/libqwebview.so

%post -n qt5-qdbusviewer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-qdbusviewer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files -n qt5-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt5_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%post devel
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans devel
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun devel
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi

%files devel
%{_bindir}/designer*
%{_bindir}/lconvert*
%{_bindir}/linguist*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/pixeltool*
%{_bindir}/qcollectiongenerator*
%{_bindir}/qhelpconverter*
%{_bindir}/qhelpgenerator*
%{_qt5_bindir}/designer*
%{_qt5_bindir}/lconvert*
%{_qt5_bindir}/linguist*
%{_qt5_bindir}/lrelease*
%{_qt5_bindir}/lupdate*
%{_qt5_bindir}/pixeltool*
%{_qt5_bindir}/qcollectiongenerator*
%{_qt5_bindir}/qhelpconverter*
%{_qt5_bindir}/qhelpgenerator*
%{_qt5_headerdir}/QtCLucene/
%{_qt5_headerdir}/QtDesigner/
%{_qt5_headerdir}/QtDesignerComponents/
%{_qt5_headerdir}/QtHelp/
%{_qt5_libdir}/libQt5CLucene.prl
%{_qt5_libdir}/libQt5CLucene.so
%{_qt5_libdir}/libQt5Designer*.prl
%{_qt5_libdir}/libQt5Designer*.so
%{_qt5_libdir}/libQt5Help.prl
%{_qt5_libdir}/libQt5Help.so
%{_qt5_libdir}/cmake/Qt5Designer/
%{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/pkgconfig/Qt5CLucene.pc
%{_qt5_libdir}/pkgconfig/Qt5Designer.pc
%{_qt5_libdir}/pkgconfig/Qt5DesignerComponents.pc
%{_qt5_libdir}/pkgconfig/Qt5Help.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_datadir}/applications/*designer.desktop
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%{_datadir}/icons/hicolor/*/apps/linguist*.*
# example designer plugins
%{_qt5_plugindir}/designer/libcontainerextension.so
%{_qt5_plugindir}/designer/libcustomwidgetplugin.so
%{_qt5_plugindir}/designer/libtaskmenuextension.so
%{_qt5_plugindir}/designer/libworldtimeclockplugin.so

%files static
%{_qt5_headerdir}/QtUiTools/
%{_qt5_libdir}/libQt5UiTools.*a
%{_qt5_libdir}/libQt5UiTools.prl
%{_qt5_libdir}/cmake/Qt5UiTools/
%{_qt5_libdir}/pkgconfig/Qt5UiTools.pc

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtassistant.qch
%{_qt5_docdir}/qtassistant/
%{_qt5_docdir}/qtdesigner.qch
%{_qt5_docdir}/qtdesigner/
%{_qt5_docdir}/qthelp.qch
%{_qt5_docdir}/qthelp/
%{_qt5_docdir}/qtlinguist.qch
%{_qt5_docdir}/qtlinguist/
%{_qt5_docdir}/qtuitools.qch
%{_qt5_docdir}/qtuitools/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- -examples subpkg

* Tue Jan 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- epel7 bootstrapped

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-6
- lupdate can't find qmake configuration file default (#1009893)

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- use upstream cmake fix(es) (QTBUG-32570, #1006254)

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- wrong path to lrelease (#1006254)
- %%check: first try

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: %{ix86} x86_64 %{arm}
- epel-6 love

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- qttools-5.1.1
- qt5-assistant, qt5-qdbusviewer, qt5-designer-plugin-webkit subpkgs (to match qt4)

* Mon Aug 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- use system clucene09-core

* Mon Apr 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- drop deprecated Encoding= key from .desktop files
- add justification for desktop vendor usage

* Fri Apr 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- add .desktop/icons for assistant, designer, linguist, qdbusviewer

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- BR: pkgconfig(zlib)
- -static subpkg

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

