%define rversion %{kde4_kdelibs_version}
#define rversion 4.4.7
%define release_number 1
%define real_name kdepim

# do not enable final...
# I'm lazy to make a patch for this..
# too many errors...
%define kde4_enable_final_bool OFF

# KPilot's Avantgo conduit
%define build_kpilot_avantgo_conduit 0
# kitchensync
%define build_kitchensync 0

Name: kdepim4
Summary: The KDE PIM Components
License: LGPL v2 or later
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
URL: http://www.kde.org/
Version: %{rversion}
Release: %{release_number}%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: boost-devel cyrus-sasl-devel gpgme openldap-devel
BuildRequires: libkdelibs4-devel
BuildRequires: libkdepimlibs4-devel
BuildRequires: kdepim4-runtime-devel
BuildRequires: libassuan-devel
%if %build_kitchensync
BuildRequires: libopensync-devel >= 0.33
%endif
%if %build_kpilot_avantgo_conduit
BuildRequires: libmal >= 0.40
%endif

Requires: %{name}-akregator = %{version}
Requires: %{name}-console = %{version}
Requires: %{name}-kaddressbook = %{version}
Requires: %{name}-kalarm = %{version}
Requires: %{name}-icons = %{version}
%if %build_kitchensync
Requires: %{name}-kitchensync = %{version}
%endif
Requires: %{name}-kjots = %{version}
Requires: %{name}-kleopatra = %{version}
Requires: %{name}-kmail = %{version}
Requires: %{name}-kmailcvt = %{version}
Requires: %{name}-knode = %{version}
Requires: %{name}-knotes = %{version}
Requires: %{name}-kontact = %{version}
Requires: %{name}-korganizer = %{version}
Requires: %{name}-kresources = %{version}
Requires: %{name}-ksendemail = %{version}
Requires: %{name}-ktimetracker = %{version}
Requires: %{name}-libkdepim = %{version}
Requires: %{name}-libkleo = %{version}
Requires: %{name}-libkpgp = %{version}
Requires: %{name}-libksieve = %{version}
Requires: %{name}-plugins = %{version}
Requires: %{name}-strigi-analyzer = %{version}
Requires: %{name}-blogilo = %{version}
Requires: %{name}-akonadi = %{version}
Requires: %{name}-akonadiconsole = %{version}
Requires: %{name}-messagecore = %{version}
Requires: %{name}-messagelist = %{version}
Requires: %{name}-messageviewer = %{version}

Obsoletes: %{name}-kontactinterfaces

Patch0: kdepim-4.1.80-libqgpgme-link-fix.patch
# http://bugzilla.redhat.com/show_bug.cgi?id=496988
Patch1: kdepim-4.3.1-kmail-saveAttachments.patch

Patch600: kmail_remove_charsets.diff
Patch601: korgac_no_autostart.patch

# 默认添加一些额外的中文网站种子
Patch100: magic-akregator_extra_feeds.patch

Patch1000: 01_at_least_build_against_new_opensync-4.1.80.diff

Patch1001: kdepim-4.1.80-no_kitchensync.diff

# upstream patches

%description
The KDE PIM Components.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- 开发包
%package -n %{name}-devel
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: KDE PIM Libraries: Build Environment
Requires: libkdelibs4-devel cyrus-sasl-devel openldap-devel boost-devel
Requires: %{name} = %{version}

%description -n %{name}-devel
This package contains all necessary include files and libraries needed
to develop KDE PIM applications.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- akregator
%package -n %{name}-akregator
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: akregator

%description -n %{name}-akregator
akregator.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- console
%package -n %{name}-console
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: console

%description -n %{name}-console
console.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kaddressbook
%package -n %{name}-kaddressbook
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kaddressbook

%description -n %{name}-kaddressbook
kaddressbook.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kalarm
%package -n %{name}-kalarm
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kalarm

%description -n %{name}-kalarm
kalarm.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- icons
%package -n %{name}-icons
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: icons

%description -n %{name}-icons
icons.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kjots
%package -n %{name}-kjots
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kjots

%description -n %{name}-kjots
kjots.

%if %build_kitchensync
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kitchensync
%package -n %{name}-kitchensync
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kitchensync

%description -n %{name}-kitchensync
kitchensync.

%endif
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kleopatra
%package -n %{name}-kleopatra
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kleopatra

%description -n %{name}-kleopatra
kleopatra.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmail
%package -n %{name}-kmail
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kmail

%description -n %{name}-kmail
kmail.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kmailcvt
%package -n %{name}-kmailcvt
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kmailcvt

%description -n %{name}-kmailcvt
kmailcvt.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- knode
%package -n %{name}-knode
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: knode

%description -n %{name}-knode
knode.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- knotes
%package -n %{name}-knotes
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: knotes

%description -n %{name}-knotes
knotes.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kontact
%package -n %{name}-kontact
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kontact

%description -n %{name}-kontact
kontact.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- korganizer
%package -n %{name}-korganizer
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: korganizer

%description -n %{name}-korganizer
korganizer.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kpilot
%package -n %{name}-kpilot
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kpilot

%description -n %{name}-kpilot
kpilot.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- kresources
%package -n %{name}-kresources
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: kresources

