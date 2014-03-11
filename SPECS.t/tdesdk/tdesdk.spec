%define debug 0
%define final 1

%define qt_version 3.3.8
%define arts 1

%define libtool 1
%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111228

Summary: a collection of applications and tools used by KDE developers
Summary(zh_CN.UTF-8): KDE 开发人员用的应用程序和工具集合
Name:          tdesdk
Version:       3.5.14
%if %{git}
Release:	0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:		GPL
URL:		http://www.kde.org
Group:         User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
%if %{git}
Source0:	%{name}-git%{gitdate}.tar.xz
%else
Source0:      ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Source1:	make_tdesdk_git_package.sh
Source3:      kdesdk-perl-requires.sh
Patch0:		kdesdk-3.5.x-kompare-cjk.patch
Patch1:		kdesdk-3.5.10-gcc44.patch
# upstream patches
Requires: tdelibs, tdebase

%description
A collection of applications and tools used by KDE developers.
Among other things, kdesdk provides tools for working on the KDE CVS
repository.

%description -l zh_CN.UTF-8
KDE 开发人员用的应用程序和工具集合。kdesdk 提供了可以在 KDE CVS 仓库上工作的工具。

%package devel
Summary: Development files for kdesdk
Summary(zh_CN.UTF-8): kdesdk 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}
Requires: tdelibs-devel
#Requires: XFree86-devel

%description devel
Development files for kdesdk. Install kdesdk-devel if you wish
to develop or compile KDE sdk applications.

%description devel -l zh_CN.UTF-8
kdesdk 的开发文件。

#**************************************************************************************

%package umbrello
Summary:    UML Modeller
Summary(zh_CN.UTF-8): UML 建模器
Group:         User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Obsoletes:      umbrello
Provides:       umbrello = %version-%release
 
%description umbrello
Umbrello UML Modeller is a UML diagramming tool for KDE.

%description umbrello -l zh_CN.UTF-8
基于 UML1.4 标准的 UML（统一建模语言）建模工具。作为定位专一的软件，
Umbrello 的设计规划和功能分类均较为严谨，支持用例图、状态图、协作图、
活动图、序列图、类图、部署图、组件图、实体关系图九种构图方案。它还
有一个吸引人的特点在于可以根据建模导出为C++、Java、PHP等多种语言的
代码模型，也可以导入既成代码分析出构图。

