
%global qt_module qtwebkit

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif

Summary: Qt5 - QtWebKit components
Name:    qt5-qtwebkit
Version: 5.2.1
Release: 3%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

# Search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: qtwebkit-opensource-src-5.2.0-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-opensource-src-5.0.1-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-opensource-src-5.2.0-save_memory.patch

# use unbundled system angleproject library
#define system_angle 1
# NEEDS REBASE for 5.1 -- rex
Patch5: qtwebkit-opensource-src-5.0.2-system_angle.patch
# Fix compilation against latest ANGLE
# https://bugs.webkit.org/show_bug.cgi?id=109127
Patch6: webkit-commit-142567.patch

# Add AArch64 support
Patch7: 0001-Add-ARM-64-support.patch

# truly madly deeply no rpath please, kthxbye
Patch8: qtwebkit-opensource-src-5.2.1-no_rpath.patch

%if 0%{?system_angle}
BuildRequires: angleproject-devel angleproject-static
%endif

# fix build with JIT disabled
# https://bugzilla.redhat.com/show_bug.cgi?id=1034940
Patch10: qtwebkit-opensource-src-5.2.0-beta1-nojit.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: qt5-qtlocation-devel
BuildRequires: qt5-qtsensors-devel

BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(gio-2.0) pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
%if 0%{?fedora} || 0%{?rhel} > 6
# gstreamer media support
BuildRequires: pkgconfig(gstreamer-1.0) pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libwebp)
%else
# gstreamer media support
BuildRequires: pkgconfig(gstreamer-0.10) pkgconfig(gstreamer-app-0.10)
BuildRequires: libicu-devel
%endif
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xcomposite) pkgconfig(xrender)
BuildRequires: perl perl(version) perl(Digest::MD5) perl(Text::ParseWords)
BuildRequires: ruby
BuildRequires: zlib-devel

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

##upstream patches


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
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


%prep
%setup -q -n qtwebkit-opensource-src-%{version}%{?pre:-%{pre}}

%patch1 -p1 -b .pluginpath
%patch3 -p1 -b .debuginfo
%patch4 -p1 -b .save_memory
%if 0%{?system_angle}
#patch5 -p1 -b .system_angle
%patch6 -p1 -b .svn142567
%endif
%patch7 -p1 -b .aarch64
%patch8 -p1 -b .no_rpath
%patch10 -p1 -b .nojit

echo "nuke bundled code..."
# nuke bundled code
mkdir Source/ThirdParty/orig
mv Source/ThirdParty/{gtest/,qunit/} \
   Source/ThirdParty/orig/

%if 0%{?system_angle}
mv Source/ThirdParty/ANGLE/ \
   Source/ThirdParty/orig/
%endif


%build
%{_qt5_qmake} %{?system_angle:DEFINES+=USE_SYSTEM_ANGLE=1} \
%ifnarch %{arm} %{ix86} x86_64
	DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0
%else
	%{nil}
%endif

make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

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
%doc Source/WebCore/LICENSE*
%doc ChangeLog* VERSION
%{_qt5_libdir}/libQt5WebKit.so.5*
%{_qt5_libdir}/libQt5WebKitWidgets.so.5*
%{_qt5_libexecdir}/QtWebPluginProcess
%{_qt5_libexecdir}/QtWebProcess
%{_qt5_archdatadir}/qml/QtWebKit/

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtwebkit.qch
%{_qt5_docdir}/qtwebkit/
%endif


%changelog
* Fri May 02 2014 Rex Dieter <rdieter@fedoraproject.org> 
- 5.2.1-3
- no rpath, drop chrpath hacks
- BR: qt5-qtlocation qt5-qtsensors

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (libicu)

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sun Feb 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- Add AArch64 support to qtwebkit (#1056160)

* Wed Jan 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- rebuild (libwebp)

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Nov 28 2013 Dan Horák <dan[at]danny.cz> 5.2.0-0.6.beta1
- disable JIT on secondary arches, fix build with JIT disabled (#1034940)

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg
- use gstreamer1 (where available)

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Tue Aug 20 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-8
- qt5-qtjsbackend only supports ix86, x86_64 and arm

* Fri Aug 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-7
- use bundled angleproject (until system version passes review)

* Fri Jun 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-6
- %%doc ChangeLog VERSION
- %%doc Source/WebCore/LICENSE*
- squash more rpaths

* Fri May 17 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-5
- unbundle angleproject code

* Wed May 15 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- BR: perl(version) perl(Digest::MD5) pkgconfig(xslt)
- deal with bundled code
- add (commented) upstream link http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
  to clarify licensing

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- -devel: Requires: qt5-qtdeclarative-devel

* Fri Apr 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- BR: qt5-qtdeclarative-devel

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- .prl love
- BR: pkgconfig(gl)

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

