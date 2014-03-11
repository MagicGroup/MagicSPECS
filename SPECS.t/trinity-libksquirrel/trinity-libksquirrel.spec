# Default version for this component
%define kdecomp libksquirrel
%define tdeversion 3.5.13.2

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:		trinity-%{kdecomp}
Summary:	Trinity image viewer
Version:	0.8.0
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Environment/Libraries

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz
Patch0:		libksquirrel-3.5.13-detect_netpbm.patch
Patch1:		libksquirrel-3.5.13-fix_docdir.patch

BuildRequires: trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires: trinity-arts-devel >= 3.5.13.1
BuildRequires: trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	gettext-devel
BuildRequires:	transfig
BuildRequires:	djvulibre

# XMEDCON support
%if 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion}
%define with_xmedcon 1
BuildRequires:	xmedcon
BuildRequires:	xmedcon-devel
%endif

# RSVG support
%if 0%{?fedora} || 0%{?rhel} 
BuildRequires:	librsvg2
%endif
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	librsvg
%endif
%if 0%{?suse_version}
BuildRequires:	rsvg-view
BuildRequires:	librsvg-devel
%endif

BuildRequires:	libwmf-devel

%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
BuildRequires:	netpbm
%else
BuildRequires:	netpbm-progs
%endif


%description
Runtime libraries for KSquirrel.


%package devel
Group:		Development/Libraries
Summary:	Trinity image viewer
Requires:	%{name}

%description devel
Development libraries for KSquirrel.


%package tools
Summary:	Trinity image viewer
Group:		Environment/Libraries
Requires:	%{name}

%description tools
Tools for KSquirrel.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}
%patch0 -p1

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_includedir} \
  --disable-rpath \
  --with-extra-includes=%{tde_includedir}/tqt \
  --enable-djvu

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}


%clean
%__rm -rf %{buildroot}