%description -n %{name}-kresources
kresources.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ksendemail
%package -n %{name}-ksendemail
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: ksendemail

%description -n %{name}-ksendemail
ksendemail.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- ktimetracker
%package -n %{name}-ktimetracker
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: ktimetracker

%description -n %{name}-ktimetracker
ktimetracker.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkdepim
%package -n %{name}-libkdepim
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: libkdepim

%description -n %{name}-libkdepim
libkdepim.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkleo
%package -n %{name}-libkleo
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: libkleo

%description -n %{name}-libkleo
libkleo.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libkpgp
%package -n %{name}-libkpgp
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: libkpgp

%description -n %{name}-libkpgp
libkpgp.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- libksieve
%package -n %{name}-libksieve
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: libksieve

%description -n %{name}-libksieve
libksieve.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- mimelib
%package -n %{name}-mimelib
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: mimelib

%description -n %{name}-mimelib
mimelib.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- plugins
%package -n %{name}-plugins
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: plugins

%description -n %{name}-plugins
plugins.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- strigi-analyzer
%package -n %{name}-strigi-analyzer
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: strigi-analyzer

%description -n %{name}-strigi-analyzer
strigi-analyzer.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- wizards
%package -n %{name}-wizards
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: wizards

%description -n %{name}-wizards
wizards.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- blogilo
%package -n %{name}-blogilo
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: blogilo

%description -n %{name}-blogilo
blogilo.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- akonadi
%package -n %{name}-akonadi
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: akonadi

%description -n %{name}-akonadi
akonadi.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- akonadiconsole
%package -n %{name}-akonadiconsole
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: akonadiconsole

%description -n %{name}-akonadiconsole
akonadiconsole.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- akonadi-mailfilter-agent
%package -n %{name}-akonadi-mailfilter-agent
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: Akonadi mailfilter agent 

%description -n %{name}-akonadi-mailfilter-agent
Akonadi mailfilter agent

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- messagecore
%package -n %{name}-messagecore
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: messagecore

%description -n %{name}-messagecore
messagecore.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- messagelist
%package -n %{name}-messagelist
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: messagelist

%description -n %{name}-messagelist
messagelist.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#     <--- messageviewer
%package -n %{name}-messageviewer
Group: System/GUI/KDE
Group(zh_CN): 系统/GUI/KDE
Summary: messageviewer

%description -n %{name}-messageviewer
messageviewer.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

%prep
%setup -q -n %{real_name}-%{rversion}

#%patch0 -p1
#%patch1 -p0

#%patch600 -p0
#%patch601 -p1

#%patch100 -p0
#%patch5

#%if %build_kitchensync
#%patch1000 -p1
#%else
#%patch1001 -p0 -b .no_kicthensync
#%endif

