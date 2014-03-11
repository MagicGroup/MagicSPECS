%define debug 0
%define final 0

%define arts 1

%define qt_version 3.3.8
%define kde_version 3.5.13
%define _iconsdir %_datadir/icons

%define git 1
%define gitdate 20111229

Summary: KDE WebDev - WEB Development package for the K Desktop Environment.
Summary(zh_CN.UTF-8): KDE WebDev - K 桌面环境的网页开发包。
Name:          tdewebdev
Version:       3.5.14
%if %{git}
Release: 	0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: http://quanta.sourceforge.net/
Group:       Applications/Editors
Group(zh_CN.UTF-8):	应用程序/编辑器
BuildRoot:  %{_tmppath}/%{name}-%{version}-buildroot
%if %{git}
Source:	%name-git%{gitdate}.tar.xz
%else
Source:     ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Source1: http://download.sourceforge.net/quanta/css.tar.bz2
Source2: http://download.sourceforge.net/quanta/html.tar.bz2
Source3: http://puzzle.dl.sourceforge.net/sourceforge/quanta/php-quanta-doc-20051114.tar.bz2
Source4: http://download.sourceforge.net/quanta/javascript.tar.bz2
Source5: http://tidy.sourceforge.net/src/tidy_src.tgz
Source6: make_tdewebdev_git_package.sh

Patch1: klinkstatus-chinese-3.5.5.patch
#Patch2: javascript.patch

Requires: kdelibs, kdebase
Obsoletes: WebMaker
Obsoletes: quanta
Provides: quanta

%description
WEB Development package for the K Desktop Environment.

%description -l zh_CN.UTF-8
K 桌面环境的网页开发包。

#--------------------------------------------------------------------------
 
%package kfilereplace
Summary:        Kfilereplace
Summary(zh_CN.UTF-8): 文件内容批量搜索/替换程序。
Group:          Applications/Editors
Group(zh_CN.UTF-8):   应用程序/编辑器
Provides:       kfilereplace
 
%description kfilereplace
Kfilereplace program

%description kfilereplace -l zh_CN.UTF-8
文件内容批量搜索/替换程序。很多时候用户都希望能够简单地对一大批文件进行有逻辑性的
批量编辑处理，这也便是KFileReplace的目的，为了应付各种复杂苛刻的需求，程序提供了
许多谨慎细致的过滤与修改选项。

每当一次批量搜索/替换完成时，程序会印出此次操作的所有动作细节与统计数据，这让用户
能更放心地交付并追踪自己要完成的任务。

%files kfilereplace
%defattr(-,root,root)
%_bindir/kfilereplace
%dir %_datadir/apps/kfilereplacepart
%_datadir/apps/kfilereplacepart/*
%dir %_datadir/apps/kfilereplace/
%_datadir/apps/kfilereplace/*
%_datadir/services/kfilereplacepart.desktop
#%doc %_docdir/kde/HTML/en/kfilereplace
%_datadir/applications/kde/kfilereplace.desktop
%_libdir/trinity/libkfilereplacepart.*
%_iconsdir/*/*/*/kfilerep*
 
#--------------------------------------------------------------------------

%package kommander
Summary:        Kommander
Summary(zh_CN.UTF-8): 动态对话框设计器与解释器
Group:          Applications/Editors
Group(zh_CN.UTF-8):   应用程序/编辑器
Provides:       kommander
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
 
%description kommander
Kommander program

%description kommander -l zh_CN.UTF-8
动态对话框设计器与解释器，您可以用它设计和一般KDE程序的外观和使用习惯上毫无二致的实用
程序，但您却不需要懂得C++编码，所有Kommander程序都是用XML文本描述，并通过Kommander 提
供的对话框解释器解释执行的。

%if 0
%files kommander
%defattr(-,root,root)
%_bindir/kmdr-executor
%_bindir/kmdr-plugins
%_bindir/kmdr-editor
%_bindir/xsldbg
%_datadir/mimelnk/application/x-kommander.desktop
%doc %_docdir/HTML/en/kommander
%_datadir/applnk/.hidden/kmdr-executor.desktop
%_datadir/applications/kde/kmdr-editor.desktop
%_iconsdir/*/*/*/kommand*
%_datadir/apps/kommander
%_datadir/apps/kmdr-editor
%_datadir/apps/katepart/syntax/kommand*
%_datadir/apps/kdevappwizard/templates/kommander*
%_datadir/apps/kdevappwizard/kommander*
%_datadir/services/kommander_part.desktop
%_libdir/trinity/libkommander_part.*
%_libdir/libkommanderwidgets.la
%_libdir/libkommanderwidgets.so.*
%_libdir/libkommanderplugin.la
%_libdir/libkommanderplugin.so.*
%_libdir/libkommanderwidget.la
%_libdir/libkommanderwidget.so.*
%endif

#--------------------------------------------------------------------------

%package devel
Summary: Development files for kdewebdev
Summary(zh_CN.UTF-8): kdewebdev的开发文件
Group: Development/Libraries
Requires: tdewebdev
Requires: kdelibs-devel 
%description devel
Development files for %{name}.
Install %{name}-devel if you want to write or compile %{name} plugins.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。
如果你编写或编译 %{name} 插件请安装 %{name}-devel。

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate} a 1 -a 2 -a 3 -a 4 -a 5
%else
%setup -q a 1 -a 2 -a 3 -a 4 -a 5
%endif

%patch1 -p1
#%patch2 -p0
#临时补丁
sed -i 's/localtdedir/localkdedir/g' quanta/src/dtds.cpp

%Build
QTDIR="" && . /etc/profile.d/qt.sh
mkdir build
cd build
%cmake -DBUILD_ALL=ON ..
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT
cd build
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root)
%{_bindir}/quanta
%{_libdir}/trinity/quantadebugger*
%{_datadir}/applications/kde/quanta.desktop
%{_datadir}/icons/hicolor/*/apps/quanta.png
%{_datadir}/mimelnk/application/x-webprj.desktop
%{_datadir}/services/*.desktop
%{_datadir}/servicetypes/quantadebugger.desktop
%{_datadir}/apps/*

%files devel
%defattr(-,root,root)

%changelog
* Sat Sep 20 2008 Ni Hui <shuizhuyuanluo@126.com> - 3.5.10-1.1mgc
- 重写 spec file 字段
- rebuild against subversion > 1.5
- 戊子  八月廿一

* Mon Sep 01 2008 Liu Di <liudidi@gmail.com> - 3.5.10-1mgc
- 更新到 3.5.10

* Wed Feb 20 2008 Liu Di <liudidi@gmail.com> - 3.5.9-1mgc
- update to 3.5.9

* Fri Oct 19 2007 Liu Di <liudidi@gmail.com> - 3.5.8-1mgc
- update to 3.5.8

* Tue May 29 2007 Liu Di <liudidi@gmail.com> - 3.5.7-1mgc
- update to 3.5.7

* Sat Jan 27 2007 Liu Di <liudidi@gmail.com> - 3.5.6-1mgc
- update to 3.5.6

* Sun Oct 22 2006 Liu Di <liudidi@gmail.com> - 3.5.5-1mgc
- update to 3.5.5

* Fri Aug 25 2006 Liu Di <liudidi@gmail.com> - 3.5.4-1mgc
- update to 3.5.4

* Thu Jul  1 2006 Liu Di <liudidi@gmail.com>
- update to 3.5.3

* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux.

*Thu Dec 14 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML and add some patch form FC3

* Wed Oct 27 2004 KanKer <kanker@163.com>
- fix klinkstatus Chinese  bug.

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.
