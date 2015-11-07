#
# spec file for package tde-style-qtcurve (version R14)
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
%define tde_pkg tde-style-qtcurve
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
Version:	0.55.2
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	This is a set of widget styles for Trinity based apps
Summary(zh_CN.UTF-8): TDE 基本程序的部件风格集合
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	cmake libtool
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# IDN support
BuildRequires:	libidn-devel

# ACL support
BuildRequires:	libacl-devel

# GAMIN support
#  Not on openSUSE.
%define with_gamin 1
BuildRequires:	gamin-devel

Obsoletes:		trinity-kde-style-qtcurve < %{version}-%{release}
Provides:		trinity-kde-style-qtcurve = %{version}-%{release}
Obsoletes:		trinity-style-qtcurve < %{version}-%{release}
Provides:		trinity-style-qtcurve = %{version}-%{release}


%description
This package together with gtk2-engines-qtcurve aim to provide a unified look
and feel on the desktop when using TDE and Gnome applications.

This package is most useful when installed together with 
gtk2-engines-qtcurve.

%description -l zh_CN.UTF-8
这个包和 gtk2-engines-qtcurve 一起提供了 TDE 和 Gnome 程序的统一外观风格。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}



%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Shitty hack for RHEL4 ...
if [ -d "/usr/X11R6" ]; then
  export CMAKE_INCLUDE_PATH="${CMAKE_INCLUDE_PATH}:/usr/X11R6/include:/usr/X11R6/%{_lib}"
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

# Error in "po/tr.po"
%if 0%{?rhel} == 4
%__rm -f "po/tr.po"
%endif

if ! rpm -E %%cmake|grep -q "cd build"; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DTDE_INCLUDE_DIR=%{tde_tdeincludedir} \
  -DQTC_QT_ONLY=false \
  -DQTC_STYLE_SUPPORT=true \
  -DBUILD_ALL=on \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} -C build

%find_lang qtcurve || touch qtcurve.lang


%clean
%__rm -rf %{buildroot}



%files -f qtcurve.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_tdelibdir}/tdestyle_qtcurve_config.la
%{tde_tdelibdir}/tdestyle_qtcurve_config.so
%{tde_tdelibdir}/plugins/styles/qtcurve.so
%{tde_tdelibdir}/plugins/styles/qtcurve.la
%{tde_datadir}/apps/tdedisplay/color-schemes/QtCurve.kcsrc
%{tde_datadir}/apps/tdestyle/themes/qtcurve.themerc
%{tde_datadir}/apps/QtCurve/


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.55.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.55.2-1
- Initial release for TDE 14.0.0
