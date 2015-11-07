# -*- rpm-spec -*-

# Plugin isn't ready for real world use yet - it needs
# a security audit at very least
%define with_plugin 0

%define with_gir 0
%if 0%{?fedora} >= 12
%define with_gir 1
%endif

%define with_gtk3 0
%if 0%{?fedora} >= 15
%define with_gtk3 1
%endif

%define with_vala 0
%if 0%{with_gtk3}
%define with_vala 1
%endif

Summary: A GTK2 widget for VNC clients
Summary(zh_CN.UTF-8): VNC 客户端的 GTK 控件
Name: gtk-vnc
Version:	0.5.4
Release: 3%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://live.gnome.org/gtk-vnc
BuildRequires: gtk2-devel >= 2.14
BuildRequires: pygtk2-devel python-devel zlib-devel
BuildRequires: gnutls-devel cyrus-sasl-devel intltool
%if %{with_gir}
BuildRequires: gobject-introspection-devel
%if 0%{?fedora} < 14
BuildRequires: gir-repository-devel
%endif
%endif
%if %{with_plugin}
%if 0%{?fedora} > 8
BuildRequires: xulrunner-devel
%else
BuildRequires: firefox-devel
%endif
%endif
%if %{with_gtk3}
BuildRequires: gtk3-devel
%endif
%if %{with_vala}
BuildRequires: vala-tools
%endif

%description
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package devel
Summary: Development files to build GTK2 applications with gtk-vnc
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk2-devel

%description devel
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%package python
Summary: Python bindings for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description python
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

A module allowing use of the GTK-VNC widget from python

%if %{with_plugin}
%package plugin
Summary: Mozilla plugin for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description plugin
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

This package provides a web browser plugin for Mozilla compatible
browsers.
%endif

%package -n gvnc
Summary: A GObject for VNC connections

%description -n gvnc
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

%package -n gvnc-devel
Summary: Libraries, includes, etc. to compile with the gvnc library
Group: Development/Libraries
Requires: gvnc = %{version}-%{release}
Requires: pkgconfig

%description -n gvnc-devel
gvnc is a GObject for managing a VNC connection. It provides all the
infrastructure required to build a VNC client without having to deal
with the raw protocol itself.

Libraries, includes, etc. to compile with the gvnc library

%package -n gvnc-tools
Summary: Command line VNC tools
Group: Applications/Internet

%description -n gvnc-tools
Provides useful command line utilities for interacting with
VNC servers. Includes the gvnccapture program for capturing
screenshots of a VNC desktop

%if %{with_gtk3}
%package -n gtk-vnc2
Summary: A GTK3 widget for VNC clients
Group: Applications/Internet

%description -n gtk-vnc2
gtk-vnc is a VNC viewer widget for GTK2. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package -n gtk-vnc2-devel
Summary: Development files to build GTK3 applications with gtk-vnc
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel

%description -n gtk-vnc2-devel
gtk-vnc is a VNC viewer widget for GTK3. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library
%endif

%prep
%setup -q -n gtk-vnc-%{version} -c
%if %{with_gtk3}
cp -a gtk-vnc-%{version} gtk-vnc2-%{version}
%endif

%build
%if %{with_gir}
%define gir_arg --enable-introspection=yes
%else
%define gir_arg --enable-introspection=no
%endif

%if %{with_plugin}
%define plugin_arg --enable-plugin=yes
%else
%define plugin_arg --enable-plugin=no
%endif

cd gtk-vnc-%{version}
%configure --with-gtk=2.0 %{plugin_arg} %{gir_arg}
%__make %{?_smp_mflags} V=1
cd ..

%if %{with_gtk3}
cd gtk-vnc2-%{version}
%configure --with-gtk=3.0 %{gir_arg}
%__make %{?_smp_mflags} V=1
cd ..
%endif

%install
rm -fr %{buildroot}
cd gtk-vnc-%{version}
%__make install DESTDIR=%{buildroot}
cd ..

%if %{with_gtk3}
cd gtk-vnc2-%{version}
%__make install DESTDIR=%{buildroot}
cd ..
%endif

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
%if %{with_plugin}
rm -f %{buildroot}%{_libdir}/mozilla/plugins/%{name}-plugin.a
rm -f %{buildroot}%{_libdir}/mozilla/plugins/%{name}-plugin.la
%endif
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/libgtk-vnc-1.0.so.*
%if %{with_gir}
%{_libdir}/girepository-1.0/GtkVnc-1.0.typelib
%endif

