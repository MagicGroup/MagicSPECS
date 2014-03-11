# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%define _docdir %{_datadir}/doc
%define tde_datadir %{tde_prefix}/share
%endif

Name:		trinity-desktop
Version:	3.5.13.2
Release:	2%{?dist}%{?_variant}
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

Source11:	pclinuxos201304-32.jpg
Source12:	pclinuxos201304-64.jpg

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
Requires:	hal

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

# Some applications are disabled for now ...
# Compiz-related stuff does not work (obsolete)
#Requires: trinity-compizconfig-backend-kconfig
#Requires: trinity-desktop-effects-kde
#Requires: trinity-fusion-icon

# Obsolete l10n package
#Requires: trinity-filelight-l10n

# Not even an RPM package ...
#Requires: trinity-konstruct

# Debian/Ubuntu specific ...
#Requires: trinity-adept

# Future R14 packages
#Requires: trinity-kvpnc
#Requires: trinity-qt4-tqt-theme-engine

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
Requires: trinity-gwenview-i18n
Requires: trinity-k3b
Requires: trinity-katapult
Requires: trinity-kbarcode
Requires: trinity-kbfx
Requires: trinity-kbookreader
Requires: trinity-kchmviewer
Requires: trinity-kcpuload
Requires: trinity-k9copy
Requires: trinity-kdiff3
Requires: trinity-kdirstat
Requires: trinity-keep
Requires: trinity-kile
Requires: trinity-kiosktool
Requires: trinity-kmyfirewall
Requires: trinity-kmymoney
Requires: trinity-knemo
Requires: trinity-knetload
Requires: trinity-knetstats
Requires: trinity-knights
Requires: trinity-knowit
Requires: trinity-knutclient
Requires: trinity-koffice-suite
Requires: trinity-konversation
Requires: trinity-kpicosim
Requires: trinity-krename
Requires: trinity-krusader
Requires: trinity-ksplash-engine-moodin
Requires: trinity-ksquirrel
Requires: trinity-kstreamripper
Requires: trinity-ksystemlog
Requires: trinity-ktechlab
Requires: trinity-ktorrent
Requires: trinity-kuickshow
Requires: trinity-kvirc
Requires: trinity-kvkbd
Requires: trinity-twin-style-crystal
Requires: trinity-piklab
Requires: trinity-potracegui
Requires: trinity-smb4k
Requires: trinity-smartcardauth
Requires: trinity-soundkonverter
Requires: trinity-tde-guidance
Requires: trinity-tde-guidance-powermanager
Requires: trinity-tde-style-lipstik
Requires: trinity-tde-style-qtcurve
Requires: trinity-tde-systemsettings
Requires: trinity-tdeio-apt
Requires: trinity-tdeio-locate
Requires: trinity-tdeio-umountwrapper
Requires: trinity-tderadio
Requires: trinity-tdesudo
Requires: trinity-tdmtheme
Requires: trinity-tellico
Requires: trinity-wlassistant
Requires: trinity-yakuake


# Disabled applications for RHEL5
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
# On RHEL 5, HAL version is too old for kpowersave .
Requires: trinity-kpowersave
# On RHEL 5, GTK2 version is too old for GTK stuff ...
Requires: trinity-gtk-qt-engine
# On RHEL 5, lilypond is not available, so no rosegarden :'-(
Requires: trinity-rosegarden
# RHEL5: kpilot library is too old
Requires: trinity-kpilot
%endif

# This one causes several crashes . Obsolete.
#Requires: trinity-kgtk-qt3
Obsoletes: trinity-kgtk-qt3

# OBSOLETE: beagle does not exist anymore. Kerry is now useless.
# RHEL, openSUSE 12: no Beagle library
Obsoletes: trinity-kerry

# RHEL 6 only: knetworkmanager8
#  knetworkmanager9 is too unstable for now.
%if 0%{?rhel} == 6
Requires: trinity-knetworkmanager
%endif

