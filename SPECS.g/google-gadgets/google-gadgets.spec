#
# spec file for package google-gadgets (Version 0.10.1)
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

Name:           google-gadgets
Version:        0.11.2
Release:        7%{?dist}
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Group(zh_CN.UTF-8): 	应用程序/系统
Summary:        Google Gadgets for Linux
Summary(zh_CN.UTF-8): Linux 下的 Google Gadgets
Url:            http://code.google.com/p/google-gadgets-for-linux/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        http://google-gadgets-for-linux.googlecode.com/files/google-gadgets-for-linux-%{version}.tar.bz2
Patch1:		01_am_maintainer_mode.patch
Patch2:		02_kfreebsd.patch
Patch3:		03_GRE_Version.patch
Patch4:		04_hurd.patch
Patch5:		05_hurd_pthread.patch
Patch6:		fix_desktop.patch
Patch7:		nm09.patch
Patch8:		nm-mobile-devtypes.patch
Patch9:		glib_includes.diff
Patch10:	gcc-4.7.diff

BuildRequires:  gcc-c++ zip autoconf flex libtool
BuildRequires:  gtk2-devel >= 2.10.0
BuildRequires:  cairo-devel >= 1.2.0
BuildRequires:  libxml2-devel >= 2.6.0
BuildRequires:  zlib-devel >= 1.2.0
BuildRequires:  librsvg2-devel >= 2.18.0
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.6
BuildRequires:  gstreamer-devel >= 0.10.6
#BuildRequires:  dbus-devel >= 1.0.2
BuildRequires:  libtool-ltdl-devel
BuildRequires:  startup-notification-devel

BuildRequires:  xulrunner-devel >= 1.9

BuildRequires:  firefox >= 2.0
BuildRequires:  qt4-devel >= 4.3
BuildRequires:  curl-devel >= 7.16.0


# 修正 gcc3 编译支持, patch1 written by nihui, Oct.12th, 2008
#Patch1: google-gadgets-for-linux-0.10.2.fix_gcc3_build.patch


%description
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>

%description -l zh_CN.UTF-8
跨平台桌面工具集的 Linux 版本。

%package -n libggadget-1_0-0
License:        Apache License Version 2.0
Group:          System/Libraries
Group(zh_CN.UTF-8): 	系统环境/库
Summary:        Google Gadgets main libraries
Summary(zh_CN.UTF-8): Google Gadgets 的主要库


Requires:       libtool-ltdl
#Requires:       dbus >= 1.0.2

%description -n libggadget-1_0-0
This package contains the main Google Gadgets libraries, it is required by both
the GTK+ and QT versions of Google Gadgets.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package -n libggadget-devel
License:        Apache License Version 2.0
Group:          Development/Libraries/C and C++
Summary:        Google Gadgets main development files
Requires:       libggadget-1_0-0 = %{version}

#Requires:       dbus-devel >= 1.0.2

%description -n libggadget-devel
This package contains the development files assoicated with libggadget, it is
needed to write programs that utilise libggadget.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package -n libggadget-gtk-1_0-0
License:        Apache License Version 2.0
Group:          System/Libraries
Summary:        Google Gadgets GTK+ library
Requires:       libggadget-1_0-0 = %{version}

Requires:       gtk2 >= 2.10.0
Requires:       cairo >= 1.2.0
Requires:       librsvg2 >= 2.18.0

%description -n libggadget-gtk-1_0-0
This package contains the GTK+ Google Gadgets library, it is required to run
the GTK+ version of Google Gadgets.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package -n libggadget-gtk-devel
License:        Apache License Version 2.0
Group:          Development/Libraries/C and C++
Summary:        Google Gadgets GTK+ development files
Requires:       libggadget-devel = %{version}
Requires:       libggadget-gtk-1_0-0 = %{version}

Requires:       gtk2-devel >= 2.10.0
Requires:       cairo-devel >= 1.2.0
Requires:       librsvg2-devel >= 2.18.0

%description -n libggadget-gtk-devel
This package contains the development files assoicated with libggadget-gtk,
it is needed to write GTK+ programs that utilise libggadget.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package -n libggadget-qt-1_0-0
License:        Apache License Version 2.0
Group:          System/Libraries
Summary:        Google Gadgets QT library
Requires:       libggadget-1_0-0 = %{version}

Requires:       qt4 >= 4.3

%description -n libggadget-qt-1_0-0
This package contains the QT Google Gadgets library, it is required to run
the QT version of Google Gadgets.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package -n libggadget-qt-devel
License:        Apache License Version 2.0
Group:          Development/Libraries/C and C++
Summary:        Google Gadgets QT development files
Requires:       libggadget-devel = %{version}
Requires:       libggadget-qt-1_0-0 = %{version}

Requires:       qt4-devel >= 4.3

%description -n libggadget-qt-devel
This package contains the development files assoicated with libggadget-qt,
it is needed to write QT programs that utilise libggadget.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>

%package common
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Summary:        Common files for QT and GTK+ versions of google-gadgets
Requires:       libggadget-1_0-0 = %{version}

Requires:       curl >= 7.16.0
Requires:       libxml2 >= 2.6.0

