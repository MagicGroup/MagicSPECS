# Avoids relinking, which breaks consolehelper
%define dont_relink 1

# If TDE is built iwn a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_sbindir %{tde_prefix}/sbin

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


# Fedora review:  http://bugzilla.redhat.com/195486

## Conditional build:
# RHEL6: xmms is outdated !
#define _with_xmms --with-xmms
%ifnarch s390 s390x
%define _with_wifi --with-wifi
%endif

Name:    trinity-tdenetwork
Version: 3.5.13.2
Release: 1%{?dist}%{?_variant}
Summary: Trinity Desktop Environment - Network Applications

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

License: GPLv2
Group:   Applications/Internet

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: kdenetwork-trinity-%{version}.tar.xz
Source1: kppp.pamd
Source2: ktalk
Source4: lisarc
Source5: lisa.redhat

# RedHat/Fedora legacy patches
Patch3: kdenetwork-3.5.8-kppp.patch
Patch4: kdenetwork-3.2.3-resolv.patch
# include more/proper ppp headers
Patch6: kdenetwork-3.5.9-krfb_httpd.patch

# [kdenetworks] Missing LDFLAGS cause FTBFS
Patch1:		kdenetwork-3.5.13-missing_ldflags.patch

# [kdenetworks] FTBFS in SMS client [Bug #1241]
Patch2:		kdenetwork-3.5.13.1-fix_smsclient_ftbfs.patch

BuildRequires:	gettext
BuildRequires:	trinity-tqtinterface-devel >= %{version}
BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	coreutils 
BuildRequires:	openssl-devel
#BuildRequires:  avahi-qt3-devel
BuildRequires:	sqlite-devel
BuildRequires:	gnutls-devel
BuildRequires:	libgadu-devel
BuildRequires:	speex-devel

%if 0%{?fedora} >= 5 || 0%{?rhel} >= 5
BuildRequires:	libXmu-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	libXxf86vm-devel
%endif

# Wifi support
%if "%{?_with_wifi:1}" == "1"
%if 0%{?fedora} >= 6 || 0%{?rhel} >= 5
BuildRequires: wireless-tools-devel
%endif
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}iw29-devel
%endif
%if 0%{?rhel} == 5
BuildRequires: wireless-tools
%endif
%if 0%{?suse_version}
BuildRequires:	libiw-devel
%endif
%endif

BuildRequires: openslp-devel

%ifarch %{ix86}
# BR: %{tde_includedir}/valgrind/valgrind.h
BuildRequires: valgrind
%endif

%{?_with_xmms:BuildRequires: xmms-devel}

# V4L support
%if 0%{?rhel} >= 6 || 0%{?fedora} >= 15 || 0%{?suse_version}
BuildRequires:	libv4l-devel
%endif
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}v4l-devel
%endif

Obsoletes:	trinity-kdenetwork < %{version}-%{release}
Provides:	trinity-kdenetwork = %{version}-%{release}
Obsoletes:	trinity-kdenetwork-libs < %{version}-%{release}
Provides:	trinity-kdenetwork-libs = %{version}-%{release}
Obsoletes:	trinity-kdenetwork-extras < %{version}-%{release}
Provides:	trinity-kdenetwork-extras = %{version}-%{release}
Obsoletes:	tdenetwork < %{version}-%{release}
Provides:	tdenetwork = %{version}-%{release}

Requires: trinity-dcoprss = %{version}-%{release}
Requires: %{name}-filesharing = %{version}-%{release}
Requires: trinity-kdict = %{version}-%{release}
Requires: %{name}-kfile-plugins = %{version}-%{release}
Requires: trinity-kget = %{version}-%{release}
Requires: trinity-knewsticker = %{version}-%{release}
Requires: trinity-kopete = %{version}-%{release}
Requires: trinity-kopete-nowlistening = %{version}-%{release}
Requires: trinity-kpf = %{version}-%{release}
Requires: trinity-kppp = %{version}-%{release}
Requires: trinity-krdc = %{version}-%{release}
Requires: trinity-krfb = %{version}-%{release}
Requires: trinity-ksirc = %{version}-%{release}
Requires: trinity-ktalkd = %{version}-%{release}
Requires: trinity-kwifimanager = %{version}-%{release}
Requires: trinity-librss = %{version}-%{release}
Requires: trinity-lisa = %{version}-%{release}

%description
This metapackage includes a collection of network and networking related
applications provided with the official release of Trinity.

Networking applications, including:
* dcoprss: RSS utilities for Trinity
* filesharing: Network filesharing configuration module for Trinity
* kdict: Dictionary client for Trinity
* kfile-plugins: Torrent metainfo plugin for Trinity
* kget: downloader manager
* knewsticker: RDF newsticker applet
* kopete: chat client
* kopete-nowlistening: (xmms) plugin for Kopete.
* kpf: Public fileserver for Trinity
* kppp: dialer and front end for pppd
* krdc: a client for Desktop Sharing and other VNC servers
* krfb: Desktop Sharing server, allow others to access your desktop via VNC
* ksirc: IRC client for Trinity
* ktalkd: Talk daemon for Trinity
* kwifimanager: Wireless lan manager for Trinity
* librss: RSS library for Trinity
* lisa: lan information server

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README


