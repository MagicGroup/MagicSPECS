# Default version for this component
%define kdecomp kde-style-qtcurve
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


Name:		trinity-style-qtcurve
Summary:	This is a set of widget styles for Trinity based apps
Version:	0.55.2
Release:	5%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

Obsoletes:		trinity-kde-style-qtcurve
Provides:		trinity-kde-style-qtcurve

%description
This package together with gtk2-engines-qtcurve aim to provide a unified look
and feel on the desktop when using TDE and Gnome applications.

This package is most useful when installed together with 
gtk2-engines-qtcurve.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake
# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "CMakeLists.txt" \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|/usr/bin/uic-tqt|%{tde_bindir}/uic-tqt|g" \
  -e "s|/usr/bin/tmoc|%{tde_bindir}/tmoc|g"


%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"

export CXXFLAGS="-I${QTINC} -I%{tde_tdeincludedir} ${CXXFLAGS}"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_PREFIX_PATH=%{tde_prefix} \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
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

%find_lang qtcurve


%clean
%__rm -rf %{buildroot}



%files -f qtcurve.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_tdelibdir}/kstyle_qtcurve_config.la
%{tde_tdelibdir}/kstyle_qtcurve_config.so
%{tde_tdelibdir}/plugins/styles/qtcurve.so
%{tde_tdelibdir}/plugins/styles/qtcurve.la
%{tde_datadir}/apps/kdisplay/color-schemes/QtCurve.kcsrc
%{tde_datadir}/apps/kstyle/themes/qtcurve.themerc
%{tde_datadir}/apps/QtCurve/*.qtcurve


%changelog
* Wed Jul 31 2013 Liu Di <liudidi@gmail.com> - 0.55.2-5.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.55.2-4
- Initial build for TDE 3.5.13.1

* Sun Sep 09 2012 Francois Andriot <francois.andriot@free.fr> - 0.55.2-3
- Switch to v3.5.13-sru branch

* Tue May 01 2012 Francois Andriot <francois.andriot@free.fr> - 0.55.2-2
- Rebuilt for Fedora 17
- Removes post and postun

* Sat Nov 19 2011 Francois Andriot <francois.andriot@free.fr> - 0.55.2-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
