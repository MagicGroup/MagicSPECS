#
# spec file for package dolphin (version R14)
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
%define tde_version 14.0.0
%endif
%define tde_pkg dolphin
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.9.2
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:		File manager for TDE focusing on usability
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif


%description
Dolphin focuses on being only a file manager.
This approach allows to optimize the user
interface for the task of file management.

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --docdir=%{tde_tdedocdir} \
  --libdir=%{tde_libdir} \
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

# Makes 'media_safelyremove.desktop' an alternative
%__mv -f %{buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop %{buildroot}%{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin

# Locales
%find_lang d3lphin


%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} -q &> /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
update-alternatives --install \
  %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop \
  media_safelyremove.desktop_d3lphin \
  %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin \
  15

%preun
if [ $1 -eq 0 ]; then
  update-alternatives --remove \
    media_safelyremove.desktop_d3lphin \
    %{tde_datadir}/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin || :
fi

%postun
update-desktop-database %{tde_tdeappdir} -q &> /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files -f d3lphin.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING TODO
%{tde_bindir}/d3lphin
%{tde_tdeappdir}/d3lphin.desktop
%{tde_datadir}/apps/d3lphin/
%{tde_datadir}/icons/hicolor/*/apps/d3lphin.png
%lang(en) %{tde_tdedocdir}/HTML/en/d3lphin/
%dir %{tde_datadir}/locale/d3lphin/
%dir %{tde_datadir}/locale/d3lphin/LC_MESSAGES


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.9.2-1
- Initial release for TDE 14.0.0
