Name:           v4l-utils
Version:	1.8.1
Release:	3%{?dist}
Summary:        Utilities for video4linux and DVB devices
Summary(zh_CN.UTF-8): video4linux 和 DVB 设备的工具
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
# ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
BuildRequires:  libjpeg-devel qt4-devel kernel-headers desktop-file-utils
# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.

%description -l zh_CN.UTF-8
video4linux 和 DVB 设备的工具。

%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
Summary(zh_CN.UTF-8): %{name} 的开发工具
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.
%description devel-tools -l zh_CN.UTF-8
%{name} 的开发工具。

%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
Summary(zh_CN.UTF-8): QT v4l2 测试控制和流测试程序
License:        GPLv2+
Requires:       libv4l = %{version}-%{release}

%description -n qv4l2
QT v4l2 test control and streaming test application.

%description -n qv4l2 -l zh_CN.UTF-8
QT v4l2 测试控制和流测试程序。

%package -n     libv4l
Summary:        Collection of video4linux support libraries 
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.

%description -n libv4l -l zh_CN.UTF-8
%{name} 的运行库。

%package -n     libv4l-devel
Summary:        Development files for libv4l
Summary(zh_CN.UTF-8): libv4l 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.

%description -n libv4l-devel -l zh_CN.UTF-8
libv4l 的开发包。

%package -n     libdvbv5
Summary:        Libraries to control, scan and zap on Digital TV channels
Summary(zh_CN.UTF-8): libdvbv5 的运行库
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv2

%description -n libdvbv5
Libraries to control, scan and zap on Digital TV channels

%description -n libdvbv5 -l zh_CN.UTF-8
libdvbv5 的运行库。

%package -n     libdvbv5-devel
Summary:        Development files for libdvbv5
Summary(zh_CN.UTF-8): libdvbv5 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv2
Requires:       libdvbv5%{?_isa} = %{version}-%{release}

%description -n libdvbv5-devel
The libdvbv5-devel package contains libraries and header
files for developing applications that use libdvbv5

%description -n libdvbv5-devel -l zh_CN.UTF-8
libdvbv5 的开发包。

%prep
%setup -q


%build
%configure --disable-static --enable-libdvbv5 --enable-doxygen-man
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make doxygen-run


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
cp -arv %{_builddir}/%{name}-%{version}/doxygen-doc/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rm $RPM_BUILD_ROOT%{_mandir}/man3/_*3
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop
%find_lang %{name}
%find_lang libdvbv5


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig

%post -n libdvbv5 -p /sbin/ldconfig

%postun -n libdvbv5 -p /sbin/ldconfig

%post -n qv4l2
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qv4l2
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qv4l2
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang -f libdvbv5.lang
%doc README
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%{_udevrulesdir}/70-infrared.rules
%{_prefix}/lib/udev/rc_keymaps/*
%{_bindir}/cx18-ctl
%{_bindir}/dvb*
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_mandir}/man1/*.1*
%exclude %{_mandir}/man1/qv4l2.1*
%exclude %{_mandir}/man1/v4l2-compliance.1*

%files devel-tools
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_mandir}/man1/v4l2-compliance.1*
%{_sbindir}/v4l2-dbg

%files -n qv4l2
%doc README
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*
%{_mandir}/man1/qv4l2.1*

%files -n libv4l
%doc COPYING.libv4l COPYING ChangeLog README.libv4l TODO
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*

%files -n libv4l-devel
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc

%files -n libdvbv5
%doc COPYING ChangeLog lib/libdvbv5/README
%{_libdir}/libdvbv5*.so.*

%files -n libdvbv5-devel
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc
%{_mandir}/man3/*.3*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.8.1-3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.8.1-2
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 1.8.1-1
- 更新到 1.8.1

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.8.5-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Hans de Goede <hdegoede@redhat.com> 0.8.5-1
- New upstream release 0.8.5
- Fixes rhbz#711492

* Wed Jun  1 2011 Hans de Goede <hdegoede@redhat.com> 0.8.4-1
- New upstream release 0.8.4

* Sat Mar 12 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-2
- Add a .desktop file for qv4l2
- Add fully versioned Requires on libv4l to other (sub)packages

* Thu Feb 10 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-1
- New upstream release 0.8.3

* Wed Jan 26 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-3
- Add missing BuildRequires: kernel-headers

* Mon Jan 24 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-2
- Change tarbal to official upstream 0.8.2 release
- This fixes multiple Makefile issues pointed out in the review (#671883)
- Add ir-keytable config files
- Explicitly specify CXXFLAGS so that qv4l2 gets build with rpm_opt_flags too

* Sat Jan 22 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-1
- Initial Fedora package