%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE README
%{tde_libdir}/ksquirrel-libs/libkls_avs.so.0
%{tde_libdir}/ksquirrel-libs/libkls_avs.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_bmp.so.0
%{tde_libdir}/ksquirrel-libs/libkls_bmp.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_camera.so.0
%{tde_libdir}/ksquirrel-libs/libkls_camera.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_cut.so.0
%{tde_libdir}/ksquirrel-libs/libkls_cut.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_dds.so.0
%{tde_libdir}/ksquirrel-libs/libkls_dds.so.0.8.0
%if 0%{?with_xmedcon}
%{tde_libdir}/ksquirrel-libs/libkls_dicom.so.0
%{tde_libdir}/ksquirrel-libs/libkls_dicom.so.0.8.0
%endif
%{tde_libdir}/ksquirrel-libs/libkls_djvu.so.0
%{tde_libdir}/ksquirrel-libs/libkls_djvu.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_eps.so.0
%{tde_libdir}/ksquirrel-libs/libkls_eps.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_fig.so.0
%{tde_libdir}/ksquirrel-libs/libkls_fig.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_fli.so.0
%{tde_libdir}/ksquirrel-libs/libkls_fli.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_gif.so.0
%{tde_libdir}/ksquirrel-libs/libkls_gif.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_hdr.so.0
%{tde_libdir}/ksquirrel-libs/libkls_hdr.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_ico.so.0
%{tde_libdir}/ksquirrel-libs/libkls_ico.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_iff.so.0
%{tde_libdir}/ksquirrel-libs/libkls_iff.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_jbig.so.0
%{tde_libdir}/ksquirrel-libs/libkls_jbig.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_jpeg.so.0
%{tde_libdir}/ksquirrel-libs/libkls_jpeg.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_jpeg2000.so.0
%{tde_libdir}/ksquirrel-libs/libkls_jpeg2000.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_koala.so.0
%{tde_libdir}/ksquirrel-libs/libkls_koala.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_leaf.so.0
%{tde_libdir}/ksquirrel-libs/libkls_leaf.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_lif.so.0
%{tde_libdir}/ksquirrel-libs/libkls_lif.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_ljpeg.so.0
%{tde_libdir}/ksquirrel-libs/libkls_ljpeg.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_mac.so.0
%{tde_libdir}/ksquirrel-libs/libkls_mac.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_mdl.so.0
%{tde_libdir}/ksquirrel-libs/libkls_mdl.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_mng.so.0
%{tde_libdir}/ksquirrel-libs/libkls_mng.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_mtv.so.0
%{tde_libdir}/ksquirrel-libs/libkls_mtv.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_neo.so.0
%{tde_libdir}/ksquirrel-libs/libkls_neo.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_openexr.so.0
%{tde_libdir}/ksquirrel-libs/libkls_openexr.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pcx.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pcx.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pi1.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pi1.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pi3.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pi3.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pix.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pix.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_png.so.0
%{tde_libdir}/ksquirrel-libs/libkls_png.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pnm.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pnm.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_psd.so.0
%{tde_libdir}/ksquirrel-libs/libkls_psd.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_psp.so.0
%{tde_libdir}/ksquirrel-libs/libkls_psp.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_pxr.so.0
%{tde_libdir}/ksquirrel-libs/libkls_pxr.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_ras.so.0
%{tde_libdir}/ksquirrel-libs/libkls_ras.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_rawrgb.so.0
%{tde_libdir}/ksquirrel-libs/libkls_rawrgb.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_sct.so.0
%{tde_libdir}/ksquirrel-libs/libkls_sct.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_sgi.so.0
%{tde_libdir}/ksquirrel-libs/libkls_sgi.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_sun.so.0
%{tde_libdir}/ksquirrel-libs/libkls_sun.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_svg.so.0
%{tde_libdir}/ksquirrel-libs/libkls_svg.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_tga.so.0
%{tde_libdir}/ksquirrel-libs/libkls_tga.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_tiff.so.0
%{tde_libdir}/ksquirrel-libs/libkls_tiff.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_ttf.so.0
%{tde_libdir}/ksquirrel-libs/libkls_ttf.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_utah.so.0
%{tde_libdir}/ksquirrel-libs/libkls_utah.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_wal.so.0
%{tde_libdir}/ksquirrel-libs/libkls_wal.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_wbmp.so.0
%{tde_libdir}/ksquirrel-libs/libkls_wbmp.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_wmf.so.0
%{tde_libdir}/ksquirrel-libs/libkls_wmf.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xbm.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xbm.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xcf.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xcf.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xcur.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xcur.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xim.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xim.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xpm.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xpm.so.0.8.0
%{tde_libdir}/ksquirrel-libs/libkls_xwd.so.0
%{tde_libdir}/ksquirrel-libs/libkls_xwd.so.0.8.0
%{tde_libdir}/libksquirrel-libs-png.so.0
%{tde_libdir}/libksquirrel-libs-png.so.0.0.0
%{tde_libdir}/libksquirrel-libs.so.0
%{tde_libdir}/libksquirrel-libs.so.0.8.0
%{tde_datadir}/ksquirrel-libs/libkls_camera.so.ui
%{tde_datadir}/ksquirrel-libs/libkls_djvu.so.ui
%{tde_datadir}/ksquirrel-libs/libkls_svg.so.ui
%{tde_datadir}/ksquirrel-libs/libkls_tiff.so.ui
%{tde_datadir}/ksquirrel-libs/libkls_xcf.so.ui
%{tde_datadir}/ksquirrel-libs/rgbmap

