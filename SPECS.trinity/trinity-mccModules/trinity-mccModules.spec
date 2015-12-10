#
# spec file for package kchmviewer (version R14)
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
%define tde_pkg mccModules
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		3.1.2
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.4
Summary: Magic Control Center Modules
Summary(zh_CN.UTF-8): Magic 控制中心模块
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.trinitydesktop.org/
License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Packager: lovewilliam <lovewilliam@gmail.com>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig


%description
KCometen3 is an comet OpenGL screensaver for TDE.

%description -l zh_CN.UTF-8
TDE 下的 3D 屏幕保护。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

for i in fcitxconfig grubui mlimecfg;do 
pushd $i
%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"
popd
done

%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

for i in fcitxconfig grubui mlimecfg;do
pushd $i
# Warning: --enable-final causes FTBFS !
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility 

%__make %{?_smp_mflags}
popd
done

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
for i in fcitxconfig grubui mlimecfg;do
pushd $i
%__make install DESTDIR=%{buildroot}
popd
done

mkdir -p $RPM_BUILD_ROOT/etc/ime
install -m 664 mlimecfg/src/ime/fcitx $RPM_BUILD_ROOT/etc/ime/fcitx
install -m 664 mlimecfg/src/ime/scim $RPM_BUILD_ROOT/etc/ime/scim

mkdir -p $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/128x128/apps
mkdir -p $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/64x64/apps
mkdir -p $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/22x22/apps
mkdir -p $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps

install -m 664 icons/hi128-app-grub.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/128x128/apps/grub.png
install -m 664 icons/hi16-app-grub.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/grub.png
install -m 664 icons/hi22-app-grub.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/22x22/apps/grub.png
install -m 664 icons/hi32-app-grub.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/32x32/apps/grub.png
install -m 664 icons/hi64-app-grub.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/32x32/apps/grub.png
install -m 664 icons/hi16-app-boot.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/boot.png
install -m 664 icons/hi16-app-core.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/core.png
install -m 664 icons/hi16-app-hdd.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/hdd.png
install -m 664 icons/hi16-app-vmlinuz.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/vmlinuz.png
install -m 664 icons/hi32-app-qfcitxconfig.png $RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/32x32/apps/qfcitxconfig.png


magic_rpm_clean.sh

# Removes useless files
%__rm -f %{?buildroot}%{tde_libdir}/*.a

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%files 
%defattr(-,root,root,-)
%{tde_tdelibdir}/*
%{tde_datadir}/*
%{_sysconfdir}/*


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.4
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.3
- 为 Magic 3.0 重建

* Wed Oct 14 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.2
- 为 Magic 3.0 重建

* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.1.2-1
- Initial release for TDE 14.0.0