%build
mkdir build
cd build
%cmake_kde4 -DCMAKE_SKIP_RPATH:BOOL=ON ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh
%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files -n %{name}-devel
%defattr(-,root,root)
#%{kde4_includedir}/*
%{kde4_libdir}/*.so
#%{kde4_appsdir}/cmake
#%doc %lang(en) %{kde4_htmldir}/en/kwsdl_compiler
#%exclude %{kde4_libdir}/libkpilot_akonadibase.so
#%exclude %{kde4_libdir}/libkpilot_conduit_base.so


#新增文件，暂没有分到合适的包。
%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB
#%{kde4_bindir}/akonadi_nepomuk_email_feeder
#%{kde4_bindir}/kaddressbook-mobile
%{kde4_bindir}/kincidenceeditor
#%{kde4_bindir}/kmail-mobile
#%{kde4_bindir}/korganizer-mobile
#%{kde4_bindir}/notes-mobile
#%{kde4_bindir}/tasks-mobile
%{kde4_bindir}/akonadi_sendlater_agent
%{kde4_bindir}/headerthemeeditor
#%{kde4_plugindir}/grammar_link.so
#%{kde4_plugindir}/imports/org/kde/pim/mobileui/*
%{kde4_plugindir}/kcm_kpimidentities.so
%{kde4_plugindir}/libexec/kalarm_helper
%{kde4_plugindir}/messageviewer_bodypartformatter_*.so
%{kde4_plugindir}/plasma_applet_akonotes_*.so
%{kde4_libdir}/libcalendarsupport.so.4*
%{kde4_libdir}/libeventviews.so.4*
%{kde4_libdir}/libincidenceeditorsng.so.4*
%{kde4_libdir}/libincidenceeditorsngmobile.so.4*
%{kde4_libdir}/libkdepimdbusinterfaces.so.4*
#%{kde4_libdir}/libkdepimmobileui.so.4*
%{kde4_libdir}/libkdgantt2.so.0*
%{kde4_libdir}/libkleopatraclientcore.so.0*
%{kde4_libdir}/libkleopatraclientgui.so.0*
%{kde4_libdir}/libkmanagesieve.so.4*
%{kde4_libdir}/libksieveui.so.4*
%{kde4_libdir}/libmailcommon.so.4*
%{kde4_libdir}/libmessagecomposer.so.4*
%{kde4_libdir}/libtemplateparser.so.4*
#%{kde4_libdir}/strigi/strigiea_ctg.so
%{kde4_datadir}/applications/kde4/*.desktop
%{kde4_appsdir}/akregator_sharemicroblog_plugin/akregator_sharemicroblog_plugin.rc
#%{kde4_appsdir}/blogilo/TextEditorInitialHtml
%{kde4_appsdir}/desktoptheme/default/widgets/stickynote.svgz
#%{kde4_appsdir}/kaddressbook-mobile/*
%{kde4_appsdir}/kconf_update/knode.upd
#%{kde4_appsdir}/kmail-mobile/*
%{kde4_appsdir}/kmail2/*
#%{kde4_appsdir}/kontact-touch/*
#%{kde4_appsdir}/korganizer-mobile/*
%{kde4_appsdir}/libmessageviewer/pics/*.png
%{kde4_appsdir}/messagelist/pics/mail-*.png
#%{kde4_appsdir}/messageviewer/about/main_mobile.html
#%{kde4_appsdir}/messageviewer/about/messageviewer_mobile.css
#%{kde4_appsdir}/messageviewer/plugins/bodypartformatter/*.desktop
#%{kde4_appsdir}/notes-mobile/*
#%{kde4_appsdir}/mobileui/*
#%{kde4_appsdir}/tasks-mobile/*
%{kde4_iconsdir}/hicolor/*/apps/*
%{kde4_iconsdir}/oxygen/16x16/actions/*.png
%{kde4_servicesdir}/ServiceMenus/kmail_addattachmentservicemenu.desktop
%{kde4_servicesdir}/akonotes_list.desktop
%{kde4_servicesdir}/akonotes_note.desktop
%{kde4_servicesdir}/kcm_kpimidentities.desktop
%{_datadir}/dbus-1/system-services/org.kde.kalarmrtcwake.service
%{kde4_bindir}/pimsettingexporter
%{kde4_libdir}/libpimcommon.so.*
%{kde4_appsdir}/pimsettingexporter/pimsettingexporter.rc
%{kde4_plugindir}/kcm_pimactivity.so
%{kde4_plugindir}/plugins/designer/mailcommonwidgets.so
%{kde4_plugindir}/plugins/designer/pimcommonwidgets.so
%{kde4_plugindir}/plugins/grantlee/0.4/grantlee_messageheaderfilters.so
%{kde4_libdir}/libcomposereditorng.so.*
%{kde4_libdir}/libgrammar.so.*
%{kde4_libdir}/libpimactivity.so.*
%{kde4_libdir}/libsendlater.so.*
%{kde4_datadir}/akonadi/agents/sendlateragent.desktop
%{kde4_appsdir}/akonadi_sendlater_agent/akonadi_sendlater_agent.notifyrc
%{kde4_appsdir}/composereditor/composereditorinitialhtml
%{kde4_appsdir}/headerthemeeditor/headerthemeeditorui.rc
%{kde4_appsdir}/messageviewer/*
%{kde4_configdir}/messageviewer_header_themes.knsrc
%{kde4_htmldir}/en/akonadi_archivemail_agent/*
%{kde4_htmldir}/en/akonadi_sendlater_agent/*
%{kde4_htmldir}/en/headerthemeeditor/*
%{kde4_htmldir}/en/importwizard/*
%{kde4_htmldir}/en/kmailcvt/*
%{kde4_htmldir}/en/pimsettingexporter/*
%{kde4_iconsdir}/hicolor/16x16/actions/knotes_*.png
#%{kde4_servicesdir}/grammar_link.desktop
%{kde4_servicesdir}/kcmpimactivity.desktop

%{kde4_bindir}/akonadi_folderarchive_agent
%{kde4_bindir}/calendarjanitor
%{kde4_bindir}/contactthemeeditor
%{kde4_bindir}/kaddressbook-mobile
%{kde4_bindir}/kmail-mobile
%{kde4_bindir}/korganizer-mobile
%{kde4_bindir}/mboximporter
%{kde4_bindir}/notes-mobile
%{kde4_bindir}/tasks-mobile
%{kde4_plugindir}/imports/org/kde/pim/mobileui/*
%{kde4_libdir}/libfolderarchive.so.4
%{kde4_libdir}/libfolderarchive.so.4.12.2
%{kde4_libdir}/libgrantleetheme.so.4
%{kde4_libdir}/libgrantleetheme.so.4.12.2
%{kde4_libdir}/libgrantleethemeeditor.so.4
%{kde4_libdir}/libgrantleethemeeditor.so.4.12.2
%{kde4_libdir}/libkaddressbookgrantlee.so.4
%{kde4_libdir}/libkaddressbookgrantlee.so.4.12.2
%{kde4_libdir}/libkdepimmobileui.so.4
%{kde4_libdir}/libkdepimmobileui.so.4.12.2
%{kde4_libdir}/libknotesprivate.so.4
%{kde4_libdir}/libknotesprivate.so.4.12.2
%{kde4_datadir}/akonadi/agents/folderarchiveagent.desktop
%{kde4_appsdir}/akonadi_folderarchive_agent/akonadi_folderarchive_agent.notifyrc
%{kde4_appsdir}/contactthemeeditor/contactthemeeditorui.rc
%{kde4_appsdir}/kaddressbook-mobile/*
%{kde4_appsdir}/kconf_update/grantleetheme.upd
%{kde4_appsdir}/kmail-mobile/*
%{kde4_appsdir}/kontact-touch/*
%{kde4_appsdir}/korganizer-mobile/*
%{kde4_appsdir}/mobileui/*
%{kde4_appsdir}/notes-mobile/*
%{kde4_appsdir}/pimsettingexporter/backup-structure.txt
%{kde4_appsdir}/tasks-mobile/*
%{kde4_configdir}/kaddressbook_themes.knsrc
%{kde4_configdir}/ksieve_script.knsrc
%{kde4_htmldir}/en/akonadi_folderarchive_agent/*

%files -n %{name}-akregator
%defattr(-,root,root)
%{kde4_bindir}/akregator*
%{kde4_plugindir}/akregator_*.so
%{kde4_plugindir}/akregatorpart.so
%{kde4_libdir}/libakregatorinterfaces.so.*
%{kde4_libdir}/libakregatorprivate.so.*
%{kde4_appsdir}/akregator/*
%{kde4_kcfgdir}/akregator.kcfg
%{kde4_dbus_interfacesdir}/org.kde.akregator.part.xml
%{kde4_iconsdir}/hicolor/*/apps/akregator*
%{kde4_xdgappsdir}/akregator.desktop
%{kde4_servicesdir}/akregator_*.desktop
%{kde4_servicesdir}/feed.protocol
%{kde4_servicetypesdir}/akregator_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/akregator

