%define git 1
%define gitdate 20111222
%define debug 0

%define final 0
%define rpm_clean 1
%define arts 1

%define qt_version 3.3.8
%define _iconsdir %_datadir/icons

Summary: Admin Tools under KDE 
Summary(zh_CN.UTF-8): KDE下的管理工具
Name:          tdeadmin
Version:       3.5.14
%if %{git}
Release:	0.git%{gitdate}%{?dist}
%else
Release:       0.1%{?dist}
%endif
License:     GPL
URL: http://www.kde.org
Group:         User Interface/Desktops
Group(zh_CN.UTF-8):	用户界面/桌面
BuildRoot:     %{_tmppath}/%{name}-buildroot
%if %{git}
Source: %{name}-git%{gitdate}.tar.xz
%else
Source:     ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
%endif
Patch0: kdeadmin-kuser-add_sudo.patch
Patch1: kdeadmin-kpackage_crash.patch
Patch2: kdeadmin-kpackage_locale.patch
Patch3: tdeadmin-git20111222-libtool.patch
Requires: qt, arts, tdelibs, tdebase
%description
Some admin tools under KDE, such as kpackage, kuser and so on

%description -l zh_CN.UTF-8
一些KDE下的管理工具，比如kpackage, kuser等等。

#-------------------------------------------------------------------------------------------

%package kpackage
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Summary:    Manager for DEB, RPM
Summary(zh_CN.UTF-8): KDE 软件包管理程序
Requires:   tdeadmin = %version-%release
Obsoletes:  kpackage < 2:3.4.3
Provides:   kpackage = %version

%description kpackage
Kpackage is a package manager that is integrated into the K Desktop
Environemnt.  It works with the KDE File Manager to manage DEB, RPM
and Slackware tgz software packages.

%description kpackage -l zh_CN.UTF-8
KDE软件包管理程序。KPackage现支持RPM、DEB、TGZ、Portage、Ports+PKG等主流的BSD或GNU/Linux发行
版包管理机制，它除提供基本的安装、卸载支持外，在用户需要对整个系统的软件包储备状况实行通览、
搜索、批量操作时会给予即使纯命令行界面拥护者也应承认的便利。

#--------------------------------------------------------------------------------------------

%package ksysv
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Summary:    Edit your SysV-style init configuration
Summary(zh_CN.UTF-8): 基于 System V 标准的初始化脚本设置程序
Provides:       ksysv

%description ksysv
SysV-Init Editor lets you edit your SysV-style init configuration
using drag'n'drop.

%description ksysv -l zh_CN.UTF-8
基于System V标准的初始化脚本设置程序，只支持GNU/Linux系统。这里的System V脚本是一系列在不同
运行级别下，系统在引导或退出时要自动执行的一批服务进程调度脚本，它们的执行先后顺序由文件名
里的序号来决定。KSysV在第一次启动时会通过向导让用户确认当前的发行版类型，从而保证程序运作合
规，支持鼠标拖放和操作日志。此程序的一个缺憾在于，主界面上各个列表框架的尺寸不能任意拖放，
在同时选中多个运行级别时界面显得杂乱。

#---------------------------------------------------------------------------------------------

%package kcron
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Summary:    Kcron Program
Summary(zh_CN.UTF-8): 计划任务服务 Crond 的图形化配置前端
Provides:       kcron

%description kcron
Kcron Program

%description kcron -l zh_CN.UTF-8
KCron是计划任务服务Crond的图形化配置前端。Crond是一个类Unix系统中常见的计划任务服务，一般用于
系统定时维护，它允许将定时规则设得很精细，例如在“每月第一周周五晚十时至周六上午七时之间每两
小时，以及周六上午八时”这几个时间点上执行某程序，只要一条任务描述语句就能做到。一般不建议用
KCron 调度在图形界面下运行的程序，如果要这样做，您可以选择 KDE-PIM 中的 KAlarm。

#---------------------------------------------------------------------------------------------

%package kdat
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Summary:    Kdat Program
Summary(zh_CN.UTF-8): 磁带备份工具
Provides:       kdat

%description kdat
Kdat Program

%description kdat -l zh_CN.UTF-8
KDE的磁带备份工具，基于传统的磁带备份程序tar工作。一般个人电脑现在很少有理由使用磁带设备，不过
磁带设备现今仍然还是许多Unix系统管理员首选的备份媒介。在KDE中，有的发行版在发布预编译软件包时
会将这个程序剥除掉，毕竟个人用户很可能永远没必要接触它。

#---------------------------------------------------------------------------------------------

%package kuser
Group:      User Interface/Desktops
Group(zh_CN.UTF-8):   用户界面/桌面
Summary:    Kuser Program
Summary(zh_CN.UTF-8): KDE 下的系统用户管理程序
Provides:       kuser

