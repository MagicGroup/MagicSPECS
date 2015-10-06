#
# spec file for package libart-lgpl (version R14)
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

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libart %{_lib}art
%else
%define libart libart
%endif


Name:           trinity-libart-lgpl
Version:        2.3.22
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:        Library of functions for 2D graphics
Group:			System/Libraries
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	LGPL-2.0+
%else
License:	LGPLv2+
%endif

#Vendor:			Trinity Project
#Packager:		Francois Andriot <francois.andriot@free.fr>

Prefix:			/usr
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
A library of functions for 2D graphics supporting a superset of the
PostScript imaging model, designed to be integrated with graphics, artwork,
and illustration programs. It is written in optimized C, and is fully
compatible with C++. With a small footprint of 10,000 lines of code, it is
especially suitable for embedded applications.

##########

%package -n %{libart}_lgpl_2-2
Summary:        Library of functions for 2D graphics - runtime files
Group:			System/Libraries
Obsoletes:		libart_lgpl < %{version}-%{release}
Provides:		libart_lgpl = %{version}-%{release}
Obsoletes:		%{_lib}art_lgpl2 < %{version}-%{release}
Provides:		%{_lib}art_lgpl2 = %{version}-%{release}
Provides:		libart_lgpl_2-2 = %{version}-%{release}

%description -n %{libart}_lgpl_2-2
A library of functions for 2D graphics supporting a superset of the
PostScript imaging model, designed to be integrated with graphics, artwork,
and illustration programs. It is written in optimized C, and is fully
compatible with C++. With a small footprint of 10,000 lines of code, it is
especially suitable for embedded applications.

%post -n %{libart}_lgpl_2-2
/sbin/ldconfig || :

%postun -n %{libart}_lgpl_2-2
/sbin/ldconfig || :

%files -n %{libart}_lgpl_2-2
%defattr(-,root,root,-)
%{_libdir}/libart_lgpl_2.so.2
%{_libdir}/libart_lgpl_2.so.2.3.21

##########

%package -n %{libart}_lgpl-devel
Summary:        Library of functions for 2D graphics - development files
Group:          Development/Libraries
Provides:		libart_lgpl-devel = %{version}-%{release}
Requires:       %{libart}_lgpl_2-2 = %{version}-%{release}

%description -n %{libart}_lgpl-devel
A library of functions for 2D graphics supporting a superset of the
PostScript imaging model, designed to be integrated with graphics, artwork,
and illustration programs. It is written in optimized C, and is fully
compatible with C++. With a small footprint of 10,000 lines of code, it is
especially suitable for embedded applications.

%post -n %{libart}_lgpl-devel
/sbin/ldconfig || :

%postun -n %{libart}_lgpl-devel
/sbin/ldconfig || :

%files -n %{libart}_lgpl-devel
%defattr(-,root,root,-)
%{_bindir}/libart2-config
%{_libdir}/libart_lgpl_2.a
%{_libdir}/libart_lgpl_2.la
%{_libdir}/libart_lgpl_2.so
%dir %{_includedir}/libart-2.0
%dir %{_includedir}/libart-2.0/libart_lgpl
%{_includedir}/libart-2.0/libart_lgpl/art_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_alphagamma.h
%{_includedir}/libart-2.0/libart_lgpl/art_bpath.h
%{_includedir}/libart-2.0/libart_lgpl/art_config.h
%{_includedir}/libart-2.0/libart_lgpl/art_filterlevel.h
%{_includedir}/libart-2.0/libart_lgpl/art_gray_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_misc.h
%{_includedir}/libart-2.0/libart_lgpl/art_pathcode.h
%{_includedir}/libart-2.0/libart_lgpl/art_pixbuf.h
%{_includedir}/libart-2.0/libart_lgpl/art_point.h
%{_includedir}/libart-2.0/libart_lgpl/art_rect.h
%{_includedir}/libart-2.0/libart_lgpl/art_rect_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_rect_uta.h
%{_includedir}/libart-2.0/libart_lgpl/art_render.h
%{_includedir}/libart-2.0/libart_lgpl/art_render_gradient.h
%{_includedir}/libart-2.0/libart_lgpl/art_render_mask.h
%{_includedir}/libart-2.0/libart_lgpl/art_render_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_a_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_bitmap_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_pixbuf_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_rgba_affine.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgb_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_rgba.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_intersect.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_ops.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_point.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_render_aa.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_vpath.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_vpath_stroke.h
%{_includedir}/libart-2.0/libart_lgpl/art_svp_wind.h
%{_includedir}/libart-2.0/libart_lgpl/art_uta.h
%{_includedir}/libart-2.0/libart_lgpl/art_uta_ops.h
%{_includedir}/libart-2.0/libart_lgpl/art_uta_rect.h
%{_includedir}/libart-2.0/libart_lgpl/art_uta_svp.h
%{_includedir}/libart-2.0/libart_lgpl/art_uta_vpath.h
%{_includedir}/libart-2.0/libart_lgpl/art_vpath.h
%{_includedir}/libart-2.0/libart_lgpl/art_vpath_bpath.h
%{_includedir}/libart-2.0/libart_lgpl/art_vpath_dash.h
%{_includedir}/libart-2.0/libart_lgpl/art_vpath_svp.h
%{_includedir}/libart-2.0/libart_lgpl/libart-features.h
%{_includedir}/libart-2.0/libart_lgpl/libart.h
%{_libdir}/pkgconfig/libart-2.0.pc

##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp -f "/usr/share/aclocal/libtool.m4" "libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "ltmain.sh"
autoreconf -fiv


%build
unset QTDIR QTINC QTLIB

%configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --datadir=%{_datadir} \
  --includedir=%{_includedir} \
  \
  --disable-dependency-tracking
  
%__make %{?_smp_mflags}


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT


%clean
%__rm -rf $RPM_BUILD_ROOT



%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2.3.22-1
- Initial release for TDE 14.0.0