%files devel
%defattr(-,root,root,-)
%{tde_includedir}/ksquirrel-libs/error.h
%{tde_includedir}/ksquirrel-libs/fileio.h
%{tde_includedir}/ksquirrel-libs/fmt_codec_base.h
%{tde_includedir}/ksquirrel-libs/fmt_defs.h
%{tde_includedir}/ksquirrel-libs/fmt_types.h
%{tde_includedir}/ksquirrel-libs/fmt_utils.h
%{tde_includedir}/ksquirrel-libs/settings.h
%{tde_libdir}/ksquirrel-libs/libkls_avs.la
%{tde_libdir}/ksquirrel-libs/libkls_avs.so
%{tde_libdir}/ksquirrel-libs/libkls_bmp.la
%{tde_libdir}/ksquirrel-libs/libkls_bmp.so
%{tde_libdir}/ksquirrel-libs/libkls_camera.la
%{tde_libdir}/ksquirrel-libs/libkls_camera.so
%{tde_libdir}/ksquirrel-libs/libkls_cut.la
%{tde_libdir}/ksquirrel-libs/libkls_cut.so
%{tde_libdir}/ksquirrel-libs/libkls_dds.la
%{tde_libdir}/ksquirrel-libs/libkls_dds.so
%if 0%{?with_xmedcon}
%{tde_libdir}/ksquirrel-libs/libkls_dicom.la
%{tde_libdir}/ksquirrel-libs/libkls_dicom.so
%endif
%{tde_libdir}/ksquirrel-libs/libkls_djvu.la
%{tde_libdir}/ksquirrel-libs/libkls_djvu.so
%{tde_libdir}/ksquirrel-libs/libkls_eps.la
%{tde_libdir}/ksquirrel-libs/libkls_eps.so
%{tde_libdir}/ksquirrel-libs/libkls_fig.la
%{tde_libdir}/ksquirrel-libs/libkls_fig.so
%{tde_libdir}/ksquirrel-libs/libkls_fli.la
%{tde_libdir}/ksquirrel-libs/libkls_fli.so
%{tde_libdir}/ksquirrel-libs/libkls_gif.la
%{tde_libdir}/ksquirrel-libs/libkls_gif.so
%{tde_libdir}/ksquirrel-libs/libkls_hdr.la
%{tde_libdir}/ksquirrel-libs/libkls_hdr.so
%{tde_libdir}/ksquirrel-libs/libkls_ico.la
%{tde_libdir}/ksquirrel-libs/libkls_ico.so
%{tde_libdir}/ksquirrel-libs/libkls_iff.la
%{tde_libdir}/ksquirrel-libs/libkls_iff.so
%{tde_libdir}/ksquirrel-libs/libkls_jbig.la
%{tde_libdir}/ksquirrel-libs/libkls_jbig.so
%{tde_libdir}/ksquirrel-libs/libkls_jpeg.la
%{tde_libdir}/ksquirrel-libs/libkls_jpeg.so
%{tde_libdir}/ksquirrel-libs/libkls_jpeg2000.la
%{tde_libdir}/ksquirrel-libs/libkls_jpeg2000.so
%{tde_libdir}/ksquirrel-libs/libkls_koala.la
%{tde_libdir}/ksquirrel-libs/libkls_koala.so
%{tde_libdir}/ksquirrel-libs/libkls_leaf.la
%{tde_libdir}/ksquirrel-libs/libkls_leaf.so
%{tde_libdir}/ksquirrel-libs/libkls_lif.la
%{tde_libdir}/ksquirrel-libs/libkls_lif.so
%{tde_libdir}/ksquirrel-libs/libkls_ljpeg.la
%{tde_libdir}/ksquirrel-libs/libkls_ljpeg.so
%{tde_libdir}/ksquirrel-libs/libkls_mac.la
%{tde_libdir}/ksquirrel-libs/libkls_mac.so
%{tde_libdir}/ksquirrel-libs/libkls_mdl.la
%{tde_libdir}/ksquirrel-libs/libkls_mdl.so
%{tde_libdir}/ksquirrel-libs/libkls_mng.la
%{tde_libdir}/ksquirrel-libs/libkls_mng.so
%{tde_libdir}/ksquirrel-libs/libkls_mtv.la
%{tde_libdir}/ksquirrel-libs/libkls_mtv.so
%{tde_libdir}/ksquirrel-libs/libkls_neo.la
%{tde_libdir}/ksquirrel-libs/libkls_neo.so
%{tde_libdir}/ksquirrel-libs/libkls_openexr.la
%{tde_libdir}/ksquirrel-libs/libkls_openexr.so
%{tde_libdir}/ksquirrel-libs/libkls_pcx.la
%{tde_libdir}/ksquirrel-libs/libkls_pcx.so
%{tde_libdir}/ksquirrel-libs/libkls_pi1.la
%{tde_libdir}/ksquirrel-libs/libkls_pi1.so
%{tde_libdir}/ksquirrel-libs/libkls_pi3.la
%{tde_libdir}/ksquirrel-libs/libkls_pi3.so
%{tde_libdir}/ksquirrel-libs/libkls_pix.la
%{tde_libdir}/ksquirrel-libs/libkls_pix.so
%{tde_libdir}/ksquirrel-libs/libkls_png.la
%{tde_libdir}/ksquirrel-libs/libkls_png.so
%{tde_libdir}/ksquirrel-libs/libkls_pnm.la
%{tde_libdir}/ksquirrel-libs/libkls_pnm.so
%{tde_libdir}/ksquirrel-libs/libkls_psd.la
%{tde_libdir}/ksquirrel-libs/libkls_psd.so
%{tde_libdir}/ksquirrel-libs/libkls_psp.la
%{tde_libdir}/ksquirrel-libs/libkls_psp.so
%{tde_libdir}/ksquirrel-libs/libkls_pxr.la
%{tde_libdir}/ksquirrel-libs/libkls_pxr.so
%{tde_libdir}/ksquirrel-libs/libkls_ras.la
%{tde_libdir}/ksquirrel-libs/libkls_ras.so
%{tde_libdir}/ksquirrel-libs/libkls_rawrgb.la
%{tde_libdir}/ksquirrel-libs/libkls_rawrgb.so
%{tde_libdir}/ksquirrel-libs/libkls_sct.la
%{tde_libdir}/ksquirrel-libs/libkls_sct.so
%{tde_libdir}/ksquirrel-libs/libkls_sgi.la
%{tde_libdir}/ksquirrel-libs/libkls_sgi.so
%{tde_libdir}/ksquirrel-libs/libkls_sun.la
%{tde_libdir}/ksquirrel-libs/libkls_sun.so
%{tde_libdir}/ksquirrel-libs/libkls_svg.la
%{tde_libdir}/ksquirrel-libs/libkls_svg.so
%{tde_libdir}/ksquirrel-libs/libkls_tga.la
%{tde_libdir}/ksquirrel-libs/libkls_tga.so
%{tde_libdir}/ksquirrel-libs/libkls_tiff.la
%{tde_libdir}/ksquirrel-libs/libkls_tiff.so
%{tde_libdir}/ksquirrel-libs/libkls_ttf.la
%{tde_libdir}/ksquirrel-libs/libkls_ttf.so
%{tde_libdir}/ksquirrel-libs/libkls_utah.la
%{tde_libdir}/ksquirrel-libs/libkls_utah.so
%{tde_libdir}/ksquirrel-libs/libkls_wal.la
%{tde_libdir}/ksquirrel-libs/libkls_wal.so
%{tde_libdir}/ksquirrel-libs/libkls_wbmp.la
%{tde_libdir}/ksquirrel-libs/libkls_wbmp.so
%{tde_libdir}/ksquirrel-libs/libkls_wmf.la
%{tde_libdir}/ksquirrel-libs/libkls_wmf.so
%{tde_libdir}/ksquirrel-libs/libkls_xbm.la
%{tde_libdir}/ksquirrel-libs/libkls_xbm.so
%{tde_libdir}/ksquirrel-libs/libkls_xcf.la
%{tde_libdir}/ksquirrel-libs/libkls_xcf.so
%{tde_libdir}/ksquirrel-libs/libkls_xcur.la
%{tde_libdir}/ksquirrel-libs/libkls_xcur.so
%{tde_libdir}/ksquirrel-libs/libkls_xim.la
%{tde_libdir}/ksquirrel-libs/libkls_xim.so
%{tde_libdir}/ksquirrel-libs/libkls_xpm.la
%{tde_libdir}/ksquirrel-libs/libkls_xpm.so
%{tde_libdir}/ksquirrel-libs/libkls_xwd.la
%{tde_libdir}/ksquirrel-libs/libkls_xwd.so
%{tde_libdir}/libksquirrel-libs-png.la
%{tde_libdir}/libksquirrel-libs-png.so
%{tde_libdir}/libksquirrel-libs.la
%{tde_libdir}/libksquirrel-libs.so
%{tde_libdir}/pkgconfig/ksquirrellibs.pc
%{tde_docdir}/ksquirrel-libs/

