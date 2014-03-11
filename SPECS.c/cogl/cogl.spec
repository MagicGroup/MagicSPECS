%if 0%{?fedora}
%global with_wayland 1
%endif

Name:          cogl
Version:       1.14.0
Release:       1%{?dist}
Summary:       A library for using 3D graphics hardware to draw pretty pictures

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/cogl/1.14/cogl-%{version}.tar.xz

BuildRequires: cairo-devel
BuildRequires: gdk-pixbuf2-devel
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: libXrandr-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pango-devel
BuildRequires: pkgconfig

%if %{with_wayland}
BuildRequires: libwayland-client-devel
BuildRequires: libwayland-cursor-devel
BuildRequires: libwayland-egl-devel
BuildRequires: libxkbcommon-devel
%endif


%description
Cogl is a small open source library for using 3D graphics hardware to draw
pretty pictures. The API departs from the flat state machine style of
OpenGL and is designed to make it easy to write orthogonal components that
can render without stepping on each others toes.

As well aiming for a nice API, we think having a single library as opposed
to an API specification like OpenGL has a few advantages too; like being
able to paper over the inconsistencies/bugs of different OpenGL
implementations in a centralized place, not to mention the myriad of OpenGL
extensions. It also means we are in a better position to provide utility
APIs that help software developers since they only need to be implemented
once and there is no risk of inconsistency between implementations.

Having other backends, besides OpenGL, such as drm, Gallium or D3D are
options we are interested in for the future.

%package devel
Summary:       %{name} development environment
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      pkgconfig glib2-devel pango-devel cairo-devel
Requires:      mesa-libGL-devel
Requires:      gobject-introspection-devel

%description devel
Header files and libraries for building and developing apps with %{name}.

%package       doc
Summary:       Documentation for %{name}
Group:         Documentation
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   doc
This package contains documentation for %{name}.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"

%configure --enable-cairo=yes --enable-gdk-pixbuf=yes --enable-cogl-pango=yes --enable-glx=yes --enable-gtk-doc --enable-introspection=yes --enable-wayland-egl-platform

make V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# This gets installed by mistake
rm %{buildroot}%{_datadir}/cogl/examples-data/crate.jpg

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING NEWS README ChangeLog
%{_libdir}/libcogl*.so.*
%{_libdir}/girepository-1.0/Cogl*.typelib

%files devel
%{_includedir}/cogl
%{_libdir}/libcogl*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir

%files doc
%{_datadir}/gtk-doc/html/cogl
%{_datadir}/gtk-doc/html/cogl-2.0-experimental

%changelog
* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> 1.14.0-1
- Update to 1.14.0

* Wed Mar 13 2013 Matthias Clasen <mclasen@redhat.com> 1.13.4-2
- Enable wayland backend

* Thu Feb 21 2013 Bastien Nocera <bnocera@redhat.com> 1.13.4-1
- Update to 1.13.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.2-1
- Update to 1.13.2

* Mon Jan  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.12.2-1
- Update to 1.12.2

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.6-1
- Update to 1.11.6
- Drop upstreamed cogl-1.11.4-mesa-strings.patch

* Mon Sep 17 2012 Adam Jackson <ajax@redhat.com> 1.11.4-2
- cogl-1.11.4-mesa-strings.patch: Update match strings for Mesa.

* Mon Sep  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.4-1
- Update to 1.11.4

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.11.2-1
- Update to 1.11.2

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.4-1
- Update to 1.10.4
- Dropped no-framebuffer-blit patch which is included in the release

* Thu Apr 19 2012 Adel Gadllah <adel.gadllah@gmail.com> - 1.10.2-1
- Update to 1.10.2

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.8-1
- Update to 1.9.8

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.6-1
- Update to 1.9.6

* Tue Jan 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4
- http://ftp.gnome.org/pub/GNOME/sources/cogl/1.9/cogl-1.9.4.news

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> 1.9.2-1
- Update to 1.9.2

* Thu Nov 03 2011 Adam Jackson <ajax@redhat.com> 1.8.2-4
- cogl-1.8.2-lp-no-framebuffer-blit.patch: Disable the subbuffer blit code
  when running on llvmpipe until it's unbroken.

* Tue Nov 01 2011 Adam Jackson <ajax@redhat.com> 1.8.2-3
- cogl-1.8.2-no-drm-hax.patch: Don't try insane direct DRM vblank wait.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.2-1
- 1.8.2 stable release
- http://ftp.gnome.org/pub/GNOME/sources/cogl/1.8/cogl-1.8.2.news
- Enable gdk-pixbuf2 support - Fixes RHBZ # 738092

* Mon Sep 19 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.0-1
- 1.8.0 stable release
- http://ftp.gnome.org/pub/GNOME/sources/cogl/1.8/cogl-1.8.0.news

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Mon Jul  4 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-3
- Update spec for review feedback

* Thu Jun 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-2
- Update spec for review feedback

* Wed Jun 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-1
- Initial Package
