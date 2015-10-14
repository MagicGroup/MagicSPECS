#
# spec file for package kpilot (version R14)
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
%define tde_pkg kpilot
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
Version:	0.7
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	TDE Palm Pilot hot-sync tool
Summary(zh_CN.UTF-8): TDE 平台的 Palm 同步工具
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-kpilot-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdepim-devel >= %{tde_version}
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes


# FLEX
BuildRequires:	flex
BuildRequires:	flex-devel

# PILOT support
BuildRequires:	pilot-link-devel >= 0.12


%description
KPilot is an application that synchronizes your Palm Pilot or similar device
(like the Handspring Visor) with your TDE desktop, much like the Palm HotSync
software does for Windows.  KPilot can back-up and restore your Palm Pilot
and synchronize the built-in applications with their TDE counterparts.

%description -l zh_CN.UTF-8
TDE 平台的 Palm 同步工具。

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

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{?buildroot}%{tde_libdir}/libkpilot.so

magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
for f in hicolor locolor crystalsvg; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
for f in hicolor locolor crystalsvg; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :


%files
%defattr(-,root,root,-)
%{tde_bindir}/kpalmdoc
%{tde_bindir}/kpilot
%{tde_bindir}/kpilotDaemon
%{tde_tdeincludedir}/kpilot
%{tde_libdir}/libkpilot.la
%{tde_libdir}/libkpilot.so.0
%{tde_libdir}/libkpilot.so.0.0.0
%{tde_tdelibdir}/conduit_address.la
%{tde_tdelibdir}/conduit_address.so
%{tde_tdelibdir}/conduit_doc.la
%{tde_tdelibdir}/conduit_doc.so
%{tde_tdelibdir}/conduit_knotes.la
%{tde_tdelibdir}/conduit_knotes.so
%{tde_tdelibdir}/conduit_memofile.la
%{tde_tdelibdir}/conduit_memofile.so
%{tde_tdelibdir}/conduit_notepad.la
%{tde_tdelibdir}/conduit_notepad.so
%{tde_tdelibdir}/conduit_popmail.la
%{tde_tdelibdir}/conduit_popmail.so
%{tde_tdelibdir}/conduit_sysinfo.la
%{tde_tdelibdir}/conduit_sysinfo.so
%{tde_tdelibdir}/conduit_time.la
%{tde_tdelibdir}/conduit_time.so
%{tde_tdelibdir}/conduit_todo.la
%{tde_tdelibdir}/conduit_todo.so
%{tde_tdelibdir}/conduit_vcal.la
%{tde_tdelibdir}/conduit_vcal.so
%{tde_tdelibdir}/kcm_kpilot.la
%{tde_tdelibdir}/kcm_kpilot.so
%{tde_tdeappdir}/kpalmdoc.desktop
%{tde_tdeappdir}/kpilot.desktop
%{tde_tdeappdir}/kpilotdaemon.desktop
%{tde_datadir}/apps/kaddressbook/contacteditorpages/
%{tde_datadir}/apps/tdeconf_update/kpalmdoc.upd
%{tde_datadir}/apps/tdeconf_update/kpilot.upd
%{tde_datadir}/apps/kpilot
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/icons/crystalsvg/*/apps/*.png
%{tde_datadir}/icons/hicolor/*/apps/*.png
%{tde_datadir}/icons/locolor/*/apps/*.png
%{tde_datadir}/services/*.desktop
%{tde_datadir}/servicetypes/kpilotconduit.desktop
%{tde_tdedocdir}/HTML/en/kpilot/

%changelog
* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.7-1
- Initial release for TDE 14.0.0
