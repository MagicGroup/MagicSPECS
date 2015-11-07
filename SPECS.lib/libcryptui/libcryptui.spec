Name: libcryptui
Version: 3.12.2
Release: 4%{?dist}
Summary: Interface components for OpenPGP
Summary(zh_CN.UTF-8): OpenPGP 的接口组件

Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+
URL: http://projects.gnome.org/seahorse/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0: http://download.gnome.org/sources/libcryptui/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: dbus-glib-devel
BuildRequires: gnome-doc-utils
BuildRequires: libgnome-keyring-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gpgme-devel
BuildRequires: gtk3-devel
BuildRequires: intltool
BuildRequires: libnotify-devel
BuildRequires: libtool
BuildRequires: libSM-devel

%description
libcryptui is a library used for prompting for PGP keys.

%description -l zh_CN.UTF-8
OpenPGP 的接口组件

%package devel
Summary: Header files required to develop with libcryptui
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libcryptui-devel package contains the header files and developer
documentation for the libcryptui library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang cryptui --with-gnome --all-name

find ${RPM_BUILD_ROOT} -type f -name "*.a" -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f cryptui.lang
%doc AUTHORS COPYING-LIBCRYPTUI NEWS README
%{_bindir}/*
%{_mandir}/man1/*.gz
%{_datadir}/cryptui
%{_libdir}/libcryptui.so.*
%{_datadir}/dbus-1/services/*
%{_datadir}/pixmaps/cryptui
%{_libdir}/girepository-1.0/*
%{_datadir}/GConf/gsettings/org.gnome.seahorse.recipients.convert
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.recipients.gschema.xml

%files devel
%{_libdir}/libcryptui.so
%{_libdir}/pkgconfig/*
%{_includedir}/libcryptui
%{_datadir}/gtk-doc/html/libcryptui
%{_datadir}/gir-1.0/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 3.12.2-4
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 3.12.2-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.2-1
- Update to 3.12.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Aug 28 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> -3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.2.2-3
- Fix BuildRequires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Fri Nov 18 2011 Matthew Barnes <mbarnes@redhat.com> - 3.2.0-2
- Remove gtk-doc req in devel subpackage (RH bug #754500).

* Wed Sep 28 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Wed Jul 27 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.4-3
- Add upstream patch to avoid file conflicts with seahorse.

* Tue Jul 26 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.4-2
- Package review changes.

* Mon Jul 25 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.4-1
- Initial packaging.
