%define debug 0
%define final 1
%define arts 1
%define qt_version 3.3.8
%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111221

Summary: KDE network Package
Summary(zh_CN.UTF-8): KDE 网络包
Name:          tdenetwork
Version:       3.5.14
%if %{git}
Release:	0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: http://www.kde.org
Group:         Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source0:	%{name}-git%{gitdate}.tar.xz
%else
Source0:     ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Source1:     kppp
Source2:	make_tdenetwork_git_package.sh
#临时措施
Source3:	dummy.cpp
Patch0: kdenetwork-kcm_sambaconf.patch
Patch1: knetwork-kfile_torrent-cjk.patch
Patch10: kopete-0.10.1-fix_delete_account.patch
Patch11: kopete-0.10.1-contactlist_delete.patch
Patch12: kopete-0.12b1-fix-unknown-reason.patch
Patch13: kopete-move-ogg-to-wav.patch
Patch14: kopete-add-msngroup.patch
Patch15: kopete-jingle.patch
Patch16: tdenetwork-git20111221-gcc46.patch
Patch17: tdenetwork-git20111221-tqname.patch
Patch18: tdenetwork-git20111221-typo.patch
Patch19: tdenetwork-git20111221-videodev.patch
# upstream patches

Requires: qt,  kdelibs, kdebase
%if %{arts} == 0
Requires:arts
%endif

Requires: %{name}-common
Requires: %{name}-kopete
Requires: %{name}-krfb

%description
KDE network package include kmail, kppp, kget, knode and so on

%description -l zh_CN.UTF-8
KDE 网络包包括 kmail，kppp，kget，knode 等等

#===================================================================================

%package common
Summary:        Common files for kdenetwork
Summary(zh_CN.UTF-8): %{name} 的公用文件
Group:          Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
 
Requires: kdebase-core >= 3.1
Requires: kdelibs >= 3.1.1
 
%description common
Common files for kdenetwork

%description common -l zh_CN.UTF-8
%{name} 的公用文件。

#===================================================================================

%package kopete
Group:   Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Kopete
Summary(zh_CN.UTF-8): 多种 IM 的客户端
Requires: tdenetwork-common >= %version-%release
Provides: kopete
#Need for yahoo webcam
Requires:       jasper, libjingle
 
%description kopete
Kopete is a flexible and extendable multiple protocol instant messaging
system designed as a plugin-based system.
 
All protocols are plugins and allow modular installment, configuration,
and usage without the main application knowing anything about the plugin
being loaded.
 
The goal of Kopete is to provide users with a standard and easy to use
interface between all of their instant messaging systems, but at the same
time also providing developers with the ease of writing plugins to support
a new protocol.
 
The core Kopete development team provides a handful of plugins that most
users can use, in addition to templates for new developers to base a
plugin off of.

%description kopete -l zh_CN.UTF-8
Kopete 是一个稳定可扩展的多种即时消息客户端，支持插件。

#===========================================================================

%package lisa
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Lisa server
Summary(zh_CN.UTF-8): Lisa 服务
Provides: lisa
Requires: tdenetwork-common >= %version-%release
 
%description lisa
LISa is intended to provide a kind of "network neighbourhood" but only
relying on the TCP/IP protocol stack, no smb or whatever.

%description lisa -l zh_CN.UTF-8
LISa 提供了类似“网上邻居”的功能，但是只在 TCP/IP 协议上使用，不支持
smb 或其它的东西。

#============================================================================

%package ktalk
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Ktalk program
Summary(zh_CN.UTF-8): Ktalk 程序
Provides: ktalk
Requires: tdenetwork-common >= %version-%release 

%description ktalk
ktalk is a graphical talk client capable of multiple connections. It contains
an addressbook and provides word-wrap, copy and paste, configurable fonts,
ping, and file transfer.

%description ktalk -l zh_CN.UTF-8
Ktalk 是一个图形的 talk 客户端，支持多重连接。它包含了地址本，提供自动换行，
复制粘贴，配置字体，ping和文件传输等。

#============================================================================

%package kppp
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: KDE 下的拨号器
Requires: ppp
Provides: kppp
Requires: tdenetwork-common >= %version-%release
 
%description kppp
Kppp is a dialer and front end for pppd.

%description kppp -l zh_CN.UTF-8
KDE 下的拨号器。

#=============================================================================

%package ksirc
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: KDE IRC
Summary(zh_CN.UTF-8): KDE 下的 IRC 客户端
Provides: ksirc
Requires: tdenetwork-common >= %version-%release
 
%description ksirc
KDE internet relay chat client.