%description common
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

This package includes files common to both GTK+ and QT versions.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package gtk
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Summary:        GTK+ Version of Google Gadgets
Requires:       libggadget-gtk-1_0-0 = %{version}
Requires:       google-gadgets-common = %{version}
Requires:       google-gadgets-gst = %{version}

%description gtk
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

This package includes the GTK+ version.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package qt
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Summary:        QT Version of Google Gadgets
Requires:       libggadget-qt-1_0-0 = %{version}
Requires:       google-gadgets-common = %{version}
Requires:       google-gadgets-gst = %{version}

%description qt
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

This package includes the QT version.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package gst
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Summary:        GStreamer modules for Google Gadgets
Requires:       libggadget-1_0-0 = %{version}

Requires:       gstreamer-plugins-base >= 0.10.6

%description gst
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

This package includes the GStreamer modules.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>


%package webkit
License:        Apache License Version 2.0
Group:          Productivity/Networking/Web/Utilities
Summary:        XULRunner modules for Google Gadgets
Requires:       libggadget-1_0-0 = %{version}

Requires:       xulrunner >= 1.9
Requires:       firefox >= 2.0

%description webkit
Google Gadgets for Linux provides a platform for running desktop gadgets under
Linux, catering to the unique needs of Linux users. It's compatible with the
gadgets written for Google Desktop for Windows as well as the Universal
Gadgets on iGoogle. Following Linux norms, this project is open-sourced
under the Apache License.

This package includes the XULRunner modules.

Authors:
--------
    Google Gadgets for Linux team<google-gadgets-for-linux-dev@googlegroups.com>

%package webkit-devel
Summary: webkit-devel

Requires: %{name}-webkit = %{version}

%description webkit-devel
webkit-devel

%prep
%setup -q -n google-gadgets-for-linux-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1


%build
# FIXME workaround --- nihui
# http://code.google.com/p/google-gadgets-for-linux/issues/detail?id=352
autoreconf -fisv
CXXFLAGS="${CXXFLAGS:-%optflags -Wno-invalid-offsetof }" ; export CXXFLAGS ;
#autoreconf
%configure \
  --with-browser-plugins-dir=%{_libdir}/flash-plugin \
  --disable-werror --enable-ltdl-install=no --disable-gtkmoz-browser-element --disable-smjs-script-runtime
for i in `find . -name Makefile`;do sed -i 's/\-fstack-protector/\-fstack-protector\ \-fno-strict-aliasing/g' $i;done
make %{?_smp_mflags} 

