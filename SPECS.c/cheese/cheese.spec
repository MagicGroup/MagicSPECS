Name:           cheese
Epoch:          2
Version:	3.18.1
Release:        5%{?dist}
Summary:        Application for taking pictures and movies from a webcam
Summary(zh_CN.UTF-8): 从网络摄像头中抓取图像和视频的程序

%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Group:          Amusements/Graphics
Group(zh_CN.UTF-8): 娱乐/图像
License:        GPLv2+
URL:            http://projects.gnome.org/cheese/
#VCS: git:git://git.gnome.org/cheese
Source0:        http://download.gnome.org/sources/cheese/%{majorver}/%{name}-%{version}.tar.xz
# https://bugzilla.gnome.org/show_bug.cgi?id=678447
# Patch2: 0002-Setup-vp8enc-in-a-way-suitable-for-realtime-encoding.patch

BuildRequires: gtk3-devel >= 3.0.0
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-bad-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: cairo-devel >= 1.4.0
BuildRequires: librsvg2-devel >= 2.18.0
BuildRequires: evolution-data-server-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXtst-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libgudev1-devel
BuildRequires: libcanberra-devel
BuildRequires: clutter-devel
BuildRequires: clutter-gtk-devel
BuildRequires: clutter-gst2-devel
BuildRequires: libmx-devel
BuildRequires: vala-devel
BuildRequires: pkgconfig(gee-1.0)
BuildRequires: gnome-video-effects
BuildRequires: gnome-desktop3-devel
BuildRequires: chrpath
BuildRequires: itstool

Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: gstreamer1-plugins-good
Requires: gstreamer1-plugins-bad
Requires: gnome-video-effects

%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It can also apply fancy graphical effects.

%description -l zh_CN.UTF-8
从网络摄像头中抓取图像和视频的程序。

%package libs
Summary:	Webcam display and capture widgets
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv2+

%description libs
This package contains libraries needed for applications that
want to display a webcam in their interface.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package libs-devel
Summary:	Development files for %{name}-libs
Summary(zh_CN.UTF-8): %{name}-libs 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	GPLv2+
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs-devel
This package contains the libraries and header files that are needed
for writing applications that require a webcam display widget.

%description libs-devel -l zh_CN.UTF-8
%{name}-libs 的开发包。

%prep
%setup -q
# %patch2 -p1


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libcheese.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/libcheese-gtk.{a,la}

magic_rpm_clean.sh
%find_lang %{name} --with-gnome

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cheese
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libcheese-gtk.so.*

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :


%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%post libs
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%postun libs
/sbin/ldconfig
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%doc AUTHORS COPYING README
%{_bindir}/cheese
%{_datadir}/icons/hicolor/*/apps/cheese.png
# FIXME find-lang is supposed to pick these up
%doc %{_datadir}/help/*/cheese
%{_libexecdir}/gnome-camera-service
%{_datadir}/appdata/org.gnome.Cheese.appdata.xml
%{_datadir}/applications/org.gnome.Cheese.desktop
%{_datadir}/dbus-1/services/org.gnome.*.service
%{_datadir}/icons/hicolor/symbolic/apps/cheese-symbolic.svg

%files -f %{name}.lang libs
%{_libdir}/libcheese.so.*
%{_libdir}/libcheese-gtk.so.*
%{_datadir}/glib-2.0/schemas/org.gnome.Cheese.gschema.xml
%{_libdir}/girepository-1.0/Cheese-3.0.typelib

%files libs-devel
#%doc COPYING
%{_libdir}/libcheese.so
%{_libdir}/libcheese-gtk.so
%{_includedir}/cheese/
%{_datadir}/gtk-doc/
%{_libdir}/pkgconfig/cheese.pc
%{_libdir}/pkgconfig/cheese-gtk.pc
%{_datadir}/gir-1.0/Cheese-3.0.gir

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2:3.18.1-5
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2:3.18.1-4
- 更新到 3.18.1

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.12.1-3
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.12.1-2
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.12.1-1
- 更新到 3.12.1

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.13.1-2
- 更新到 3.13.1

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.12.1-2
- 更新到 3.12.1

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.13.1-2
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 2:3.13.1-1
- 更新到 3.13.1

* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 2:3.12.0-1
- 更新到 3.12.0

* Mon Mar 24 2014 Liu Di <liudidi@gmail.com> - 2:3.11.92-1
- 更新到 3.11.92

* Sun Mar 09 2014 Liu Di <liudidi@gmail.com> - 2:3.11.91-1
- 更新到 3.11.91

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 2:3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2:3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2:3.7.92-2
- Rebuilt for clutter-gtk soname bump

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 2:3.7.92-1
- Update to 3.7.92

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 2:3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2:3.7.90-3
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 2:3.7.90-2
- Rebuilt for libgnome-desktop soname bump

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 2:3.7.90-1
- Update to 3.7.90

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:3.7.4-2
- Rebuild for new cogl

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 2:3.7.4-1
- Update to 3.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2:3.7.3-1
- Update to 3.7.3

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 2:3.6.2-1
- Update to 3.6.2

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 2:3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 2:3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 2:3.5.92-1
- Update to 3.5.92

* Thu Sep  6 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.5.91-1
- Update to 3.5.91
- Drop upstreamed patches

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.5.5-2
- Rebuild against new cogl/clutter

