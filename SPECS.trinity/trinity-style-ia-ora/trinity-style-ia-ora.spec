#
# spec file for package style-ia-ora (version R14)
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

# Default version for this component
%define tde_pkg style-ia-ora
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif

%define tde_prefix /opt/trinity
# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:			trinity-%{tde_pkg}
Summary:        Mandriva theme for TDE - Widget design
Summary(zh_CN.UTF-8): TDE 下的 Mandriva 主题
Version:        1.0.8
Release:		%{?!preversion:4}%{?preversion:3_%{preversion}}%{?dist}%{?_variant}.1

License:        GPL
Group:          Environment/Desktop
Group(zh_CN.UTF-8): 用户界面/桌面
URL:            http://www.mandrivalinux.com/

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        %{tde_pkg}-14.0.0.tar.gz

Patch1: 	%{name}-14.0.1-tqt.patch

Prefix:		%{_prefix}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}

Requires:	trinity-twin

%description
Mandriva theme for Trinity

%description -l zh_CN.UTF-8
TDE 下的 Mandriva 主题。

%prep
%setup -q -n ia_ora-kde-%{version}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  \
  --enable-rpath \
  --enable-closure \
  --disable-dependency-tracking \
  --enable-new-ldflags \
  --enable-final \
  --enable-shared \
  --disable-static

%__make %{?_smp_mflags}


%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{?buildroot}

# Removes useless files
%__rm -f %{?buildroot}%{tde_tdelibdir}/*.a
%__rm -f %{?buildroot}%{tde_tdelibdir}/plugins/styles/*.a
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{tde_tdelibdir}/twin3_iaora.la
%{tde_tdelibdir}/twin3_iaora.so
%{tde_tdelibdir}/twin_iaora_config.la
%{tde_tdelibdir}/twin_iaora_config.so
%{tde_tdelibdir}/plugins/styles/ia_ora.la
%{tde_tdelibdir}/plugins/styles/ia_ora.so
%{tde_datadir}/apps/kstyle/themes/ia_ora.themerc
%{tde_datadir}/apps/twin/iaora.desktop




%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.0.8-4.opt.1
- 为 Magic 3.0 重建

* Sat Jan 19 2013 Francois Andriot <francois.andriot@free.fr> - 1.0.8-4
- Initial release for TDE 14.0.0
