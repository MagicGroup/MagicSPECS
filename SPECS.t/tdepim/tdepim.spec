%define debug 0
%define final 0

%define git 1
%define gitdate 20111221

%define qt_version 3.3.8d
%define arts_version 1.5.14

%define arts 1
%define libtool 1

%define _iconsdir %_datadir/icons

Summary: KDE personal Information Management tools
Summary(zh_CN.GB18030): KDE 个人信息管理工具
Name:          tdepim
Version:       3.5.14
%if %{git}
Release:       0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:		GPL
URL:		http://www.kde.org
Group:         Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source:	     %{name}-git%{gitdate}.tar.xz
%else
Source:      ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Patch1:      knode-cjk.patch 
Patch2:      kdepim-kontact_Makefile.am.patch
Patch3:	     kdepim-gcc44.patch
#Source10: cr48-app-kandy.png
#Source11: cr32-app-kandy.png
#Source12: cr16-app-kandy.png

#Patch101: kdepim-3.4.0-kandy-icons.patch
Patch102: kdepim-xdg_open.patch
# patch by Dirk Müller from openSUSE to fix gnokii detection
Patch6: kdepim-3.5.9-gnokii-no-libintl.patch
# http://websvn.kde.org/?view=rev&revision=775015
# http://bugs.kde.org/show_bug.cgi?id=127696
# Upstream fix for "Unable to complete LIST operation" errors with some servers,
# just missed the 3.5.9 tagging.
Patch4: kdepim-3.5.9-kde#127696.patch
Patch5: kdepim-3.5.10-gnokii.patch
 
## upstream patches
Patch100: kdepim-3.5.x-kmail-imap-crash.patch

# upstream patches
# LANG=en_US.UTF-8 svn diff svn://anonsvn.kde.org/home/kde/tags/KDE/3.5.9/kdepim/kitchensync@774532 \
# svn://anonsvn.kde.org/home/kde/branches/work/kitchensync-OpenSync0.30API@774532 >kdepim-3.5.9-opensync03.patch
# Patch3: kdepim-3.5.9-opensync03.patch
# from gentoo project
Patch9: kitchensync-3.5.9-OpenSync0.30API.patch

Patch1000: kitchensync-3.5.13-OpenSync0.37API_at_least_build.patch

Requires: tdelibs, tdebase, tdenetwork, efax, libmal
BuildRequires: tdelibs-devel, tdebase-devel, tdenetwork-devel, libopensync-devel, libmal-devel
Requires: %{name}-common
Requires: %{name}-kmail
Requires: %{name}-knode
Requires: %{name}-akregator

%description
A PIM (Personal Information Manager) for KDE.

%descrition -l zh_CN.GB18030
KDE 下的 PIM(个人信息管理程序)。

%package common
Summary: Common files for kdepim
Summary(zh_CN.GB18030): %{name} 的公用文件
Group:         Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力

%description common
Common files for kdepim

%description common -l zh_CN.GB18030
%{name} 的公用文件。

#===========================================================================================

%package kitchensync
Group: Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Summary: Multiple backend sync program
Summary(zh_CN.GB18030): 多种后端的同步程序
Provides: kitchensync
Requires: %{name}-common = %{version}-%{release}
Conflicts: kdenetwork-common < 3.5.7
 
%description kitchensync
kitchensync is a multiple backend sync program

%description kitchensync -l zh_CN.GB18030
多种后端的同步程序。

#=========================================================================================

%package wizards
Summary: Kdepim groupware wizards
Summary(zh_CN.GB18030): Kdepim 组件向导
Group: Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Conflicts: tdepim-common < 3.5.7
Conflicts: kdepim-kontact < 3.5.7
Requires: %{name}-common = %{version}-%{release}
 
%description wizards
This kdepim groupware wizards. This package provides transition tool to setup
or migrate groupware
accounts from some common existing groupware solutions on market.

%description wizards -l zh_CN.GB18030
Kdepim 组件向导。这个包提供了从已有的组件中设置或合并组件账号的转换工具。 

#======================================================================================

%package korn
Group:      Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Summary:    Mail checker
Summary(zh_CN.GB18030): 邮件检查器
Provides:       korn
Conflicts:  kdenetwork <= 3.1.92
Provides:       kdenetwork-korn = %version-%release
Requires:       tdepim-common = %version-%release
Conflicts:      %name-kontact < 3.5.8-1
 
%description korn
A mail checker

%description korn -l zh_CN.GB18030
一个邮件检查器。

#====================================================================================

%package kandy
Group:      Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Summary:    A mobile simple sync tool
Summary(zh_CN.GB18030): 一个简单的手机同步工具
Provides:       kandy
Requires:       tdepim-common = %version-%release
 
%description kandy
A mobile simple sync tool

%description kandy -l zh_CN.GB18030
一个简单的手机同步工具。

#===================================================================================

%package akregator
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Summary:        KDE RSS aggregator with great look and feel
Summary(zh_CN.GB18030):	KDE 下的 RSS 阅读器
Provides:       akregator = %version-%release
Requires:       tdepim-common = %version-%release
Conflicts:      %name-kontact < 3.5.8-1
 
%description akregator
aKregator is KDE RSS aggregator with great look and feel.

%description akregator -l zh_CN.GB18030
aKregator 是一个 KDE 下的 RSS 阅读器，有非常好的界面和操作。

#==================================================================================

%package kmail
Group:      Applications/Internet
Group(zh_CN.GB18030): 应用程序/互联网
Summary:    KDE Mailer
Summary(zh_CN.GB18030): KDE 邮件程序
Requires:   tdepim-common = %version-%release
Provides:   kmail
Requires:   kdebase-core
 
%description kmail
KDE Mailer

%description kmail -l zh_CN.GB18030
KDE 邮件程序。

#=================================================================================

%package knode
Group:      Applications/Internet
Group(zh_CN.GB18030): 应用程序/互联网
Summary:    KDE News Reader
Summary(zh_CN.GB18030): KDE 新闻组阅读器
Requires:   tdepim-common = %version-%release
Provides:       knode
 
%description knode
KDE News Reader.