##########

%package -n trinity-dcoprss
Summary:		RSS utilities for Trinity
Group:			Applications/Internet

%description -n trinity-dcoprss
dcoprss is a RSS to DCOP bridge, allowing all
DCOP aware applications to access RSS news feeds. There is also
a few sample utilities provided.
RSS is a standard for publishing news headlines.
DCOP is the TDE interprocess communication protocol.

%files -n trinity-dcoprss
%defattr(-,root,root,-)
%{tde_bindir}/feedbrowser
%{tde_bindir}/rssclient
%{tde_bindir}/rssservice
%{tde_datadir}/services/rssservice.desktop

%post -n trinity-dcoprss
update-desktop-database 2> /dev/null || : 

%postun -n trinity-dcoprss
update-desktop-database 2> /dev/null || : 

##########

%package devel
Summary:		Development files for the Trinity network module
Group:			Development/Libraries
Requires:		trinity-kdict = %{version}-%{release}
Requires:		trinity-kopete = %{version}-%{release}
Requires:		trinity-ksirc = %{version}-%{release}
Requires:		trinity-librss = %{version}-%{release}
Requires:		trinity-kdelibs-devel

Obsoletes:	trinity-kdenetwork-devel < %{version}-%{release}
Provides:	trinity-kdenetwork-devel = %{version}-%{release}
Obsoletes:	tdenetwork-devel < %{version}-%{release}
Provides:	tdenetwork-devel = %{version}-%{release}

%description devel
This is the development package which contains the headers for the KDE RSS
library as well as the Kopete chat client, as well as miscellaneous
development-related files for the TDE network module.

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kopete/*.h
%{tde_tdeincludedir}/kopete/ui/*.h
%{tde_tdeincludedir}/rss/*.h
%{tde_libdir}/libkdeinit_kdict.la
%{tde_libdir}/libkdeinit_ksirc.la
%{tde_libdir}/libkopete.la
%{tde_libdir}/libkopete.so
%{tde_libdir}/libkopete_msn_shared.la
%{tde_libdir}/libkopete_msn_shared.so
%{tde_libdir}/libkopete_oscar.la
%{tde_libdir}/libkopete_oscar.so
%{tde_libdir}/libkopete_videodevice.la
%{tde_libdir}/libkopete_videodevice.so
%{tde_libdir}/librss.la
%{tde_libdir}/librss.so
%{tde_datadir}/cmake/librss.cmake

%post devel
/sbin/ldconfig

%postun devel
/sbin/ldconfig

##########

%package filesharing
#Recommends:	perl-suid
Summary:		Network filesharing configuration module for Trinity
Group:   		Applications/Internet

Obsoletes:		tdenetwork-filesharing < %{version}-%{release}
Provides:		tdenetwork-filesharing = %{version}-%{release}

%description filesharing
This package provides a TDE Control Center module to configure
NFS and Samba.

%files filesharing
%defattr(-,root,root,-)
%{tde_tdelibdir}/fileshare_propsdlgplugin.la
%{tde_tdelibdir}/fileshare_propsdlgplugin.so
%{tde_tdelibdir}/kcm_fileshare.la
%{tde_tdelibdir}/kcm_fileshare.so
%{tde_tdelibdir}/kcm_kcmsambaconf.la
%{tde_tdelibdir}/kcm_kcmsambaconf.so
%{tde_tdeappdir}/fileshare.desktop
%{tde_tdeappdir}/kcmsambaconf.desktop
%{tde_datadir}/icons/hicolor/*/apps/kcmsambaconf.png
%{tde_datadir}/services/fileshare_propsdlgplugin.desktop

%post filesharing
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun filesharing
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-kdict
Summary:		Dictionary client for Trinity
Group:			Applications/Internet

%description -n trinity-kdict
KDict is an advanced TDE graphical client for the DICT Protocol, with full
Unicode support. It enables you to search through dictionary databases for a
word or phrase, then displays suitable definitions. KDict tries to ease
basic as well as advanced queries.

