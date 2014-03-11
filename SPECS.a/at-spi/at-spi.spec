%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define atk_version 1.29.2
%define gtk2_version 2.10.0
%define gail_version 1.9.0
%define libbonobo_version 2.4.0
%define orbit2_version 2.6.0
%define pango_version 1.2.0

Summary: Assistive Technology Service Provider Interface
Summary(zh_CN.UTF-8): 辅助技术服务提供者接口
Name: at-spi
Version: 1.32.0
Release: 9%{?dist}
URL: http://developer.gnome.org/projects/gap/
#VCS: git:git://git.gnome.org/at-spi
Source0: http://download.gnome.org/sources/at-spi/1.32/%{name}-%{version}.tar.bz2

License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: gtk2 >= %{gtk2_version}
Requires: libbonobo >= %{libbonobo_version}
Requires: ORBit2 >= %{orbit2_version}
Requires: gail >= %{gail_version}
Requires: atk >= %{atk_version}

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: ORBit2-devel >= %{orbit2_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: dbus-glib-devel
BuildRequires: GConf2-devel
BuildRequires: fontconfig
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libX11-devel
BuildRequires: libXtst-devel
BuildRequires: libXi-devel
BuildRequires: libXevie-devel
BuildRequires: libXt-devel
BuildRequires: gnome-common
BuildRequires: automake, autoconf, libtool, intltool

# http://bugzilla.gnome.org/show_bug.cgi?id=548782
Patch0: evo-crash.patch

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%description -l zh_CN.UTF-8
at-spi 允许辅助技术访问基于 GTK 的程序。

%package devel
Summary: Development files for at-spi
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %{version}-%{release}
Requires: atk-devel >= %{atk_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libbonobo-devel >= %{libbonobo_version}
Requires: ORBit2-devel >= %{orbit2_version}
Requires: gail-devel >= %{gail_version}
Requires: pkgconfig

%description devel
This package contains libraries, header files and developer documentation
needed for developing applications that interact directly with at-spi.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package python
Summary: Python bindings for at-spi
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %name = %{version}-%{release}
Requires: python
Requires: pyorbit
Requires: gnome-python2-bonobo


%description python
This package contains Python bindings allowing to use at-spi in Python programs.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q
%patch0 -p1 -b .evo-crash

%build
%configure --disable-gtk-doc --disable-static --enable-relocate
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh
%find_lang at-spi

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version} \
   $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}

%pre
%gconf_schema_prepare at-spi

%preun
%gconf_schema_remove at-spi

%post
/usr/sbin/ldconfig
%gconf_schema_upgrade at-spi

%postun -p /usr/sbin/ldconfig

%files -f at-spi.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/bonobo/servers/*
%{_libdir}/orbit-2.0/*
%{_libdir}/gtk-2.0/modules/at-spi-corba
%{_libexecdir}/*
%{_sysconfdir}/gconf/schemas/at-spi.schemas
%{_sysconfdir}/xdg/autostart/at-spi-registryd.desktop

%files devel
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-devel-%{version}
%{_datadir}/gtk-doc/html/*
%{_datadir}/idl/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files python
%defattr(-,root,root)
%{python_sitearch}/pyatspi_corba


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.32.0-8
- 为 Magic 3.0 重建

* Tue Oct 30 2012 Liu Di <liudidi@gmail.com> - 1.32.0-7
- 为 Magic 3.0 重建

* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 1.32.0-6
- 为 Magic 3.0 重建
