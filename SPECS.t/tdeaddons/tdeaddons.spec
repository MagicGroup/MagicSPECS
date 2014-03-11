%define git 1
%define gitdate 20111222
%define debug 0
%define final 0
%define libtool 0

%define qt_version 3.3.8
%define arts_version 1.5.10
%define arts 1
%define _iconsdir %_datadir/icons

Summary: KDE Additional Tools
Summary(zh_CN.UTF-8): KDE 附加工具
Name: tdeaddons
Version: 3.5.14
%if %{git}
Release: 0.git%{gitdate}%{?dist}
%else
Release: 0.1%{?dist}
%endif
License:  GPL
URL: http://www.kde.org
Group:  User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
BuildRoot:%{_tmppath}/%{name}-buildroot
%if %{git}
Source:  %{name}-git%{gitdate}.tar.xz
%else
Source:  ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Source1: make_tdeaddons_git_package.sh
patch0: rm-rellinks.patch
#from lovewilliam
Patch1: http://ftp.magiclinux.org.cn/lovewilliam/Patch/KDE/kdeaddons-3.5.10-kfile_html-tag.patch
Patch2: kdeaddons-3.5.6-love.patch
Patch3: kdeaddons-3.5.13-gcc45.patch
Patch4: tdeaddons-git20111222-libtool.patch
Requires: qt, arts, kdelibs, kdebase, alsa-lib, SDL
Requires: %{name}-kfile-plugins
Requires: %{name}-konq-plugins
Requires: %{name}-kate
Requires: %{name}-searchbar
Requires: %{name}-metabar

%description
Plugins for some KDE applications: %{name} extends the functionality
of Konqueror (web browser and file manager), noatun (media player)
and Kate (text editor), Kicker, knewsticker.

%description -l zh_CN.UTF-8.GB18030
一些KDE程序的插件：%{name}扩展了Konqueror（网页浏览器和文件管理器），
noatun（媒体播放器）和Kate（文本编辑器），Kicker，knewsticker的功能。

#--------------------------------------------------------------------------------------------

%package kfile-plugins
Summary: Kfile-plugins addons
Summary(zh_CN.UTF-8): Kfile 的额外插件
Group:  User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description kfile-plugins
Kfile-plugins addons.

%description kfile-plugins -l zh_CN.UTF-8.GB18030
Kfile 的额外插件。

#-----------------------------------------------------------------------------------------------

%package kicker-applets
Summary: Kicker-applets addons
Summary(zh_CN.UTF-8): Kicker面板小程序
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdebase-core

%description kicker-applets
Kicker-applets addons.

%description kicker-applets -l zh_CN.UTF-8.GB18030
附赠的几个任务栏小程序。包括二进制时钟小程序，颜色撷取器，一个构造非常简单的即时系统监视器，
数学表达式计算器，媒体播放控制器。

#-------------------------------------------------------------------------------------------

%package konqimagegallery
Summary: Konqimagegallery addon
Summary(zh_CN.UTF-8): 个人相册生成器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description konqimagegallery
Konqimagegallery addons.

%description konqimagegallery -l zh_CN.UTF-8.GB18030
个人相册生成器，属文件管理模式下特有的工具插件。此插件可藉由一个塞满图片的目录自动整编出一
套基于HTML组织的相册目录树，用户可以调控相册页面的色彩、每行显示图片数量、缩略图大小、文字
摘要格式等各项参数。

#-------------------------------------------------------------------------------------------

%package renamedlg
Summary: Renamedlg addons
Summary(zh_CN.UTF-8): 文件替换对话框强化插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description renamedlg
Renamedlg addons.

%description renamedlg -l zh_CN.UTF-8.GB18030
文件替换对话框强化插件。在日常操作中，经常进行文件复制或移动操作的用户时而会遇到文件重名现象时
（这包括本地对本地、本地对远程、远程对远程三种可能）生效，这套插件就是为这种异常而设计的人性化
辅助工具，它的工作特征分为两个部分。

当重名文件双方都为可被识别的音频格式时，KDE在弹出的警示框里会分别陈列二首音乐的头信息，并嵌入
一对迷你的试听播放按钮让用户决定该怎么取舍。您可以重命名被复制/移动的那个文件，或是直接覆盖，
或是取消。

当重名文件双方都为可被识别的图片格式时，KDE在弹出的警示框里会分别显示出两幅图片的预览和色彩属
性，呈现直观的比对，并以和上面一样的形式让用户下达进一步指示。

如果在通常情况下发生此类重名现象时，KDE所弹出的警示框只会比对冲突两方的文件大小和最后修改时间，
此插件是对这些基本特性的功能增补。

#------------------------------------------------------------------------------------------------

%package konq-plugins
Summary: Konq-plugins addons
Summary(zh_CN.UTF-8): 一组 Konqueror 插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdebase-core