%files -n trinity-kdict
%defattr(-,root,root,-)
%{tde_bindir}/kdict
%{tde_tdelibdir}/kdict.*
%{tde_tdelibdir}/kdict_panelapplet.*
%{tde_libdir}/libkdeinit_kdict.*
%{tde_tdeappdir}/kdict.desktop
%{tde_datadir}/apps/kdict
%{tde_datadir}/apps/kicker/applets/kdictapplet.desktop
%{tde_datadir}/icons/hicolor/*/apps/kdict.*
%{tde_tdedocdir}/HTML/en/kdict

%post -n trinity-kdict
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kdict
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package kfile-plugins
Summary:		Torrent metainfo plugin for Trinity
Group:			Applications/Internet

Obsoletes:		tdenetwork-kfile-plugins < %{version}-%{release}
Provides:		tdenetwork-kfile-plugins = %{version}-%{release}

%description kfile-plugins
This package provides a metainformation plugin for bittorrent files.
TDE uses kfile-plugins to provide metainfo tab in the files properties
dialog in konqueror and other file-handling applications.

%files kfile-plugins
%{tde_tdelibdir}/kfile_torrent.la
%{tde_tdelibdir}/kfile_torrent.so
%{tde_datadir}/services/kfile_torrent.desktop

%post kfile-plugins
update-desktop-database 2> /dev/null || : 

%postun kfile-plugins
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-kget
Summary:		download manager for Trinity
Group:			Applications/Internet

%description -n trinity-kget
KGet is a a download manager similar to GetRight or Go!zilla. It keeps
all your downloads in one dialog and you can add and remove transfers.
Transfers can be paused, resumed, queued or scheduled.
Dialogs display info about status of transfers - progress, size, speed
and remaining time. Program supports drag & drop from TDE
applications and Netscape.

%files -n trinity-kget
%defattr(-,root,root,-)
%{tde_bindir}/kget
%{tde_tdelibdir}/khtml_kget.la
%{tde_tdelibdir}/khtml_kget.so
%{tde_tdeappdir}/kget.desktop
%{tde_datadir}/apps/kget
%{tde_datadir}/apps/khtml/kpartplugins/kget_plug_in.desktop
%{tde_datadir}/apps/khtml/kpartplugins/kget_plug_in.rc
%{tde_datadir}/apps/konqueror/servicemenus/kget_download.desktop
%{tde_datadir}/icons/crystalsvg/*/actions/khtml_kget.png
%{tde_datadir}/icons/crystalsvg/*/apps/kget.png
%{tde_datadir}/icons/crystalsvg/*/mimetypes/kget_list.png
%{tde_datadir}/mimelnk/application/x-kgetlist.desktop
%{tde_datadir}/sounds/KGet_Added.ogg
%{tde_datadir}/sounds/KGet_Finished.ogg
%{tde_datadir}/sounds/KGet_Finished_All.ogg
%{tde_datadir}/sounds/KGet_Started.ogg
%{tde_tdedocdir}/HTML/en/kget

%post -n trinity-kget
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kget
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-knewsticker
Summary:		news ticker applet for Trinity
Group:			Applications/Internet

%description -n trinity-knewsticker
This is a news ticker applet for the Trinity panel. It can scroll news from
your favorite news sites, such as lwn.net, /. and freshmeat.net.
To achieve this, KNewsTicker requires the news sites to provide a
RSS feed to newsitems. KNewsTicker already comes with a selection of
good news sources which provide such files.