# RHEL 4
%if 0%{?rhel} >= 5 || 0%{?fedora} >= 15 || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?suse_version}
# HAL is too old
Requires: trinity-kima
Requires: trinity-kaffeine
Requires: trinity-kaffeine-mozilla
Requires: trinity-kmplayer
# No OTR support
Requires: trinity-kopete-otr
# No DBUS support
Requires: trinity-kdbusnotification
# Subversion 1.1 is too old
Requires: trinity-tdesvn
%endif

%description applications
%{summary}

%files  applications

##########

%package extras
Group:		User Interface/Desktops
Summary:	Meta-package to install all extras (unofficial) TDE packages

Requires:	trinity-akode
#Requires:	trinity-kasablanca
#Requires:	trinity-kdebluetooth
#Requires:	trinity-kcheckgmail
#Requires:	trinity-icons-crystalsvg-updated
#Requires:	trinity-icons-kfaenza
#Requires:	trinity-icons-oxygen
#Requires:	trinity-kbibtex
#Requires:	trinity-kbiff
Requires:	trinity-kcmautostart
#Requires:	trinity-kftpgrabber
Requires:	trinity-kickoff-i18n
#Requires:	trinity-knmap
#Requires:	trinity-knoda
#Requires:	trinity-ksensors
#Requires:	trinity-kshowmail
#Requires:	trinity-mplayerthumbs
Requires:	trinity-style-ia-ora
#Requires:	trinity-tdeio-ftps-plugin
#Requires:	trinity-tdeio-sysinfo-plugin
#Requires:	trinity-theme-baghira
#Requires:	trinity-tork


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

%if 0%{?pclinuxos}
%package -n trinity-wallpaper-theme-default
Group:		User Interface/Desktops
Summary:	Default wallpaper for Trinity

%description -n trinity-wallpaper-theme-default
%{summary}

%files -n trinity-wallpaper-theme-default
%defattr(-,root,root,-)
%{tde_datadir}/wallpapers/pclinuxos32.jpg
%{tde_datadir}/wallpapers/pclinuxos64.jpg
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
  >"%{?buildroot}%{_sysconfdir}/yum.repos.d/trinity-3.5.13.repo"
%endif

# RHEL configuration for YUM
# $releasever is replaced with its value
%if 0%{?rhel}
%__sed %{SOURCE1} \
  -e 's/\$releasever/%{rhel}/g' \
  >"%{?buildroot}%{_sysconfdir}/yum.repos.d/trinity-3.5.13.repo"
%endif

%if 0%{?fedora} || 0%{?rhel}
%__chmod 644 %{?buildroot}%{_sysconfdir}/yum.repos.d/*.repo
%endif

# RPM signing key
%if 0%{?rhel} || 0%{?fedora}
%__install -D -m 644 "%{SOURCE2}" "%{?buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-trinity"
%endif

# PCLinuxOS wallpaper
%if 0%{?pclinuxos} == 2013
%__install -D -m 644 "%{SOURCE11}" "%{?buildroot}%{tde_datadir}/wallpapers/pclinuxos32.jpg"
%__install -D -m 644 "%{SOURCE12}" "%{?buildroot}%{tde_datadir}/wallpapers/pclinuxos64.jpg"
%endif

%changelog
* Thu Aug 15 2013 Liu Di <liudidi@gmail.com> - 3.5.13.2-2.opt
- 为 Magic 3.0 重建

* Mon Jun 03 2013 Francois Andriot <francois.andriot@free.fr> - 3.5.13.2-1
- Update to version 3.5.13.2
- Add GPG signing key

* Mon Oct 01 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Update to version 3.5.13.1

* Mon Aug 06 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-6
- Add 'applications' subpackage

* Wed Aug 01 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-5
- Updates to reflect new packages names
- Add Mageia 2 support
- Removes 'extras' packages

* Wed Jun 06 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13-4
- Enable mirrorlist

* Wed Nov 30 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-3
- Fix repo files name and content

* Sat Nov 12 2011 Francois Andriot <francois.andriot@free.fr> - 3.5.13-2
- Add 'repo' package