* Wed Aug 22 2012 Hans de Goede <hdegoede@redhat.com> - 2:3.5.5-1
- New upstream release 3.5.5
- Fix cheese crashing on tvcards which report they can capture 0x0 as
  minimum resolution (rhbz#850505)

* Tue Aug 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 2:3.5.2-6
- Rebuild for new libcogl.

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:3.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Hans de Goede <hdegoede@redhat.com> - 2:3.4.2-3
- Reduce camerabin pipeline creation time (rhbz#797188, gnome#677731)
- Don't add 0 byte sized files to the thumb-view (rhbz#830166, gnome#677735)
- Fix sizing of horizontal thumbnail list (rhbz#829957)
- Optimize encoding parameters (rhbz#572169)

* Wed Jun 13 2012 Owen Taylor <otaylor@redhat.com> - 2:3.5.2-3
- Require matching version of cheese-libs for cheese

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.5.2-2
- Rebuild against new gnome-desktop

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 2:3.5.2-1
- Update to 3.5.2

* Tue Jun  5 2012 Hans de Goede <hdegoede@redhat.com> - 2:3.5.1-2
- Fix missing images on buttons, also fixes the "Gtk-WARNING **: Attempting to
  add a widget with type GtkImage to a GtkButton ..." warnings (gnome#677543)
- Fix cheese crashing when started on machines with v4l2 radio or vbi devices
  (rhbz#810429, gnome#677544)

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 2:3.5.1-1
- Update to 3.5.1

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2:3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 2:3.4.0-1
- Update to 3.4.0

* Wed Mar 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 2:3.3.5-2
- Rebuild for new cogl

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.4-1
- Update to 3.3.4

* Mon Jan 16 2012 Matthias Clasen <mclasen@redhat.com> - 2:3.3.3-3
- Add a BuildRequires for itstool

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 2:3.3.3-1
- Update to 3.3.3

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.2-2
- Rebuild against new clutter

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 1:3.3.2-1
- Update to 3.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.3.1-1
- Update to 3.3.1-1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.2.1-1
- Update to 3.2.1

* Thu Sep 29 2011 Hans de Goede <hdegoede@redhat.com> - 1:3.2.0-2
- Add Requires: gstreamer-plugins-bad-free for the camerabin element (#717872)

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Wed Sep 21 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:3.1.92-2
- Rebuld for new libcogl.
- Use old libgee api.

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.1.91.1-1
- Update to 3.1.91.1

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.2-2
- Rebuild

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.2-1
- Update to 3.0.2

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:3.0.1-3
- Removed RPATHS (RH #703636)

* Wed Jun 15 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-2
- Rebuild against newest gnome-desktop3

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 1:3.0.1-1
- Update to 3.0.1

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> 1:3.0.0-2
- Add newer icons from upstream

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 1:3.0.0-1
- Update to 3.0

* Wed Mar 30 2011 Alexander Larsson <alexl@redhat.com> - 1:2.91.93-3
- Move gsettings schema to cheese-libs, fixes control-center crash (#691667)
- Move typelib to cheese-libs

* Mon Mar 28 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-2
- Add missing gnome-video-effects dependency

* Fri Mar 25 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.92-1
- Update to 2.91.92

* Sat Mar 12 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91.1-1
- Update to 2.91.91.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 1:2.91.4-1
- Update to 2.91.4

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 1:2.91.3-1
- Update to 2.91.3

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> 1:2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.91-1
- Update to 2.31.91

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.90-2
- Co-own /usr/share/gtk-doc

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.90-1
- Update to 2.31.90

* Fri Aug 11 2010 Matthias Clasen <mclasen@redhat.com> 1:2.31.1-2
- Add an epoch to stay ahead of F14

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Wed Mar 24 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-4
- Fix possible crasher when countdown reaches zero

* Fri Mar 19 2010 Matthias Clasen <mclasen@redhat.com> 2.29.92-3
- Fix text rendering issues on the effects tab

* Tue Mar 16 2010 Matthias Clasen <mclasen@redhat.com> 2.29.92-2
- Use an existing icon

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-2
- Fix include path, and missing requires for the pkg-config file

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.90-1
- Update to 2.29.90

* Sun Jan 17 2010 Matthias Clasen  <mclasen@redhat.com> 2.29.5-2
- Rebuild

* Tue Jan 12 2010 Matthias Clasen  <mclasen@redhat.com> 2.29.5-1
- Update to 2.29.5

* Sun Sep 27 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.28.0-2
- Update desktop file according to F-12 FedoraStudio feature

* Mon Sep 21 2009 Matthias Clasen  <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Sat Aug 22 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-3
- Update sensitivity of menu items

* Fri Aug 14 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-2
- Fix schemas file syntax

* Tue Aug 11 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Sun May 31 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.2-1
- Update to 2.27.2

* Fri May 15 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.90-1
- Update to 2.25.90

* Tue Jan  6 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.3-1
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.2-1
- Update to 2.25.2

* Thu Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-4
- Better URL

* Thu Nov 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-3
- Update to 2.25.1

* Sun Nov  9 2008 Hans de Goede <hdegoede@redhat.com> 2.24.1-2
- Fix cams which only support 1 resolution not working (rh470698, gnome560032)

* Mon Oct 20 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-2
- Save space

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-1
- Update to 2.24.0

* Tue Sep  9 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.92-3
- Update to 2.23.92
- Drop upstreamed patches

* Wed Sep  3 2008 Hans de Goede <hdegoede@redhat.com> 2.23.91-2
- Fix use with multiple v4l devices (rh 460956, gnome 546868, gnome 547144)

* Tue Sep  2 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Tue May 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.2-1
- Update to 2.23.2

* Fri Apr 25 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Apr 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-2
- Fix an invalid free

* Mon Apr  7 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.92-1
- Update to 2.21.92

* Fri Feb 15 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-3
- Fix a locking problem that causes the UI to freeze

* Fri Feb  8 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-1
- Update to 2.21.91

* Mon Jan 14 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Mon Dec 24 2007  Matthias Clasen  <mclasen@redhat.com> 0.3.0-1
- Update to 0.3.0

* Fri Sep  7 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-2
- package review feedback

* Thu Sep  6 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-1
- Initial packages
