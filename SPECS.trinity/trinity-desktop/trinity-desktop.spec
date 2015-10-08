#
# spec file for package trinity-desktop (version R14)
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

# Starting with TDE R14.0.0, TDE is not intended to run in RHEL4 and older.
# Minimum (oldest) distribution supported is RHEL5.

%if "%{?tde_version}" == ""
%define tde_version 14.0.0
%endif

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%define _docdir %{_datadir}/doc
%define tde_datadir %{tde_prefix}/share
%endif

Name:		trinity-desktop
Version:	%{tde_version}
Release:	1%{?dist}%{?_variant}
License:	GPL
Summary:	Meta-package to install TDE
Group:		User Interface/Desktops

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Source0:	trinity-3.5.13-fedora.repo
Source1:	trinity-3.5.13-rhel.repo
Source2:	RPM-GPG-KEY-trinity

Requires:	trinity-tdeaccessibility >= %{version}
Requires:	trinity-tdeaddons >= %{version}
Requires:	trinity-tdeadmin >= %{version}
Requires:	trinity-tdeartwork >= %{version}
Requires:	trinity-tdebase >= %{version}
Requires:	trinity-tdebindings >= %{version}
Requires:	trinity-tdeedu >= %{version}
Requires:	trinity-tdegames >= %{version}
Requires:	trinity-tdegraphics >= %{version}
Requires:	trinity-tdemultimedia >= %{version}
Requires:	trinity-tdenetwork >= %{version}
Requires:	trinity-tdepim >= %{version}
Requires:	trinity-tdeutils >= %{version}
Requires:	trinity-tdetoys >= %{version}

%if 0%{?rhel} || 0%{?fedora}
# YUM configuration file
Requires:	trinity-repo >= %{version}
%endif

%description
The TDE project aims to keep the KDE3.5 computing style alive, as well as 
polish off any rough edges that were present as of KDE 3.5.10. Along 
the way, new useful features will be added to keep the environment 
up-to-date.
Toward that end, significant new enhancements have already been made in 
areas such as display control, network connectivity, user 
authentication, and much more!

%files

##########

%package devel
Group:		User Interface/Desktops
Summary:	Meta-package to install TDE development tools

Obsoletes:	trinity-desktop-dev < %{version}-%{release}
Provides:	trinity-desktop-dev = %{version}-%{release}

Requires:	trinity-tdesdk >= %{version}
Requires:	trinity-tdevelop >= %{version}
Requires:	trinity-tdewebdev >= %{version}

%description devel
%{summary}

%files devel

##########

%package applications
Group:		User Interface/Desktops
Summary:	Meta-package to install all TDE applications

# Warning, k9copy requires ffmpeg
# Warning, tderadio requires libmp3lame

Requires: trinity-abakus
Requires: trinity-amarok
Requires: trinity-basket
Requires: trinity-bibletime
Requires: trinity-digikam
Requires: trinity-dolphin
Requires: trinity-filelight
Requires: trinity-gwenview
Requires: trinity-k3b
Requires: trinity-k9copy
Requires: trinity-kaffeine
Requires: trinity-kaffeine-mozilla
Requires: trinity-kasablanca
Requires: trinity-katapult
Requires: trinity-kbarcode
Requires: trinity-kbfx
Requires: trinity-kbibtex
Requires: trinity-kbiff
Requires: trinity-kbookreader
Requires: trinity-kchmviewer
Requires: trinity-kcmautostart
Requires: trinity-kcmldap
Requires: trinity-kcmldapcontroller
Requires: trinity-kcmldapmanager
Requires: trinity-kcpuload
Requires: trinity-kdbg
Requires: trinity-kdbusnotification
Requires: trinity-kdiff3
Requires: trinity-kdirstat
Requires: trinity-keep
Requires: trinity-kerberostray
Requires: trinity-kftpgrabber
Requires: trinity-kile
Requires: trinity-kima
Requires: trinity-kiosktool
Requires: trinity-kkbswitch
Requires: trinity-klcddimmer
Requires: trinity-kmplayer
Requires: trinity-kmyfirewall
Requires: trinity-kmymoney
Requires: trinity-knemo
Requires: trinity-knetload
Requires: trinity-knetstats
Requires: trinity-knights
Requires: trinity-knowit
Requires: trinity-knmap
Requires: trinity-knutclient
Requires: trinity-koffice-suite
Requires: trinity-konversation
Requires: trinity-kopete-otr
Requires: trinity-kpicosim
Requires: trinity-krecipes
Requires: trinity-krename
Requires: trinity-krusader
Requires: trinity-kscope
Requires: trinity-ksensors
Requires: trinity-ksplash-engine-moodin
Requires: trinity-ksquirrel
Requires: trinity-kshowmail
Requires: trinity-kshutdown
Requires: trinity-kstreamripper
Requires: trinity-ksystemlog
Requires: trinity-ktechlab
Requires: trinity-ktorrent
Requires: trinity-kuickshow
Requires: trinity-kvirc
Requires: trinity-kvkbd
Requires: trinity-kvpnc
Requires: trinity-mplayerthumbs
Requires: trinity-piklab
Requires: trinity-potracegui
Requires: trinity-smb4k
Requires: trinity-smartcardauth
Requires: trinity-soundkonverter
Requires: trinity-tde-guidance
Requires: trinity-tde-style-lipstik
Requires: trinity-tde-style-qtcurve
Requires: trinity-tde-systemsettings
Requires: trinity-tdeio-apt
Requires: trinity-tdeio-ftps
Requires: trinity-tdeio-locate
Requires: trinity-tdeio-sword
Requires: trinity-tdeio-umountwrapper
Requires: trinity-tderadio
Requires: trinity-tdesvn
Requires: trinity-tdmtheme
Requires: trinity-tellico
Requires: trinity-tork
Requires: trinity-twin-style-crystal
Requires: trinity-wlassistant
Requires: trinity-yakuake