%files -n %{name}-console
%defattr(-,root,root)
%{kde4_bindir}/konsolekalendar
%{kde4_bindir}/kabcclient
%{kde4_bindir}/kabc2mutt
#%{kde4_appsdir}/konsolekalendar/*
%{kde4_xdgappsdir}/konsolekalendar.desktop
%{kde4_mandir}/man1/kabcclient.1*
%doc %lang(en) %{kde4_htmldir}/en/konsolekalendar
%doc %lang(en) %{kde4_htmldir}/en/kabcclient

%files -n %{name}-kaddressbook
%defattr(-,root,root)
%{kde4_bindir}/kaddressbook
%{kde4_plugindir}/kaddressbookpart.so
%{kde4_plugindir}/kcm_ldap.so
%{kde4_libdir}/libkaddressbookprivate.so.*
%{kde4_appsdir}/kaddressbook/*
%{kde4_iconsdir}/hicolor/*/apps/kaddressbook.*
%{kde4_xdgappsdir}/kaddressbook.desktop
%{kde4_servicesdir}/kaddressbookpart.desktop
%{kde4_servicesdir}/kcmldap.desktop
#%doc %lang(en) %{kde4_htmldir}/en/kaddressbook

%files -n %{name}-kalarm
%defattr(-,root,root)
%{kde4_bindir}/kalarm
%{kde4_bindir}/kalarmautostart
#%{kde4_plugindir}/kalarm_*.so
#%{kde4_libdir}/libkalarm_resources.so.*
#%{kde4_libdir}/libkalarm_calendar.so.*
%{kde4_appsdir}/kalarm
%{kde4_kcfgdir}/kalarmconfig.kcfg
%{kde4_appsdir}/kconf_update/kalarm*.pl
%{kde4_appsdir}/kconf_update/kalarm.upd
%{kde4_dbus_interfacesdir}/org.kde.kalarm.kalarm.xml
#%{kde4_iconsdir}/oxygen/*/apps/kalarm.*
%{kde4_iconsdir}/hicolor/*/apps/kalarm.*
%{kde4_datadir}/autostart/kalarm.autostart.desktop
%{kde4_xdgappsdir}/kalarm.desktop
%{_sysconfdir}/dbus-1/system.d/org.kde.kalarmrtcwake.conf
%doc %lang(en) %{kde4_htmldir}/en/kalarm

%files -n %{name}-icons
%defattr(-,root,root)
#%{kde4_iconsdir}/oxygen/*/status/mail-tagged*
%{kde4_iconsdir}/oxygen/*/mimetypes/x-mail-distribution-list.*

%if %build_kitchensync
%files -n %{name}-kitchensync
%defattr(-,root,root)
%{kde4_bindir}/kitchensync
%{kde4_libdir}/libkitchensyncprivate.so.*
%{kde4_libdir}/libqopensync.so.*
%{kde4_plugindir}/kitchensyncpart.so
%{kde4_appsdir}/kitchensync/*
%{kde4_iconsdir}/hicolor/*/apps/kitchensync.*
%{kde4_iconsdir}/hicolor/*/actions/sync-start.*
%{kde4_xdgappsdir}/kitchensync.desktop
#%doc %lang(en) %{kde4_htmldir}/en/kitchensync
%endif

%files -n %{name}-kjots
%defattr(-,root,root)
%{kde4_bindir}/kjots
%{kde4_plugindir}/kcm_kjots.so
%{kde4_plugindir}/kjotspart.so
%{kde4_appsdir}/kjots/*
%{kde4_kcfgdir}/kjots.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kjots.*
%{kde4_iconsdir}/oxygen/*/actions/edit-delete-page.*
%{kde4_xdgappsdir}/Kjots.desktop
%{kde4_servicesdir}/kjots_config_misc.desktop
%{kde4_servicesdir}/kjotspart.desktop
%doc %lang(en) %{kde4_htmldir}/en/kjots

