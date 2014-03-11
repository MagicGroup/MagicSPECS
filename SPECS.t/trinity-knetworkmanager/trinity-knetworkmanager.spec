# Default version for this component
%define kdecomp knetworkmanager
%if 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion}
%define version 0.9
%else
%define version 0.8
%endif

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


Name:			trinity-%{kdecomp}
Version:		%{?version}
Release:	4%{?dist}%{?_variant}

Summary:        Trinity applet for Network Manager

Group:          Applications/Internet
License:        GPLv2+
URL:            http://en.opensuse.org/Projects/KNetworkManager

%if "%{?version}" == "0.9"
Source0:		%{kdecomp}9-3.5.13.tar.gz
%else
Source0:		%{kdecomp}8-3.5.13.tar.gz
%endif

Patch0:			knetworkmanager-3.5.13-missing_includes.patch

# For knetworkmanager 0.9 only !
Patch10:		knetworkmanager-3.5.13-subdir_version.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Requires:       kde-filesystem
BuildRequires:  desktop-file-utils

%if 0%{?rhel} || 0%{?fedora}
Requires:       NetworkManager-gnome
%else
Requires:       networkmanager
%endif

BuildRequires:	dbus-1-tqt-devel
BuildRequires:	dbus-tqt-devel
BuildRequires:	NetworkManager-glib-devel

%description
KNetworkManager is a system tray applet for controlling network
connections on systems that use the NetworkManager daemon.


%package devel
Summary:        Common data shared among the MySQL GUI Suites
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for knetworkmanager


%if 0%{?suse_version}
%debug_package
%endif


%prep 
%if "%{?version}" == "0.9"
%setup -q -n %{kdecomp}-3.5.13.19
%else
%setup -q -n applications/knetworkmanager8
%endif

%if "%{?version}" == "0.9"
%patch10 -p1
%endif

cd knetworkmanager-0.*/src
%patch0 -p3



%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export CMAKE_INCLUDE_PATH="%{tde_includedir}:%{tde_includedir}/tqt"
export LD_LIBRARY_PATH="%{tde_libdir}"

# Missing TDE macros
%__mkdir_p cmake
%__ln_s %{tde_datadir}/cmake cmake/modules

%if 0%{?rhel} || 0%{?fedora}
%__mkdir_p build
cd build
%endif

%cmake \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DCMAKE_SKIP_RPATH="OFF" \
  ..
  
%__make %{?_smp_mflags} 

%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=%{?buildroot} -C build


%clean
%__rm -rf $RPM_BUILD_ROOT


%post
update-desktop-database %{tde_appdir} > /dev/null
/sbin/ldconfig
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_appdir} > /dev/null
/sbin/ldconfig
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

%files 
%defattr(-,root,root,-)
%{tde_bindir}/knetworkmanager
%{tde_libdir}/*.la
%{tde_libdir}/*.so
%{_sysconfdir}/dbus-1/system.d/knetworkmanager.conf
%{tde_tdeappdir}/knetworkmanager.desktop
%{tde_datadir}/apps/knetworkmanager
%{tde_datadir}/icons/hicolor/*/apps/knetworkmanager*
%{tde_datadir}/servicetypes/knetworkmanager_plugin.desktop
%{tde_datadir}/servicetypes/knetworkmanager_vpnplugin.desktop


%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/*.h
%{tde_tdelibdir}/*.la
%{tde_tdelibdir}/*.so

%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - %{?version}-4
- Initial build for TDE 3.5.13.1

* Wed May 02 2012 Francois Andriot <francois.andriot@free.fr> - 0.8-3 / 0.9-3
- Rebuild for Fedora 17

* Sat Nov 13 2011 Francois Andriot <francois.andriot@free.fr> - 0.8-2 / 0.9-2
- Remove faulty patch for WPA authentication

* Tue Nov 11 2011 Francois Andriot <francois.andriot@free.fr> - 0.8-1 / 0.9-1
- Initial build