%install
rm -fr $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install-strip
# These are dynamic modules... we shouldn't be installing them
rm -f $RPM_BUILD_ROOT/%{_libdir}/google-gadgets/modules/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/google-gadgets/modules/*.a
# Remove all static libraries.
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a


%post -n google-gadgets-common
if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
if [ -x /usr/bin/xdg-icon-resource ]; then
  /usr/bin/xdg-icon-resource forceupdate --theme hicolor &> /dev/null || :
fi

%postun -n google-gadgets-common
if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
if [ -x /usr/bin/xdg-icon-resource ]; then
  /usr/bin/xdg-icon-resource forceupdate --theme hicolor &> /dev/null || :
fi

%post -n libggadget-1_0-0 -p /sbin/ldconfig
%postun -n libggadget-1_0-0 -p /sbin/ldconfig

%post -n libggadget-gtk-1_0-0 -p /sbin/ldconfig
%postun -n libggadget-gtk-1_0-0 -p /sbin/ldconfig

%post -n libggadget-qt-1_0-0 -p /sbin/ldconfig
%postun -n libggadget-qt-1_0-0 -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n google-gadgets-common
%defattr(-, root, root)
%doc COPYING AUTHORS README NEWS
%dir %{_libdir}/google-gadgets/
%dir %{_libdir}/google-gadgets/modules/
%{_libdir}/google-gadgets/modules/analytics*.so
%{_libdir}/google-gadgets/modules/default*.so
%{_libdir}/google-gadgets/modules/linux*.so
%{_libdir}/google-gadgets/modules/google-gadget-manager.so
%{_libdir}/google-gadgets/modules/libxml2*.so
%{_libdir}/google-gadgets/modules/curl*.so
%{_libdir}/google-gadgets/modules/dbus*.so
%{_libdir}/google-gadgets/modules/html*.so
%dir %{_datadir}/google-gadgets/
%{_datadir}/google-gadgets/*.gg
%{_datadir}/mime/packages/*.xml
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png

%files -n libggadget-1_0-0
%defattr(-, root, root)
%{_libdir}/libggadget-1.0*.so.*
%{_libdir}/libggadget-dbus-1.0*.so.*
%{_libdir}/libggadget-js-1.0*.so.*
%{_libdir}/libggadget-xdg-1.0*.so.*
%{_libdir}/libggadget-npapi-1.0*.so.*

%files -n libggadget-devel
%defattr(-, root, root)
%dir %{_includedir}/google-gadgets/
%dir %{_includedir}/google-gadgets/ggadget
%dir %{_includedir}/google-gadgets/ggadget/dbus
%dir %{_includedir}/google-gadgets/ggadget/js
%dir %{_includedir}/google-gadgets/ggadget/xdg
%dir %{_includedir}/google-gadgets/ggadget/npapi
%{_includedir}/google-gadgets/ggadget/*.h
%{_includedir}/google-gadgets/ggadget/dbus/*.h
%{_includedir}/google-gadgets/ggadget/js/*.h
%{_includedir}/google-gadgets/ggadget/xdg/*.h
%{_includedir}/google-gadgets/ggadget/npapi/*.h
%dir %{_libdir}/google-gadgets/include/
%dir %{_libdir}/google-gadgets/include/ggadget/
%{_libdir}/google-gadgets/include/ggadget/sysdeps.h
%{_libdir}/libggadget-1.0*.so
%{_libdir}/libggadget-dbus-1.0*.so
%{_libdir}/libggadget-js-1.0*.so
%{_libdir}/libggadget-xdg-1.0*.so
%{_libdir}/libggadget-npapi-1.0*.so
%{_libdir}/libggadget-1.0*.la
%{_libdir}/libggadget-dbus-1.0*.la
%{_libdir}/libggadget-js-1.0*.la
%{_libdir}/libggadget-xdg-1.0*.la
%{_libdir}/libggadget-npapi-1.0*.la
%{_libdir}/pkgconfig/libggadget-1.0.pc
%{_libdir}/pkgconfig/libggadget-dbus-1.0.pc
%{_libdir}/pkgconfig/libggadget-js-1.0.pc
%{_libdir}/pkgconfig/libggadget-xdg-1.0.pc
%{_libdir}/pkgconfig/libggadget-npapi-1.0.pc

%files -n libggadget-gtk-1_0-0
%defattr(-, root, root)
%{_libdir}/libggadget-gtk-1.0*.so.*

%files -n libggadget-gtk-devel
%defattr(-, root, root)
%dir %{_includedir}/google-gadgets/ggadget/gtk/
%{_includedir}/google-gadgets/ggadget/gtk/*.h
%{_libdir}/libggadget-gtk-1.0*.so
%{_libdir}/libggadget-gtk-1.0*.la
%{_libdir}/pkgconfig/libggadget-gtk-1.0.pc

%files -n libggadget-qt-1_0-0
%defattr(-, root, root)
%{_libdir}/libggadget-qt-1.0*.so.*

%files -n libggadget-qt-devel
%defattr(-, root, root)
%dir %{_includedir}/google-gadgets/ggadget/qt/
%{_includedir}/google-gadgets/ggadget/qt/*.h
%{_libdir}/libggadget-qt-1.0*.so
%{_libdir}/libggadget-qt-1.0*.la
%{_libdir}/pkgconfig/libggadget-qt-1.0.pc

%files -n google-gadgets-gtk
%defattr(-, root, root)
#%{_bindir}/ggl-gtk
#%{_datadir}/applications/ggl-gtk.desktop
#%{_datadir}/applications/ggl-designer.desktop
%{_libdir}/google-gadgets/modules/gtk-*.so

%files -n google-gadgets-qt
%defattr(-, root, root)
%{_bindir}/ggl-qt
%{_datadir}/applications/ggl-qt.desktop
%{_libdir}/google-gadgets/modules/qt*.so

%files -n google-gadgets-gst
%defattr(-, root, root)
%{_libdir}/google-gadgets/modules/gst*.so

%files -n google-gadgets-webkit
%defattr(-, root, root)
#%{_libdir}/google-gadgets/modules/gtkwebkit-browser-element.so
%{_libdir}/google-gadgets/modules/soup-xml-http-request.so
#%{_libdir}/google-gadgets/modules/webkit-script-runtime.so
#%{_libdir}/libggadget-webkitjs-1.0.so.*

%if 0
%files -n google-gadgets-webkit-devel
%{_libdir}/libggadget-webkitjs-1.0.so
%{_libdir}/libggadget-webkitjs-1.0.la
%endif

%changelog
* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 0.11.2-7
- 为 Magic 3.0 重建

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 0.11.2-6
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.11.2-5
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.11.2-4
- 为 Magic 3.0 重建

* Tue Nov 27 2012 Liu Di <liudidi@gmail.com> - 0.11.2-2
- 为 Magic 3.0 重建

* Tue Jan 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 0.10.5-0.1mgc
- 更新至 0.10.5
- 戊子  十二月十八

* Sat Dec 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.10.4-0.1mgc
- 更新至 0.10.4
- 纳入 flash 插件支持
- 戊子  十一月廿三

* Sun Oct 12 2008 Ni Hui <shuizhuyuanluo@126.com> -0.10.2-0.1mgc
- rebuild
- 修正 gcc3 编译支持(patch1 written by nihui, Oct.12th, 2008)
- 戊子  九月十四

* Sun Sep 14 2008 Jack Coulter <jscinoz@gmail.com>
- version 0.10.2-1
- Upgraded to 0.10.2
- Merged libggadget-xdg into libggadget (and respective -dev packages)
* Sat Jun 14 2008 Jack Coulter <jscinoz@gmail.com>
- version 0.10.1-1
- Initial release