%description knode -l zh_CN.GB18030
KDE 新闻组阅读器。

#===================================================================================================

%package karm
Summary:        Karm program
Summary(zh_CN.GB18030): Karm 程序
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:       karm
Requires:	%{name}-common = %{version}-%{release}
 
%description karm
Time tracker.

%description karm -l zh_CN.GB18030
时间跟踪器。

#===============================================================================================

%package ktnef
Summary:    KDE TNEF Viewer
Group:      Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:   ktnef
Requires:   %{name}-common >= %version-%release
 
%description ktnef
KDE TNEF Viewer。

%description ktnef -l zh_CN.GB18030
KDE 下的 TNEF 查看器。

#==============================================================================================

%package knotes
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Summary:        A color configurable tooltip notes application for desktop
Summary(zh_CN.GB18030): 桌面即时贴程序
Provides:       knotes
 
%description knotes
A color configurable tooltip notes application for desktop

%description knotes -l zh_CN.GB18030
KNotes是KDE工程中的一个可用而且外观漂亮的notes应用程序。 

KNotes可以胜任的:

接受拖放操作(甚至可以是远端的FTP站点) 
将你的note作为邮件发送 
打印你的note(试一试，看起来是非常棒 ) 
插入日期或当月的日历 
将定时器与note关联起来，时间到了会通知你. 
可以为背景和文本选择任意的颜色 

#=====================================================================================================

%package kaddressbook
Summary:        Kaddressbook program
Summary(zh_CN.GB18030): KDE 地址本程序
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:       kaddressbook
Requires: 	%{name}-common = %{version}-%release
 
%description kaddressbook
The KDE addressbook application.

%description kaddressbook -l zh_CN.GB18030
KDE 地址本程序。

#===================================================================================================

%package korganizer
Summary:        Korganizer program
Summary(zh_CN.GB18030): KDE 下的日历和行程管理程序
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:       korganizer
Provides:       kalarm
Provides:       kalarmd
Requires:       tdepim-common = %version-%release
 
%description korganizer
A calendar-of-events and todo-list manager.

%description korganizer -l zh_CN.GB18030
KDE 下的日历和行程管理程序。

#==============================================================================================---

%package kpilot
Summary:        Kpilot program
Summary(zh_CN.GB18030): Palm 同步程序
Group:          Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:       kpilot
Provides:       kpilotDaemon
Requires:       %name-common = %version-%release
 
%description kpilot
To sync with your PalmPilot
Sync phone book entries between your palmtop and computer

%description kpilot -l zh_CN.GB18030
同步 Palm 的电话本的程序。

#===============================================================================================

%package kontact
Summary:   Kontact program
Summary(zh_CN.GB18030): 一个集成个人信息管理程序
Group:     Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Provides:  kontact
Requires:  %name-common >= %version-%release
 
%description kontact
KDE Kontact, an integrated personal information suite container application for
KDE.

%description kontact -l zh_CN.GB18030
一个集成个人信息管理程序。

#============================================================================================

%package devel
Summary: Development files for kdepim
Summary(zh_CN.GB18030): kdepim 的开发文件
Group: Development/Libraries
Group(zh_CN.GB18030): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: kdelibs-devel >= %{version}

%description devel
Development files for %{name}.
Install %{name}-devel if you want to write or compile %{name} plugins.

%description devel -l zh_CN.GB18030
%{name} 的开发文件。

%package extras
Summary: extra files for kdepim
Summary(zh_CN.GB18030): kdepim 的额外组件
Group:         Applications/Productivity
Group(zh_CN.GB18030):  应用程序/生产力
Requires: %{name} = %{version}-%{release}
Requires: libopensync > 0.30

%description extras
extra files for %{name}.
Install %{name}-extra if you want to install extra apps.

%description extras -l zh_CN.GB18030
%{name} 额外组件。


%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q -n %{name}-%{version}
%endif

#%patch3 -p1

%patch102 -p1 -b .xdg_open
%patch5 -p1

#%patch1000 -p1

for i in `grep -rl "localtdedir" *`;do sed -i 's/localtdedir/localkdedir/g' $i;done

%build
mkdir build
cd build
%cmake 	-DWITH_ARTS=ON \
	-DWITH_SASL=ON \
	-DWITH_NEWDISTRLISTS=ON \
	-DWITH_GNOKII=ON \
	-DWITH_EXCHANGE=ON \
	-DWITH_EGROUPWARE=ON \
	-DWITH_KOLAB=ON \
	-DWITH_SLOX=ON \
	-DWITH_GROUPWISE=ON \
	-DWITH_FEATUREPLAN=ON \
	-DWITH_GROUPDAV=ON \
	-DWITH_BIRTHDAYS=ON \
	-DWITH_NEWEXCHANGE=ON \
	-DWITH_SCALIX=ON \
	-DWITH_CALDAV=ON \
	-DWITH_CARDDAV=ON \
	-DWITH_INDEXLIB=ON \
	-DBUILD_ALL=ON ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

%clean 
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/kabcdistlistupdater
/usr/share/autostart/kabcdistlistupdater.desktop