%files -n trinity-knewsticker
%defattr(-,root,root,-)
%{tde_bindir}/knewstickerstub
%{tde_tdelibdir}/knewsticker_panelapplet.la
%{tde_tdelibdir}/knewsticker_panelapplet.so
%{tde_tdelibdir}/libkntsrcfilepropsdlg.la
%{tde_tdelibdir}/libkntsrcfilepropsdlg.so
%{tde_tdeappdir}/knewsticker-standalone.desktop
%{tde_datadir}/applnk/.hidden/knewstickerstub.desktop
%{tde_datadir}/apps/kconf_update/knewsticker.upd
%{tde_datadir}/apps/kconf_update/knt-0.1-0.2.pl
%{tde_datadir}/apps/kicker/applets/knewsticker.desktop
%{tde_datadir}/apps/knewsticker/eventsrc
%{tde_datadir}/icons/hicolor/*/apps/knewsticker.png
%{tde_datadir}/services/kntsrcfilepropsdlg.desktop
%{tde_tdedocdir}/HTML/en/knewsticker

%post -n trinity-knewsticker
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-knewsticker
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-kopete
Summary:		instant messenger for Trinity
Group:			Applications/Internet
URL:			http://kopete.kde.org

#Recommends: qca-tls
#Suggests: tdeartwork-emoticons-trinity, khelpcenter-trinity, imagemagick, gnupg, gnomemeeting
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	meanwhile-devel
#jabber
BuildRequires:	libidn-devel
#jabber/jingle
%if 0%{?suse_version}
BuildRequires:	libexpat-devel
%else
BuildRequires:	expat-devel
BuildRequires:	ortp-devel
%endif
BuildRequires:	glib2-devel
BuildRequires:	speex-devel
# jabber/ssl
#{?fedora:Requires(hint): qca-tls}
Requires:		jasper

%description -n trinity-kopete
Kopete is an instant messenger program which can communicate with a variety
of IM systems, such as Yahoo, ICQ, MSN, IRC and Jabber.

Support for more IM protocols can be added through a plugin system.

%files -n trinity-kopete
%defattr(-,root,root,-)
# nowlistening support
%exclude %{tde_datadir}/apps/kopete/*nowlisteningchatui*
%exclude %{tde_datadir}/apps/kopete/*nowlisteningui*
%exclude %{tde_datadir}/config.kcfg/nowlisteningconfig.kcfg
%exclude %{tde_datadir}/services/kconfiguredialog/*nowlistening*
%exclude %{tde_datadir}/services/*nowlistening*
%exclude %{tde_tdelibdir}/*nowlistening*
# Main kopete package
%{tde_bindir}/kopete
%{tde_bindir}/kopete_latexconvert.sh
%{tde_libdir}/kconf_update_bin/kopete-account-kconf_update
%{tde_libdir}/kconf_update_bin/kopete-nameTracking-kconf_update
%{tde_libdir}/kconf_update_bin/kopete-pluginloader2-kconf_update
%{tde_tdelibdir}/kcm_kopete_*.so
%{tde_tdelibdir}/kcm_kopete_*.la
%{tde_tdelibdir}/kio_jabberdisco.la
%{tde_tdelibdir}/kio_jabberdisco.so
%{tde_tdelibdir}/kopete_*.la
%{tde_tdelibdir}/kopete_*.so
%{tde_tdelibdir}/libkrichtexteditpart.la
%{tde_tdelibdir}/libkrichtexteditpart.so
%{tde_libdir}/libkopete_msn_shared.so.*
%{tde_libdir}/libkopete_oscar.so.*
%{tde_libdir}/libkopete.so.*
%{tde_libdir}/libkopete_videodevice.so.*
%{tde_tdeappdir}/kopete.desktop
%{tde_datadir}/apps/kconf_update/kopete-*
%{tde_datadir}/apps/kopete
%{tde_datadir}/apps/kopete_*/*.rc
%{tde_datadir}/apps/kopeterichtexteditpart/kopeterichtexteditpartfull.rc
%{tde_datadir}/config.kcfg/historyconfig.kcfg
%{tde_datadir}/config.kcfg/kopeteidentityconfigpreferences.kcfg
%{tde_datadir}/config.kcfg/kopete.kcfg
%{tde_datadir}/config.kcfg/latexconfig.kcfg
%{tde_datadir}/icons/crystalsvg/*/actions/voicecall.png
%{tde_datadir}/icons/crystalsvg/*/actions/webcamreceive.png
%{tde_datadir}/icons/crystalsvg/*/actions/webcamsend.png
%{tde_datadir}/icons/crystalsvg/*/actions/account_offline_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/add_user.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_away_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_busy_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_food_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_invisible_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_phone_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/contact_xa_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/delete_user.png
%{tde_datadir}/icons/crystalsvg/*/actions/edit_user.png
%{tde_datadir}/icons/crystalsvg/*/actions/emoticon.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_away.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_chatty.png
#%{tde_datadir}/icons/crystalsvg/*/actions/jabber_connecting.mng
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_group.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_invisible.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_na.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_offline.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_online.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_original.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_raw.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_serv_off.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_serv_on.png
%{tde_datadir}/icons/crystalsvg/*/actions/jabber_xa.png
%{tde_datadir}/icons/crystalsvg/*/actions/kopeteavailable.png
%{tde_datadir}/icons/crystalsvg/*/actions/kopeteaway.png
%{tde_datadir}/icons/crystalsvg/*/actions/kopeteeditstatusmessage.png
%{tde_datadir}/icons/crystalsvg/*/actions/kopetestatusmessage.png
%{tde_datadir}/icons/crystalsvg/*/actions/metacontact_away.png
%{tde_datadir}/icons/crystalsvg/*/actions/metacontact_offline.png
%{tde_datadir}/icons/crystalsvg/*/actions/metacontact_online.png
%{tde_datadir}/icons/crystalsvg/*/actions/metacontact_unknown.png
%{tde_datadir}/icons/crystalsvg/*/actions/newmsg.png
%{tde_datadir}/icons/crystalsvg/*/actions/search_user.png
%{tde_datadir}/icons/crystalsvg/*/actions/show_offliners.png
%{tde_datadir}/icons/crystalsvg/*/actions/status_unknown_overlay.png
%{tde_datadir}/icons/crystalsvg/*/actions/status_unknown.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_aim.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_gadu.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_http-ws.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_icq.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_irc.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_msn.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_qq.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_smtp.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_tlen.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_gateway_yahoo.png
%{tde_datadir}/icons/crystalsvg/*/apps/jabber_protocol.png
%{tde_datadir}/icons/crystalsvg/*/apps/kopete_all_away.png
%{tde_datadir}/icons/crystalsvg/*/apps/kopete_offline.png
%{tde_datadir}/icons/crystalsvg/*/apps/kopete_some_away.png
%{tde_datadir}/icons/crystalsvg/*/apps/kopete_some_online.png
%{tde_datadir}/icons/crystalsvg/*/mimetypes/kopete_emoticons.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/account_offline_overlay.svgz
%{tde_datadir}/icons/hicolor/*/apps/kopete.png
%{tde_datadir}/icons/hicolor/*/actions/emoticon.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_away.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_chatty.png
#%{tde_datadir}/icons/hicolor/*/actions/jabber_connecting.mng
%{tde_datadir}/icons/hicolor/*/actions/jabber_group.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_invisible.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_na.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_offline.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_online.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_original.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_raw.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_serv_off.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_serv_on.png
%{tde_datadir}/icons/hicolor/*/actions/jabber_xa.png
%{tde_datadir}/icons/hicolor/*/actions/kopeteavailable.png
%{tde_datadir}/icons/hicolor/*/actions/kopeteaway.png
%{tde_datadir}/icons/hicolor/*/actions/newmsg.png
%{tde_datadir}/icons/hicolor/*/actions/status_unknown_overlay.png
%{tde_datadir}/icons/hicolor/*/actions/status_unknown.png
%{tde_datadir}/icons/hicolor/*/apps/jabber_protocol.png
%{tde_datadir}/icons/*/*/actions/jabber_connecting.mng
%{tde_datadir}/icons/*/*/actions/newmessage.mng
%{tde_datadir}/icons/hicolor/scalable/apps/kopete2.svgz
%{tde_datadir}/mimelnk/application/x-icq.desktop
%{tde_datadir}/mimelnk/application/x-kopete-emoticons.desktop
%{tde_datadir}/services/aim.protocol
%{tde_datadir}/services/chatwindow.desktop
%{tde_datadir}/services/emailwindow.desktop
%{tde_datadir}/services/jabberdisco.protocol
%{tde_datadir}/services/kconfiguredialog/kopete_*.desktop
%{tde_datadir}/services/kopete_*.desktop
%{tde_datadir}/icons/crystalsvg/16x16/apps/jabber_gateway_sms.png
%{tde_datadir}/servicetypes/kopete*.desktop
%{tde_datadir}/sounds/Kopete_*.ogg
%{tde_tdedocdir}/HTML/en/kopete
# jingle support for kopete
%{tde_bindir}/relayserver
%{tde_bindir}/stunserver
# winpopup support for kopete
%{tde_bindir}/winpopup-install.sh
%{tde_bindir}/winpopup-send.sh
# meanwhile protocol support for kopete
#%{tde_libdir}/new_target0.la
#%{tde_libdir}/new_target0.so
# motionaway plugin for kopete
%{tde_datadir}/config.kcfg/motionawayconfig.kcfg
# smpp plugin for kopete
%{tde_datadir}/config.kcfg/smpppdcs.kcfg