%files -n %{name}-kleopatra
%defattr(-,root,root)
%{kde4_bindir}/kleopatra
%{kde4_bindir}/kgpgconf
%{kde4_bindir}/kwatchgnupg
%{kde4_plugindir}/kcm_kleopatra.so
# %{kde4_libdir}/libkleopatraclientcore.so.*
# %{kde4_libdir}/libkleopatraclientgui.so.*
%{kde4_appsdir}/kleopatra/*
%{kde4_appsdir}/kwatchgnupg/*
%{kde4_appsdir}/kconf_update/kpgp-*
%{kde4_appsdir}/kconf_update/kpgp.upd
#%{kde4_iconsdir}/oxygen/*/apps/kleopatra.*
%{kde4_xdgappsdir}/kleopatra.desktop
%{kde4_xdgappsdir}/kleopatra_import.desktop
%{kde4_servicesdir}/kleopatra_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/kleopatra
%doc %lang(en) %{kde4_htmldir}/en/kwatchgnupg

%files -n %{name}-kmail
%defattr(-,root,root)
%{kde4_bindir}/kmail
%{kde4_bindir}/kmail_*.sh
%{kde4_plugindir}/kcm_kmail.so
%{kde4_plugindir}/kmailpart.so
%{kde4_libdir}/libkmailprivate.so.*
#%{kde4_appsdir}/kmail/*
%{kde4_appsdir}/kconf_update/kmail-*
%{kde4_appsdir}/kconf_update/kmail.upd
%{kde4_appsdir}/kconf_update/upgrade-signature.pl
%{kde4_appsdir}/kconf_update/upgrade-transport.pl
%{kde4_kcfgdir}/kmail.kcfg
%{kde4_kcfgdir}/customtemplates_kfg.kcfg
%{kde4_kcfgdir}/templatesconfiguration_kfg.kcfg
%config %{kde4_configdir}/kmail.antispamrc
%config %{kde4_configdir}/kmail.antivirusrc
%{kde4_dbus_interfacesdir}/org.kde.kmail.*.xml
%{kde4_iconsdir}/hicolor/*/apps/kmail.*
%{kde4_xdgappsdir}/kmail_view.desktop
%{kde4_servicesdir}/kmail_*.desktop
%{kde4_servicetypesdir}/dbusmail.desktop
%doc %lang(en) %{kde4_htmldir}/en/kmail
# plugin 部分文件
#以下需要重分包
%{kde4_bindir}/akonadi_archivemail_agent
#%{kde4_bindir}/backupmail
%{kde4_bindir}/importwizard
%{kde4_bindir}/ktnef
%{kde4_libdir}/libmailimporter.so.*
%{kde4_datadir}/akonadi/agents/archivemailagent.desktop
%{kde4_appsdir}/akonadi_archivemail_agent/akonadi_archivemail_agent.notifyrc
%{kde4_appsdir}/akonadi_mailfilter_agent/akonadi_mailfilter_agent.notifyrc
#%{kde4_appsdir}//backupmail/backupmail.rc
%{kde4_appsdir}//ktnef/ktnefui.rc
%{kde4_htmldir}/en/ktnef/*
%{kde4_iconsdir}/*color/*/a*/ktnef*.*
%{kde4_datadir}/ontology/kde/messagetag.ontology
%{kde4_datadir}/ontology/kde/messagetag.trig

%files -n %{name}-kmailcvt
%defattr(-,root,root)
%{kde4_bindir}/kmailcvt
%{kde4_appsdir}/kmailcvt/*
#%{kde4_iconsdir}/oxygen/*/apps/kmailcvt.*
#%doc %lang(en) %{kde4_htmldir}/en/
#可能不属于这个包

%files -n %{name}-akonadi-mailfilter-agent
%{kde4_bindir}/akonadi_mailfilter_agent
%{kde4_plugindir}/plugins/accessible/messagevieweraccessiblewidgetfactory.so
#%{kde4_libdir}/strigi/strigiea_mail.so
%{kde4_datadir}/akonadi/agents/mailfilteragent.desktop
%{kde4_datadir}/apps/kconf_update/mailfilteragent.upd
%{kde4_datadir}/apps/kconf_update/migrate-kmail-filters.pl
%{kde4_auth_policy_filesdir}/org.kde.kalarmrtcwake.policy

%files -n %{name}-knode
%defattr(-,root,root)
%{kde4_bindir}/knode
%{kde4_plugindir}/kcm_knode.so
%{kde4_plugindir}/knodepart.so
%{kde4_libdir}/libknodecommon.so.*
%{kde4_appsdir}/knode/*
%{kde4_dbus_interfacesdir}/org.kde.knode.xml
%{kde4_iconsdir}/hicolor/*/apps/knode*
%{kde4_xdgappsdir}/KNode.desktop
#%{kde4_servicesdir}/knewsservice.protocol
%{kde4_servicesdir}/knode_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/knode
%doc %lang(en) %{kde4_htmldir}/en/kioslave/news