%description konq-plugins
Konq-plugins addons.

%description konq-plugins -l zh_CN.UTF-8.GB18030
一组Konqueror插件。这些插件的工作性质可以分为多个种类，您可以将其视作Konqueror扩展性的体现。

#------------------------------------------------------------------------------------------------

%package kaddressbook-plugins
Summary: Kaddressbook-plugins addons
Summary(zh_CN.UTF-8): 地址簿管理器KAddressBook的插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description kaddressbook-plugins
Kaddressbook-plugins addons.

%description kaddressbook-plugins -l zh_CN.UTF-8.GB18030
针对KDE-PIM中的地址簿管理器KAddressBook的两组插件。

#----------------------------------------------------------------------------------------------

%package knewsticker
Summary: Knewsticker addons
Summary(zh_CN.UTF-8): KNewsTicker脚本集
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: tdenetwork-knewsticker

%description knewsticker
knewsticker addons

%description knewsticker -l zh_CN.UTF-8.GB18030
KNewsticker是KDE中的一个新闻简报浏览程序。这里提供的几个Perl或Python脚本是用于支持某些摘要
格式规范较特别的网络新闻源。

#---------------------------------------------------------------------------------------------

%package kate
Summary: Kate addons
Summary(zh_CN.UTF-8): KDE 高级文本编辑器 Kate 的一组插件
Group:  User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdebase-kate

%description kate
Kate addons.

%description kate -l zh_CN.UTF-8.GB18030
面向 KDE 高级文本编辑器 Kate 的一组十余个插件。要注意它们是 Kate 所特有的，不能被其他以 
Kate_Part 作为文本编辑器框架的软件如 Quanta、KDevelop 等继承。
Kate 之所以比标准文本编辑器 KWrite 又强大许多，前者支持更多额外插件这点起到了很大作用，
当然，Kate 还有嵌入侧边栏、会话管理、外部工具联合等特有机制。

#----------------------------------------------------------------------------------------------

%package ksig
Summary: Signature generator
Summary(zh_CN.UTF-8): 签名编辑器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Provides:	ksig

%description  ksig
Signature generator.

%description ksig -l zh_CN.UTF-8.GB18030
签名编辑器。KSig并不是常规意义上的插件，它是完全独立的KDE应用程序。其功能很单一，就是一个
个人文书签名的编写器与储存库，一般很少用到。

#---------------------------------------------------------------------------------------------

%package atlantik
Summary: Atlantik map generator
Summary(zh_CN.UTF-8): Atlantik 棋盘设计器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description atlantik
Map generator for atlantik game

%description atlantik -l zh_CN.UTF-8.GB18030
对应 KDE-Games 中的大富翁式游戏 Atlantik 的地图设计器，独立程序。它提供了包含 Atlantik 棋
格内可能设定的各种地产元素、随机卡片、监狱等游戏元素，在一个循环式的棋局里自主定制其地图
的工具。

#------------------------------------------------------------------------------------------

%package searchbar
Summary: Searchbar
Summary(zh_CN.UTF-8): 速搜工具栏
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面

%description searchbar
Search bar for konqueror

%description searchbar -l zh_CN.UTF-8.GB18030
速搜工具，属扩展插件。它在Konqueror界面上嵌入了一个快捷搜索栏，可选的搜索引擎从综合性的Google、
韦氏辞典、维基百科到专向性的音乐指南、电影数据库、Qt手册等有数十项，且可通过Konqueror设置对话框
随时添删，任何可用引擎都能通过插件提供的下拉菜单即时切换。

#-------------------------------------------------------------------------------------------

%package akregator
Summary: Akregator plugins
Summary(zh_CN.UTF-8): Akregator 插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: tdepim-akregator

%description akregator
Akregator plugins.

%description akregator -l zh_CN.UTF-8.GB18030
Akregator 插件。

#-----------------------------------------------------------------------------------------------

%package noatun
Summary: Noatun plugins
Summary(zh_CN.UTF-8): Noatun 插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdemultimedia-noatun >= 3.2

%description noatun
Plugins for noatun.

%description noatun -l zh_CN.UTF-8.GB18030
面向KDE-Multimedia中的媒体播放器Noatun的一组插件，它们中包括了许多界面皮肤和可视化特效，分别适
应华丽或简洁的视觉偏爱，还有一些其它功能型杂类插件。

#-------------------------------------------------------------------------------------------------

%package metabar
Summary: A sidebar plugin for KDE's Konqueror
Summary(zh_CN.UTF-8): Konqueror 的侧边栏插件
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: kdebase-core >= 3.2
Provides: metabar = %version-%release

%description metabar
A sidebar plugin for KDE's Konqueror which shows information and actions for
selected files and directories.

