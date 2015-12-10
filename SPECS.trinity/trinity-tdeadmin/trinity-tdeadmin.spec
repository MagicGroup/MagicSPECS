#
# spec file for package tdeadmin (version R14)
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

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg tdeadmin
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_sbindir %{tde_prefix}/sbin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_sbindir %{tde_prefix}/sbin
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:		trinity-%{tde_pkg}
Summary:	Administrative tools for TDE
Version:	%{tde_version}
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Group:		System/GUI/Other
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz
Source1:		kuser.pam
Source2:		kuser.pamd
Source5:		kpackagerc
Source6:		ksysvrc
Source7:		kuserrc
Patch1:			trinity-tdeadmin-14.0.1-tqt.patch

Obsoletes:		trinity-kdeadmin < %{version}-%{release}
Provides:		trinity-kdeadmin = %{version}-%{release}

BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	fdupes
BuildRequires:	gcc-c++

# RPM support
BuildRequires: rpm-devel

# PAM support
BuildRequires: pam-devel

# LILO support
%if 0%{?with_lilo}
BuildRequires:	lilo
%endif

Requires: trinity-kcron = %{version}-%{release}
Requires: trinity-kdat = %{version}-%{release}
Requires: %{name}-kfile-plugins = %{version}-%{release}
Requires: trinity-knetworkconf = %{version}-%{release}
Requires: trinity-kpackage = %{version}-%{release}
Requires: trinity-ksysv = %{version}-%{release}
Requires: trinity-kuser = %{version}-%{release}
%if 0%{?with_lilo}
Requires: trinity-lilo-config = %{version}-%{release}
%else
Obsoletes: trinity-lilo-config
%endif

# CONSOLEHELPER (usermode) support
%define with_consolehelper 1

# Avoids relinking, which breaks consolehelper
%define dont_relink 1

%description
The tdeadmin package includes administrative tools for the Trinity Desktop
Environment (TDE) including:
kcron, kdat, knetworkconf, kpackage, ksysv, kuser.

%files
%defattr(-,root,root,-)

##########

%package -n trinity-kcron
Summary:	The Trinity crontab editor
Group:		System/GUI/Other

%description -n trinity-kcron
KCron is an application for scheduling programs to run in the background.
It is a graphical user interface to cron, the UNIX system scheduler.

%files -n trinity-kcron
%defattr(-,root,root,-)
%{tde_bindir}/kcron
%{tde_tdeappdir}/kcron.desktop
%{tde_datadir}/apps/kcron/
%{tde_datadir}/icons/hicolor/*/apps/kcron.png
%{tde_tdedocdir}/HTML/en/kcron/

%post -n trinity-kcron
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kcron
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kdat
Summary:	A Trinity tape backup tool
Group:		System/GUI/Other

%description -n trinity-kdat
KDat is a tar-based tape archiver. It is designed to work with multiple
archives on a single tape.

Main features are:
* Simple graphical interface to local filesystem and tape contents.
* Multiple archives on the same physical tape.
* Complete index of archives and files is stored on local hard disk.
* Selective restore of files from an archive.
* Backup profiles for frequently used backups.

%files -n trinity-kdat
%defattr(-,root,root,-)
%doc rpmdocs/kdat/*
%{tde_bindir}/kdat
%{tde_tdeappdir}/kdat.desktop
%{tde_datadir}/apps/kdat/
%{tde_datadir}/icons/hicolor/*/apps/kdat.png
%{tde_datadir}/icons/locolor/*/apps/kdat.png
%{tde_tdedocdir}/HTML/en/kdat/

%post -n trinity-kdat
for icon_theme in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kdat
for icon_theme in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package kfile-plugins
Summary:	Trinity file metainfo plugins for deb and rpm files
Group:		System/GUI/Other

%description kfile-plugins
This package contains the Trinity File metainfo plugins for deb and rpm
package files.

%files kfile-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/tdefile_deb.la
%{tde_tdelibdir}/tdefile_deb.so
%{tde_tdelibdir}/tdefile_rpm.la
%{tde_tdelibdir}/tdefile_rpm.so
%{tde_datadir}/services/tdefile_deb.desktop
%{tde_datadir}/services/tdefile_rpm.desktop

##########

%package -n trinity-knetworkconf
Summary:	Trinity network configuration tool
Group:		System/GUI/Other

%description -n trinity-knetworkconf
This is a TDE control center module to configure TCP/IP settings.  It
can be used to manage network devices and settings for each device.

%files -n trinity-knetworkconf
%defattr(-,root,root,-)
%doc rpmdocs/knetworkconf/*
%{tde_datadir}/icons/hicolor/*/apps/knetworkconf.png
%{tde_datadir}/icons/hicolor/22x22/actions/network_disconnected_wlan.png
%{tde_datadir}/icons/hicolor/22x22/actions/network_connected_lan_knc.png
%{tde_datadir}/icons/hicolor/22x22/actions/network_disconnected_lan.png
%{tde_datadir}/icons/hicolor/22x22/actions/network_traffic_wlan.png
%{tde_datadir}/apps/knetworkconf/
%{tde_tdeappdir}/kcm_knetworkconfmodule.desktop
%{tde_tdelibdir}/kcm_knetworkconfmodule.so
%{tde_tdelibdir}/kcm_knetworkconfmodule.la
%{tde_tdedocdir}/HTML/en/knetworkconf/