%files -n %{name}-knotes
%defattr(-,root,root)
%{kde4_bindir}/knotes
%{kde4_plugindir}/kcm_knote.so
%{kde4_plugindir}/knotes_local.so
%{kde4_appsdir}/knotes/*
%{kde4_kcfgdir}/knoteconfig.kcfg
%{kde4_kcfgdir}/knotesglobalconfig.kcfg
%{kde4_dbus_interfacesdir}/org.kde.KNotes.xml
%{kde4_iconsdir}/hicolor/*/apps/knotes.*
%{kde4_xdgappsdir}/knotes.desktop
%{kde4_servicesdir}/kresources/knotes/local.desktop
%{kde4_servicesdir}/kresources/knotes_manager.desktop
%{kde4_servicesdir}/knote_config_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/knotes

# kontactpart 引用文件
%exclude %{kde4_appsdir}/knotes/knotes_part.rc

%files -n %{name}-kontact
%defattr(-,root,root)
%{kde4_bindir}/kontact
%{kde4_plugindir}/kontact_*plugin.so
%{kde4_plugindir}/kcm_*summary.so
#%{kde4_plugindir}/kcm_planner.so
%{kde4_plugindir}/kcm_kontact.so
%{kde4_libdir}/libkontactprivate.so.*
%{kde4_appsdir}/kontact/*
%{kde4_appsdir}/kontactsummary/*
%{kde4_appsdir}/knotes/knotes_part.rc
%{kde4_kcfgdir}/kontact.kcfg
%{kde4_dbus_interfacesdir}/org.kde.kontact.KNotes.xml
%{kde4_iconsdir}/hicolor/*/apps/kontact*
%{kde4_xdgappsdir}/Kontact.desktop
%{kde4_xdgappsdir}/kontact-admin.desktop
%{kde4_servicesdir}/kontact/*
%{kde4_servicesdir}/kcm*summary.desktop
#%{kde4_servicesdir}/kcmplanner.desktop
%{kde4_servicesdir}/kontactconfig.desktop
%doc %lang(en) %{kde4_htmldir}/en/kontact
%doc %lang(en) %{kde4_htmldir}/en/kontact-admin

%files -n %{name}-korganizer
%defattr(-,root,root)
%{kde4_bindir}/korganizer
%{kde4_bindir}/korgac
%{kde4_bindir}/ical2vcal
%{kde4_plugindir}/kcm_korganizer.so
%{kde4_plugindir}/korganizerpart.so
%{kde4_plugindir}/korg_*.so
#%{kde4_libdir}/libkorganizer_eventviewer.so.*
#%{kde4_libdir}/libkorganizer_calendar.so.*
%{kde4_libdir}/libkorganizerprivate.so.*
%{kde4_libdir}/libkorganizer_core.so.*
#%{kde4_libdir}/libkorg_stdprinting.so.*
%{kde4_libdir}/libkorganizer_interfaces.so.*
%{kde4_appsdir}/korganizer/*
%{kde4_appsdir}/korgac/*
%{kde4_appsdir}/kconf_update/korganizer.upd
%config %{kde4_configdir}/korganizer.knsrc
%{kde4_kcfgdir}/korganizer.kcfg
%{kde4_datadir}/autostart/korgac.desktop
%{kde4_dbus_interfacesdir}/org.kde.Korganizer.Calendar.xml
%{kde4_dbus_interfacesdir}/org.kde.korganizer.KOrgac.xml
%{kde4_dbus_interfacesdir}/org.kde.korganizer.Korganizer.xml
%{kde4_iconsdir}/oxygen/*/actions/smallclock.*
%{kde4_iconsdir}/oxygen/*/actions/upindicator.*
%{kde4_iconsdir}/oxygen/*/actions/checkmark.*
%{kde4_iconsdir}/hicolor/*/apps/korganizer.*
%{kde4_xdgappsdir}/korganizer*.desktop
%{kde4_servicesdir}/korganizer_*.desktop
%{kde4_servicesdir}/webcal.protocol
%{kde4_servicetypesdir}/dbuscalendar.desktop
%{kde4_servicesdir}/korganizer/*
%{kde4_servicetypesdir}/calendardecoration.desktop
%{kde4_servicetypesdir}/calendarplugin.desktop
%{kde4_servicetypesdir}/korganizerpart.desktop
%{kde4_servicetypesdir}/korgprintplugin.desktop
%doc %lang(en) %{kde4_htmldir}/en/korganizer

%if 0
%files -n %{name}-kpilot
%defattr(-,root,root)
%{kde4_bindir}/kpilot
%{kde4_bindir}/kpilotDaemon
%{kde4_plugindir}/kcm_kpilot.so
%{kde4_plugindir}/kpilot_*.so
%{kde4_libdir}/libkpilot.so.*
#%{kde4_libdir}/libkpilot_akonadibase.so
#%{kde4_libdir}/libkpilot_conduit_base.so
%{kde4_appsdir}/kpilot/*
%{kde4_appsdir}/kconf_update/kpilot.upd
%{kde4_kcfgdir}/calendarsettings.kcfg
%{kde4_kcfgdir}/contactssettings.kcfg
%{kde4_kcfgdir}/kpilotlib.kcfg
%{kde4_kcfgdir}/kpilot.kcfg
%{kde4_kcfgdir}/memofileconduit.kcfg
%{kde4_kcfgdir}/timeconduit.kcfg
%{kde4_kcfgdir}/todosettings.kcfg
%{kde4_iconsdir}/hicolor/*/apps/kpilotdaemon.*
%{kde4_iconsdir}/hicolor/*/apps/kpilot.*
%{kde4_iconsdir}/hicolor/*/actions/kpilot_*.*
%{kde4_xdgappsdir}/kpilot*.desktop
%{kde4_servicesdir}/kpilot_config.desktop
%{kde4_servicesdir}/*-conduit.desktop
%{kde4_servicesdir}/time_conduit.desktop
%{kde4_servicetypesdir}/kpilotconduit.desktop
%{kde4_servicesdir}/kpilot-conduit-*.desktop
%doc %lang(en) %{kde4_htmldir}/en/kpilot
%endif

%files -n %{name}-kresources
%defattr(-,root,root)
%{kde4_plugindir}/kcal_remote.so
%{kde4_plugindir}/kcal_blog.so
%{kde4_libdir}/libkcal_resourceremote.so.*
%{kde4_libdir}/libkcal_resourceblog.so.*
%{kde4_servicesdir}/kresources/*

%files -n %{name}-ksendemail
%defattr(-,root,root)
%{kde4_bindir}/ksendemail

%files -n %{name}-ktimetracker
%defattr(-,root,root)
%{kde4_bindir}/karm
%{kde4_bindir}/ktimetracker
%{kde4_plugindir}/kcm_ktimetracker.so
%{kde4_plugindir}/ktimetrackerpart.so
%{kde4_appsdir}/ktimetracker/*
%{kde4_dbus_interfacesdir}/org.kde.ktimetracker.ktimetracker.xml
%{kde4_iconsdir}/hicolor/*/apps/ktimetracker.*
%{kde4_xdgappsdir}/ktimetracker.desktop
%{kde4_servicesdir}/ktimetrackerpart.desktop
%{kde4_servicesdir}/ktimetracker_config_*.desktop
%doc %lang(en) %{kde4_htmldir}/en/ktimetracker