%files devel
%defattr(-,root,root)
%_includedir/*


%if 0
%files kitchensync
%defattr(-,root,root,-)
%_bindir/kitchensync
%dir %_datadir/apps/kitchensync
%_datadir/apps/kitchensync/*
%_libdir/trinity/libkitchensyncpart.*
%_libdir/libkitchensync.*
%_libdir/libqopensync.*
%_datadir/applications/kde/kitchensync.desktop
%_datadir/icons/*/*/*/kitchensync*
%endif

%files wizards
%defattr(-,root,root)
%_datadir/applications/kde/groupwarewizard.desktop
%_bindir/*wizard
%_libdir/trinity/*wizard.*

%files korn
%defattr(-,root,root,-)
%doc %_docdir/kde/HTML/en/korn
%_bindir/korn
%_datadir/applications/kde/KOrn.desktop
%_datadir/apps/kconf_update/korn-*
%_libdir/kconf_update_bin/korn-3-4-config_change
%_datadir/icons/*/*/*/korn*

%files kandy
%defattr(-,root,root,-)
%_bindir/kandy
%_bindir/kandy_client
%doc %_docdir/kde/HTML/en/kandy
%_datadir/applications/kde/kandy.desktop
%dir %_datadir/apps/kandy/
%_datadir/apps/kandy/*
%_datadir/config.kcfg/kandy.kcfg
%_datadir/applnk/Utilities/kandy.desktop

%files akregator
%defattr(-,root,root,0755)
%_bindir/akregator
%_libdir/trinity/libakregator*
%_libdir/libakregatorprivate.*
%_datadir/services/kontact/akregatorplugin.desktop
%_datadir/applications/kde/akregator.desktop
%dir %_datadir/apps/akregator
%_datadir/apps/akregator/*
%_iconsdir/*/*/*/rss_tag*
%_iconsdir/*/*/*/akregator*
%_datadir/services/akregator_part.desktop
%_datadir/config.kcfg/akregator.kcfg
%_datadir/services/feed.protocol
%_datadir/services/kontact/akregatorplugin3.2.desktop
%doc %_docdir/kde/HTML/en/akregator
%_datadir/services/akregator_mk4storage_plugin.desktop
%_datadir/servicetypes/akregator_plugin.desktop

%files kmail
%defattr(-,root,root,-)
%_bindir/kmail
%_bindir/kmailcvt
%_bindir/kmail_antivir.sh
%_bindir/kmail_clamav.sh
%_bindir/kmail_fprot.sh
%_bindir/kmail_sav.sh
%_bindir/indexlib-config
%_libdir/trinity/kcm_kmail.*
%_libdir/trinity/kcm_kmailsummary.*
%_libdir/libkmailprivate.*
%_libdir/trinity/libkmailpart.*
%_libdir/trinity/libkmail_*
%_datadir/services/kcmkmailsummary.desktop
%_datadir/services/kmail_*
%_datadir/services/kontact/kmailplugin.desktop
%_datadir/apps/kconf_update/kmail*
%_datadir/applications/kde/KMail.desktop
%_iconsdir/*/*/*/gpg*
%_iconsdir/*/*/*/kmail*
%dir %_datadir/apps/kmail
%_datadir/apps/kmail/*
%_datadir/config/kmail.antivirusrc
%_datadir/applnk/Utilities/kmailcvt.desktop
%_datadir/applications/kde/kmail_view.desktop
%_datadir/config/kmail.antispamrc
%_datadir/apps/kconf_update/upgrade-signature.pl
%_datadir/apps/kconf_update/upgrade-transport.pl
%doc %_docdir/kde/HTML/en/kmail
%dir %_datadir/apps/kmailcvt/
%_datadir/apps/kmailcvt/*
%_datadir/servicetypes/dcopmail.desktop
%_libdir/libindex.so.*
%_libdir/libindex.la

%files knode
%defattr(-,root,root,-)
%_bindir/knode
%_libdir/trinity/libknodepart.*
%_datadir/services/knewsservice.protocol
%_datadir/services/kontact/knodeplugin.desktop
%_datadir/services/kontact/newstickerplugin.desktop
%_datadir/applications/kde/KNode.desktop
%_iconsdir/*/*/*/knode*
%doc %_docdir/kde/HTML/en/knode/*
%dir %_datadir/apps/knode
%_datadir/apps/knode/*
%_datadir/services/knode_*
%_libdir/trinity/kcm_knode.*
%_libdir/libknodecommon.so.*
%_libdir/libknodecommon.la

%files karm
%defattr(-,root,root)
%doc %_docdir/kde/HTML/en/karm
%_bindir/karm
%_datadir/applnk/Utilities/karm.desktop
%_datadir/services/karm_part.desktop
%_datadir/services/kontact/karmplugin.desktop
%_iconsdir/*/*/*/karm*
%_libdir/trinity/libkarmpart.*
%dir %_datadir/apps/karm/
%_datadir/apps/karm/*
%_datadir/applications/kde/karm.desktop
%dir %_datadir/apps/karmpart
%_datadir/apps/karmpart/*

%files ktnef
%defattr(-,root,root,-)
%_bindir/ktnef
%dir %_datadir/apps/ktnef/
%_datadir/apps/ktnef/*
%_iconsdir/*/*/*/ktnef*
%doc %_docdir/kde/HTML/en/ktnef/*
%_datadir/applications/kde/ktnef.desktop
%_datadir/mimelnk/application/ms-tnef.desktop
%_libdir/libktnef.la
%_libdir/libktnef.so.*

%files knotes
%defattr(-,root,root)
%_bindir/knotes
%doc %_docdir/kde/HTML/en/knotes
%dir %_datadir/apps/knotes/
%_datadir/apps/knotes/*
%_libdir/trinity/knotes_*
%_iconsdir/*/*/*/knotes*
%_datadir/applications/kde/knotes.desktop
%_datadir/services/kresources/knotes/kolabresource.desktop
%_datadir/services/kresources/knotes_manager.desktop
%_datadir/services/kontact/knotesplugin.desktop

%files kaddressbook
%defattr(-,root,root)
%_bindir/kaddressbook
%_bindir/kabc2mutt
%doc %_docdir/kde/HTML/en/kaddressbook
%dir %_datadir/apps/kaddressbook
%_datadir/apps/kaddressbook/*
%_iconsdir/*/*/*/kaddressbook*
%_datadir/applications/kde/kaddressbook.desktop
%_datadir/services/kfile_ics.desktop
%_datadir/services/kfile_vcf.desktop
%_libdir/trinity/kabc_*
%_libdir/trinity/kfile_vcf.*
%_libdir/trinity/kfile_ics.*
%_libdir/trinity/libkaddressbookpart.*
%_libdir/trinity/kcm_kabconfig.*
%_libdir/trinity/kcm_kabldapconfig.*
%_libdir/trinity/libkaddrbk_*.*
%_libdir/trinity/ldifvcardthumbnail.*
%_libdir/trinity/kcm_kabcustomfields.*
%dir %_datadir/services/kaddressbook/
%_datadir/services/kaddressbook/*
%_datadir/services/kabconfig.desktop
%_datadir/services/kabldapconfig.desktop
%_datadir/services/ldifvcardthumbnail.desktop
%_datadir/servicetypes/dcopaddressbook.desktop
%_datadir/servicetypes/kaddressbook_*
%_datadir/services/kontact/kaddressbookplugin.desktop
%_datadir/services/kabcustomfields.desktop
%dir %_datadir/services/kresources/kabc/
%_datadir/services/kresources/kabc/*
%_libdir/libkaddressbook.la
%_libdir/libkaddressbook.so.*
%_libdir/libkabinterfaces.so.*
%_libdir/libkabinterfaces.la
%_libdir/libkabc*.la
%_libdir/libkabc*.so.*

%files korganizer
%defattr(-,root,root)
%_bindir/kalarm
%_bindir/kalarmd
%_bindir/konsolekalendar
%_bindir/korgac
%_bindir/korganizer
%_bindir/ical2vcal
%_datadir/apps/kconf_update/korganizer.upd
%dir %_datadir/apps/korganizer
%_datadir/apps/korganizer/*
%dir %_datadir/apps/kalarm/
%_datadir/apps/kalarm/*
%dir %_datadir/apps/libkholidays/
%_datadir/apps/libkholidays/*
%_datadir/autostart/kalarm.tray.desktop
%_datadir/autostart/kalarmd.autostart.desktop
%_datadir/autostart/korgac.desktop
%_libdir/trinity/libkorg_*
%_libdir/trinity/kcm_korganizer.*
%_libdir/trinity/libkorganizerpart.*
%_datadir/applications/kde/kalarm.desktop
%_datadir/applications/kde/korganizer.desktop
%_iconsdir/*/*/*/kalarm*
%doc %_docdir/kde/HTML/en/korganizer/*
%doc %_docdir/kde/HTML/en/konsolekalendar/*
%doc %_docdir/kde/HTML/en/kalarm
%_datadir/services/korganizer_*
%dir %_datadir/services/korganizer/
%_datadir/services/korganizer/*
%dir %_datadir/services/webcal.protocol
%_datadir/servicetypes/calendardecoration.desktop
%_datadir/servicetypes/calendarplugin.desktop
%_datadir/servicetypes/korganizerpart.desktop
%_datadir/services/kontact/korganizerplugin.desktop
%_datadir/services/kontact/journalplugin.desktop
%_datadir/services/kontact/todoplugin.desktop
%_libdir/libkorganizer.la
%_libdir/libkorganizer.so.*
%_libdir/libkorganizer_eventviewer.la
%_libdir/libkorganizer_eventviewer.so.*
%_libdir/libkorg_stdprinting.la
%_libdir/libkorg_stdprinting.so.*

%if 0
%files kpilot
%defattr(-,root,root)
%_bindir/kpalmdoc
%_bindir/kpilot
%_bindir/kpilotDaemon
%_iconsdir/*/*/*/kpalmdoc*
%_iconsdir/*/*/*/kpilot*
%_libdir/trinity/kcm_kpilot.*
%_libdir/trinity/conduit_*
%_libdir/trinity/kfile_palm.*
%_datadir/services/kfile_palm.desktop
%_datadir/services/kpilot_config.desktop
%_datadir/services/*conduit.desktop
%_datadir/services/kontact/kpilotplugin.desktop
%_datadir/apps/kconf_update/kpilot.upd
%_datadir/applications/kde/kpalmdoc.desktop
%_datadir/apps/kconf_update/kpalmdoc.upd
%dir %_datadir/apps/kpilot
%_datadir/apps/kpilot/*
%_datadir/servicetypes/*conduit.desktop
%doc %_docdir/kde/HTML/en/kpilot
%_datadir/applications/kde/kpilotdaemon.desktop
%_datadir/applications/kde/kpilot.desktop
%_libdir/libkpilot.so.*
%_libdir/libkpilot.la
%endif

%files kontact
%defattr(-,root,root)
%_bindir/kontact
%dir %_datadir/services/kontact/
%_datadir/services/kontact/*
%_datadir/services/kontactconfig.desktop
%_datadir/applications/kde/Kontact.desktop
%_datadir/applications/kde/kontactdcop.desktop
%dir %_datadir/apps/kontact/
%_datadir/apps/kontact/*
%_datadir/services/kcmkontactsummary.desktop
%dir %_datadir/apps/kontactsummary/
%_datadir/apps/kontactsummary/*
%_libdir/libkontact.la
%_libdir/libkontact.so.*
%_libdir/libkpinterfaces.so.*
%_libdir/libkpinterfaces.la
%_libdir/trinity/libkontact*
%_libdir/trinity/kcm_kontact*
%_datadir/servicetypes/kontactplugin.desktop
%_datadir/services/kcmkontactknt.desktop
%_iconsdir/*/*/*/kontact*
%doc %_docdir/kde/HTML/en/kontact/*
 
%exclude %_datadir/services/kontact/akregatorplugin.desktop
%exclude %_datadir/services/kontact/akregatorplugin3.2.desktop
%exclude %_datadir/services/kontact/journalplugin.desktop
%exclude %_datadir/services/kontact/kaddressbookplugin.desktop
%exclude %_datadir/services/kontact/karmplugin.desktop
%exclude %_datadir/services/kontact/kmailplugin.desktop
%exclude %_datadir/services/kontact/knodeplugin.desktop
%exclude %_datadir/services/kontact/knotesplugin.desktop
%exclude %_datadir/services/kontact/korganizerplugin.desktop
%exclude %_datadir/services/kontact/newstickerplugin.desktop
%exclude %_datadir/services/kontact/todoplugin.desktop

%files common
%defattr(-,root,root)
%_bindir/kleopatra
%_bindir/kode
%_bindir/kwatchgnupg
%_bindir/kxml_compiler
#%_bindir/networkstatustestservice
%_bindir/scalixadmin
%_libdir/trinity/kcal_groupdav.la
%_libdir/trinity/kcal_groupdav.so
%_libdir/trinity/kcal_groupwise.la
%_libdir/trinity/kcal_groupwise.so
%_libdir/trinity/kcal_kabc.la
%_libdir/trinity/kcal_kabc.so
%_libdir/trinity/kcal_kolab.la
%_libdir/trinity/kcal_kolab.so
%_libdir/trinity/kcal_local.la
%_libdir/trinity/kcal_local.so
%_libdir/trinity/kcal_localdir.la
%_libdir/trinity/kcal_localdir.so
%_libdir/trinity/kcal_newexchange.la
%_libdir/trinity/kcal_newexchange.so
%_libdir/trinity/kcal_remote.la
%_libdir/trinity/kcal_remote.so
%_libdir/trinity/kcal_resourcefeatureplan.la
%_libdir/trinity/kcal_resourcefeatureplan.so
%_libdir/trinity/kcal_scalix.la
%_libdir/trinity/kcal_scalix.so
%_libdir/trinity/kcal_slox.la
%_libdir/trinity/kcal_slox.so
%_libdir/trinity/kcal_xmlrpc.la
%_libdir/trinity/kcal_xmlrpc.so
%_libdir/trinity/kcm_kleopatra.la
%_libdir/trinity/kcm_kleopatra.so
%_libdir/trinity/kcm_korgsummary.la
%_libdir/trinity/kcm_korgsummary.so
%_libdir/trinity/kcm_sdsummary.la
%_libdir/trinity/kcm_sdsummary.so
#%_libdir/trinity/kded_networkstatus.la
#%_libdir/trinity/kded_networkstatus.so
%_libdir/trinity/kio_groupwise.la
%_libdir/trinity/kio_groupwise.so
%_libdir/trinity/kio_imap4.la
%_libdir/trinity/kio_imap4.so
%_libdir/trinity/kio_mbox.la
%_libdir/trinity/kio_mbox.so
%_libdir/trinity/kio_scalix.la
%_libdir/trinity/kio_scalix.so
%_libdir/trinity/kio_sieve.la
%_libdir/trinity/kio_sieve.so
%_libdir/trinity/plugins/designer/kpartsdesignerplugin.la
%_libdir/trinity/plugins/designer/kpartsdesignerplugin.so
%_libdir/trinity/resourcecalendarexchange.la
%_libdir/trinity/resourcecalendarexchange.so
%_libdir/libgpgme++.la
%_libdir/libgpgme++.so*
%_libdir/libgwsoap.la
%_libdir/libgwsoap.so
%_libdir/libgwsoap.so.0
%_libdir/libgwsoap.so.0.0.0
%_libdir/libindex.so
%_libdir/libkabc_groupdav.so
%_libdir/libkabc_groupwise.so
%_libdir/libkabc_newexchange.so
%_libdir/libkabc_slox.so
%_libdir/libkabc_xmlrpc.so
%_libdir/libkabckolab.so
%_libdir/libkabcscalix.so
%_libdir/libkabinterfaces.so
%_libdir/libkaddressbook.so
%_libdir/libkcal.la
%_libdir/libkcal.so
%_libdir/libkcal.so.2
%_libdir/libkcal.so.2.0.0
%_libdir/libkcal_groupdav.la
%_libdir/libkcal_groupdav.so
%_libdir/libkcal_groupdav.so.1
%_libdir/libkcal_groupdav.so.1.0.0
%_libdir/libkcal_groupwise.la
%_libdir/libkcal_groupwise.so
%_libdir/libkcal_groupwise.so.1
%_libdir/libkcal_groupwise.so.1.0.0
%_libdir/libkcal_newexchange.la
%_libdir/libkcal_newexchange.so
%_libdir/libkcal_newexchange.so.1
%_libdir/libkcal_newexchange.so.1.0.0
%_libdir/libkcal_resourcefeatureplan.la
%_libdir/libkcal_resourcefeatureplan.so
%_libdir/libkcal_resourcefeatureplan.so.1
%_libdir/libkcal_resourcefeatureplan.so.1.0.0
%_libdir/libkcal_resourceremote.la
%_libdir/libkcal_resourceremote.so
%_libdir/libkcal_resourceremote.so.1
%_libdir/libkcal_resourceremote.so.1.0.0
%_libdir/libkcal_slox.la
%_libdir/libkcal_slox.so
%_libdir/libkcal_slox.so.0
%_libdir/libkcal_slox.so.0.0.0
%_libdir/libkcal_xmlrpc.la
%_libdir/libkcal_xmlrpc.so
%_libdir/libkcal_xmlrpc.so.1
%_libdir/libkcal_xmlrpc.so.1.0.0
%_libdir/libkcalkolab.la
%_libdir/libkcalkolab.so
%_libdir/libkcalkolab.so.0
%_libdir/libkcalkolab.so.0.0.0
%_libdir/libkcalscalix.la
%_libdir/libkcalscalix.so
%_libdir/libkcalscalix.so.0
%_libdir/libkcalscalix.so.0.0.0
%_libdir/libtdepim.la
%_libdir/libtdepim.so
%_libdir/libtdepim.so.1
%_libdir/libtdepim.so.1.0.0
%_libdir/libkgantt.la
%_libdir/libkgantt.so
%_libdir/libkgantt.so.0
%_libdir/libkgantt.so.0.0.2
%_libdir/libkgroupwarebase.la
%_libdir/libkgroupwarebase.so
%_libdir/libkgroupwarebase.so.0
%_libdir/libkgroupwarebase.so.0.0.0
%_libdir/libkgroupwaredav.la
%_libdir/libkgroupwaredav.so
%_libdir/libkgroupwaredav.so.0
%_libdir/libkgroupwaredav.so.0.0.0
%_libdir/libkholidays.la
%_libdir/libkholidays.so
%_libdir/libkholidays.so.1
%_libdir/libkholidays.so.1.0.0
%_libdir/libkleopatra.la
%_libdir/libkleopatra.so
%_libdir/libkleopatra.so.1
%_libdir/libkleopatra.so.1.0.0
%_libdir/libkmime.la
%_libdir/libkmime.so
%_libdir/libkmime.so.2
%_libdir/libkmime.so.2.2.0
%_libdir/libknodecommon.so
%_libdir/libknotes_xmlrpc.la
%_libdir/libknotes_xmlrpc.so
%_libdir/libknotes_xmlrpc.so.1
%_libdir/libknotes_xmlrpc.so.1.0.0
%_libdir/libknoteskolab.la
%_libdir/libknoteskolab.so
%_libdir/libknoteskolab.so.0
%_libdir/libknoteskolab.so.0.0.0
%_libdir/libknotesscalix.la
%_libdir/libknotesscalix.so
%_libdir/libknotesscalix.so.0
%_libdir/libknotesscalix.so.0.0.0
%_libdir/libkocorehelper.la
%_libdir/libkocorehelper.so
%_libdir/libkocorehelper.so.1
%_libdir/libkocorehelper.so.1.0.0
%_libdir/libkode.la
%_libdir/libkode.so
%_libdir/libkode.so.1
%_libdir/libkode.so.1.0.0
%_libdir/libkontact.so
%_libdir/libkorg_stdprinting.so
%_libdir/libkorganizer.so
%_libdir/libkorganizer_calendar.la
%_libdir/libkorganizer_calendar.so
%_libdir/libkorganizer_calendar.so.1
%_libdir/libkorganizer_calendar.so.1.0.0
%_libdir/libkorganizer_eventviewer.so
%_libdir/libkpgp.la
%_libdir/libkpgp.so
%_libdir/libkpgp.so.2
%_libdir/libkpgp.so.2.2.0
%_libdir/libkpimexchange.la
%_libdir/libkpimexchange.so
%_libdir/libkpimexchange.so.1
%_libdir/libkpimexchange.so.1.0.0
%_libdir/libkpimidentities.la
%_libdir/libkpimidentities.so
%_libdir/libkpimidentities.so.1
%_libdir/libkpimidentities.so.1.0.0
%_libdir/libkpinterfaces.so
%_libdir/libksieve.la
%_libdir/libksieve.so
%_libdir/libksieve.so.0
%_libdir/libksieve.so.0.0.0
%_libdir/libkslox.la
%_libdir/libkslox.so
%_libdir/libkslox.so.0
%_libdir/libkslox.so.0.0.0
%_libdir/libktnef.so
%_libdir/libmimelib.la
%_libdir/libmimelib.so
%_libdir/libmimelib.so.1
%_libdir/libmimelib.so.1.0.1
%_libdir/libqgpgme.la
%_libdir/libqgpgme.so
%_libdir/libqgpgme.so.0
%_libdir/libqgpgme.so.0.0.0
%_datadir/applications/kde/kleopatra_import.desktop
%_datadir/applications/kde/konsolekalendar.desktop
%_datadir/applnk/.hidden/kalarmd.desktop
%_datadir/applnk/Applications/kalarm.desktop
%_datadir/apps/kconf_update/kolab-resource.upd
%_datadir/apps/kconf_update/kpgp-3.1-upgrade-address-data.pl
%_datadir/apps/kconf_update/kpgp.upd
%_datadir/apps/kconf_update/upgrade-resourcetype.pl
%_datadir/apps/kgantt/icons/crystalsvg/16x16/actions/ganttSelect.png
%_datadir/apps/kgantt/icons/crystalsvg/16x16/actions/ganttSelecttask.png
%_datadir/apps/kgantt/icons/crystalsvg/16x16/actions/ganttUnselecttask.png
%_datadir/apps/kgantt/icons/crystalsvg/22x22/actions/ganttSelect.png
%_datadir/apps/kgantt/icons/crystalsvg/22x22/actions/ganttSelecttask.png
%_datadir/apps/kgantt/icons/crystalsvg/22x22/actions/ganttUnselecttask.png
%_datadir/apps/kgantt/icons/crystalsvg/32x32/actions/ganttSelect.png
%_datadir/apps/kgantt/icons/crystalsvg/32x32/actions/ganttSelecttask.png
%_datadir/apps/kgantt/icons/crystalsvg/32x32/actions/ganttUnselecttask.png
%_datadir/apps/kleopatra/kleopatraui.rc
%_datadir/apps/korgac/icons/crystalsvg/22x22/actions/korgac.png
%_datadir/apps/korgac/icons/crystalsvg/22x22/actions/korgac_disabled.png
%_datadir/apps/kwatchgnupg/kwatchgnupgui.rc
%_datadir/apps/kwatchgnupg/pics/kwatchgnupg.png
%_datadir/apps/kwatchgnupg/pics/kwatchgnupg2.png
%_datadir/apps/libkleopatra/pics/chiasmus_chi.png
%_datadir/apps/libkleopatra/pics/key.png
%_datadir/apps/libkleopatra/pics/key_bad.png
%_datadir/apps/libkleopatra/pics/key_ok.png
%_datadir/apps/libkleopatra/pics/key_unknown.png
%_datadir/config.kcfg/custommimeheader.kcfg
%_datadir/config.kcfg/customtemplates_kfg.kcfg
%_datadir/config.kcfg/egroupware.kcfg
%_datadir/config.kcfg/groupwise.kcfg
%_datadir/config.kcfg/kmail.kcfg
%_datadir/config.kcfg/knoteconfig.kcfg
%_datadir/config.kcfg/knotesglobalconfig.kcfg
%_datadir/config.kcfg/kolab.kcfg
%_datadir/config.kcfg/kontact.kcfg
%_datadir/config.kcfg/korganizer.kcfg
%_datadir/config.kcfg/mk4config.kcfg
%_datadir/config.kcfg/pimemoticons.kcfg
%_datadir/config.kcfg/replyphrases.kcfg
%_datadir/config.kcfg/scalix.kcfg
%_datadir/config.kcfg/slox.kcfg
%_datadir/config.kcfg/templatesconfiguration_kfg.kcfg
%_datadir/config/libkleopatrarc
%_datadir/doc/kde/HTML/en/kleopatra/common
%_datadir/doc/kde/HTML/en/kleopatra/index.cache.bz2
%_datadir/doc/kde/HTML/en/kleopatra/index.docbook
%_datadir/doc/kde/HTML/en/kwatchgnupg/common
%_datadir/doc/kde/HTML/en/kwatchgnupg/index.cache.bz2
%_datadir/doc/kde/HTML/en/kwatchgnupg/index.docbook
%_datadir/icons/crystalsvg/16x16/apps/konsolekalendar.png
%_datadir/icons/crystalsvg/22x22/actions/button_fewer.png
%_datadir/icons/crystalsvg/22x22/actions/button_more.png
%_datadir/icons/crystalsvg/22x22/apps/konsolekalendar.png
%_datadir/icons/crystalsvg/32x32/apps/konsolekalendar.png
%_datadir/icons/hicolor/128x128/apps/korganizer.png
%_datadir/icons/hicolor/16x16/apps/korganizer.png
%_datadir/icons/hicolor/32x32/apps/korganizer.png
%_datadir/icons/hicolor/48x48/apps/korganizer.png
%_datadir/icons/hicolor/64x64/apps/korganizer.png
%_datadir/services/groupwise.protocol
%_datadir/services/groupwises.protocol
%_datadir/services/imap4.protocol
%_datadir/services/imaps.protocol
%_datadir/services/kcmkorgsummary.desktop
%_datadir/services/kcmsdsummary.desktop
#%_datadir/services/kded/networkstatus.desktop
%_datadir/services/kleopatra_config_appear.desktop
%_datadir/services/kleopatra_config_dirserv.desktop
%_datadir/services/kleopatra_config_dnorder.desktop
%_datadir/services/kresources/kcal/exchange.desktop
%_datadir/services/kresources/kcal/imap.desktop
%_datadir/services/kresources/kcal/kabc.desktop
%_datadir/services/kresources/kcal/kcal_groupdav.desktop
%_datadir/services/kresources/kcal/kcal_groupwise.desktop
%_datadir/services/kresources/kcal/kcal_newexchange.desktop
%_datadir/services/kresources/kcal/kcal_opengroupware.desktop
%_datadir/services/kresources/kcal/kcal_ox.desktop
%_datadir/services/kresources/kcal/kcal_resourcefeatureplan.desktop
%_datadir/services/kresources/kcal/kcal_slox.desktop
%_datadir/services/kresources/kcal/kcal_xmlrpc.desktop
%_datadir/services/kresources/kcal/kolab.desktop
%_datadir/services/kresources/kcal/local.desktop
%_datadir/services/kresources/kcal/localdir.desktop
%_datadir/services/kresources/kcal/remote.desktop
%_datadir/services/kresources/kcal/scalix.desktop
%_datadir/services/kresources/kcal_manager.desktop
%_datadir/services/kresources/knotes/imap.desktop
%_datadir/services/kresources/knotes/knotes_xmlrpc.desktop
%_datadir/services/kresources/knotes/local.desktop
%_datadir/services/kresources/knotes/scalix.desktop
%_datadir/services/mbox.protocol
%_datadir/services/scalix.protocol
%_datadir/services/scalixs.protocol
%_datadir/services/sieve.protocol
%_datadir/servicetypes/dcopcalendar.desktop
%_datadir/servicetypes/dcopimap.desktop
%_datadir/servicetypes/kaddressbookimprotocol.desktop
%_datadir/servicetypes/korgprintplugin.desktop
   /usr/bin/kmobile
   /usr/lib/libkabc_carddav.so
   /usr/lib/libkarm.la
   /usr/lib/libkarm.so
   /usr/lib/libkarm.so.0
   /usr/lib/libkarm.so.0.0.0
   /usr/lib/libkcal_caldav.la
   /usr/lib/libkcal_caldav.so
   /usr/lib/libkcal_caldav.so.1
   /usr/lib/libkcal_caldav.so.1.0.0
   /usr/lib/libkmobileclient.la
   /usr/lib/libkmobileclient.so
   /usr/lib/libkmobiledevice.la
   /usr/lib/libkmobiledevice.so
   /usr/lib/libknotes.la
   /usr/lib/libknotes.so
   /usr/lib/libknotes.so.0
   /usr/lib/libknotes.so.0.0.0
   /usr/lib/trinity/kcal_caldav.la
   /usr/lib/trinity/kcal_caldav.so
   /usr/lib/trinity/libkmobile_skeleton.la
   /usr/lib/trinity/libkmobile_skeleton.so
   /usr/lib/trinity/plugins/designer/tdepimwidgets.la
   /usr/lib/trinity/plugins/designer/tdepimwidgets.so
   /usr/share/applications/kde/kmobile.desktop
   /usr/share/apps/kmobile/kmobileui.rc
   /usr/share/apps/libtdepim/about/bar-bottom-left.png
   /usr/share/apps/libtdepim/about/bar-bottom-middle.png
   /usr/share/apps/libtdepim/about/bar-bottom-right.png
   /usr/share/apps/libtdepim/about/bar-middle-left.png
   /usr/share/apps/libtdepim/about/bar-middle-right.png
   /usr/share/apps/libtdepim/about/bar-top-left.png
   /usr/share/apps/libtdepim/about/bar-top-middle.png
   /usr/share/apps/libtdepim/about/bar-top-right.png
   /usr/share/apps/libtdepim/about/bottom-left.png
   /usr/share/apps/libtdepim/about/bottom-middle.png
   /usr/share/apps/libtdepim/about/bottom-right.png
   /usr/share/apps/libtdepim/about/box-bottom-left.png
   /usr/share/apps/libtdepim/about/box-bottom-middle.png
   /usr/share/apps/libtdepim/about/box-bottom-right.png
   /usr/share/apps/libtdepim/about/box-middle-left.png
   /usr/share/apps/libtdepim/about/box-middle-right.png
   /usr/share/apps/libtdepim/about/box-top-left.png
   /usr/share/apps/libtdepim/about/box-top-middle.png
   /usr/share/apps/libtdepim/about/box-top-right.png
   /usr/share/apps/libtdepim/about/kde_infopage.css
   /usr/share/apps/libtdepim/about/kde_infopage_rtl.css
   /usr/share/apps/libtdepim/about/top-left.png
   /usr/share/apps/libtdepim/about/top-middle.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/appointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/bell.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/inverse_recur.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/journal.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/newappointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/readonlyevent.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/recur.png
   /usr/share/apps/tdepim/icons/crystalsvg/16x16/actions/todo.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/appointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/checkedbox.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/checkedbox_mask.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/checkedclipboard.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/checkmark.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/journal.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/newappointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/newjournal.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/newrecurevent.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/newtodo.png
   /usr/share/apps/tdepim/icons/crystalsvg/22x22/actions/todo.png
   /usr/share/apps/tdepim/icons/crystalsvg/32x32/actions/appointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/32x32/actions/journal.png
   /usr/share/apps/tdepim/icons/crystalsvg/32x32/actions/newappointment.png
   /usr/share/apps/tdepim/icons/crystalsvg/32x32/actions/todo.png
   /usr/share/apps/tdepimwidgets/pics/addresseelineedit.png
   /usr/share/apps/tdepimwidgets/pics/clicklineedit.png
   /usr/share/apps/tdepimwidgets/pics/kdateedit.png
   /usr/share/apps/tdepimwidgets/pics/ktimeedit.png
   /usr/share/cmake/certmanager.cmake
   /usr/share/cmake/indexlib.cmake
   /usr/share/cmake/kgantt.cmake
   /usr/share/cmake/kmail.cmake
   /usr/share/cmake/knotes.cmake
   /usr/share/cmake/korganizer.cmake
   /usr/share/cmake/kresources.cmake
   /usr/share/cmake/ktnef.cmake
   /usr/share/cmake/libkcal.cmake
   /usr/share/cmake/libkholidays.cmake
   /usr/share/cmake/libkmime.cmake
   /usr/share/cmake/libkpgp.cmake
   /usr/share/cmake/libkpimexchange.cmake
   /usr/share/cmake/libkpimidentities.cmake
   /usr/share/cmake/libksieve.cmake
   /usr/share/cmake/libtdenetwork.cmake
   /usr/share/cmake/libtdepim.cmake
   /usr/share/cmake/mimelib.cmake
   /usr/share/doc/kde/HTML/en/kpilot/address-app.png
   /usr/share/doc/kde/HTML/en/kpilot/common
   /usr/share/doc/kde/HTML/en/kpilot/conduit-knotes.png
   /usr/share/doc/kde/HTML/en/kpilot/conduit-mal.png
   /usr/share/doc/kde/HTML/en/kpilot/conduit-palmdoc.png
   /usr/share/doc/kde/HTML/en/kpilot/conduit-popmail-kmail.png
   /usr/share/doc/kde/HTML/en/kpilot/conduit-sysinfo.png
   /usr/share/doc/kde/HTML/en/kpilot/conduit-vcal.png
   /usr/share/doc/kde/HTML/en/kpilot/configuration.docbook
   /usr/share/doc/kde/HTML/en/kpilot/daemon-menu.png
   /usr/share/doc/kde/HTML/en/kpilot/db-app.png
   /usr/share/doc/kde/HTML/en/kpilot/faq.docbook
   /usr/share/doc/kde/HTML/en/kpilot/file-app.png
   /usr/share/doc/kde/HTML/en/kpilot/index.cache.bz2
   /usr/share/doc/kde/HTML/en/kpilot/index.docbook
   /usr/share/doc/kde/HTML/en/kpilot/main-app.png
   /usr/share/doc/kde/HTML/en/kpilot/memo-app.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-address.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-conduit.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-dbspecial.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-general.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-hotsync.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-items.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-startup-exit.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-tabs.png
   /usr/share/doc/kde/HTML/en/kpilot/setup-viewer.png
   /usr/share/doc/kde/HTML/en/kpilot/sidebar.png
   /usr/share/doc/kde/HTML/en/kpilot/sync.docbook
   /usr/share/doc/kde/HTML/en/kpilot/todo-app.png
   /usr/share/doc/kde/HTML/en/kpilot/toolbar_backup.png
   /usr/share/doc/kde/HTML/en/kpilot/toolbar_hotsync.png
   /usr/share/doc/kde/HTML/en/kpilot/usage.docbook
   /usr/share/doc/kde/HTML/en/kpilot/wizard-conduits.png
   /usr/share/doc/kde/HTML/en/kpilot/wizard-connection.png
   /usr/share/doc/kde/HTML/en/kpilot/wizard-general.png
   /usr/share/icons/default.kde/32x32/devices/mobile_camera.png
   /usr/share/icons/default.kde/32x32/devices/mobile_musicplayer.png
   /usr/share/icons/default.kde/32x32/devices/mobile_organizer.png
   /usr/share/icons/default.kde/32x32/devices/mobile_phone.png
   /usr/share/icons/default.kde/32x32/devices/mobile_unknown.png
   /usr/share/icons/hicolor/16x16/apps/kmobile.png
   /usr/share/icons/hicolor/32x32/apps/kmobile.png
   /usr/share/icons/hicolor/48x48/apps/kmobile.png
   /usr/share/services/kresources/kcal/kcal_caldav.desktop
   /usr/share/services/libkmobile_digicam.desktop
   /usr/share/services/libkmobile_gammu.desktop
   /usr/share/services/libkmobile_skeleton.desktop
   /usr/share/servicetypes/libkmobile.desktop

%changelog
* Tue Mar 17 2009 Liu Di <liudidi@gmail.com> - 3.5.10-4
- 细分包
 
* Sun Sep 28 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.10-2.2mgc
- 修正文件分包依赖问题
- 恢复 kandy 和 karm
- 基于 libopensync 0.37 编译(patch 1000 modified by nihui, merged two patch from gentoo project and debian patch)
- 戊子  八月廿九
 
* Sat Sep 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.10-2.1mgc
- 拆出 extras 包(korn, kpilot, kpilotdaemon, kitchensync)
- 将 qt-designer 移入 devel 包
- 戊子  八月廿一