%description metabar -l zh_CN.UTF-8.GB18030
文件/目录元信息预览器，属侧边栏插件，只在文件管理模式下有实际作用。它可以被视作对一种文件的鼠标
右键动作列表的侧边栏替换，对选中对象的所有可执行动作、打开方式、头信息等都会在Metabar工作区域内
以分类图例的形式被列举出来，您也可以向图例中添加更多的自定义动作选项。

#-------------------------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n %{name}-git%{?gitdate}
%else
%setup -q 
%endif
%patch2 -p1
%patch1 -p1
#%patch3 -p1
%patch4 -p1

%Build
unset QTDIR || : ; . /etc/profile.d/qt.sh

export KDEDIR=%{prefix}
export CXXFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG -fno-use-cxa-atexit"
export CFLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG"

make -f admin/Makefile.common

#CFLAGS="$CFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
#CXXFLAGS="$CXXFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
%configure \
	--disable-rpath \
	--enable-closure \
	%if %{final}
	--enable-final \
	%endif
	--with-qt-libraries=$QTDIR/lib

make
%install
mkdir -p $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
   
%files kfile-plugins
%defattr(-,root,root)
%_bindir/lnkforward
%_libdir/trinity/kfile_*
%_datadir/mimelnk/application/x-win-lnk.desktop
%_datadir/applnk/.hidden/lnkforward.desktop
%_datadir/services/kfile_*

%files kicker-applets
%defattr(-,root,root)
%_datadir/apps/mediacontrol
%_iconsdir/*/*/*/ktimemon.png
%_datadir/apps/kicker
%_datadir/config.kcfg/kbinaryclock.kcfg
%_docdir/HTML/en/kicker-applets
%_libdir/trinity/*_panelapplet.*

%files konqimagegallery
%defattr(-,root,root)
%_iconsdir/*/*/*/imagegallery.png
%_libdir/trinity/libkimgallery.*
%_datadir/applnk/.hidden/kimgalleryplugin.desktop
%_datadir/apps/konqiconview/kpartplugins/kimgalleryplugin.rc

%files renamedlg
%defattr(-,root,root)
%_libdir/trinity/librenaudioplugin.*
%_libdir/trinity/librenimageplugin.*
%_datadir/services/renaudiodlg.desktop
%_datadir/services/renimagedlg.desktop

%files konq-plugins
%defattr(-,root,root)
%_bindir/kio_media_realfolder
%_bindir/fsview
%_bindir/jpegorient
%_libdir/trinity/libarkplugin.*
%_libdir/trinity/kcm_kuick.*
%_libdir/trinity/libkuickplugin.*
%_libdir/trinity/libcrashesplugin.*
%_libdir/trinity/webarchivethumbnail.*
%_libdir/trinity/konq_sidebarnews.*
%_libdir/trinity/libbabelfishplugin.*
%_libdir/trinity/libkhtmlsettingsplugin.*
%_libdir/trinity/libminitoolsplugin.*
%_libdir/trinity/libfsviewpart.*
%_libdir/trinity/libdomtreeviewerplugin.*
%_libdir/trinity/konqsidebar_delicious.*
%_libdir/trinity/konqsidebar_mediaplayer.*
%_libdir/trinity/librellinksplugin.*
%_libdir/trinity/libdirfilterplugin.*
%_libdir/trinity/libautorefresh.*
%_libdir/trinity/libwebarchiverplugin.*
%_libdir/trinity/libmfkonqmficon.*
%_libdir/trinity/libvalidatorsplugin.*
%_libdir/trinity/libuachangerplugin.*
%_datadir/apps/khtml
%_datadir/apps/domtreeviewer
%_datadir/apps/microformat
%_datadir/apps/fsview
%_datadir/apps/konqsidebartng
%_datadir/apps/konqlistview
%_datadir/apps/konqiconview
%_datadir/apps/konqueror
%_datadir/apps/imagerotation
%_iconsdir/*/*/*/fsview.png
%_iconsdir/*/*/*/konqside*
%_iconsdir/*/*/*/autorefresh*
%_iconsdir/*/*/*/htmlvalidator.png
%_iconsdir/*/*/*/minitools.png
%_iconsdir/*/*/*/webarchiver.png
%_iconsdir/*/*/*/domtreeviewer.png
%_iconsdir/*/*/*/cssvalidator.png
%_iconsdir/*/*/*/babelfish.png
%_iconsdir/*/*/*/validators.png
%_datadir/applnk/.hidden/plugin_domtreeviewer.desktop
%_datadir/applnk/.hidden/fsview.desktop
%_datadir/applnk/.hidden/kcmkuick.desktop
%_datadir/applnk/.hidden/khtmlsettingsplugin.desktop
%_datadir/applnk/.hidden/mediaplayerplugin.desktop
%_datadir/applnk/.hidden/plugin_babelfish.desktop
%_datadir/applnk/.hidden/plugin_validators.desktop
%_datadir/applnk/.hidden/kuickplugin.desktop
%_datadir/applnk/.hidden/dirfilterplugin.desktop
%_datadir/applnk/.hidden/uachangerplugin.desktop
%_datadir/applnk/.hidden/crashesplugin.desktop
%_datadir/applnk/.hidden/arkplugin.desktop
%_datadir/applnk/.hidden/plugin_webarchiver.desktop
%_datadir/config/translaterc
%_datadir/config.kcfg/konq_sidebarnews.kcfg
%_datadir/services/webarchivethumbnail.desktop
%_datadir/services/ark_plugin.desktop
%_datadir/services/fsview_part.desktop
%_datadir/services/kuick_plugin.desktop
%_docdir/HTML/en/konq-plugins
%exclude %_datadir/apps/konqiconview/kpartplugins/kimgalleryplugin.rc
%exclude %_datadir/apps/konqueror/kpartplugins/searchbar*
%exclude %_datadir/apps/khtml/kpartplugins/akregator*
%exclude %_datadir/apps/konqsidebartng/entries/metabar.desktop
%exclude %_datadir/apps/konqsidebartng/add/metabar_add.desktop
%exclude %_datadir/apps/konqueror/icons/crystalsvg/16x16/actions/google*
%{_libdir}/trinity/libadblock.*
%{_libdir}/trinity/librsyncplugin.*
%{_datadir}/applnk/.hidden/rsyncplugin.desktop
%{_datadir}/icons/crystalsvg/*x*/actions/remotesync*.png