%description ksirc -l zh_CN.UTF-8
KDE 下的 IRC 客户端。

#------------------------------------------------------------------------------

%package kwifimanager
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: KWifimanager
Summary(zh_CN.UTF-8): KDE 无线管理器
Provides: kwifimanager
Requires: wireless-tools
Requires: tdenetwork-common >= %version-%release
 
%description kwifimanager
A wireless LAN connection monitor.

%description kwifimanager -l zh_CN.UTF-8
KDE 下的无线网络连接监视器。

#================================================================================

%package kdict
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Kdict program
Summary(zh_CN.UTF-8): KDE 下的字典客户端
Provides: kdict
Requires: tdenetwork-common >= %version-%release
 
%description kdict
Kdict is a graphical client for the DICT Protocol. It enables you
to search through dictionary-like databases for a word or phrase, then
displays suitable definitions.

%description kdict -l zh_CN.UTF-8
Kdict 是 DICT 协议的图形客户端。它可以让你在类似字典的数据库中查找单词
或词组，然后显示合适的定义。

#===============================================================================

%package kget
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Kget program
Summary(zh_CN.UTF-8): KDE 下的下载管理器
Provides: kget
Requires: tdenetwork-common >= %version-%release
 
%description kget
An advanced download manager for KDE.

%description kget -l zh_CN.UTF-8
KDE 下的高级下载管理器。

#=========================================================================

%package krfb
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: Krfb, Krdc program
Summary(zh_CN.UTF-8): KDE 下的远程桌面
Provides: krdc, krfb
Requires: tdenetwork-common >= %version-%release
 
%description krfb
KDE Desktop Sharing allows you to invite somebody at a remote
location to watch and possibly control your desktop.

%description krfb -l zh_CN.UTF-8
KDE 桌面共享允许你邀请一些人在远程查看和控制你的桌面。
这个包也包含了连接 Windows 远程桌面的客户端。

#=========================================================================

%package knewsticker
Group: Applications/Internet
Group(zh_CN.UTF-8):  应用程序/互联网
Summary: RDF newsticker applet
Summary(zh_CN.UTF-8): RDF 新闻获取程序
Provides: knewsticker
Requires: tdenetwork-common >= %version-%release
 
%description knewsticker
Knewsticker: RDF newsticker applet

%description knewsticker -l zh_CN.UTF-8
RDF 新闻获取程序。

#==========================================================================

%package devel
Summary: Development files for kdenetwork
Summary(zh_CN.UTF-8): kdenetwork 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}
Requires: kdelibs-devel

%description devel
Development files for kdenetwork. Install kdenetwork-devel if you wish
to develop or compile KDE networking applications.

%description devel -l zh_CN.UTF-8
kdenetwork 的开发文件。如果您想开发或编译 KDE 网络应用程序请安装 kdenetwork-devel 包。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q
%endif
%patch0 -p1
%patch1 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

pushd kopete/sounds
for soundi in `ls *.ogg`
do
oggdec $soundi
done
popd

cp %{SOURCE3} kopete/protocols/msn/

cp kopete/libkopete/private/kopeteemoticons.* kopete/libkopete/

%Build
unset QTDIR || : ; . /etc/profile.d/qt.sh
mkdir build
cd build
%cmake 	-DWITH_JINGLE=ON \
	-DWITH_SPEEX=ON \
	-DWITH_WEBCAM=ON \
	-DWITH_GSM=ON \
	-DWITH_ARTS=ON \
	-DBUILD_KOPETE_PROTOCOL_ALL=ON \
	-DBUILD_KOPETE_PLUGIN_ALL=ON \
	-DBUILD_ALL=ON \
	..
#多线程编译出错
make

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/etc/pam.d
install -m 644 %{SOURCE1} %{buildroot}/etc/pam.d
rm -rf %{buildroot}/usr/share/applnk/Internet/More

# 已经包含在 libjingle 中
rm -f %{buildroot}%{_bindir}/relayserver
rm -f %{buildroot}%{_bindir}/stunserver

chmod +s %{buildroot}/usr/bin/kppp

%clean   
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)

