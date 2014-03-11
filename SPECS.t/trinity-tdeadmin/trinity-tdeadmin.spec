# Avoids relinking, which breaks consolehelper
%define dont_relink 1

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_sbindir %{tde_prefix}/sbin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Name:			trinity-tdeadmin
Summary:		Administrative tools for TDE
Version:		3.5.13.2
Release:		1%{?dist}%{?_variant}

License:		GPLv2
Group:			User Interface/Desktops
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
URL:			http://www.trinitydesktop.org/

Prefix:			%{tde_prefix}

Obsoletes:		trinity-kdeadmin < %{version}-%{release}
Provides:		trinity-kdeadmin = %{version}-%{release}

Source0: kdeadmin-trinity-%{version}.tar.xz
Source1: kuser.pam
Source2: kuser.pamd
Source5: kpackagerc
Source6: ksysvrc
Source7: kuserrc

BuildRequires: autoconf automake libtool m4
BuildRequires: trinity-tqtinterface-devel >= %{version}
BuildRequires: trinity-arts-devel >= %{version}
BuildRequires: trinity-tdelibs-devel >= %{version}
BuildRequires: rpm-devel
BuildRequires: pam-devel
%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
BuildRequires:	lilo
%endif

Requires: trinity-tdeadmin = %{version}-%{release}
Requires: trinity-kcron = %{version}-%{release}
Requires: trinity-kdat = %{version}-%{release}
Requires: %{name}-kfile-plugins = %{version}-%{release}
Requires: trinity-knetworkconf = %{version}-%{release}
Requires: trinity-kpackage = %{version}-%{release}
Requires: trinity-ksysv = %{version}-%{release}
Requires: trinity-kuser = %{version}-%{release}
%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
Requires: trinity-lilo-config = %{version}-%{release}
%endif


%description
The tdeadmin package includes administrative tools for the Trinity Desktop
Environment (TDE) including:
kcron, kdat, knetworkconf, kpackage, ksysv, kuser.

%files
%defattr(-,root,root,-)
# LILO is not provided in RHEL or Fedora
%if 0%{?rhel} || 0%{?fedora}
%exclude %{tde_tdedocdir}/HTML/en/lilo-config/
%endif

##########

%package -n trinity-kcron
Summary:	The Trinity crontab editor
Group:		Applications/Utilities

%description -n trinity-kcron
KCron is an application for scheduling programs to run in the background.
It is a graphical user interface to cron, the UNIX system scheduler.

%files -n trinity-kcron
%defattr(-,root,root,-)
%{tde_bindir}/kcron
%{tde_tdeappdir}/kcron.desktop
%{tde_datadir}/apps/kcron/kcronui.rc
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
Group:		Applications/Utilities

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
Group:		Environment/Libraries

%description kfile-plugins
File metainfo plugins for deb and rpm package files.

%files kfile-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/kfile_deb.la
%{tde_tdelibdir}/kfile_deb.so
%{tde_tdelibdir}/kfile_rpm.la
%{tde_tdelibdir}/kfile_rpm.so
%{tde_datadir}/services/kfile_deb.desktop
%{tde_datadir}/services/kfile_rpm.desktop

##########

%package -n trinity-knetworkconf
Summary:	Trinity network configuration tool
Group:		Applications/Utilities

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
Group:		Applications/Utilities

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
%{tde_datadir}/config/kpackagerc
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
Group:		Applications/Utilities

%description -n trinity-ksysv
This program allows you to edit your start and stop scripts using a
drag and drop GUI.

%files -n trinity-ksysv
%defattr(-,root,root,-)
%doc rpmdocs/ksysv/*
%{tde_bindir}/ksysv
%{tde_tdeappdir}/ksysv.desktop
%{tde_datadir}/apps/ksysv/
%{tde_datadir}/config/ksysvrc
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
Group:		Applications/Utilities
# package 'usermode' provides '/usr/bin/consolehelper-gtk'
%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
Requires:	usermode-gtk
%else
Requires:	usermode
%endif

%description -n trinity-kuser
A user/group administration tool for TDE.

%files -n trinity-kuser
%defattr(-,root,root,-)
%doc rpmdocs/kuser/*
%{_sbindir}/kuser
%{tde_bindir}/kuser
%{tde_sbindir}/kuser
%{tde_tdeappdir}/kuser.desktop
%{tde_datadir}/apps/kuser/
%{tde_datadir}/config/kuserrc
%{tde_datadir}/config.kcfg/kuser.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kuser.png
%{tde_tdedocdir}/HTML/en/kuser/
%config(noreplace) /etc/pam.d/kuser
%config(noreplace) /etc/security/console.apps/kuser

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

%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
%package -n trinity-lilo-config
Summary:	Trinity frontend for lilo configuration
Group:		Applications/Utilities
Requires:	trinity-kcontrol
Requires:	trinity-tdebase-bin
#Requires:	lilo

%description -n trinity-lilo-config
lilo-config is a TDE based frontend to the lilo boot manager configuration.
It runs out of the TDE Control Center.

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

%if 0%{?suse_version}
%debug_package
%endif

##########

%prep
%setup -q -n kdeadmin-trinity-%{version}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
   --prefix=%{tde_prefix} \
   --exec-prefix=%{tde_prefix} \
   --bindir=%{tde_bindir} \
   --sbindir=%{tde_sbindir} \
   --libdir=%{tde_libdir} \
   --datadir=%{tde_datadir} \
   --docdir=%{tde_docdir} \
   --includedir=%{tde_tdeincludedir} \
   --enable-new-ldflags \
   --disable-dependency-tracking \
   --disable-rpath \
   --with-rpm \
   --with-pam=kde \
   --with-shadow \
   --with-private-groups \
   --enable-final \
   --enable-closure \
   --with-private-groups \
   --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags}

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

%__install -p -m644 %{SOURCE5} %{SOURCE6} %{SOURCE7} %{buildroot}%{tde_datadir}/config/

# Run kuser through consolehelper
%__install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/security/console.apps/kuser
%__install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/kuser
%__mv %{buildroot}%{tde_bindir}/kuser %{buildroot}%{tde_sbindir}
%__ln_s %{_bindir}/consolehelper %{buildroot}%{tde_bindir}/kuser
%if "%{tde_prefix}" != "/usr"
%__ln_s %{tde_sbindir}/kuser %{?buildroot}%{_sbindir}/kuser
%endif

# locale's
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}/$HTML_DIR ]; then
for lang_dir in %{buildroot}/$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && ln -nsf ../common $i/common
      done
    popd
  fi
done
fi

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



%clean
%__rm -rf %{buildroot}



%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