%files tools
%defattr(-,root,root,-)
%{tde_bindir}/ksquirrel-libs-camera2ppm
%{tde_bindir}/ksquirrel-libs-dcraw
%if 0%{?with_xmedcon}
%{tde_bindir}/ksquirrel-libs-dicom2png
%endif
%{tde_bindir}/ksquirrel-libs-fig2ppm
%{tde_bindir}/ksquirrel-libs-iff2ppm
%{tde_bindir}/ksquirrel-libs-leaf2ppm
%{tde_bindir}/ksquirrel-libs-ljpeg2ppm
%{tde_bindir}/ksquirrel-libs-ljpeg2ppm-s
%{tde_bindir}/ksquirrel-libs-mac2ppm
%{tde_bindir}/ksquirrel-libs-neo2ppm
%{tde_bindir}/ksquirrel-libs-pi12ppm
%{tde_bindir}/ksquirrel-libs-pi32ppm
%{tde_bindir}/ksquirrel-libs-svg2png
%{tde_bindir}/ksquirrel-libs-ttf2pnm
%{tde_bindir}/ksquirrel-libs-utah2ppm
%{tde_bindir}/ksquirrel-libs-xcf2pnm
%{tde_bindir}/ksquirrel-libs-xim2ppm


%Changelog
* Tue Oct 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.8.0-2
- Initial release for TDE 3.5.13.1