%post -n trinity-knetworkconf
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

%postun -n trinity-knetworkconf
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done

##########

%package -n trinity-kpackage
Summary:	Trinity package management tool
Group:		System/GUI/Other

%description -n trinity-kpackage
This is a frontend to both .rpm and .deb package formats. It allows you
to view currently installed packages, browse available packages, and
install/remove them.

%files -n trinity-kpackage
%defattr(-,root,root,-)
%doc rpmdocs/kpackage/*
%{tde_bindir}/kpackage
%{tde_tdeappdir}/kpackage.desktop
%{tde_datadir}/apps/kpackage/
%{tde_confdir}/kpackagerc
%{tde_datadir}/icons/hicolor/*/apps/kpackage.png
%{tde_tdedocdir}/HTML/en/kpackage/

%post -n trinity-kpackage
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kpackage
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-ksysv
Summary:	Trinity SysV-style init configuration editor
Group:		System/GUI/Other

%description -n trinity-ksysv
This program allows you to edit your start and stop scripts using a
drag and drop GUI.

%files -n trinity-ksysv
%defattr(-,root,root,-)
%doc rpmdocs/ksysv/*
%{tde_bindir}/ksysv
%{tde_tdeappdir}/ksysv.desktop
%{tde_datadir}/apps/ksysv/
%{tde_confdir}/ksysvrc
%{tde_datadir}/icons/crystalsvg/16x16/actions/toggle_log.png
%{tde_datadir}/icons/hicolor/*/apps/ksysv.png
%{tde_datadir}/mimelnk/application/x-ksysv.desktop
%{tde_datadir}/mimelnk/text/x-ksysv-log.desktop
%{tde_tdedocdir}/HTML/en/ksysv/

%post -n trinity-ksysv
for icon_theme in crystalsvg hicolor  ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-ksysv
for icon_theme in crystalsvg hicolor  ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%package -n trinity-kuser
Summary:	Trinity user/group administration tool
Group:		System/GUI/Other

%if 0%{?with_consolehelper}
# package 'usermode' provides '/usr/bin/consolehelper-gtk'
%if 0%{?rhel} || 0%{?fedora}
Requires:	usermode-gtk
%endif
%if 0%{?mgaversion} || 0%{?mdkversion}
Requires:	usermode
%endif
%endif

%description -n trinity-kuser
A user/group administration tool for TDE.