%files kaddressbook-plugins
%defattr(-,root,root)
%_libdir/trinity/libkaddrbk_geo_xxport.*
%_libdir/trinity/libkaddrbk_gmx_xxport.*
%_datadir/apps/kaddressbook
%_datadir/services/kaddressbook/gmx_xxport.desktop
%_datadir/services/kaddressbook/geo_xxport.desktop

%files knewsticker
%defattr(-,root,root)
%_datadir/apps/knewsticker

%files kate
%defattr(-,root,root)
%_libdir/trinity/kate*
%_libdir/trinity/libkate*
%_datadir/apps/kat*
%_datadir/applnk/.hidden/kate*
%_docdir/HTML/en/kate-plugins
%_datadir/services/kate*

%files ksig
%defattr(-,root,root)
%_iconsdir/*/*/*/ksig.png
%_datadir/applications/kde/ksig.desktop
%_datadir/apps/ksig
%_bindir/ksig
%_docdir/HTML/en/ksig

%if 0
%files atlantik
%defattr(-,root,root)
%_bindir/atlantikdesigner
%dir %_datadir/apps/atlantikdesigner/
%_datadir/apps/atlantikdesigner/*
%_datadir/applications/kde/atlantikdesigner.desktop
%_iconsdir/*/*/*/atlantikdesigner.*
%endif

%files searchbar
%defattr(-,root,root)
%_libdir/trinity/libsearchbarplugin.*
%_datadir/apps/konqueror/kpartplugins/searchbar*
%_datadir/apps/konqueror/icons/crystalsvg/16x16/actions/google*

%files akregator
%defattr(-,root,root)
%_libdir/trinity/libakregatorkonqfeedicon.*
%_libdir/trinity/libakregatorkonqplugin.*
%_datadir/apps/akregator/*
%_datadir/apps/khtml/kpartplugins/akregator*
%_datadir/services/akregator_konqplugin.desktop

%if 0
%files noatun
%defattr(-,root,root)
%_bindir/*.bin
%_datadir/apps/noatun/*
%_libdir/trinity/noatun*
%_iconsdir/*/*/*/synaescope.png
%endif

%files metabar
%defattr(-,root,root,-)
%{_libdir}/trinity/konqsidebar_metabar.*
%dir %{_datadir}/apps/metabar
%{_datadir}/apps/metabar/*
%_datadir/apps/konqsidebartng/entries/metabar.desktop
%_iconsdir/*/*/*/metabar*
%_datadir/apps/konqsidebartng/add/metabar_add.desktop

%changelog
* Wed Oct 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-2mgc
- lovewilliam 更新补丁

* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Tue May 29 2007 Liu Di <liudidi@gmail.com> - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Sat Oct 21 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Mon Apr 17 2006 KanKer <kanker@163.com>
- 3.5.2

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3

* Mon Aug 1 2005 KanKer <kanker@163.com>
- 3.4.2

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Mon Mar 21 2005 KanKer <kanker@163.com>
- 3.4.0

* Tue Feb 01 2005 Bamfox <bamfox@163.com>
- remove the rm -rf konq-plugins/rellinks
- add rm-rellinks.patch

* Sun Jan 30 2005 Bamfox <bamfox@163.com>
- fix rellinksToolbar configure

* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux.

* Thu Dec 15 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.