%post -n trinity-kopete
for f in crystalsvg hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 
/sbin/ldconfig

%postun -n trinity-kopete
for f in crystalsvg hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 
/sbin/ldconfig

##########

%package -n trinity-kopete-nowlistening
Summary:		Nowlistening (xmms) plugin for Kopete.
Group:			Applications/Internet

%description -n trinity-kopete-nowlistening
Kopete includes the "Now Listening" plug-in that can report what music you
are currently listening to, in a number of different players, including
noatun, kscd, juk, kaffeine and amarok.

%files -n trinity-kopete-nowlistening
%defattr(-,root,root,-)
%{tde_datadir}/apps/kopete/*nowlisteningchatui*
%{tde_datadir}/apps/kopete/*nowlisteningui*
%{tde_datadir}/config.kcfg/nowlisteningconfig.kcfg
%{tde_datadir}/services/kconfiguredialog/*nowlistening*
%{tde_datadir}/services/*nowlistening*
%{tde_tdelibdir}/*nowlistening*

##########

%package -n trinity-kpf
Summary:		Public fileserver for Trinity
Group:			Applications/Internet

%description -n trinity-kpf
kpf provides simple file sharing using HTTP. kpf is strictly a public
fileserver, which means that there are no access restrictions to shared
files. Whatever you select for sharing is available to anyone. kpf is
designed to be used for sharing files with friends.

%files -n trinity-kpf
%defattr(-,root,root,-)
%{tde_tdelibdir}/kpf*
%{tde_datadir}/apps/kicker/applets/kpfapplet.desktop
%{tde_datadir}/icons/crystalsvg/*/apps/kpf.*
%{tde_datadir}/services/kpfpropertiesdialogplugin.desktop
%{tde_tdedocdir}/HTML/en/kpf

%post -n trinity-kpf
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kpf
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-kppp
Summary:		modem dialer and ppp frontend for Trinity
Group:			Applications/Internet
Requires:		ppp
%if 0%{?rhel} || 0%{?fedora}
Requires:		usermode-gtk
%else
Requires:		usermode
%endif

%description -n trinity-kppp
KPPP is a dialer and front end for pppd. It allows for interactive
script generation and network setup. It will automate the dialing in
process to your ISP while letting you conveniently monitor the entire
process.

Once connected KPPP will provide a rich set of statistics and keep
track of the time spent online for you.

