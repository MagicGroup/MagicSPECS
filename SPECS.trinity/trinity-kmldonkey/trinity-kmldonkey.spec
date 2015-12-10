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
%define tde_pkg kmldonkey
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
Version:		0.11
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.3
Summary:        Advanced GUI frontend for the MLDonkey P2P core.
Summary(zh_CN): MLDonkey P2P 核心的高级界面前端。
Group:          Applications/Internet
Group(zh_CN):   应用程序/互联网

URL:			http://www.trinitydesktop.org/
License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

%description
KMLDonkey is a frontend for MLDonkey, a powerful P2P file sharing tool,
designed for the KDE desktop.
Feature Overview:
  * A flexible, powerful and KDE Style Guide compliant graphical interface.
  * A complete implementation of the MLDonkey GUI protocol, meaning
    KMLDonkey can do everything the original GUI does.
  * A convenient and configurable on-demand MLDonkey launcher.
  * Real-time graphical bandwidth and network statistics.
  * MobileMule mi%description -l zh_CN.UTF-8leware for controlling your MLDonkey using your Java
    enabled mobile phone.
  * Embe%description -l zh_CN.UTF-8ed previewing of all downloads using KParts viewers.
  * Embe%description -l zh_CN.UTF-8ed web browser providing P2P related web services such as
    availability and fake checks.
  * KDE panel applet for statistics and easy access to the GUI.
  * KIOSlave for opening current and complete downloads in all KDE
    applications (eg. "mldonkey:/Default/downloading/")

%description -l zh_CN
KMLDonkey 是 MLDonkey 一个 KDE 桌面的前端，MLDonkey 是一个很强的 P2P
文件分享工具。


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

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

# Warning: --enable-final causes FTBFS !
%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --mandir=%{tde_mandir} \
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


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

magic_rpm_clean.sh

# Removes useless files
%__rm -f %{?buildroot}%{tde_libdir}/*.la

%clean
%__rm -rf %{buildroot}


%post

%postun

%files 
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{tde_bindir}/*
%{tde_datadir}/apps/%{tde_pkg}
%{tde_datadir}/applications/*
%{tde_datadir}/apps/kicker/applets/mldonkeyapplet.desktop
%{tde_datadir}/apps/konqueror/servicemenus/*
%{tde_datadir}/apps/mldonkeyapplet/
%{tde_datadir}/icons/*/*/*/*
%{tde_datadir}/services/*
%{tde_datadir}/servicetypes/*
%{tde_libdir}/lib*.so.*
%{tde_libdir}/trinity/*.so*
%{tde_libdir}/trinity/*.la
%{tde_libdir}/*.so
%{tde_tdeincludedir}/kmldonkey/*
%{tde_tdedocdir}/HTML/en/kmldonkey/*
%{tde_mandir}/man1/*.1*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:0.11-1.3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.11-1.2
- 为 Magic 3.0 重建

* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.1.2-1
- Initial release for TDE 14.0.0
