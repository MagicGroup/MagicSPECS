#
# spec file for package ksquirrel (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg ksquirrel
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.8.0
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	Powerful Trinity image viewer
Summary(zh_CN.UTF-8): TDE 下的图像查看器
Group:		Amusements/Games
Group(zh_CN.UTF-8): 娱乐/游戏
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	trinity-libkipi-devel
BuildRequires:	trinity-libksquirrel-devel

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# MESA support
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel

%description
KSquirrel is an image viewer for TDE with disk navigator, file tree,
multiple directory view, thumbnails, extended thumbnails, dynamic
format support, DCOP interface, KEXIF and KIPI plugins support.

KSquirrel is a fast and convenient image viewer for TDE featuring
OpenGL and dynamic format support.

%description -l zh_CN.UTF-8
TDE 下的图像查看器。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export CXXFLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

# Warning: --enable-final causes FTBFS
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --disable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE LICENSE.GFDL LICENSE.LGPL README TODO
%{tde_bindir}/ksquirrel
%{tde_bindir}/ksquirrel-libs-configurator
%{tde_bindir}/ksquirrel-libs-configurator-real
%{tde_tdelibdir}/libksquirrelpart.la
%{tde_tdelibdir}/libksquirrelpart.so
%{tde_tdeappdir}/ksquirrel.desktop
%dir %{tde_datadir}/apps/dolphin
%dir %{tde_datadir}/apps/dolphin/servicemenus
%{tde_datadir}/apps/dolphin/servicemenus/dolphksquirrel-dir.desktop
%{tde_datadir}/apps/konqueror/servicemenus/konqksquirrel-dir.desktop
%{tde_datadir}/apps/ksquirrel/
%{tde_datadir}/apps/ksquirrelpart/
%{tde_confdir}/magic/x-ras.magic
%{tde_confdir}/magic/x-sun.magic
%{tde_confdir}/magic/x-utah.magic
%{tde_tdedocdir}/HTML/*/ksquirrel
%{tde_datadir}/icons/hicolor/*/apps/ksquirrel.png
%{tde_datadir}/mimelnk/image/*.desktop
%{tde_datadir}/services/ksquirrelpart.desktop
%{tde_mandir}/man1/ksquirrel.1

%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.8.0-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.8.0-1
- Initial release for TDE 14.0.0