%files -n trinity-kppp
%defattr(-,root,root,-)
%config(noreplace) /etc/security/console.apps/kppp3
%config(noreplace) /etc/pam.d/kppp3
%{tde_bindir}/kppp3
%{tde_bindir}/kppplogview
%{_sbindir}/kppp3
%{tde_sbindir}/kppp3
%{tde_tdeappdir}/Kppp.desktop
%{tde_tdeappdir}/kppplogview.desktop
#%{tde_datadir}/apps/checkrules
%{tde_datadir}/apps/kppp
%{tde_datadir}/icons/hicolor/*/apps/kppp.png
%{tde_tdedocdir}/HTML/en/kppp

%post -n trinity-kppp
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kppp
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-krdc
Summary:		Remote Desktop Connection for Trinity
Group:			Applications/Internet
Requires:		rdesktop

%description -n trinity-krdc
krdc is an TDE graphical client for the rfb protocol, used by VNC,
and if rdesktop is installed, krdc can connect to Windows Terminal
Servers using RDP.

%files -n trinity-krdc
%defattr(-,root,root,-)
%{tde_bindir}/krdc
%{tde_tdeappdir}/krdc.desktop
%{tde_datadir}/apps/konqueror/servicemenus/smb2rdc.desktop
%{tde_datadir}/apps/krdc
%{tde_datadir}/icons/crystalsvg/*/apps/krdc.png
%{tde_datadir}/services/rdp.protocol
%{tde_datadir}/services/vnc.protocol
%{tde_tdedocdir}/HTML/en/krdc

%post -n trinity-krdc
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-krdc
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-krfb
Summary:		Desktop Sharing for Trinity
Group:			Applications/Internet

%description -n trinity-krfb
Desktop Sharing (krfb) is a server application that allows you to share
your current session with a user on another machine, who can use a
VNC client like krdc to view or even control the desktop. It doesn't
require you to start a new X session - it can share the current session.
This makes it very useful when you want someone to help you perform a
task.

%files -n trinity-krfb
%defattr(-,root,root,-)
%{tde_bindir}/krfb
%{tde_bindir}/krfb_httpd
%{tde_tdelibdir}/kcm_krfb.la
%{tde_tdelibdir}/kcm_krfb.so
%{tde_tdelibdir}/kded_kinetd.la
%{tde_tdelibdir}/kded_kinetd.so
%{tde_tdeappdir}/kcmkrfb.desktop
%{tde_tdeappdir}/krfb.desktop
%{tde_datadir}/apps/kinetd/eventsrc
%{tde_datadir}/apps/krfb
%{tde_datadir}/icons/crystalsvg/*/apps/krfb.png
%{tde_datadir}/icons/locolor/*/apps/krfb.png
%{tde_datadir}/services/kded/kinetd.desktop
%{tde_datadir}/services/kinetd_krfb.desktop
%{tde_datadir}/services/kinetd_krfb_httpd.desktop
%{tde_datadir}/servicetypes/kinetdmodule.desktop
%{tde_tdedocdir}/HTML/en/krfb

%post -n trinity-krfb
for f in crystalsvg locolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-krfb
for f in crystalsvg locolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-ksirc
Summary:		IRC client for Trinity
Group:			Applications/Internet

%description -n trinity-ksirc
KSirc is an IRC chat client for KDE. It supports scripting with Perl and has a
lot of compatibility with mIRC for general use.

If you want to connect to an IRC server via SSL, you will need to install the
recommended package libio-socket-ssl-perl.

%files -n trinity-ksirc
%defattr(-,root,root,-)
%{tde_bindir}/dsirc
%{tde_bindir}/ksirc
%{tde_libdir}/libkdeinit_ksirc.*
%{tde_tdelibdir}/ksirc.*
%{tde_tdeappdir}/ksirc.desktop
%{tde_datadir}/apps/ksirc/
%config(noreplace) %{tde_datadir}/config/ksircrc
%{tde_datadir}/icons/hicolor/*/apps/ksirc.*
%{tde_tdedocdir}/HTML/??/ksirc/

%post -n trinity-ksirc
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 
/sbin/ldconfig


%postun -n trinity-ksirc
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 
/sbin/ldconfig

##########

%package -n trinity-ktalkd
Summary:		Talk daemon for Trinity
Group:			Applications/Internet

%description -n trinity-ktalkd
KTalkd is an enhanced talk daemon - a program to handle incoming talk
requests, announce them and allow you to respond to it using a talk
client. Note that KTalkd is designed to run on a single-user workstation,
and shouldn't be run on a multi-user machine.

%files -n trinity-ktalkd
%defattr(-,root,root,-)
%{tde_bindir}/ktalkd*
%{tde_bindir}/mail.local
%{tde_tdelibdir}/kcm_ktalkd.*
%{tde_tdeappdir}/kcmktalkd.desktop
%config(noreplace) %{tde_datadir}/config/ktalkdrc
%{tde_datadir}/icons/crystalsvg/*/apps/ktalkd.*
%{tde_datadir}/sounds/ktalkd.wav
%config(noreplace) %{_sysconfdir}/xinetd.d/ktalk
%{tde_tdedocdir}/HTML/en/kcontrol/kcmtalkd
%{tde_tdedocdir}/HTML/en/ktalkd