%if 0
%files umbrello
%defattr(-,root,root,-)
%_bindir/umbrello
%_datadir/applications/kde/umbrello.desktop
%doc %_docdir/kde/HTML/en/umbrello
%dir %_datadir/apps/umbrello/
%_datadir/apps/umbrello/*
%_iconsdir/*/*/*/umbrello*
%_datadir/mimelnk/application/x-umbrello.desktop
%endif

#****************************************************************************


%package cervisia
Summary:    CVS client part
Summary(zh_CN.UTF-8): 并行版本控制系统CVS（Concurrent Versions System）前端
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Obsoletes:      cervisia
Provides:       cervisia = %version-%release
Requires:       cvs
 
%description cervisia
CVS client part.

%description cervisia -l zh_CN.UTF-8
并行版本控制系统CVS（Concurrent Versions System）前端，CVS是一种在开源业界
常见的一种特殊文件服务器，用于在多人协调开发的环境中管理不断更新的代码文件
及其历史记录，而Cervisia可以为本只有命令行界面的cvs提供在图形界面下工作的
良好助力，除支持cvs自备的各项子命令外，它还拥有生成版本分支历史树和补丁对
照视图等非常便利的特性。

%files cervisia
%defattr(-,root,root,-)
%_bindir/cervisia
%_bindir/cvsaskpass
%_bindir/cvsservice
%_datadir/apps/kconf_update/cervisia-change_repos_list.pl
%_datadir/apps/kconf_update/cervisia-normalize_cvsroot.pl
%_iconsdir/*/*/*/cervisia*
%_iconsdir/*/*/*/vcs*
#%_iconsdir/*/*/*/svn*
#%_datadir/apps/konqueror/servicemenus/subversion*
#%_mandir/man1/cervisia*
#%_mandir/man1/cvs*
#%_mandir/man1/noncvslist*
%_datadir/config.kcfg/cervisiapart.kcfg
%dir %_datadir/apps/cervisia/
%_datadir/apps/cervisia/*
%_datadir/applications/kde/cervisia.desktop
%doc %_docdir/kde/HTML/en/cervisia
%dir %_datadir/apps/cervisiapart/
%_datadir/apps/cervisiapart/*
%_datadir/apps/kconf_update/cervisia.upd
%_datadir/apps/kconf_update/change_colors.pl
%_datadir/apps/kconf_update/move_repositories.pl
%_datadir/services/cvsservice.desktop
%_libdir/trinity/libcervisiapart.*
%_libdir/trinity/cervisia.*
%_libdir/trinity/cvsaskpass.*
%_libdir/trinity/cvsservice.*
%_libdir/libtdeinit_cervisia.*
%_libdir/libtdeinit_cvsaskpass.*
%_libdir/libtdeinit_cvsservice.*

#****************************************************************************

%package kompare
Summary: KDE diff graphic tool
Summary(zh_CN.UTF-8): 补丁制作、预览程序。
Group:  User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Provides: kompare = %version-%release
 
%description kompare
kompare is a KDE diff graphic tool

%description kompare -l zh_CN.UTF-8
补丁制作、预览程序。这里指的补丁不是二进制文件补丁，而是针对一对纯文本文件集产生
的差异对比数据。Kompare最大的特色是精致生动的校勘界面，它可以避免让用户直接接触
补丁原文，以对比视图将补丁应用前后的文本内容分页显示出来，并给出量化的更改点统计。

%if 0
%files kompare
%defattr(-,root,root,-)
%_bindir/kompare
%doc %_docdir/kde/HTML/en/kompare
%_datadir/applications/kde/kompare.desktop
%_datadir/servicetypes/kompareviewpart.desktop
%dir %_datadir/apps/kompare/
%_datadir/apps/kompare/*
%_iconsdir/*/*/*/kompare*
%endif

#***********************************************************************************

%package kcachegrind
Summary: KCachegrind
Summary(zh_CN.UTF-8): Profile数据剖析器。
Group: User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Provides: kcachegrind = %version-%release
Requires: valgrind
 
%description kcachegrind
KCachegrind is a visualisation tool for the profiling data generated by
Cachegrind and Calltree (they profile data file format is upwards compatible).
Calltree extends Cachegrind, which is part of Valgrind.

%description kcachegrind -l zh_CN.UTF-8
Profile数据剖析器。profile一词在此可理解为一种供分析程序运行中涉及调用的内存使用
状况数据，常用于检查在编码阶段难以避免且难以追踪的内存泄漏隐患，由于这种问题难以
被肉眼发现，所以需要辅助工具来帮助除错，也可以通过它为优化编码提供参考。

KCachegrind也随赠了一批脚本，可将由其他几种常见内存分析工具，如Memprof、pprof所
生成的profile数据转换成可供KCachegrind识别处理的格式。

%if 0
%files kcachegrind
%defattr(-,root,root,-)
%_bindir/kcachegrind
%doc %_docdir/kde/HTML/en/kcachegrind
%_iconsdir/*/*/*/kcachegrind*
%dir %_datadir/apps/kcachegrind/
%_datadir/apps/kcachegrind/*
%_datadir/mimelnk/application/x-kcachegrind.desktop
%_datadir/applications/kde/kcachegrind.desktop
%endif

#************************************************************************************

%package po2xml
Summary: An xml2po and vice versa converters
Summary(zh_CN.UTF-8): 一组用于语言包处理的小工具集合
Group: User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Provides: po2xml = %version-%release
Provides: %{name}-xml2pot = %version-%release
 
%description po2xml
An xml2po and vice versa converters.

%description po2xml -l zh_CN.UTF-8
一组用于语言包处理的小工具集合，包含五个程序：

  -- po2xml：可将翻译过的po语言包转换成原始的XML格式，在KDE中一般是软件文档翻译流程中
             的步骤。

  -- split2po：可将一对翻译前、翻译后的XML格式DocBook文档整理归档出一份对应的po格式语
               言包，在KDE中一般也是用于软件文档翻译。

  -- swappo：将po文件中的译文原句与译文本身交换，例如可将英语──法语的语言包转换为法
             语──英语的语言包。

  -- transxx：用于将已被翻译过的po文件转换回未经翻译的原始模板形式。

  -- xml2pot：用于将XML形式的文档原件转换成po语言包样板，在KDE中也是用于软件文档翻译。

%if 0
%files po2xml
%defattr(-,root,root,-)
%_bindir/po2xml
%_bindir/split2po
%_bindir/swappo
%_bindir/transxx
%_bindir/xml2pot
%endif

#****************************************************************************************

%package kbabel
Summary:    KBabel is a set of tools for editing and managing gettext PO files
Summary(zh_CN.UTF-8): 一套翻译工具
Group: User Interface/Desktops
Group(zh_CN.UTF-8):  用户界面/桌面
Provides:       kbabel = %version-%release
Requires:       gettext
 
%description kbabel
KBabel is a set of tools for editing and managing gettext PO files.
Main part is a powerful and comfortable PO file editor which features
full navigation capabilities, full editing functionality, possibility
to search for translations in different dictionaries, spell and
syntax checking, showing diffs and many more. Also included is a
"Catalog Manager", a file manager view which helps keeping an overview
of PO files. Last but not least it includes a standalone
dictionary application as an additional possibility to access KBabel's
powerful dictionaries.
KBabel will help you to translate fast and also keep consistent translations.

%description kbabel -l zh_CN.UTF-8
一套翻译工具，它在狭义上是一个图形界面的软件翻译工作环境，广义上则是对一个支持国际化软件
实施规范软件的多语种翻译、提交工作的集成套件，它的中心思想将整个软件翻译当作工程来管理。
完整的KBabel包含三个主要组件：

   CatalogManager：翻译工作目录管理器，对于管理有一定规模的多人参与的本地化软件语言包目录
有一定裨益。它可以针对一个或一组语言包的翻译进度实施查询、校验、搜索等需要，并且和邮件系
统、并行版本控制系统（主要是Subversion，这是KDE项目官方当前采用的系统）有集成，能够在网络
环境中协调翻译项目的管理控制。

   KBabel：本套件核心工具，一个语言包文件（po文件）编辑器，是面向翻译者的主要翻译工具。po文
件虽然是纯文本格式，但有其固定的编排格式，KBabel提供的友好编辑界面结合拼写检查、翻译有效性
检查、外挂词典、差异对比等一系列辅助功能可以增强翻译工作的效率。

   如前文所言，KBabel视翻译工作为一组工程，在使用KBabel时您会发现它有一套身份定义机制，这便
是考虑到多人工作的需要，如果您结合并行版本控制系统使用，这种设计的轮廓也就更为清晰。

   KBabelDict：这是一个给翻译人员使用的词典搜索工具，可以和KDE的本地化项目官方主页协作进行在
线词汇搜索。

另外，KBabel还附带了一个针对po格式文件的文件信息预览插件，它允许用户以饼状图形式查看一个po文
件的翻译进度。


%files kbabel
%defattr(-,root,root,-)
%_bindir/kbabel
%_bindir/kbabeldict
%_bindir/catalogmanager
%_datadir/applications/kde/kbabel.desktop
%_datadir/applications/kde/kbabeldict.desktop
%_datadir/applications/kde/catalogmanager.desktop
%_iconsdir/*/*/*/catalogmanager*
%_iconsdir/*/*/*/kbabel*
%dir %_datadir/apps/kbabel
%_datadir/apps/kbabel/*
%_datadir/apps/kconf_update/kbabel-difftoproject.upd
%_datadir/apps/kconf_update/kbabel-project.upd
%_datadir/apps/kconf_update/kbabel-projectrename.upd
%_datadir/config.kcfg/kbabel.kcfg
%_datadir/config.kcfg/kbprojectsettings.kcfg
%dir %_datadir/apps/catalogmanager
%_datadir/apps/catalogmanager/*
%doc %_docdir/kde/HTML/en/kbabel
%_datadir/services/kbabel_*.desktop
%_datadir/services/po*.desktop
%_datadir/services/dbsea*.desktop
%_datadir/services/kfile_po.desktop
%_datadir/services/tmx*.desktop
%_datadir/servicetypes/kbabel*.desktop
%_libdir/libkbabelcommon.so.*
%_libdir/libkbabelcommon.la
%_libdir/libkbabeldictplugin.la
%_libdir/libkbabeldictplugin.so.*
%_libdir/trinity/kbabel*.so
%_libdir/trinity/kbabel*.la
%_libdir/trinity/kfile_po.so
%_libdir/trinity/kfile_po.la
%_libdir/trinity/pothumbnail.so
%_libdir/trinity/pothumbnail.la

#*************************************************************************************************



%define __perl_requires %{SOURCE3}

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q 
%endif

%Build
unset QTDIR && . /etc/profile.d/qt.sh

mkdir build
cd build
%cmake	-DWITH_DBSEARCHENGINE=ON \
	-DWITH_KCAL=ON \
	-DBUILD_ALL=ON ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make DESTDIR=%{buildroot} install

%clean   
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
 /usr/bin/kbugbuster
   /usr/lib/libcvsservice.la
   /usr/lib/libcvsservice.so
   /usr/lib/libcvsservice.so.0
   /usr/lib/libcvsservice.so.0.1.0
   /usr/lib/libkbabelcommon.so
   /usr/lib/libkbabeldictplugin.so
   /usr/lib/trinity/kcal_bugzilla.la
   /usr/lib/trinity/kcal_bugzilla.so
   /usr/share/applications/kde/kbugbuster.desktop
   /usr/share/apps/kapptemplate/appframework/AUTHORS
   /usr/share/apps/kapptemplate/appframework/COPYING
   /usr/share/apps/kapptemplate/appframework/ChangeLog
   /usr/share/apps/kapptemplate/appframework/INSTALL
   /usr/share/apps/kapptemplate/appframework/NEWS
   /usr/share/apps/kapptemplate/appframework/README
   /usr/share/apps/kapptemplate/appframework/VERSION
   /usr/share/apps/kapptemplate/appframework/app.lsm
   /usr/share/apps/kapptemplate/appframework/app.spec
   /usr/share/apps/kapptemplate/appframework/base-Makefile.am
   /usr/share/apps/kapptemplate/appframework/base-Makefile.cvs
   /usr/share/apps/kapptemplate/appframework/configure.in.in.in
   /usr/share/apps/kapptemplate/appframework/no-exe/COPYING
   /usr/share/apps/kapptemplate/appframework/no-exe/INSTALL
   /usr/share/apps/kapptemplate/appframework/po-Makefile.am
   /usr/share/apps/kapptemplate/bin/kapptemplate
   /usr/share/apps/kapptemplate/existing/app-Makefile.am
   /usr/share/apps/kapptemplate/existing/app-desktop
   /usr/share/apps/kapptemplate/include/existing.module
   /usr/share/apps/kapptemplate/include/kapptemplate.common
   /usr/share/apps/kapptemplate/include/kapptemplate.module
   /usr/share/apps/kapptemplate/include/kpartapp.module
   /usr/share/apps/kapptemplate/include/kpartplugin.module
   /usr/share/apps/kapptemplate/kapp/app-Makefile.am
   /usr/share/apps/kapptemplate/kapp/app-configure.in.in
   /usr/share/apps/kapptemplate/kapp/app-desktop
   /usr/share/apps/kapptemplate/kapp/app.cpp
   /usr/share/apps/kapptemplate/kapp/app.h
   /usr/share/apps/kapptemplate/kapp/app_client.cpp
   /usr/share/apps/kapptemplate/kapp/appiface.h
   /usr/share/apps/kapptemplate/kapp/apppref.cpp
   /usr/share/apps/kapptemplate/kapp/apppref.h
   /usr/share/apps/kapptemplate/kapp/appui.rc
   /usr/share/apps/kapptemplate/kapp/appview.cpp
   /usr/share/apps/kapptemplate/kapp/appview.h
   /usr/share/apps/kapptemplate/kapp/doc-Makefile.am
   /usr/share/apps/kapptemplate/kapp/doc-app-Makefile.am
   /usr/share/apps/kapptemplate/kapp/hi16-app-app.png
   /usr/share/apps/kapptemplate/kapp/hi32-app-app.png
   /usr/share/apps/kapptemplate/kapp/hi48-app-app.png
   /usr/share/apps/kapptemplate/kapp/index.docbook
   /usr/share/apps/kapptemplate/kapp/lo16-app-app.png
   /usr/share/apps/kapptemplate/kapp/lo32-app-app.png
   /usr/share/apps/kapptemplate/kapp/main.cpp
   /usr/share/apps/kapptemplate/kapp/no-exe/hi16-app-app.png
   /usr/share/apps/kapptemplate/kapp/no-exe/hi32-app-app.png
   /usr/share/apps/kapptemplate/kapp/no-exe/hi48-app-app.png
   /usr/share/apps/kapptemplate/kapp/no-exe/lo16-app-app.png
   /usr/share/apps/kapptemplate/kapp/no-exe/lo32-app-app.png
   /usr/share/apps/kapptemplate/kapp/pics-Makefile.am
   /usr/share/apps/kapptemplate/kpartapp/app-Makefile.am
   /usr/share/apps/kapptemplate/kpartapp/app-configure.in.in
   /usr/share/apps/kapptemplate/kpartapp/app-desktop
   /usr/share/apps/kapptemplate/kpartapp/app.cpp
   /usr/share/apps/kapptemplate/kpartapp/app.h
   /usr/share/apps/kapptemplate/kpartapp/app_part-desktop
   /usr/share/apps/kapptemplate/kpartapp/app_part.cpp
   /usr/share/apps/kapptemplate/kpartapp/app_part.h
   /usr/share/apps/kapptemplate/kpartapp/app_part.rc
   /usr/share/apps/kapptemplate/kpartapp/app_shell.rc
   /usr/share/apps/kapptemplate/kpartapp/doc-Makefile.am
   /usr/share/apps/kapptemplate/kpartapp/doc-app-Makefile.am
   /usr/share/apps/kapptemplate/kpartapp/hi16-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/hi32-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/hi48-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/index.docbook
   /usr/share/apps/kapptemplate/kpartapp/lo16-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/lo32-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/main.cpp
   /usr/share/apps/kapptemplate/kpartapp/no-exe/hi16-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/no-exe/hi32-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/no-exe/hi48-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/no-exe/lo16-app-app.png
   /usr/share/apps/kapptemplate/kpartapp/no-exe/lo32-app-app.png
   /usr/share/apps/kapptemplate/kpartplugin/hi16-action-plugin.png
   /usr/share/apps/kapptemplate/kpartplugin/hi22-action-plugin.png
   /usr/share/apps/kapptemplate/kpartplugin/no-exe/hi16-action-plugin.png
   /usr/share/apps/kapptemplate/kpartplugin/no-exe/hi22-action-plugin.png
   /usr/share/apps/kapptemplate/kpartplugin/plugin-Makefile.am
   /usr/share/apps/kapptemplate/kpartplugin/plugin_app.cpp
   /usr/share/apps/kapptemplate/kpartplugin/plugin_app.h
   /usr/share/apps/kapptemplate/kpartplugin/plugin_app.rc
   /usr/share/apps/kbugbuster/kbugbusterui.rc
   /usr/share/apps/kbugbuster/pics/bars.png
   /usr/share/apps/kbugbuster/pics/logo.png
   /usr/share/apps/kbugbuster/pics/tools.png
   /usr/share/apps/kbugbuster/pics/top-right.png
   /usr/share/cmake/cervisia.cmake
   /usr/share/doc/kde/HTML/en/kbugbuster/common
   /usr/share/doc/kde/HTML/en/kbugbuster/index.cache.bz2
   /usr/share/doc/kde/HTML/en/kbugbuster/index.docbook
   /usr/share/doc/kde/HTML/en/kcachegrind/common
   /usr/share/doc/kde/HTML/en/kcachegrind/index.cache.bz2
   /usr/share/doc/kde/HTML/en/kcachegrind/index.docbook
   /usr/share/doc/kde/HTML/en/kompare/common
   /usr/share/doc/kde/HTML/en/kompare/index.cache.bz2
   /usr/share/doc/kde/HTML/en/kompare/index.docbook
   /usr/share/doc/kde/HTML/en/kompare/settings-diff1.png
   /usr/share/doc/kde/HTML/en/kompare/settings-diff2.png
   /usr/share/doc/kde/HTML/en/kompare/settings-diff3.png
   /usr/share/doc/kde/HTML/en/kompare/settings-diff4.png
   /usr/share/doc/kde/HTML/en/kompare/settings-view1.png
   /usr/share/doc/kde/HTML/en/kompare/settings-view2.png
   /usr/share/doc/kde/HTML/en/tdesvn-build/common
   /usr/share/doc/kde/HTML/en/tdesvn-build/index.cache.bz2
   /usr/share/doc/kde/HTML/en/tdesvn-build/index.docbook
   /usr/share/doc/kde/HTML/en/umbrello/activity-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/add-remove-languages.png
   /usr/share/doc/kde/HTML/en/umbrello/aggregation.png
   /usr/share/doc/kde/HTML/en/umbrello/association.png
   /usr/share/doc/kde/HTML/en/umbrello/authors.docbook
   /usr/share/doc/kde/HTML/en/umbrello/class-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/class.png
   /usr/share/doc/kde/HTML/en/umbrello/code-import.png
   /usr/share/doc/kde/HTML/en/umbrello/code_import_and_generation.docbook
   /usr/share/doc/kde/HTML/en/umbrello/collaboration-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/common
   /usr/share/doc/kde/HTML/en/umbrello/composition.png
   /usr/share/doc/kde/HTML/en/umbrello/credits.docbook
   /usr/share/doc/kde/HTML/en/umbrello/folders.png
   /usr/share/doc/kde/HTML/en/umbrello/generalization.png
   /usr/share/doc/kde/HTML/en/umbrello/generation-options.png
   /usr/share/doc/kde/HTML/en/umbrello/index.cache.bz2
   /usr/share/doc/kde/HTML/en/umbrello/index.docbook
   /usr/share/doc/kde/HTML/en/umbrello/introduction.docbook
   /usr/share/doc/kde/HTML/en/umbrello/other_features.docbook
   /usr/share/doc/kde/HTML/en/umbrello/sequence-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/state-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/umbrello-main-screen.png
   /usr/share/doc/kde/HTML/en/umbrello/umbrello-ui-clean.png
   /usr/share/doc/kde/HTML/en/umbrello/umbrello-ui.png
   /usr/share/doc/kde/HTML/en/umbrello/uml_basics.docbook
   /usr/share/doc/kde/HTML/en/umbrello/use-case-diagram.png
   /usr/share/doc/kde/HTML/en/umbrello/working_with_umbrello.docbook
   /usr/share/icons/hicolor/128x128/apps/kbugbuster.png
   /usr/share/icons/hicolor/16x16/apps/kbugbuster.png
   /usr/share/icons/hicolor/22x22/apps/kbugbuster.png
   /usr/share/icons/hicolor/32x32/apps/kbugbuster.png
   /usr/share/icons/hicolor/48x48/apps/kbugbuster.png
   /usr/share/icons/hicolor/64x64/apps/kbugbuster.png
   /usr/share/icons/locolor/16x16/apps/kbugbuster.png
   /usr/share/icons/locolor/32x32/apps/kbugbuster.png
   /usr/share/services/kresources/kcal/bugzilla.desktop

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Wed Feb 19 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Mon Jun 25 2007 kde <athena_star {at} 163 {dot} com> - 3.5.7-2mgc
- add kdesdk-3.5.x-kompare-cjk.patch

* Fri May 25 2007 kde <athena_star {at} 163 {dot} com> - 3.5.7-1mgc
- update to 3.5.7

* Fri Jan 26 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com> - 3.5.3-1mgc
- update to 3.5.3

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3
* Mon Aug 1 2005 KanKer <kanker@163.com>
- 3.4.2
* Tue Jun 2 2005 KanKer <kanker@163.com>
- 3.4.1
* Mon Mar 21 2005 KanKer <kanker@163.com>
- 3.4.0
* Fri Dec 17 2004 KanKer <kanker@163.com>
- build 3.3.2
* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.
