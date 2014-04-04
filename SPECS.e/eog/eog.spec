%global _changelog_trimtime %(date +%s -d "1 year ago")

%define gtk3_version 3.7.8
%define glib2_version 2.31.0
%define gnome_desktop_version 2.91.2
%define gnome_icon_theme_version 2.19.1
%define desktop_file_utils_version 0.9
%define libexif_version 0.6.14

Summary: Eye of GNOME image viewer
Summary(zh_CN.UTF-8): GNOME 的图像查看器
Name:    eog
Version:	3.12.0
Release: 2%{?dist}
URL: http://projects.gnome.org/eog/
#VCS: git:git://git.gnome.org/eog
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/eog/%{majorver}/%{name}-%{version}.tar.xz

# The GFDL has an "or later version" clause embedded inside the license.
# There is no need to add the + here.
License: GPLv2+ and GFDL
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: libexif-devel >= %{libexif_version}
BuildRequires: exempi-devel
BuildRequires: lcms2-devel
BuildRequires: intltool >= 0.50.0-1
BuildRequires: libjpeg-devel
BuildRequires: gettext
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gnome-desktop3-devel >= %{gnome_desktop_version}
BuildRequires: gnome-icon-theme-devel >= %{gnome_icon_theme_version}
BuildRequires: libXt-devel
BuildRequires: libxml2-devel
BuildRequires: librsvg2-devel
BuildRequires: libpeas-devel >= 0.7.4
BuildRequires: gdk-pixbuf2-devel
BuildRequires: shared-mime-info
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: dbus-glib-devel
BuildRequires: gobject-introspection-devel
BuildRequires: zlib-devel
BuildRequires: itstool
Requires:      gsettings-desktop-schemas

Requires(post):   desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

%description
The Eye of GNOME image viewer (eog) is the official image viewer for the
GNOME desktop. It can view single image files in a variety of formats, as
well as large image collections.

eog is extensible through a plugin system.

%description -l zh_CN.UTF-8
GNOME 桌面环境下的图像查看器，支持多种格式，也可以利用插件扩展。

%package devel
Summary: Support for developing plugins for the eog image viewer
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: gtk3-devel

%description devel
The Eye of GNOME image viewer (eog) is the official image viewer for the
GNOME desktop. This package allows you to develop plugins that add new
functionality to eog.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang %{name} --with-gnome

rm -rf $RPM_BUILD_ROOT%{_libdir}/eog/plugins/*.la

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/eog.desktop


%post
update-desktop-database >&/dev/null || :
touch %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_datadir}/eog
%{_datadir}/applications/eog.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_bindir}/*
%{_libdir}/eog
%{_datadir}/GConf/gsettings/eog.convert
%{_datadir}/appdata/eog.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.eog.gschema.xml

%files devel
%{_includedir}/eog-3.0
%{_libdir}/pkgconfig/eog.pc
%{_datadir}/gtk-doc/

%changelog
* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 3.12.0-2
- 更新到 3.12.0

* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 3.11.92-2
- 更新到 3.11.92

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-2
- Rebuilt for gnome-desktop soname bump

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Wed Oct 30 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-2
- Rebuilt for libgnome-desktop soname bump

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.1-2
- Trim %%changelog

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1
- Adapt for gnome-icon-theme packaging changes

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-5
- Drop the desktop file vendor prefix

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-4
- Rebuilt for libgnome-desktop soname bump

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.7.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.2-2
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Wed Nov 21 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1
