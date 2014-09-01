%global srcname wxWidgets
%global wxgtkname wxGTK3
%global wxbasename wxBase3
#RHEL 6 does not have gtk3
#RHEL prior to 6 is unsupported by this package
%if 0%{?el6}
%global gtkver 2
%else
%global gtkver 3
%endif

Name:           %{wxgtkname}
Version:        3.0.1
Release:        2%{?dist}
Summary:        GTK port of the wxWidgets GUI library
License:        wxWidgets
Group:          System Environment/Libraries
URL:            http://www.wxwidgets.org/
Source0:        http://downloads.sf.net/wxwindows/%{srcname}-%{version}.tar.bz2
Source1:        http://downloads.sf.net/wxwindows/%{srcname}-%{version}-docs-html.tar.bz2
Source10:       wx-config

BuildRequires:  gtk%{gtkver}-devel
#Note webkitgtk (GTK2) does not appear to be supported
%if %{gtkver} == 3
BuildRequires:  webkitgtk3-devel
%endif
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  expat-devel
BuildRequires:  SDL-devel
BuildRequires:  libgnomeprintui22-devel
BuildRequires:  libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  GConf2-devel
BuildRequires:  gettext
BuildRequires:  cppunit-devel
BuildRequires:  libmspack-devel

Provides:       %{srcname} = %{version}-%{release}
Requires:       %{wxbasename}%{?_isa} = %{version}-%{release}

%description
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        devel
Group:          Development/Libraries
Summary:        Development files for the wxGTK3 library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-gl = %{version}-%{release}
Requires:       %{name}-media = %{version}-%{release}
Requires:       %{wxbasename} = %{version}-%{release}
Requires:  	gtk%{gtkver}-devel
Requires:       libGLU-devel
Provides:       %{srcname}-devel = %{version}-%{release}

%description devel
This package include files needed to link with the wxGTK3 library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        gl
Summary:        OpenGL add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gl
OpenGL (a 3D graphics API) add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        media
Summary:        Multimedia add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description media
Multimedia add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package -n     %{wxbasename}
Summary:        Non-GUI support classes from the wxWidgets library
Group:          System Environment/Libraries

%description -n %{wxbasename}
Every wxWidgets application must link against this library. It contains
mandatory classes that any wxWidgets code depends on (like wxString) and
portability classes that abstract differences between platforms. wxBase can
be used to develop console mode applications -- it does not require any GUI
libraries or the X Window System.


%package        docs
Group:          Development/Libraries
Summary:        Documentation for the wxGTK3 library
Requires:       %{name} = %{version}-%{release}
Provides:       %{srcname}-docs = %{version}-%{release}
BuildArch:      noarch

%description docs
This package provides documentation for the %{srcname} library.


%prep
%setup -q -n %{srcname}-%{version} -a 1

# in case of gtk3
%if %{gtkver} == 3
sed -i -e 's|gtk2|gtk3|' %{SOURCE10}
%endif

# patch some installed files to avoid conflicts with 2.8.*
sed -i -e 's|aclocal)|aclocal/wxwin3.m4)|' Makefile.in
sed -i -e 's|wxstd.mo|wxstd3.mo|' Makefile.in
sed -i -e 's|wxmsw.mo|wxmsw3.mo|' Makefile.in

# rename docs directory
mv %{srcname}-%{version} html

sed -i -e 's|/usr/lib\b|%{_libdir}|' wx-config.in configure

# fix plugin dir for 64-bit
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp


%build
# likely still dereferences type-punned pointers
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
# fix unused-direct-shlib-dependency error:
export LDFLAGS="-Wl,--as-needed"

%configure \
  --with-gtk=%{gtkver} \
  --with-opengl \
  --with-sdl \
  --with-gnomeprint \
  --with-libmspack \
  --enable-intl \
  --enable-no_deps \
  --disable-rpath \
  --enable-ipv6

make %{?_smp_mflags}

%install
%makeinstall

# install our multilib-aware wrapper
rm %{buildroot}%{_bindir}/wx-config
rm %{buildroot}%{_bindir}/wxrc
install -p -m 755 %{SOURCE10} %{buildroot}%{_bindir}/wx-config-3.0

# move bakefiles to avoid conflicts with 2.8.*
mkdir %{buildroot}%{_datadir}/bakefile/presets/wx3
mv %{buildroot}%{_datadir}/bakefile/presets/*.* %{buildroot}%{_datadir}/bakefile/presets/wx3

%find_lang wxstd3
%find_lang wxmsw3
cat wxmsw3.lang >> wxstd3.lang

%check
pushd tests
make %{?_smp_mflags} test
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gl -p /sbin/ldconfig
%postun gl -p /sbin/ldconfig

%post media -p /sbin/ldconfig
%postun media -p /sbin/ldconfig

%post -n %{wxbasename} -p /sbin/ldconfig
%postun -n %{wxbasename} -p /sbin/ldconfig

%files -f wxstd3.lang
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_gtk%{gtkver}u_adv-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_aui-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_core-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_html-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_propgrid-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_qa-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_ribbon-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_richtext-*.so.*
%{_libdir}/libwx_gtk%{gtkver}u_stc-*.so.*
%if %{gtkver} == 3
%{_libdir}/libwx_gtk%{gtkver}u_webview-*.so.*
%endif
%{_libdir}/libwx_gtk%{gtkver}u_xrc-*.so.*

%files devel
%{_bindir}/wx-config*
%{_bindir}/wxrc-3.0
%{_includedir}/wx-3.0
%{_libdir}/libwx_*.so
%{_libdir}/wx
%{_datadir}/aclocal/wxwin3.m4
%{_datadir}/bakefile/presets/wx3/

%files gl
%{_libdir}/libwx_gtk%{gtkver}u_gl-*.so.*

%files media
%{_libdir}/libwx_gtk%{gtkver}u_media-*.so.*

%files -n %{wxbasename}
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.*
%{_libdir}/libwx_baseu_xml-*.so.*

%files docs
%doc html

%changelog
* Wed Aug 13 2014 Liu Di <liudidi@gmail.com> - 3.0.1-2
- 为 Magic 3.0 重建

* Sat Jul 5 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.1-1
- Bump to 3.0.1 RH#1076617

* Tue Mar 18 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-6
- Removed disable-catch_segvs, see RH#1076617

* Mon Mar 17 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-5
- Renable combat28 - without it causes bugs RH#1076617 and a few others

* Wed Feb 19 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-4
- Fixed GTK3 bug with wx-config
- Fixed a unused-direct-shlib-dependency error

* Mon Feb 17 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-3
- Added patch to avoid build fail on gtk 3.10+
- Reverted patching to make devel package compatible with wxGTK-devel
- Added combatibility for RHEL 6+
- Changed all mention of GTK3 and GTK2 to GTK for consistency

* Mon Feb 10 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-2
- Changed to build against gtk3
- Add webkit to build requires
- Removed patching to make devel package compatible with wxGTK-devel
- Disable 2.8.* combatibility (redundant functionality)

* Sat Jan 4 2014 Jeremy Newton <alexjnewt@hotmail.com> - 3.0.0-1
- Initial build of wxwidgets version 3, mostly based on wxGTK spec
