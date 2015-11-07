%global glib2_version 2.37.2

Name:           gdk-pixbuf2
Version:	2.33.1
Release:        2%{?dist}
Summary:        An image loading library
Summary(zh_CN.UTF-8): 图像装载库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.gt.org
#VCS:           git:git://git.gnome.org/gdk-pixbuf
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/gdk-pixbuf/%{majorver}/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  jasper-devel
BuildRequires:  libX11-devel
BuildRequires:  gobject-introspection-devel >= 0.9.3
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
# Bootstrap requirements
BuildRequires: autoconf automake libtool gtk-doc
BuildRequires: gettext-autopoint

Requires: glib2%{?_isa} >= %{glib2_version}

# We also need MIME information at runtime
Requires: shared-mime-info

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2 <= 2.21.2

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%description -l zh_CN.UTF-8
这是一个图像装载库，可以通过扩展载入模块支持新的图像格式。它被 GTK+ 或
clutter 工具使用。

%package devel
Summary: Development files for gdk-pixbuf
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa} >= %{glib2_version}

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2-devel <= 2.21.2

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package tests
Summary: Tests for the %{name} package
Summary(zh_CN.UTF-8): %{name} 的测试包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%description tests -l zh_CN.UTF-8
%{name} 的测试包。

%prep
%setup -q -n gdk-pixbuf-%{version}

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS             \
        --with-x11                   \
        --with-libjasper             \
        --with-included-loaders=png  \
        --enable-installed-tests
)
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT    \
             RUN_QUERY_LOADER_TEST=false

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.la

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)
magic_rpm_clean.sh
%find_lang gdk-pixbuf

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
if [ $1 -gt 0 ]; then
  gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :
fi

%files -f gdk-pixbuf.lang
%doc AUTHORS COPYING NEWS
%{_libdir}/libgdk_pixbuf-2.0.so.*
%{_libdir}/libgdk_pixbuf_xlib-2.0.so.*
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/libgdk_pixbuf_xlib-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/gdk-pixbuf-csource.1*

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.33.1-2
- 更新到 2.33.1

* Sat Apr 05 2014 Liu Di <liudidi@gmail.com> - 2.30.7-1
- 更新到 2.30.7

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.29.3-1
- Update to 2.29.3
- Tighten deps with %%_isa

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 2.29.2-1
- Update to 2.29.2
- Add a tests subpackage

* Mon Jun 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.29.0-2
- Rebuild (libpng)

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.29.0-1
- Update to 2.29.0

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.28.0-1
- Update to 2.28.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.3-1
- Update to 2.27.3

* Mon Mar 04 2013 Richard Hughes <rhughes@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.1-1
- Update to 2.27.1

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.27.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Tue Jan 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.26.5-3
- Require glib2 >= 2.34.0 for g_type_ensure().

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.26.5-2
- rebuild against new libjpeg

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.5-1
- Update to 2.26.5

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.4-1
- Update to 2.26.4

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.26.2-1
- Update to 2.26.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.0-1
- Update to 2.26.0

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.25.0-1
- Update to 2.25.0

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Rebuild against new libpng

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Jun 27 2011 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5 (fixes CVE-2011-2485)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Mar 30 2011 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Sat Mar  5 2011 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.23.0-1
- Update to 2.23.0

* Fri Nov  5 2010 Matthias Clasen <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Wed Sep 29 2010 jkeating - 2.22.0-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Mon Jul 19 2010 Bastien Nocera <bnocera@redhat.com> 2.21.6-3
- Require libpng for linking

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.21.6-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-4
- Also Require shared-mime-info for same reason

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-3
- BR shared-mime-info; see comment above it

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.21.5-2
- Changes to support snapshot builds

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-2
- Rename to gdk-pixbuf2 to avoid conflict with the
  existing gdk-pixbuf package

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-1
- Update to 2.21.4
- Incorporate package review feedback

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.3-1
- Initial packaging