%files -n trinity-kuser
%defattr(-,root,root,-)
%doc rpmdocs/kuser/*
%{tde_bindir}/kuser
%{tde_tdeappdir}/kuser.desktop
%{tde_datadir}/apps/kuser/
%{tde_confdir}/kuserrc
%{tde_datadir}/config.kcfg/kuser.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kuser.png
%{tde_tdedocdir}/HTML/en/kuser/

%if 0%{?with_consolehelper}
%{tde_sbindir}/kuser
%{_sbindir}/kuser
%config(noreplace) /etc/pam.d/kuser
%config(noreplace) /etc/security/console.apps/kuser
%endif

%post -n trinity-kuser
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

%postun -n trinity-kuser
for icon_theme in hicolor ; do
  touch --no-create %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{tde_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database %{tde_datadir}/applications > /dev/null 2>&1 || :

##########

%if 0%{?with_lilo}
%package -n trinity-lilo-config
Summary:	Trinity frontend for lilo configuration
Group:		System/GUI/Other
Requires:	trinity-kcontrol
Requires:	trinity-tdebase-bin
#Requires:	lilo

%description -n trinity-lilo-config
lilo-config is a TDE based frontend to the lilo boot manager configuration.
It runs out of the Trinity Control Center.

If you want to use the menu entry to launch lilo-config, you need to install
tdebase-bin since it uses the tdesu command to gain root privileges.

%files -n trinity-lilo-config
%defattr(-,root,root,-)
%{tde_tdelibdir}/kcm_lilo.la
%{tde_tdelibdir}/kcm_lilo.so
%{tde_tdeappdir}/lilo.desktop
%{tde_tdedocdir}/HTML/en/lilo-config/

%post -n trinity-lilo-config
touch /etc/lilo.conf
%endif

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTLIB QTINC
export PATH="%{tde_bindir}:${PATH}"
export kde_confdir="%{tde_confdir}"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --sbindir=%{tde_sbindir} \
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
  --disable-gcc-hidden-visibility \
  \
  --with-rpm \
  --with-pam=kde \
  --with-shadow \
  --with-private-groups

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

comps="kcron kdat knetworkconf kpackage ksysv kuser"
%__mkdir_p	%{buildroot}%{tde_datadir}/config \
			%{buildroot}%{_sysconfdir}/security/console.apps \
			%{buildroot}%{_sysconfdir}/pam.d \
			%{buildroot}%{tde_sbindir} \
			%{buildroot}%{_sbindir}

%__mkdir_p "%{buildroot}%{tde_confdir}/"
%__install -p -m644 %{SOURCE5} %{SOURCE6} %{SOURCE7} "%{buildroot}%{tde_confdir}/"

%if 0%{?with_consolehelper}
# Run kuser through consolehelper
%__install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/security/console.apps/kuser
%__install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/kuser
%__mv %{buildroot}%{tde_bindir}/kuser %{buildroot}%{tde_sbindir}
%__ln_s %{_bindir}/consolehelper %{buildroot}%{tde_bindir}/kuser
%if "%{tde_prefix}" != "/usr"
%__ln_s %{tde_sbindir}/kuser %{?buildroot}%{_sbindir}/kuser
%endif
%endif

# rpmdocs
for dir in $comps ; do
  for file in AUTHORS ChangeLog README TODO ; do
    test -s  "$dir/$file" && install -p -m644 -D "$dir/$file" "rpmdocs/$dir/$file"
  done
done

# The following files are not installed in any binary package.
# This is deliberate.

# - This file serves no purpose that we can see, and conflicts
#   with GNOME system tools, so be sure to leave it out.
%__rm -f %{?buildroot}%{tde_libdir}/pkgconfig/*.pc

# Extract from changelog:
# tdeadmin (4:3.5.5-2) unstable; urgency=low
#  +++ Changes by Ana Beatriz Guerrero Lopez:
#  * Removed useless program secpolicy. (Closes: #399426)
%__rm -f %{?buildroot}%{tde_bindir}/secpolicy

# Remove lilo related files, if unwanted.
%if 0%{?with_lilo} == 0
%__rm -rf %{?buildroot}%{tde_tdedocdir}/HTML/en/lilo-config/
%__rm -f %{?buildroot}%{tde_tdelibdir}/kcm_lilo.la
%__rm -f %{?buildroot}%{tde_tdelibdir}/kcm_lilo.so
%__rm -f %{?buildroot}%{tde_tdeappdir}/lilo.desktop
%endif

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file kdat     System Backup
%suse_update_desktop_file kpackage System PackageManager
%suse_update_desktop_file kcron    System ServiceConfiguration
%suse_update_desktop_file ksysv    System ServiceConfiguration
%suse_update_desktop_file kuser    System SystemSetup
%endif

# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"


%clean
%__rm -rf %{buildroot}


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial release for TDE R14.0.0