%description kuser
Kuser Program

%description kuser -l zh_CN.UTF-8
KDE下的系统用户管理程序，主要功能是用户添删、用户属性编辑、用户密码更改、组添删、组属性编辑、
组成员编辑等大批常见管理操作，而且在KUser主界面上的用户列表中，使用者能直接从横列显示颜色中区
分此用户是伪用户还是正常用户。

在高级特性方面，KUser提供了对网络信息服务NIS、轻量级目录访问协议LDAP、Samba等高级认证机制的设
定，不过较少用到。

#----------------------------------------------------------------------------------------------

%prep
%if %{git}
%setup -q -n %{name}-git%{gitdate}
%else
%setup -q 
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -rf knetworkconf
make -f Makefile.cvs

echo $PWD

%Build
unset QTDIR && . /etc/profile.d/qt.sh
FLAGS="$RPM_OPT_FLAGS -DNDEBUG -DNO_DEBUG"

%if %{debug}
  FLAGS="-O0"
%endif

export KDEDIR=%{_prefix}
export PATH=$KDEDIR/bin:$PATH
export CFLAGS="$FLAGS"
export CXXFLAGS="$FLAGS"

rm -rf kcmlinuz
rm -rf kdat
rm -rf kwuftpd
rm -rf lilo-config
rm -rf secpolicy
make -f admin/Makefile.common cvs

#CFLAGS="$CFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
#CXXFLAGS="$CXXFLAGS -lXext -lkparts -lz -lsoundserver_idl -lkmedia2_idl -lartsflow_idl -lmcop -ldl -lkdecore -lkdeui -lkdesu -lX11 -lDCOP -lkio -lkdefx" \
%configure \
   --disable-rpath \
   --with-rpm \
   --enable-closure \
   --with-qt-libraries=$QTDIR/lib \
%if %{arts} == 0
   --without-arts \
%endif
%if %{final}
   --enable-final \
%endif
%if %{debug}
   --enable-debug \
%endif
   --with-private-groups

make

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf %{buildroot}%_docdir/HTML/en/{kdat,knetworkconf,lilo-config}
magic_rpm_clean.sh

%clean   
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%files kpackage
%defattr(-,root,root)
%_bindir/kpackage
%doc %_docdir/HTML/en/kpackage
%_iconsdir/*/*/*/kpackage.png
%_datadir/applications/kde/kpackage.desktop
%dir %_datadir/apps/kpackage
%_datadir/apps/kpackage/*
%_libdir/trinity/kfile_*.*
%_datadir/services/*

%files ksysv
%defattr(-,root,root)
%_bindir/ksysv
%dir %_datadir/apps/ksysv/
%_datadir/apps/ksysv/*
%_datadir/applications/kde/ksysv.desktop
%_iconsdir/*/*/*/ksysv.png
%doc %_docdir/HTML/en/ksysv
%_datadir/mimelnk/application/x-ksysv.desktop
%_datadir/mimelnk/text/x-ksysv-log.desktop

%files kcron
%defattr(-,root,root)
%doc %_docdir/HTML/en/kcron
%_datadir/applications/kde/kcron.desktop
%_bindir/kcron
%dir %_datadir/apps/kcron
%_datadir/apps/kcron/*
%_iconsdir/*/*/*/kcron.*

%files kuser 
%defattr(-,root,root)
%doc %_docdir/HTML/en/kuser
%_datadir/applications/kde/kuser.desktop
%_bindir/kuser
%dir %_datadir/apps/kuser/
%_datadir/apps/kuser/*
%_datadir/config.kcfg/kuser.kcfg
%_iconsdir/*/*/*/kuser.*
%_iconsdir/crystalsvg/16x16/actions/toggle_log.png

%changelog
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

* Thu Feb 28 2006 KanKer <kanker@163.com>
- fix a kpackage crash bug

* Sun Jan 15 2006 KanKer <kanker@163.com>
- add sudo fix patch

* Thu Oct 18 2005 KanKer <kanker@163.com>
- 3.4.3

* Mon Aug 1 2005 KanKer <kanker@163.com>
- 3.4.2

* Wed Jun 1 2005 KanKer <kanker@163.com>
- 3.4.1

* Thu May 10 2005 KanKer <kanker@163.com>
- remove kpackage-cjk.patch

* Mon Mar 21 2005 KanKer <kanker@163.com>
- 3.4.0

* Fri Dec 17 2004 KanKer <kanker@163.com>
- rebuild to remove libselinux.

*Tue Dec 14 2004 tingxx <tingxx@21cn.com>
- update to 3.3.2 for ML

* Fri Oct 15 2004 KanKer <kanker@163.com>
- update to 3.3.1 for ML.