%files devel
%defattr(-, root, root)
%doc gtk-vnc-%{version}/examples/gvncviewer.c
%if %{with_gir}
%doc gtk-vnc-%{version}/examples/gvncviewer.js
%endif
%{_libdir}/libgtk-vnc-1.0.so
%dir %{_includedir}/%{name}-1.0/
%{_includedir}/%{name}-1.0/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/GtkVnc-1.0.gir
%endif

%files python
%defattr(-, root, root)
%{_libdir}/python*/site-packages/gtkvnc.so

%if %{with_plugin}
%files plugin
%defattr(-, root, root)
%{_libdir}/mozilla/plugins/%{name}-plugin.so
%endif

%files -n gvnc -f %{name}.lang
%defattr(-, root, root)
%{_libdir}/libgvnc-1.0.so.*
%if %{with_gir}
%{_libdir}/girepository-1.0/GVnc-1.0.typelib
%endif
%if %{with_vala}
%{_datadir}/vala/vapi/gvnc-1.0.vapi
%endif

#pulse
%{_libdir}/libgvncpulse-1.0.so.*

%files -n gvnc-devel
%defattr(-, root, root)
%{_libdir}/libgvnc-1.0.so
%dir %{_includedir}/gvnc-1.0/
%{_includedir}/gvnc-1.0/*.h
%{_libdir}/pkgconfig/gvnc-1.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/GVnc-1.0.gir
%endif

#pulse
%{_includedir}/gvncpulse-1.0/*
%{_libdir}/libgvncpulse-1.0.so
%{_libdir}/pkgconfig/gvncpulse-1.0.pc
%{_datadir}/gir-1.0/GVncPulse-1.0.gir
%{_datadir}/vala/vapi/gvncpulse-1.0.vapi
%{_libdir}/girepository-1.0/GVncPulse-1.0.typelib

%files -n gvnc-tools
%defattr(-, root, root)
%doc gtk-vnc-%{version}/AUTHORS
%doc gtk-vnc-%{version}/ChangeLog
%doc gtk-vnc-%{version}/ChangeLog-old
%doc gtk-vnc-%{version}/NEWS
%doc gtk-vnc-%{version}/README
%doc gtk-vnc-%{version}/COPYING.LIB
%{_bindir}/gvnccapture
%{_mandir}/man1/gvnccapture.1*

%if %{with_gtk3}
%files -n gtk-vnc2
%defattr(-, root, root)
%{_libdir}/libgtk-vnc-2.0.so.*
%if %{with_gir}
%{_libdir}/girepository-1.0/GtkVnc-2.0.typelib
%endif
%if %{with_vala}
%{_datadir}/vala/vapi/gtk-vnc-2.0.deps
%{_datadir}/vala/vapi/gtk-vnc-2.0.vapi
%endif

%files -n gtk-vnc2-devel
%defattr(-, root, root)
%doc gtk-vnc2-%{version}/examples/gvncviewer.c
%if %{with_gir}
%doc gtk-vnc2-%{version}/examples/gvncviewer.js
%endif
%{_libdir}/libgtk-vnc-2.0.so
%dir %{_includedir}/%{name}-2.0/
%{_includedir}/%{name}-2.0/*.h
%{_libdir}/pkgconfig/%{name}-2.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/GtkVnc-2.0.gir
%endif
%endif


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.5.4-3
- 更新到 0.5.4

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 0.5.3-2
- 更新到 0.5.3

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.4-2
- 为 Magic 3.0 重建

* Thu Nov 10 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-1
- Update to 0.4.4 release

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.4.3-2
- Rebuild to break bogus libpng dep

* Fri Feb 18 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.3-1
- Update to 0.4.3 release

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.4.2-10
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.4.2-8
- Rebuild against newer gtk

* Thu Jan 13 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-7
- Cope with multiple GDK backends in GTK3

* Tue Jan 11 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-6
- Rebuild for change in GTK3 soname

* Mon Jan 10 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-5
- Add fix to remove use of GdkDrawble for GTK3 compat

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 0.4.2-5
- Rebuild against newer gtk3

* Tue Dec 14 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-4
- Fix unref of GSource objects to address performance degradation (rhbz #657847)

* Mon Nov 29 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-3
- Re-introduce a server side pixmap via cairo to cache framebuffer (rhbz #657542)

* Mon Nov 29 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-2
- Fix crash in TLS shutdown code (rhbz #650601)
- Fix crash in motion event handler (rhbz #650104)
- Fix framebuffer update bounds checking (rhbz #655630)

* Fri Nov  5 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-1
- Update to 0.4.2 release.
- Enable experimental GTK3 build

* Mon Oct 18 2010 Colin Walters <walters@verbum.org> - 0.4.1-9
- Rebuild to use old pygobject2-python2 API again:
  https://bugzilla.redhat.com/show_bug.cgi?id=638457

* Wed Sep 29 2010 jkeating - 0.4.1-8
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.1-7
- Rebuild against newer gobject-introspection

* Tue Aug 31 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-6
- Prevent RPM picking up a dep on gjs (rhbz 628604)

* Fri Aug  6 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-5
- Reset buffer offsets on connection close (rhbz 620843)

* Thu Aug  5 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-4
- Reset buffer pointer on connection close (rhbz 620843)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.4.1-2
- Rebuild with new gobject-introspection

* Wed Jul 14 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-1
- Update to 0.4.1 release

* Sun Jul 11 2010 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-1
- Update to 0.4.0 release
- Add new sub-packages for gvnc

* Tue Apr 27 2010 Daniel P. Berrange <berrange@redhat.com> - 0.3.10-3
- Drop VNC connection if the server sends a update spaning outside bounds of desktop (rhbz #540810)
- Fix gcrypt threading initialization (rhbz #537489)

* Tue Oct 20 2009 Matthias Clasen <mclaesn@redhat.com> - 0.3.10-1
- Update to 0.3.10

* Thu Oct  8 2009 Matthias Clasen <mclaesn@redhat.com> - 0.3.9-2
- Request a full screen refresh when receives a desktop-resize encoding

* Tue Aug 11 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.9-1
- Update to 0.3.9 release

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.3.8-10
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-8.fc11
- Fix ungrab when pointer type changes

* Tue Mar 24 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-7.fc11
- Fix release of keyboard grab when releasing mouse grab outside app window (rhbz #491167)

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-6.fc11
- Fix SASL address generation when using AF_UNIX sockets

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-5.fc11
- Support SASL authentication extension

* Thu Feb 26 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-4.fc11
- Fix relative mouse handling to avoid 'invisible wall'

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3.fc11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-2.fc11
- Update URLs to gnome.org hosting

* Sun Dec  7 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-1.fc11
- Update to 0.3.8 release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.7-4
- Rebuild for Python 2.6

* Thu Oct  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.7-3.fc10
- Avoid bogus framebuffer updates for psuedo-encodings
- Fix scancode translation for evdev

* Thu Sep 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.7-2.fc10
- Allow pointer ungrab keysequence if already grabbed (rhbz #463729)

* Fri Sep  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.3.7-1
- Update to 0.3.7

* Thu Aug 28 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-4.fc10
- Fix key/mouse event propagation (rhbz #454627)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.6-3
- fix conditional comparison

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-2.fc10
- Rebuild for GNU TLS ABI change

* Wed May  7 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-1.fc10
- Updated to 0.3.6 release

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1.fc9
- Update to 0.3.5

* Fri Apr  4 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-4.fc9
- Remove bogus chunk of render patch

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-3.fc9
- Fix OpenGL rendering artifacts (rhbz #440184)

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-2.fc9
- Fixed endianness conversions
- Fix makecontext() args crash on x86_64
- Fix protocol version negotiation

* Thu Mar  6 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-1.fc9
- Update to 0.3.4 release
- Fix crash with OpenGL scaling code

* Sun Feb  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.3-1.fc9
- Update to 0.3.3 release

* Mon Jan 14 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-2.fc9
- Track keystate to avoid stuck modifier keys

* Mon Dec 31 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-1.fc9
- Update to 0.3.2 release
- Added dep on zlib-devel

* Thu Dec 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-1.fc9
- Update to 0.3.1 release

* Thu Oct 10 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-4.fc8
- Fixed coroutine cleanup to avoid SEGV (rhbz #325731)

* Thu Oct  4 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-3.fc8
- Fixed coroutine caller to avoid SEGV

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-2.fc8
- Remove use of PROT_EXEC for coroutine stack (rhbz #307531 )

* Thu Sep 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-1.fc8
- Update to 0.2.0 release

* Wed Aug 29 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-5.fc8
- Fixed handling of mis-matched client/server colour depths

* Wed Aug 22 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-4.fc8
- Fix mixed endian handling & BGR pixel format (rhbz #253597)
- Clear widget areas outside of framebuffer (rhbz #253599)
- Fix off-by-one in python demo

* Thu Aug 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-3.fc8
- Tweaked post scripts
- Removed docs from sub-packages
- Explicitly set license to LGPLv2+
- Remove use of macro for install rule

* Wed Aug 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-2.fc8
- Added gnutls-devel requirement to -devel package

* Wed Aug 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-1.fc8
- Initial official release
