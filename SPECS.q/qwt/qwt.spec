
# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

# build qt5 support (or not)
%define qt5 1

Name:    qwt
Summary: Qt Widgets for Technical Applications
Summary(zh_CN.UTF-8): 技术程序用的 Qt 部件
Version: 6.1.2
Release: 6%{?dist}

License: LGPLv2 with exceptions
URL:     http://qwt.sourceforge.net
Source:  http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

## upstream patches

## upstreamable patches
# fix pkgconfig support
Patch50: qwt-6.1.1-pkgconfig.patch
# use QT_INSTALL_ paths instead of custom prefix
Patch51: qwt-6.1.2-qt_install_paths.patch
# parallel-installable qt5 version
Patch52: qwt-qt5.patch

%if 0%{?qt5}
BuildRequires: pkgconfig(Qt5Concurrent) pkgconfig(Qt5PrintSupport) pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5OpenGL) pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Designer)
%endif
BuildRequires: pkgconfig(QtGui) pkgconfig(QtSvg)
BuildRequires: pkgconfig(QtDesigner)
# silly buildsys quirk
BuildConflicts: qwt-devel
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}


Provides: qwt6 = %{version}-%{release}
Provides: qwt6%{_isa} = %{version}-%{release}

%description
The Qwt library contains GUI Components and utility classes which are primarily
useful for programs with a technical background.
Besides a 2D plot widget it provides scales, sliders, dials, compasses,
thermometers, wheels and knobs to control or display values, arrays
or ranges of type double.

%description -l zh_CN.UTF-8
技术程序用的 Qt 部件。

%package devel
Summary:  Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Provides: qwt6-devel = %{version}-%{release}
Provides: qwt6-devel%{_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary: Developer documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
BuildArch: noarch
%description doc
%{summary}.
%description doc -l zh_CN.UTF-8
%{name} 的开发文档。

%if 0%{?qt5}
%package qt5
Summary: Qt5 Widgets for Technical Applications
Summary(zh_CN.UTF-8): 技术程序用的 Qt5 部件
Provides: qwt6-qt5 = %{version}-%{release}
Provides: qwt6-qt5%{_isa} = %{version}-%{release}
%description qt5
%{summary}.
%description qt5 -l zh_CN.UTF-8
技术程序用的 Qt5 部件。

%package qt5-devel
Summary:  Development files for %{name}-qt5
Summary(zh_CN.UTF-8): %{name}-qt5 的开发包
Provides: qwt6-qt5-devel = %{version}-%{release}
Provides: qwt6-qt5-devel%{_isa} = %{version}-%{release}
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
%description qt5-devel
%{summary}.
%description qt5-devel -l zh_CN.UTF-8
%{name}-qt5 的开发包。
%endif


%prep
%setup -q

%patch50 -p1 -b .pkgconfig
%patch51 -p1 -b .qt_install_paths
%patch52 -p1 -b .qt5


%build
%if 0%{?qt5}
mkdir %{_target_platform}-qt5
pushd %{_target_platform}-qt5
%{?qmake_qt5}%{?!qmake_qt5:%{_qt5_qmake}} QWT_CONFIG+=QwtPkgConfig ..

make %{?_smp_mflags}
popd
%endif

mkdir %{_target_platform}
pushd %{_target_platform}
%{_qt4_qmake} QWT_CONFIG+=QwtPkgConfig ..

make %{?_smp_mflags}
popd


%install
%if 0%{?qt5}
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}-qt5
%endif
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

# fixup doc path bogosity
mv %{buildroot}%{_qt4_docdir}/html/html \
   %{buildroot}%{_qt4_docdir}/html/qwt

mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_qt4_docdir}/html/man/man3 \
   %{buildroot}%{_mandir}/

