# Default version for this component
%define kdecomp wlassistant
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

%define _docdir %{tde_tdedocdir}


Name:		trinity-%{kdecomp}
Summary:	User friendly KDE frontend for wireless network connection [Trinity]
Version:	0.5.7
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/Utilities

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://wlassistant.sourceforge.net/

Prefix:    %{tde_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	python
BuildRequires:	cmake >= 2.8

%description
Wireless Assistant scans for wireless access points and displays link quality,
encryption and other useful information. When user wants to connect to a
network, Wireless Assistant opens up its wizards and guides the user through
Wi-Fi settings. After a successful connection is made the settings are
remembered so next time the user won't have to enter them again.


%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"


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
  -DBUILD_ALL=on \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} -C build

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc ChangeLog VERSION
%{tde_bindir}/wlassistant
%{tde_tdeappdir}/wlassistant.desktop
%{tde_datadir}/icons/hicolor/16x16/apps/wlassistant.png
%{tde_datadir}/icons/hicolor/32x32/apps/wlassistant.png
%lang(ar) %{tde_datadir}/locale/ar/LC_MESSAGES/wlassistant.mo
%lang(ca) %{tde_datadir}/locale/ca/LC_MESSAGES/wlassistant.mo
%lang(es) %{tde_datadir}/locale/es/LC_MESSAGES/wlassistant.mo
%lang(fr) %{tde_datadir}/locale/fr/LC_MESSAGES/wlassistant.mo
%lang(nb) %{tde_datadir}/locale/nb/LC_MESSAGES/wlassistant.mo
%lang(pl) %{tde_datadir}/locale/pl/LC_MESSAGES/wlassistant.mo
%lang(pt) %{tde_datadir}/locale/pt_BR/LC_MESSAGES/wlassistant.mo
%lang(sv) %{tde_datadir}/locale/sv/LC_MESSAGES/wlassistant.mo
%lang(zh_CN) %{tde_datadir}/locale/zh_CN/LC_MESSAGES/wlassistant.mo
%lang(zh_TW) %{tde_datadir}/locale/zh_TW/LC_MESSAGES/wlassistant.mo


%changelog
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 0.5.7-3.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 0.5.7-2
- Initial build for TDE 3.5.13.1

* Tue Nov 29 2011 Francois Andriot <francois.andriot@free.fr> - 0.5.7-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16