%post -n trinity-ktalkd
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-ktalkd
for f in crystalsvg ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

##########

%if "%{?_with_wifi:1}" == "1"
%package -n trinity-kwifimanager
#Depends: ${shlibs:Depends}, wireless-tools
#Suggests: khelpcenter-trinity
Summary:		Wireless lan manager for Trinity
Group:			Applications/Internet

%description -n trinity-kwifimanager
KWiFiManager suite is a set of tools which allows you to manage your
wireless LAN connection under the K Desktop Environment. It provides
information about your current connection. KWiFiManager supports every
wavelan card that uses the wireless extensions interface.

%files -n trinity-kwifimanager
%defattr(-,root,root,-)
%{tde_bindir}/kwifimanager
%{tde_tdelibdir}/kcm_wifi.*
%{tde_libdir}/libkwireless.la
%{tde_libdir}/libkwireless.so
%{tde_tdeappdir}/kcmwifi.desktop
%{tde_tdeappdir}/kwifimanager.desktop
%{tde_datadir}/apps/kicker/applets/kwireless.desktop
%{tde_datadir}/apps/kwifimanager
%{tde_datadir}/icons/hicolor/*/apps/kwifimanager.png
%{tde_datadir}/icons/hicolor/*/apps/kwifimanager.svgz
%doc %{tde_tdedocdir}/HTML/en/kwifimanager

%post -n trinity-kwifimanager
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kwifimanager
for f in hicolor ; do
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f}  2> /dev/null || :
done
update-desktop-database 2> /dev/null || : 
%endif

##########

%package -n trinity-librss
Summary:		RSS library for Trinity
Group:			Environment/Libraries

%description -n trinity-librss
This is the runtime package for programs that use the TDE RSS library.
End users should not need to install this, it should get installed
automatically when needed.

%files -n trinity-librss
%defattr(-,root,root,-)
%{tde_libdir}/librss.so.*

%post -n trinity-librss
/sbin/ldconfig

%postun -n trinity-librss
/sbin/ldconfig

##########

%package -n trinity-lisa
Summary:			LAN information server for Trinity
Group:				Applications/Internet
%if 0%{?suse_version}
Requires(preun):	aaa_base
Requires(post):		aaa_base
%else
Requires(preun):	chkconfig
Requires(post):		chkconfig
%endif

%description -n trinity-lisa
LISa is intended to provide KDE with a kind of "network neighborhood"
but relying only on the TCP/IP protocol.

%files -n trinity-lisa
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/lisarc*
%config(noreplace) %{_initrddir}/lisa
%{tde_tdelibdir}/kcm_lanbrowser.la
%{tde_tdelibdir}/kcm_lanbrowser.so
%{tde_tdelibdir}/kio_lan.la
%{tde_tdelibdir}/kio_lan.so
%{tde_datadir}/applnk/.hidden/kcmkiolan.desktop
%{tde_datadir}/applnk/.hidden/kcmlisa.desktop
%{tde_datadir}/applnk/.hidden/kcmreslisa.desktop
%{tde_datadir}/apps/konqsidebartng/virtual_folders/services/lisa.desktop
%{tde_datadir}/apps/konqueror/dirtree/remote/lan.desktop
%{tde_datadir}/apps/lisa/README
%{tde_datadir}/apps/remoteview/lan.desktop
%{tde_tdedocdir}/HTML/en/kcontrol/lanbrowser/common
%{tde_tdedocdir}/HTML/en/kcontrol/lanbrowser/index.cache.bz2
%{tde_tdedocdir}/HTML/en/kcontrol/lanbrowser/index.docbook
%{tde_tdedocdir}/HTML/en/lisa/
%{tde_datadir}/services/lan.protocol
%{tde_datadir}/services/rlan.protocol
%{tde_bindir}/lisa
%{tde_bindir}/reslisa

%post -n trinity-lisa
/sbin/chkconfig --add lisa ||:
update-desktop-database 2> /dev/null || : 

%postun -n trinity-lisa
if [ $1 -eq 0 ]; then
  /sbin/chkconfig --del lisa ||:
  /sbin/service lisa stop > /dev/null 2>&1 ||:
fi
update-desktop-database 2> /dev/null || : 

##########

%package -n trinity-kdnssd
#Recommends: avahi-daemon
#Suggests: avahi-autoipd | zeroconf
Summary: Zeroconf support for KDE
Group:			Applications/Internet

%description -n trinity-kdnssd
A kioslave and kded module that provide Zeroconf support. Try
"zeroconf:/" in Konqueror.

