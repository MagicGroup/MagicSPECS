#
# spec file for package png2qrgb
#
# Copyright (c) 2014 François Andriot <francois.andriot@free.fr>
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
%define tde_pkg png2qrgb
%define tde_version 14.0.0
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_includedir %{tde_prefix}/include
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_libdir %{tde_prefix}/%{_lib}

Name:		trinity-%{tde_pkg}
Version:	0.3
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Png2qrgb (Convert PNG images to an array of TQRgb hexadecimal values)
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{tde_pkg}-%{version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	libtqt4-devel >= 2:4.2.0

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig


%description
Created as a utility to aid in generating  window decorations for TDE's
TWin, png2qrgb  can read  PNG images and spew out TQRgb arrays. A second
mode png2qrgb can operate in generates image attributes rather than the
image itself. Png2qrgb can be used to embed PNG images into TQt code.

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{tde_pkg}-%{version}%{?preversion:~%{preversion}}

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
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf %{?buildroot}
%__make install DESTDIR=%{?buildroot}


%files
%{tde_bindir}/png2qrgb
%{tde_datadir}/applnk/Utilities/png2qrgb.desktop
%{_mandir}/man1/png2qrgb.1*


%clean
%__rm -rf %{?buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 0.3-1
- Initial release for TDE 14.0.0
