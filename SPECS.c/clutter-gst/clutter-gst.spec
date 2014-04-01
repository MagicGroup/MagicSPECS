Name:           clutter-gst
Version:        1.6.0
Release:        6%{?dist}
Summary:        ClutterMedia interface to GStreamer
Summary(zh_CN.UTF-8): Clutter 的 GStreamer 接口

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.5/%{name}-%{version}.tar.xz
# http://cgit.freedesktop.org/dolt/commit/?id=b6a7ccd13501ee2099c9819af4b36587f21ca1e0
# Support Linux on any architecture, and assume -fPIC
Patch0:         %{name}-1.3.12-dolt.patch
Patch1:         %{name}-1.6.0-needless-glint.patch
Patch3:         clutter-gst-1.6.0-gl.patch

BuildRequires:  clutter-devel >= 1.10.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel

%description
This package contains a video texture actor and an audio player object for
use with clutter

%description -l zh_CN.UTF-8
这个包包含了视频纹理和音频播放器对象，和旧版本的 gstreamer 配合使用。

%package devel
Summary:        clutter-gst development environment
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       clutter-devel
Requires:       gstreamer-devel
Requires:       gstreamer-plugins-base-devel
Requires:       pkgconfig

%description devel
Header files and libraries for building a extension library for the
clutter-gst

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
#%patch0 -p1 -b .dolt
%patch1 -p1 -b .glint
%patch3 -p1

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libclutter-gst-*.so.0
%{_libdir}/libclutter-gst-*.so.0.*
%{_libdir}/gstreamer-0.10/libgstclutter.so
%{_libdir}/girepository-1.0/ClutterGst-1.0.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/clutter-gst*
%{_libdir}/libclutter-gst-*.so
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/ClutterGst-1.0.gir

%changelog
* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.6.0-6
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.0-5
- Rebuild for new cogl

* Thu Jan 17 2013 Richard Hughes <hughsient@gmail.com> - 1.6.0-4
- Rebuild as I messed up and mclazy updated to the GStreamer1 version.

* Tue Aug 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.6.0-3
- Rebuild for new libcogl.
- Pull glint patch from upstream to fix build.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Richard Hughes <hughsient@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.6-1
- Update to 1.5.6

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.5.4-2
- Rebuild against new cogl

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Thu Jan 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.6-1
- New stable 1.4.6
- ftp://ftp.gnome.org/pub/gnome/sources/clutter-gst/1.4/clutter-gst-1.4.6.news

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 1.4.4-2
- Rebuild against new clutter

* Fri Oct 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.4-1
- New stable 1.4.4
- ftp://ftp.gnome.org/pub/gnome/sources/clutter-gst/1.4/clutter-gst-1.4.4.news

* Wed Oct  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.2-1
- New stable 1.4.2
- ftp://ftp.gnome.org/pub/gnome/sources/clutter-gst/1.4/clutter-gst-1.4.2.news

* Sat Oct  1 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.0-1
- New stable 1.4.0
- ftp://ftp.gnome.org/pub/gnome/sources/clutter-gst/1.4/clutter-gst-1.4.0.news

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> 1.3.12-3
- Rebuild

* Wed Jun 29 2011 Dan Horák <dan[at]danny.cz> 1.3.12-2
- use dolt on all Linuxes, workarounds issue with internal libtool

* Thu Jun  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.12-1
- Update to 1.3.12

* Tue May 10 2011 Bastien Nocera <bnocera@redhat.com> 1.3.10-1
- Update to 1.3.10

* Wed Apr  6 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.8-1
- New upstream 1.3.8 release

* Thu Mar 17 2011 Bastien Nocera <bnocera@redhat.com> 1.3.6-1
- Update to 1.3.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.4-1
- New upstream 1.3.4 release

* Wed Nov 17 2010 Michel Salim <salimma@fedoraproject.org> - 1.3.2-2
- Update Source0 location
- Build against new Clutter stack

* Tue Sep 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.2-1
- New upstream 1.3.2 release

* Sun Aug 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- New upstream 1.2.0 stable release

* Fri Mar  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-1
- New upstream 1.0.0 stable release
- Enable introspection support

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 0.10.0-1
- Update to 0.10.0

* Sat Jul 25 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.8.0-3
- Rebuild

* Fri Sep 12 2008 Allisson Azevedo <allisson@gmail.com> 0.8.0-2
- Rebuild against new gstreamer-devel

* Sat Sep  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.0-1
- Update to 0.8.0

* Fri Feb 22 2008 Allisson Azevedo <allisson@gmail.com> 0.6.1-1
- Update to 0.6.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-2
- Autorebuild for GCC 4.3

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.0-1
- Update to 0.4.0

* Sun May 13 2007 Allisson Azevedo <allisson@gmail.com> 0.1.1-2
- INSTALL removed from docs
- fix make install for keeping timestamps
- changed license for LGPL
- Fix requires/buildrequires

* Fri Apr 13 2007 Allisson Azevedo <allisson@gmail.com> 0.1.1-1
- Initial RPM release
