#
# spec file for package knemo (version R14)
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
%define tde_pkg knemo
%define tde_prefix /opt/trinity
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


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.4.8
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	Network interfaces monitor for the Trinity systray
Summary(zh_CN.UTF-8): 在 TDE 的系统栏监视网络接口的程序
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/
#URL:		http://beta.smileaf.org/projects

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-knemo--14.0.1-tqt.patch
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool


BuildRequires:	gettext

BuildRequires:	net-tools


%description
KNemo displays an icon in the systray for every network interface.
Tooltips and an info dialog provide further information about the
interface.  Passive popups inform about interface changes.
A traffic plotter is also integrated.

knemo polls the network interface status every second using the
ifconfig, route and iwconfig tools. 

Homepage: http://extragear.kde.org/apps/knemo/

%description -l zh_CN.UTF-8
在系统栏监视网络接口的工具。

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
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%files
%defattr(-,root,root,-)
%{tde_tdelibdir}/kcm_knemo.la
%{tde_tdelibdir}/kcm_knemo.so
%{tde_tdelibdir}/kded_knemod.la
%{tde_tdelibdir}/kded_knemod.so
%{tde_tdeappdir}/kcm_knemo.desktop
%{tde_datadir}/apps/knemo/
%{tde_datadir}/icons/crystalsvg/*/*/*.png
%{tde_datadir}/services/kded/knemod.desktop
%{tde_tdedocdir}/HTML/en/kcontrol/knemo/


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.4.8-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.4.8-1
- Initial release for TDE 14.0.0