%files -n %{name}-libkdepim
%defattr(-,root,root)
%{kde4_plugindir}/plugins/designer/kdepimwidgets.so
#%{kde4_plugindir}/kpartsdesignerplugin.so
%{kde4_libdir}/libkdepim.so.*
#%{kde4_appsdir}/libkdepim/*
%{kde4_appsdir}/kdepimwidgets/pics/addresseelineedit.png
%{kde4_appsdir}/kdepimwidgets/pics/clicklineedit.png
%{kde4_appsdir}/kdepimwidgets/pics/kdateedit.png
%{kde4_appsdir}/kdepimwidgets/pics/ktimeedit.png
%{kde4_dbus_interfacesdir}/org.kde.addressbook.service.xml
%{kde4_dbus_interfacesdir}/org.kde.mailtransport.service.xml
#%{kde4_iconsdir}/oxygen/*/actions/button_fewer.png
#%{kde4_iconsdir}/oxygen/*/actions/button_more.png

%files -n %{name}-libkleo
%defattr(-,root,root)
%{kde4_libdir}/libkleo.so.*
%{kde4_appsdir}/libkleopatra/*
%config %{kde4_configdir}/libkleopatrarc

%files -n %{name}-libkpgp
%defattr(-,root,root)
%{kde4_libdir}/libkpgp.so.*

%files -n %{name}-libksieve
%defattr(-,root,root)
%{kde4_libdir}/libksieve.so.*

%if 0
%files -n %{name}-mimelib
%defattr(-,root,root)
%{kde4_libdir}/libmimelib.so.*
%endif

%files -n %{name}-plugins
%defattr(-,root,root)
#%{kde4_plugindir}/kmail_bodypartformatter_text_vcard.so
#%{kde4_plugindir}/kmail_bodypartformatter_text_calendar.so
#%{kde4_plugindir}/kmail_bodypartformatter_text_xdiff.so
%{kde4_libdir}/akonadi/contact/editorpageplugins/cryptopageplugin.so
#%{kde4_appsdir}/kmail/plugins/bodypartformatter/text_vcard.desktop
#%{kde4_appsdir}/kmail/plugins/bodypartformatter/text_calendar.desktop
#%{kde4_appsdir}/kmail/plugins/bodypartformatter/text_xdiff.desktop
%{kde4_plugindir}/ktexteditorkabcbridge.so

%files -n %{name}-strigi-analyzer
%defattr(-,root,root)
#%{kde4_libdir}/strigi/strigiea_vcf.so
#%{kde4_libdir}/strigi/strigiea_ics.so

%files -n %{name}-blogilo
%defattr(-,root,root)
%{kde4_bindir}/blogilo
%{kde4_xdgappsdir}/blogilo.desktop
%{kde4_appsdir}/blogilo/blogiloui.rc
%{kde4_kcfgdir}/blogilo.kcfg
%{kde4_iconsdir}/hicolor/*/apps/blogilo.*
%{kde4_iconsdir}/hicolor/*/actions/format-text-blockquote.png
%{kde4_iconsdir}/hicolor/*/actions/format-text-code.png
%{kde4_iconsdir}/hicolor/*/actions/insert-more-mark.png
%{kde4_iconsdir}/hicolor/*/actions/remove-link.png
%{kde4_iconsdir}/hicolor/*/actions/upload-media.png
%doc %lang(en) %{kde4_htmldir}/en/blogilo/*

%files -n %{name}-akonadi
%defattr(-,root,root)
#%{kde4_libdir}/libakonadi-kcal_next.so.*
%{kde4_libdir}/libakonadi_next.so.*

%files -n %{name}-akonadiconsole
%defattr(-,root,root)
%{kde4_bindir}/akonadiconsole
%{kde4_appsdir}/akonadiconsole/*
%{kde4_xdgappsdir}/akonadiconsole.desktop

%files -n %{name}-messagecore
%defattr(-,root,root)
%{kde4_libdir}/libmessagecore.so.*

%files -n %{name}-messagelist
%defattr(-,root,root)
%{kde4_libdir}/libmessagelist.so.*

%files -n %{name}-messageviewer
%defattr(-,root,root)
%{kde4_libdir}/libmessageviewer.so.*
# %{kde4_appsdir}/libmessageviewer/*


%changelog
* Wed Aug 5 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.3.0-1mgc
- 更新至 4.3.0
- 己丑  六月十五

* Tue Jun 30 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.95-1mgc
- kdepim-akonadi 自 KDE 4.3 RC1 起独立
- 更新至 4.2.95(KDE 4.3 RC1)
- 清理 spec 文件
- 己丑  闰五月初八

* Sat Jun 13 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.91-1mgc
- 更新至 4.2.91
- 己丑  五月廿一

* Sun May 17 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.85-1mgc
- 更新至 4.2.85(KDE 4.3 beta1)
- 己丑  四月廿三

* Sat Apr 4 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.2-1mgc
- 更新至 4.2.2
- 己丑  三月初九  [清明]

* Sun Mar 8 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.1-0.1mgc
- 更新至 4.2.1
- 己丑  二月十二

* Sun Jan 25 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.2.0-0.1mgc
- 更新至 4.2.0
- 戊子  十二月三十

* Wed Jan 14 2009 Ni Hui <shuizhuyuanluo@126.com> - 4.1.96-0.1mgc
- 更新至 4.1.96(KDE 4.2 RC1)
- relwithdeb 编译模式
- 戊子  十二月十九

* Sat Dec 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.85-0.1mgc
- 更新至 4.1.85(KDE 4.2 Beta2)
- 戊子  十一月十六

* Sun Dec 1 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.80-0.1mgc
- 更新至 4.1.80
- %build_kpilot_avantgo_conduit 开关关闭
- %build_kitchensync 开关关闭，不编译 kitchensync 组件
- 新设立 ksendmail，恢复 kpilot
- 戊子  十一月初三

* Fri Nov 07 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.3-0.1mgc
- 更新至 4.1.3
- 戊子  十月初十  [立冬]

* Mon Sep 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.2-0.1mgc
- 更新至 4.1.2
- 打包 kitchensync
- 对 akregator 默认添加一些中文网站种子(patch 1 written by nihui)
- 编译依赖：libopensync-devel >= 0.33
- 戊子  九月初一

* Sat Aug 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.1.1-0.1mgc
- 更新至 4.1.1
- 戊子  七月三十

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.1.0-0.1mgc
- 更新到 4.1.0(KDE 4.1 正式版)

* Fri Jul 11 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.98-0.1mgc
- 更新至 4.0.98(KDE 4.1 RC1)
- 戊子  六月初九

* Sat Jun 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.84-0.1mgc
- 更新至 4.0.84
- 戊子  五月廿五

* Thu Jun 19 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.83-0.1mgc
- 更新至 4.0.83-try1(第一次 tag 4.1.0-beta2 内部版本)
- 戊子  五月十六

* Thu Jun 12 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.82-0.1mgc
- 更新至 4.0.82
- 戊子  五月初九

* Wed Jun 4 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.81-0.1mgc
- 更新至 4.0.81
- kmobiletools 和 kpilot 已经去除
- 戊子  五月初一

* Sat May 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.80-0.1mgc
- 更新至 4.0.80(try1 内部版本)
- 细化分包
- 戊子  四月二十

* Sat Apr 26 2008 Ni Hui <shuizhuyuanluo@126.com> - 4.0.71-0.1mgc
- 更新至 4.0.71
- 定义 kde4 路径
- 戊子  三月廿一

* Sat Nov 24 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.96.0-0.1mgc
- 更新至 3.96.0 (KDE4-RC1)

* Sat Oct 20 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.94.0-0.1mgc
- 首次生成 rpm 包
