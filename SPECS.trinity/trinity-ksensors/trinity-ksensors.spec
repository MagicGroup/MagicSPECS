#
# spec file for package ksensors (version R14)
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
%define tde_pkg ksensors
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
Version:	0.7.3
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Trinity Frontend to lm_sensors
Summary(zh_CN.UTF-8): TDE 下的 lm_sensors 前端
Group:		Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL:		http://ksensors.sourceforge.net/

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

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

BuildRequires:	lm_sensors-devel

# Keep archs in sync with lm_sensors
ExcludeArch:    s390 s390x


%description
KSensors is a nice lm-sensors frontend for the K Desktop Environment.
Install the hddtemp package if you wish to monitor hard disk
temperatures with KSensors.

%description -l zh_CN.UTF-8
TDE 下的 lm-sensors 前端。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Warning: --enable-final causes FTBFS
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

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

# Move desktop icon to correct location
%__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/"*"/%{tde_pkg}.desktop" "%{?buildroot}%{tde_tdeappdir}"

# Creates autostart shortcut
%__install -dm 755 $RPM_BUILD_ROOT%{tde_datadir}/autostart
%__ln_s "%{tde_tdeappdir}/ksensors.desktop" \
    "$RPM_BUILD_ROOT%{tde_datadir}/autostart"
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for f in locolor hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null || :
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null || :
done

%postun
for f in locolor hicolor ; do
  touch --no-create %{tde_datadir}/icons/$f 2> /dev/null || :
  gtk-update-icon-cache -q %{tde_datadir}/icons/$f 2> /dev/null || :
done


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ README TODO
%{tde_bindir}/ksensors
%{tde_tdeappdir}/ksensors.desktop
%{tde_datadir}/apps/ksensors/
%{tde_datadir}/autostart/ksensors.desktop
%{tde_datadir}/icons/hicolor/*/apps/ksensors.png
%{tde_datadir}/icons/locolor/*/apps/ksensors.png
%{tde_datadir}/sounds/ksensors_alert.wav
%{tde_tdedocdir}/HTML/en/ksensors/


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.7.3-1
- Initial release for TDE 14.0.0