%files -n trinity-kdnssd
%defattr(-,root,root,-)
%{tde_datadir}/services/zeroconf.protocol
%{tde_datadir}/services/invitation.protocol
%{tde_datadir}/services/kded/dnssdwatcher.desktop
%{tde_datadir}/apps/remoteview/zeroconf.desktop
%{tde_datadir}/apps/zeroconf/_http._tcp
%{tde_datadir}/apps/zeroconf/_ftp._tcp
%{tde_datadir}/apps/zeroconf/_ldap._tcp
%{tde_datadir}/apps/zeroconf/_webdav._tcp
%{tde_datadir}/apps/zeroconf/_nfs._tcp
%{tde_datadir}/apps/zeroconf/_ssh._tcp
%{tde_datadir}/apps/zeroconf/_rfb._tcp
%{tde_tdelibdir}/kio_zeroconf.so
%{tde_tdelibdir}/kio_zeroconf.la
%{tde_tdelibdir}/kded_dnssdwatcher.so
%{tde_tdelibdir}/kded_dnssdwatcher.la

%post -n trinity-kdnssd
update-desktop-database 2> /dev/null || : 

%postun -n trinity-kdnssd
update-desktop-database 2> /dev/null || : 

##########

%if 0%{?suse_version}
%debug_package
%endif

##########

%prep
%setup -q -n kdenetwork-trinity-%{version}

%patch1 -p1 -b .ldflags
#%patch2 -p1 -b .ftbfs
%patch3 -p1 -b .kppp
%patch4 -p1 -b .resolv
%patch6 -p1 -b .krfb_httpd

%__sed -i 's/TQT_PREFIX/TDE_PREFIX/g' cmake/modules/FindTQt.cmake

%build
unset QTDIR || : ; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"
export CMAKE_INCLUDE_PATH="%{tde_includedir}:%{tde_includedir}/tqt"
export LD_LIBRARY_PATH="%{tde_libdir}"

%if 0%{?rhel} || 0%{?fedora} || 0%{?suse_version}
%__mkdir_p build
cd build
%endif

# Ugly hack for opensuse 12.2 - libiw undefined reference to 'floor' etc ...
%if 0%{?suse_version} >= 1220
export LDFLAGS="${LDFLAGS} -lm"
%endif

%cmake \
  -DCMAKE_PREFIX_PATH=%{tde_prefix} \
  -DTDE_PREFIX=%{tde_prefix} \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  -DWITH_JINGLE=ON \
  -DWITH_SPEEX=ON \
  -DWITH_WEBCAM=ON \
  -DWITH_GSM=OFF \
  -DWITH_ARTS=ON \
  -DBUILD_ALL=ON \
  -DBUILD_KOPETE_PROTOCOL_ALL=ON \
  -DBUILD_KOPETE_PLUGIN_ALL=ON \
  ..

# Tdenetwork is not smp safe !
%__make VERBOSE=1


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot} -C build


## File lists
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && %{__rm} -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi

# Show only in KDE, FIXME, need to re-evaluate these -- Rex
for i in fileshare kcmkrfb kcmktalkd kcmwifi krfb kppp kppplogview \
   kwifimanager kget knewsticker ksirc kdict ; do
   if [ -f %{buildroot}%{tde_datadir}/applications/kde/$i.desktop ] ; then
      echo "OnlyShowIn=KDE;" >> %{buildroot}%{tde_datadir}/applications/kde/$i.desktop
   fi
done

# Run kppp through consolehelper, and rename it to 'kppp3'
%__install -p -m644 -D %{SOURCE1} %{buildroot}/etc/pam.d/kppp3
%__mkdir_p %{buildroot}%{tde_sbindir} %{buildroot}%{_sbindir}
%__mv %{buildroot}%{tde_bindir}/kppp %{buildroot}%{tde_sbindir}/kppp3
%__ln_s %{_bindir}/consolehelper %{buildroot}%{tde_bindir}/kppp3
%if "%{tde_prefix}" != "/usr"
%__ln_s %{tde_sbindir}/kppp3 %{?buildroot}%{_sbindir}/kppp3
%endif
%__mkdir_p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/kppp3 <<EOF
USER=root
PROGRAM=%{tde_sbindir}/kppp3
SESSION=true
EOF
%__sed -i %{buildroot}%{tde_tdeappdir}/Kppp.desktop -e "/Exec=/ s|kppp|kppp3|"

# ktalk
%__install -p -m 0644 -D  %{SOURCE2} %{buildroot}%{_sysconfdir}/xinetd.d/ktalk

# Add lisa startup script
%__install -p -m 0644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/lisarc
%__install -p -m 0755 -D %{SOURCE5} %{buildroot}%{_initrddir}/lisa

# RHEL 5: Avoids conflict with 'kdenetwork'
%if 0%{?rhel} == 5
%__mv -f %{buildroot}%{_sysconfdir}/lisarc %{buildroot}%{_sysconfdir}/lisarc.tde
%endif

# Avoids conflict with trinity-kvirc
%__mv -f %{buildroot}%{tde_datadir}/services/irc.protocol %{buildroot}%{tde_datadir}/apps/kopete/

%clean
%__rm -rf %{buildroot}



%changelog
* Sun Sep 30 2012 Francois Andriot <francois.andriot@free.fr> - 3.5.13.1-1
- Initial build for TDE 3.5.13.1