%if 0%{?qt5}
# nuke qt5 docs, use copies from qt4 build instead 
rm -rfv %{buildroot}%{_qt5_docdir}/html/*

cp -alf %{buildroot}%{_qt4_docdir}/html/qwt/ \
        %{buildroot}%{_qt5_docdir}/html/qwt/
%endif
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc README
%{_qt4_libdir}/libqwt.so.6*
%{?_qt4_plugindir}/designer/libqwt_designer_plugin.so
# subpkg ? -- rex
%{_qt4_libdir}/libqwtmathml.so.6*

%files devel
%{_qt4_headerdir}/qwt/
%{_qt4_libdir}/libqwt.so
%{_qt4_libdir}/libqwtmathml.so
%{_libdir}/qt4/mkspecs/features/qwt*
%{_qt4_libdir}/pkgconfig/qwt.pc
%{_qt4_libdir}/pkgconfig/qwtmathml.pc

%files doc
# own these to avoid needless dep on qt/qt-doc
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%{_qt4_docdir}/html/qwt/
%if 0%{?qt5}
%dir %{_qt5_docdir}
%dir %{_qt5_docdir}/html/
%{_qt5_docdir}/html/qwt/
%endif
%{_mandir}/man3/*


%if 0%{?qt5}
%post qt5 -p /sbin/ldconfig
%postun qt5 -p /sbin/ldconfig

%files qt5
%doc COPYING
%doc README
%{_qt5_libdir}/libqwt-qt5.so.6*
%{_qt5_plugindir}/designer/libqwt_designer_plugin.so
%{_qt5_libdir}/libqwtmathml-qt5.so.6*

%files qt5-devel
%{_qt5_headerdir}/qwt/
%{_qt5_libdir}/libqwt-qt5.so
%{_qt5_libdir}/libqwtmathml-qt5.so
%{_qt5_libdir}/qt5/mkspecs/features/qwt*
%{_qt5_libdir}/pkgconfig/Qt5Qwt6.pc
%{_qt5_libdir}/pkgconfig/qwtmathml-qt5.pc
%endif


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 6.1.2-6
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 6.1.2-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.1.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 6.1.2-2
- rebuild (gcc5)

* Fri Dec 12 2014 Rex Dieter <rdieter@fedoraproject.org> 6.1.2-1
- qwt-6.1.2

* Mon Dec 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 6.1.1-3
- %%build: use %%qmake-qt? macro variant
- RFE: Qwt build for Qt5 (#1164515)

* Tue Oct 28 2014 Rex Dieter <rdieter@fedoraproject.org> 6.1.1-2
- do out-of-src build (prep for qt5 build maybe coming someday)

* Sat Sep 20 2014 Rex Dieter <rdieter@fedoraproject.org> 6.1.1-1
- qwt-6.1.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Rex Dieter <rdieter@fedoraproject.org> - 6.1.0-1
- qwt-6.1.0
- QtDesigner plugin doesn't link to the proper header directory path (#824447)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Rex Dieter <rdieter@fedoraproject.org> 6.0.1-2
- qwtbuild.pri: drop CONFIG+=silent

* Tue Aug 14 2012 Rex Dieter <rdieter@fedoraproject.org> - 6.0.1-1
- qwt-6.0.1 (#697168)
- add pkgconfig support

* Fri Aug 03 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-6
- qwt*.pc : +Requires: QtGui QtSvg

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-5
- pkgconfig support

* Tue Jul 31 2012 Rex Dieter <rdieter@fedoraproject.org> - 5.2.2-4
- Provides: qwt5-qt4(-devel)
- pkgconfig-style deps
 
- * Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 07 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-1
- 5.2.2

* Thu Jul 14 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- .spec cosmetics
- use %%_qt4_ macros
- -doc subpkg here (instead of separately built)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 16 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.1-1
- update to 5.2.1 

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-1
- fix wrong lib names

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-0
- update to 5.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-2
 - modify path patch

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-1
 -update to 5.1.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.2-6
- Autorebuild for GCC 4.3

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-5
 - add EPEL support

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-4
- remove parallel build, because it will fail sometimes

* Fri Sep 28 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-3
- fix some errors in the spec file

* Fri Jul 06 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-2
- fix some errors in the spec file

* Mon Jun 11 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-1
- update to 5.0.2
- split doc

* Thu May 15 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.1-1
 - start