# PCLinuxOS does not have sudo ...
%if 0%{?pclinuxos} == 0
Requires: trinity-tdesudo
%endif

# RHEL5: pilot library is too old
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
Requires: trinity-kpilot
%endif

# Network management
# RHEL 6 and openSUSE 11.x: knetworkmanager8
%if 0%{?suse_version} && 0%{?suse_version} <= 1140 || 0%{?rhel} == 6
Requires: trinity-knetworkmanager
%endif
# Other distros use tdenetworkmanager (since R14)
%if 0%{?rhel} >= 7 || 0%{?suse_version} >= 1210 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?pclinuxos} || 0%{?fedora}
Requires: trinity-tdenetworkmanager
Obsoletes: trinity-knetworkmanager
Obsoletes: trinity-knetworkmanager8
%endif

# Power management
Obsoletes: trinity-tde-guidance-powermanager
Requires: trinity-tdepowersave

# Decoration-related stuff (not installed by default)
#Requires: trinity-kgtk-qt3
#Requires: trinity-gtk-qt-engine
#Requires: trinity-gtk3-tqt-engine
#Requires: trinity-qt4-tqt-theme-engine

# On RHEL 5/7, lilypond is not available, so no rosegarden :'-(
%if 0%{?rhel} == 5 || 0%{?rhel} == 7
%else
Requires: trinity-rosegarden
%endif

# Compiz-related stuff does not work (obsolete)
#Requires: trinity-compizconfig-backend-kconfig
#Requires: trinity-desktop-effects-kde
#Requires: trinity-fusion-icon

# Useless l10n package
#Requires: trinity-filelight-l10n

# Not even an RPM package ...
#Requires: trinity-konstruct

# Debian/Ubuntu specific ...
#Requires: trinity-adept

#Requires: trinity-gwenview-i18n

# Beagle does not exist anymore, so Kerry is now useless.
#Requires: trinity-kerry

%description applications
%{summary}

%files  applications

##########

%package extras
Group:		User Interface/Desktops
Summary:	Meta-package to install all extras (unofficial) TDE packages

Requires:	trinity-akode
#Requires:	trinity-kdebluetooth
#Requires:	trinity-kcheckgmail
Requires:	trinity-icons-crystalsvg-updated
Requires:	trinity-icons-kfaenza
Requires:	trinity-icons-oxygen
Requires:	trinity-kickoff-i18n
#Requires:	trinity-knoda
Requires:	trinity-style-ia-ora
#Requires:	trinity-tdeio-sysinfo-plugin
Requires:	trinity-theme-baghira


# GLIBC too old on RHEL <= 5
%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?fedora} || 0%{?suse_version} || 0%{?rhel} >= 6
#Requires:	trinity-twinkle
%endif

%description extras
%{summary}

%files extras

##########

%package all
Group:		User Interface/Desktops
Summary:	Meta-package to install all TDE packages

Requires:	%{name} = %{version}
Requires:	%{name}-applications = %{version}
Requires:	%{name}-devel = %{version}
#Requires:	%{name}-extras = %{version}

%description all
%{summary}

%files all

##########

%if 0%{?rhel} || 0%{?fedora}
%package -n trinity-repo
Group:		User Interface/Desktops
Summary:	Yum configuration files for Trinity
Requires(pre):	coreutils

%description -n trinity-repo
%{summary}

%pre -n trinity-repo
# Make sure every Trinity related repository is deleted before installing new one.
%__rm -f %{_sysconfdir}/yum.repos.d/trinity-*.repo

%files -n trinity-repo
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/*.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-trinity
%endif

##########

%prep

%build

%install
%__rm -rf %{?buildroot}
%__mkdir_p "%{?buildroot}%{_sysconfdir}/yum.repos.d"

# FEDORA configuration for YUM
%if 0%{?fedora}
%__sed %{SOURCE0} \
  -e 's/\$releasever/%{fedora}/g' \
  -e 's/-fedora/-f%{fedora}/g' \
  >"%{?buildroot}%{_sysconfdir}/yum.repos.d/trinity.repo"
%endif

# RHEL configuration for YUM
# $releasever is replaced with its value
%if 0%{?rhel}
%__sed %{SOURCE1} \
  -e 's/\$releasever/%{rhel}/g' \
  >"%{?buildroot}%{_sysconfdir}/yum.repos.d/trinity.repo"
%endif

%if 0%{?fedora} || 0%{?rhel}
%__sed -i %{?buildroot}%{_sysconfdir}/yum.repos.d/*.repo -e "s|3.5.13|r14|g"
%__chmod 644 %{?buildroot}%{_sysconfdir}/yum.repos.d/*.repo
%endif

# RPM signing key
%if 0%{?rhel} || 0%{?fedora}
%__install -D -m 644 "%{SOURCE2}" "%{?buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-trinity"
%endif


%changelog
* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 14.0.0-1
- Initial build for TDE R14
