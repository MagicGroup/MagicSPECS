
%global qt_module qtquick1

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
#define docs 1

Summary: A declarative language for describing user interfaces in Qt5
Name:    qt5-%{qt_module}
Version: 5.2.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?snap:1}
Source0: http://download.qt-project.org/snapshots/qt/5.2/%{version}-%{pre}/%{snap}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtscript-devel >= %{version}
BuildRequires: qt5-qttools-devel >= %{version}
BuildRequires: qt5-qtwebkit-devel >= %{version}

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Qt Quick is a collection of technologies that are designed to help
developers create the kind of intuitive, modern, fluid user interfaces
that are increasingly used on mobile phones, media players, set-top
boxes and other portable devices.

Qt Quick consists of a rich set of user interface elements, a declarative
language for describing user interfaces and a language runtime. A
collection of C++ APIs is used to integrate these high level features
with classic Qt applications.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

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
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


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

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    qmlviewer)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl file love (maybe consider just deleting these -- rex
# nuke dangling reference(s) to %%buildroot, excessive (.la-like) libs
sed -i \
  -e "/^QMAKE_PRL_BUILD_DIR/d" \
  -e "/^QMAKE_PRL_LIBS/d" \
  %{buildroot}%{_qt5_libdir}/*.prl

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt
%{_qt5_libdir}/libQt5Declarative.so.5*
%{_qt5_bindir}/qml*
%{_bindir}/qml*
%{_qt5_importdir}/Qt/
%{_qt5_importdir}/QtWebKit/
%{_qt5_importdir}/builtins.qmltypes
%{_qt5_plugindir}/designer/*.so
%{_qt5_plugindir}/qml1tooling/

%files devel
%{_qt5_headerdir}/QtDeclarative/
%{_qt5_libdir}/libQt5Declarative.so
%{_qt5_libdir}/libQt5Declarative.prl
%{_qt5_libdir}/cmake/Qt5Declarative/
%{_qt5_libdir}/pkgconfig/Qt5Declarative.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_declarative*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.alpha
- ppc bootstrap

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- nix -doc (no content)

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Mon Sep 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- %%doc LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt
- escape macros in comments
- better %%description/%%summary

* Tue Sep 03 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- fix qmlviewer conflict with qt4

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

