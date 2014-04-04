%define glib2_version 2.27.2
%define vala_version 0.11.7

Name:           dconf
Version:	0.20.0
Release:        1%{?dist}
Summary:        A configuration system
Summary(zh_CN.UTF-8): 一个配置系统

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        LGPLv2+ and GPLv2+ and GPLv3+
URL:            http://live.gnome.org/dconf
#VCS:           git:git://git.gnome.org/dconf
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/dconf/%{majorver}/dconf-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk3-devel
BuildRequires:  libxml2-devel
BuildRequires:  dbus-devel
BuildRequires:  vala-devel >= %{vala_version}
BuildRequires:  gtk-doc
BuildRequires:  intltool

Requires:       dbus

%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%description -l zh_CN.UTF-8
dconf 是一个低级别的配置系统。它的主要目的是使用 GLib 提供一个 GSettings API 的后端。

%package devel
Summary: Header files and libraries for dconf development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}

%description devel
dconf development package. Contains files needed for doing software
development using dconf.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package editor
Summary: Configuration editor for dconf
Summary(zh_CN.UTF-8): doconf 的配置编辑器
Group:   Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: %{name} = %{version}-%{release}

%description editor
dconf-editor allows you to browse and modify dconf databases.

%description editor -l zh_CN.UTF-8
doconf 的配置编辑器。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang dconf

%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f dconf.lang
%doc COPYING
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf.so.*
%{_libdir}/libdconf-dbus-1.so.*
%{_datadir}/bash-completion/completions/dconf
%{_datadir}/glib-2.0/schemas/ca.desrt.dconf-editor.gschema.xml
%{_mandir}/man1/dconf-service.1.gz
%{_mandir}/man1/dconf.1.gz
%{_mandir}/man7/dconf.7.gz

%files devel
%{_includedir}/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf-dbus-1
%{_libdir}/libdconf-dbus-1.so
%{_libdir}/pkgconfig/dconf-dbus-1.pc
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala

%files editor
%{_bindir}/dconf-editor
%{_datadir}/applications/dconf-editor.desktop
#%dir %{_datadir}/dconf-editor
#%{_datadir}/dconf-editor/dconf-editor.ui
#%{_datadir}/dconf-editor/dconf-editor-menu.ui
%{_datadir}/icons/hicolor/*/apps/dconf-editor.png
%{_datadir}/icons/HighContrast/*/apps/dconf-editor.png
%{_mandir}/man1/dconf-editor.1.gz
%{_datadir}/appdata/dconf-editor.appdata.xml

%changelog
* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 0.20.0-1
- 更新到 0.20.0

* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 0.19.92-1
- 更新到 0.19.92

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.15.0-4
- 为 Magic 3.0 重建