%files common
%defattr(-,root,root)
%_bindir/feedbrowser
%_bindir/kopete_latexconvert.sh
%_bindir/rssclient
%_bindir/rssservice
%_libdir/trinity/kded_dnssdwatcher.la
%_libdir/trinity/kded_dnssdwatcher.so
%_libdir/trinity/kfile_torrent.la
%_libdir/trinity/kfile_torrent.so
%_libdir/trinity/kio_zeroconf.la
%_libdir/trinity/kio_zeroconf.so
%_libdir/trinity/kpf_panelapplet.la
%_libdir/trinity/kpf_panelapplet.so
%_libdir/trinity/kpfpropertiesdialog.la
%_libdir/trinity/kpfpropertiesdialog.so
%_libdir/libkopete.so
%_libdir/libkopete_msn_shared.so
%_libdir/libkopete_oscar.so
%_libdir/libkopete_videodevice.so
%_libdir/librss.la
%_libdir/librss.so
%_libdir/librss.so.1
%_libdir/librss.so.1.0.0
%_datadir/apps/kicker/applets/kpfapplet.desktop
%_datadir/apps/remoteview/lan.desktop
%_datadir/apps/remoteview/zeroconf.desktop
%_datadir/apps/zeroconf/_ftp._tcp
%_datadir/apps/zeroconf/_http._tcp
%_datadir/apps/zeroconf/_ldap._tcp
%_datadir/apps/zeroconf/_nfs._tcp
%_datadir/apps/zeroconf/_rfb._tcp
%_datadir/apps/zeroconf/_ssh._tcp
%_datadir/apps/zeroconf/_webdav._tcp
%_datadir/config.kcfg/latexconfig.kcfg
%_datadir/config.kcfg/nowlisteningconfig.kcfg
%_datadir/doc/kde/HTML/en/kpf/common
%_datadir/doc/kde/HTML/en/kpf/index.cache.bz2
%_datadir/doc/kde/HTML/en/kpf/index.docbook
%_datadir/icons/crystalsvg/16x16/apps/kpf.png
%_datadir/icons/crystalsvg/32x32/apps/kpf.png
%_datadir/icons/crystalsvg/48x48/apps/kpf.png
%_datadir/services/emailwindow.desktop
%_datadir/services/kded/dnssdwatcher.desktop
%_datadir/services/kfile_torrent.desktop
%_datadir/services/kntsrcfilepropsdlg.desktop
%_datadir/services/kpfpropertiesdialogplugin.desktop
%_datadir/services/zeroconf.protocol
%_datadir/sounds/*.wav
%{_bindir}/winpopup-install.sh
%{_bindir}/winpopup-send.sh
%{_libdir}/trinity/kntsrcfilepropsdlg.*
%{_libdir}/trinity/libkwireless.*
%{_libdir}/trinity/new_target0.*
%{_datadir}/apps/checkrules
%{_datadir}/config.kcfg/motionawayconfig.kcfg
%{_datadir}/config.kcfg/smpppdcs.kcfg

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files kopete
%defattr(-,root,root,-)
%_bindir/kopete
%_libdir/kconf_update_bin/kopete_nameTracking_kconf_update
%dir %_docdir/kde/HTML/en/kopete
%doc %_docdir/kde/HTML/en/kopete/*
%_datadir/apps/kopete*
%_datadir/apps/kconf_update/kopete-*
%_datadir/applications/kde/kopete.desktop
%_libdir/trinity/kopete_*
%_libdir/trinity/kcm_kopete_*
%_libdir/trinity/libkrichtexteditpart.*
%_datadir/services/kconfiguredialog/kopete_*
%_datadir/sounds/*.ogg
%_datadir/servicetypes/kopete*.desktop
%_datadir/services/kopete*.desktop
%_datadir/mimelnk/application/x-icq.desktop
%_datadir/mimelnk/application/x-kopete-emoticons.desktop
%dir %_datadir/config.kcfg/
%_datadir/config.kcfg/historyconfig.kcfg
%_datadir/services/chatwindow.desktop
%_datadir/services/rdp.protocol
%_datadir/services/rssservice.desktop
%_datadir/services/aim.protocol
%_datadir/services/irc.protocol
%_iconsdir/*/*/*/kopete*
%_iconsdir/*/*/*/jabber*
%_iconsdir/*/*/*/webcam*
%_iconsdir/*/*/*/*_user*
%_iconsdir/*/*/*/*_offliners*
%_iconsdir/*/*/*/voice*
%_iconsdir/*/*/*/meta*
%_iconsdir/*/*/*/account*
%_iconsdir/*/*/*/emotico*
%_iconsdir/*/*/*/new*
%_iconsdir/*/*/*/contact*
%_iconsdir/*/*/*/status*
%_datadir/config.kcfg/kopete.kcfg
%_datadir/config.kcfg/kopeteidentityconfigpreferences.kcfg
%_datadir/services/invitation.protocol
%_datadir/services/jabberdisco.protocol
%_libdir/libkopete*.so.*
%_libdir/libkopete*.la
%_libdir/kconf_update_bin/kopete_account_kconf_update
%_libdir/kconf_update_bin/kopete_pluginloader2_kconf_update

%files lisa
%defattr(-,root,root)
%_bindir/lisa
%_bindir/reslisa
%dir %_datadir/applnk/.hidden/
%_datadir/applnk/.hidden/kcmkiolan.desktop
%_datadir/applnk/.hidden/kcmlisa.desktop
%_datadir/applnk/.hidden/kcmreslisa.desktop
%dir %_docdir/kde/HTML/en/kcontrol/lanbrowser/
%doc %_docdir/kde/HTML/en/kcontrol/lanbrowser/*
%_datadir/services/fileshare_propsdlgplugin.desktop
%_iconsdir/*/*/*/kcmsambaconf.png
%_datadir/applications/kde/fileshare.desktop
%_datadir/applications/kde/kcmsambaconf.desktop
%_datadir/apps/konqueror/dirtree/remote/lan.desktop
%_libdir/trinity/kio_lan.*
%_libdir/trinity/kcm_lanbrowser.*
%_libdir/trinity/fileshare_propsdlgplugin.*
%_libdir/trinity/kcm_fileshare.*
%_libdir/trinity/kcm_kcmsambaconf.*
%_datadir/apps/konqsidebartng/virtual_folders/services/lisa.desktop
%_datadir/apps/konqueror/servicemenus/smb2rdc.desktop
%dir %_datadir/services/
%_datadir/services/lan.protocol
%_datadir/services/rlan.protocol
%dir %_datadir/apps/lisa/
%_datadir/apps/lisa/README
%dir %_docdir/kde/HTML/en/lisa
%doc %_docdir/kde/HTML/en/lisa/*

%files ktalk
%defattr(-,root,root,-)
%_bindir/ktalkd
%_bindir/ktalkdlg
%_bindir/mail.local
%dir %_docdir/kde/HTML/en/ktalkd/
%doc %_docdir/kde/HTML/en/ktalkd/*
%_libdir/trinity/kcm_ktalkd.*
%dir %_datadir/sounds/
%_datadir/sounds/ktalkd.wav
%_datadir/applications/kde/kcmktalkd.desktop
%_datadir/config/ktalkdrc
%dir %_docdir/kde/HTML/en/kcontrol/kcmtalkd/
%doc %_docdir/kde/HTML/en/kcontrol/kcmtalkd/*
%_iconsdir/*/*/*/ktalkd*

%files kppp
%defattr(-,root,root,-)
%dir %_sysconfdir/pam.d/
%config(noreplace) %_sysconfdir/pam.d/kppp
%attr(4755,root,root) %_bindir/kppp
%_bindir/kppplogview
%dir %_datadir/apps/kppp
%_datadir/apps/kppp/*
%_datadir/applications/kde/Kppp.desktop
%_datadir/applications/kde/kppplogview.desktop
%_iconsdir/*/*/*/kppp.png
%dir %_docdir/kde/HTML/en/kppp/
%doc %_docdir/kde/HTML/en/kppp/*

%files ksirc
%defattr(-,root,root,-)
%_bindir/ksirc
%_bindir/dsirc
%_datadir/applications/kde/ksirc.desktop
%dir %_docdir/kde/HTML/en/ksirc/
%doc %_docdir/kde/HTML/en/ksirc/*
%_datadir/config/ksircrc
%_libdir/trinity/ksirc.*
%dir %_datadir/apps/ksirc/
%_datadir/apps/ksirc/*
%_iconsdir/*/*/*/ksirc.png
%_libdir/libtdeinit_ksirc.*

%files kwifimanager
%defattr(-,root,root,-)
%_bindir/kwifimanager
%_datadir/applications/kde/kcmwifi.desktop
%_datadir/applications/kde/kwifimanager.desktop
%_datadir/apps/kicker/applets/kwireless.desktop
%dir %_datadir/apps/kwifimanager/
%_datadir/apps/kwifimanager/*
%_iconsdir/*/*/*/kwifimanager*
#%_libdir/libkwireless.*
%_libdir/trinity/kcm_wifi.*
%dir %_docdir/kde/HTML/en/kwifimanager/
%doc %_docdir/kde/HTML/en/kwifimanager/*

%files kdict
%defattr(-,root,root,-)
%_bindir/kdict
%dir %_docdir/kde/HTML/en/kdict/
%doc %_docdir/kde/HTML/en/kdict/*
%dir %_datadir/apps/kdict/
%_datadir/apps/kdict/*
%_datadir/applications/kde/kdict.desktop
%_libdir/trinity/kdict_panelapplet.*
%_datadir/apps/kicker/applets/kdictapplet.desktop
%_iconsdir/*/*/*/kdict*
%_libdir/trinity/kdict.*
%_libdir/trinity/kio_jabberdisco.*
%_libdir/libtdeinit_kdict.*

%files kget
%defattr(-,root,root,-)
%_bindir/kget
%dir %_datadir/apps/kget/
%_datadir/apps/kget/*
%_datadir/apps/khtml/kpartplugins/kget_plug_in.desktop
%_libdir/trinity/khtml_kget.*
%_datadir/applications/kde/kget.desktop
%_datadir/mimelnk/application/x-kgetlist.desktop
%_datadir/apps/khtml/kpartplugins/kget_plug_in.rc
%_iconsdir/*/*/*/khtml_kget*
%_iconsdir/*/*/*/kget*
%dir %_docdir/kde/HTML/en/kget/
%doc %_docdir/kde/HTML/en/kget/*
%_datadir/apps/konqueror/servicemenus/kget_download.desktop

%files krfb
%defattr(-,root,root,-)
%_bindir/krdc
%_bindir/krfb
%_bindir/krfb_httpd
%_datadir/services/vnc.protocol
%_datadir/services/kinetd_krfb.desktop
%dir %_datadir/apps/kinetd/
%_datadir/apps/kinetd/*
%dir %_docdir/kde/HTML/en/krfb/
%doc %_docdir/kde/HTML/en/krfb/*
%doc %_docdir/kde/HTML/en/krdc/*
%_datadir/applications/kde/kcmkrfb.desktop
%_datadir/applications/kde/krdc.desktop
%_datadir/applications/kde/krfb.desktop
%dir %_datadir/apps/krfb/
%_datadir/apps/krfb/*
%dir %_datadir/apps/krdc/
%_datadir/apps/krdc/*
%_libdir/trinity/kcm_krfb.*
%_libdir/trinity/kded_kinetd.*
%_iconsdir/*/*/*/krfb*
%_iconsdir/*/*/*/krdc*
%_datadir/servicetypes/kinetdmodule.desktop
%_datadir/services/kded/kinetd.desktop
%_datadir/services/kinetd_krfb_httpd.desktop

%files knewsticker
%defattr(-,root,root,-)
%_bindir/knewstickerstub
%dir %_docdir/kde/HTML/en/knewsticker/
%doc %_docdir/kde/HTML/en/knewsticker/*
%_datadir/applications/kde/knewsticker-standalone.desktop
%dir %_datadir/apps/knewsticker/
%_datadir/apps/knewsticker/*
%_datadir/apps/kicker/applets/knewsticker.desktop
%dir %_datadir/apps/kconf_update/
%_datadir/apps/kconf_update/knewsticker.upd
%_datadir/apps/kconf_update/knt-0.1-0.2.pl
%_iconsdir/*/*/*/knewsticker.png
%_datadir/applnk/.hidden/knewstickerstub.desktop
%_libdir/trinity/knewsticker_panelapplet.*
#%_libdir/trinity/libkntsrcfilepropsdlg.*


%changelog
* Fri Aug 29 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Mon Nov 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-2mgc
- remove ksirc

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Fri May 25 2007 kde <athena_star {at} 163 {dot} com>  - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Fri Oct 20 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Sun Apr 16 2006 KanKer <kanker@163.com>
- 3.5.2

* Tue Nov 17 2005 KanKer <kanker@163.com>
- remove kopete

* Sun Oct 30 2005 KanKer <kanker@163.com>
- recover kppp

* Mon Oct 17 2005 KanKer <kanker@163.com>
- 3.4.3

* Sun Jul 31 2005 KanKer <kanker@163.com>
- 3.4.2

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Wed May 25 2005 KanKer <kanker@163.com>
- add kdenetwork-kcm_sambaconf.patch from wall_john.

* Thu May 24 2005 KanKer <kanker@163.com>
- fix kopete login msn bug

* Sun Mar 20 2005 KanKer <kanker@163.com>
- 3.4.0

* Sat Dec 18 2004 KanKer <kanker@163.com>
- recover ksir,krfb,krdc etc. 

* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux

* Tue Dec 14 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML

* Sat Aug 21 2004 KanKer <kanker@163.com>
- 3.3

* Sun Jul 11 2004 KanKer <kanker@163.com>
- 3.3beta1

* Thu Jun 10 2004 KanKer <kanker@163.com>  
- update to 3.2.3 release

